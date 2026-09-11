from __future__ import annotations

from pathlib import Path

import pytest

from evals.adaptive_worker_routing_v3.app_server import AppServerClient as BaseAppServerClient
from evals.adaptive_worker_routing_v3.app_server import AppServerError
from evals.adaptive_worker_routing_v3.config import MeasurementSurfaceBlocked
from evals.adaptive_worker_routing_v4 import runner as v4

EMPTY_ROLLOUT_ERROR = AppServerError(
    "thread/resume failed: {'code': -32600, 'message': 'thread-store error: "
    "failed to read session metadata from C:\\\\x\\\\rollout.jsonl: rollout at "
    "C:\\\\x\\\\rollout.jsonl is empty'}"
)


def _client() -> v4.V4AppServerClient:
    client = v4.V4AppServerClient(Path("codex.exe"), cwd=Path("."))
    client._v4_parent_thread_id = "parent"
    return client


def test_empty_rollout_classifier_is_exact() -> None:
    assert v4._is_empty_rollout_resume_error(EMPTY_ROLLOUT_ERROR) is True
    assert v4._is_empty_rollout_resume_error(
        AppServerError("thread/resume failed: {'message': 'thread-store error'}")
    ) is False


def test_same_child_resume_retries_then_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_calls = 0
    loaded_calls = 0
    resume_thread_ids: list[str | None] = []
    events: list[str] = []

    def fake_request(
        self: BaseAppServerClient,
        method: str,
        params: dict[str, object] | None = None,
        *,
        timeout: float = 30.0,
    ) -> dict[str, object]:
        nonlocal resume_calls, loaded_calls
        if method == "thread/resume":
            resume_calls += 1
            resume_thread_ids.append(
                params.get("threadId") if isinstance(params, dict) else None
            )
            events.append(f"resume:{resume_calls}")
            if resume_calls < 3:
                raise EMPTY_ROLLOUT_ERROR
            return {"thread": {"id": "child"}}
        if method == "thread/loaded/list":
            loaded_calls += 1
            events.append("loaded")
            return {"data": ["parent"], "nextCursor": None}
        raise AssertionError(method)

    def fake_sleep(_seconds: float) -> None:
        events.append("sleep")

    monkeypatch.setattr(BaseAppServerClient, "request", fake_request)
    monkeypatch.setattr(v4.time, "sleep", fake_sleep)
    client = _client()
    result = client.request("thread/resume", {"threadId": "child"})
    assert result == {"thread": {"id": "child"}}
    assert resume_calls == 3
    assert loaded_calls == 2
    assert resume_thread_ids == ["child", "child", "child"]
    assert events == [
        "resume:1",
        "sleep",
        "loaded",
        "resume:2",
        "sleep",
        "loaded",
        "resume:3",
    ]
    receipt = client.reattachment_receipt("child")
    assert receipt is not None
    assert receipt["retry_count"] == 2
    assert receipt["parent_residency_rechecks"] == 2
    assert receipt["same_child_reused"] is True
    assert receipt["new_provider_turn_created"] is False


def test_non_empty_rollout_resume_error_is_not_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_calls = 0

    def fake_request(
        self: BaseAppServerClient,
        method: str,
        params: dict[str, object] | None = None,
        *,
        timeout: float = 30.0,
    ) -> dict[str, object]:
        nonlocal resume_calls
        assert method == "thread/resume"
        resume_calls += 1
        raise AppServerError("thread/resume failed: {'message': 'different failure'}")

    monkeypatch.setattr(BaseAppServerClient, "request", fake_request)
    with pytest.raises(AppServerError, match="different failure"):
        _client().request("thread/resume", {"threadId": "child"})
    assert resume_calls == 1


def test_parent_loss_stops_immediately_before_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_calls = 0
    events: list[str] = []

    def fake_request(
        self: BaseAppServerClient,
        method: str,
        params: dict[str, object] | None = None,
        *,
        timeout: float = 30.0,
    ) -> dict[str, object]:
        nonlocal resume_calls
        if method == "thread/resume":
            resume_calls += 1
            events.append(f"resume:{resume_calls}")
            raise EMPTY_ROLLOUT_ERROR
        if method == "thread/loaded/list":
            events.append("loaded")
            return {"data": [], "nextCursor": None}
        raise AssertionError(method)

    monkeypatch.setattr(BaseAppServerClient, "request", fake_request)
    monkeypatch.setattr(v4.time, "sleep", lambda _seconds: events.append("sleep"))
    with pytest.raises(MeasurementSurfaceBlocked, match="parent lost residency"):
        _client().request("thread/resume", {"threadId": "child"})
    assert resume_calls == 1
    assert events == ["resume:1", "sleep", "loaded"]
    assert v4._REATTACHMENT_AUDIT[-1]["parent_residency_rechecks"] == 1


def test_empty_rollout_retry_exhaustion_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_calls = 0
    loaded_calls = 0

    def fake_request(
        self: BaseAppServerClient,
        method: str,
        params: dict[str, object] | None = None,
        *,
        timeout: float = 30.0,
    ) -> dict[str, object]:
        nonlocal resume_calls, loaded_calls
        if method == "thread/resume":
            resume_calls += 1
            raise EMPTY_ROLLOUT_ERROR
        if method == "thread/loaded/list":
            loaded_calls += 1
            return {"data": ["parent"], "nextCursor": None}
        raise AssertionError(method)

    monkeypatch.setattr(BaseAppServerClient, "request", fake_request)
    monkeypatch.setattr(v4.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(v4, "RESUME_MAX_ATTEMPTS", 3)
    client = _client()
    with pytest.raises(MeasurementSurfaceBlocked, match="barrier exhausted"):
        client.request("thread/resume", {"threadId": "child"})
    assert resume_calls == 3
    assert loaded_calls == 2
    assert v4._REATTACHMENT_AUDIT[-1]["parent_residency_rechecks"] == 2


def test_v4_identity_and_historical_heads_are_frozen() -> None:
    assert v4.EVIDENCE_BRANCH.endswith("requalification-v4")
    assert v4.TELEMETRY_DEFAULT.as_posix().endswith("telemetry-v4.json")
    assert v4.HANDOFF_DEFAULT.as_posix().endswith("handoff-v4.json")
    assert v4.HISTORICAL_BLOCKED_HEADS[-1] == v4.V3_TERMINAL_HEAD
    assert v4.RESUME_MAX_ATTEMPTS == 10
    assert v4.RESUME_RETRY_DELAY_SECONDS == 0.2
