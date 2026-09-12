from __future__ import annotations

from pathlib import Path

import pytest

from evals.adaptive_worker_routing_v3.app_server import AppServerClient as BaseAppServerClient
from evals.adaptive_worker_routing_v3.app_server import AppServerError
from evals.adaptive_worker_routing_v3.config import MeasurementSurfaceBlocked
from evals.adaptive_worker_routing_v4 import runner as v4
from evals.adaptive_worker_routing_v8 import runner as v8

CHILD = "01a09262-2515-75a1-9fa5-25fdc82791ff"
OTHER_CHILD = "01a09262-2515-75a1-9fa5-25fdc8279200"

EMPTY_ROLLOUT_ERROR = AppServerError(
    "thread/resume failed: {'code': -32603, 'message': 'failed to read thread: "
    "thread-store internal error: failed to read session metadata "
    "C:\\\\x\\\\rollout.jsonl: rollout at C:\\\\x\\\\rollout.jsonl is empty'}"
)
NO_ROLLOUT_ERROR = AppServerError(
    f"thread/resume failed: {{'code': -32600, 'message': 'no rollout found for thread id {CHILD}'}}"
)
NO_ROLLOUT_OTHER_CHILD = AppServerError(
    f"thread/resume failed: {{'code': -32600, 'message': 'no rollout found for thread id {OTHER_CHILD}'}}"
)


def _client() -> v8.V8AppServerClient:
    v4._REATTACHMENT_AUDIT.clear()
    client = v8.V8AppServerClient(Path("codex.exe"), cwd=Path("."))
    client._v4_parent_thread_id = "parent"
    return client


def _error(*, code: object = -32600, message: object | None = None) -> AppServerError:
    actual = f"no rollout found for thread id {CHILD}" if message is None else message
    return AppServerError(
        f"thread/resume failed: {{'code': {code!r}, 'message': {actual!r}}}"
    )


def test_v8_classifier_requires_exact_structured_error_and_child() -> None:
    assert (
        v8._transient_resume_error_class(NO_ROLLOUT_ERROR, CHILD)
        == "ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD"
    )
    assert v8._transient_resume_error_class(NO_ROLLOUT_OTHER_CHILD, CHILD) is None
    assert v8._transient_resume_error_class(_error(code=-32601), CHILD) is None
    assert v8._transient_resume_error_class(_error(code=True), CHILD) is None
    assert (
        v8._transient_resume_error_class(
            _error(message=f"prefix no rollout found for thread id {CHILD}"), CHILD
        )
        is None
    )
    assert (
        v8._transient_resume_error_class(
            _error(message=f"no rollout found for thread id {CHILD} suffix"), CHILD
        )
        is None
    )
    assert (
        v8._transient_resume_error_class(
            AppServerError("thread/resume failed: {'code': -32600, 'message':"), CHILD
        )
        is None
    )
    assert (
        v8._transient_resume_error_class(
            AppServerError("thread/resume failed: ['not', 'a', 'mapping']"), CHILD
        )
        is None
    )
    assert (
        v8._transient_resume_error_class(
            AppServerError(
                "thread/resume failed: {'code': -32600, 'message': 'different invalid request'}"
            ),
            CHILD,
        )
        is None
    )
    assert (
        v8._transient_resume_error_class(
            AppServerError(
                f"other/method failed: {{'code': -32600, 'message': "
                f"'no rollout found for thread id {CHILD}'}}"
            ),
            CHILD,
        )
        is None
    )
    assert (
        v8._transient_resume_error_class(EMPTY_ROLLOUT_ERROR, CHILD)
        == "EMPTY_ROLLOUT"
    )


def test_represented_error_parser_is_safe_and_mapping_only() -> None:
    assert v8._represented_resume_error(NO_ROLLOUT_ERROR) == {
        "code": -32600,
        "message": f"no rollout found for thread id {CHILD}",
    }
    assert (
        v8._represented_resume_error(
            AppServerError("thread/resume failed: __import__('os').system('echo nope')")
        )
        is None
    )
    assert (
        v8._represented_resume_error(
            AppServerError("thread/resume failed: ('tuple', -32600)")
        )
        is None
    )


def test_mixed_availability_conditions_share_one_budget_and_same_params(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_calls = 0
    loaded_calls = 0
    events: list[str] = []
    param_ids: list[int] = []
    thread_ids: list[str | None] = []

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
            param_ids.append(id(params))
            thread_ids.append(params.get("threadId") if isinstance(params, dict) else None)
            events.append(f"resume:{resume_calls}")
            if resume_calls == 1:
                raise NO_ROLLOUT_ERROR
            if resume_calls == 2:
                raise EMPTY_ROLLOUT_ERROR
            return {"thread": {"id": CHILD}}
        if method == "thread/loaded/list":
            loaded_calls += 1
            events.append("loaded")
            return {"data": ["parent"], "nextCursor": None}
        raise AssertionError(method)

    monkeypatch.setattr(BaseAppServerClient, "request", fake_request)
    monkeypatch.setattr(v8.time, "sleep", lambda _seconds: events.append("sleep"))
    params = {"threadId": CHILD, "includeTurns": False}
    client = _client()
    result = client.request("thread/resume", params)

    assert result == {"thread": {"id": CHILD}}
    assert resume_calls == 3
    assert loaded_calls == 2
    assert thread_ids == [CHILD, CHILD, CHILD]
    assert param_ids == [id(params), id(params), id(params)]
    assert events == [
        "resume:1",
        "sleep",
        "loaded",
        "resume:2",
        "sleep",
        "loaded",
        "resume:3",
    ]
    receipt = client.reattachment_receipt(CHILD)
    assert receipt is not None
    assert receipt["attempt_count"] == 3
    assert receipt["retry_count"] == 2
    assert receipt["parent_residency_rechecks"] == 2
    assert receipt["transient_error_classes"] == [
        "ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD",
        "EMPTY_ROLLOUT",
    ]
    assert receipt["shared_attempt_budget_max"] == 10
    assert receipt["same_child_reused"] is True
    assert receipt["new_provider_turn_created"] is False


@pytest.mark.parametrize(
    "failure",
    [
        NO_ROLLOUT_OTHER_CHILD,
        _error(code=-32601),
        _error(message=f"no rollout found for thread id {CHILD} suffix"),
        AppServerError("thread/resume failed: {'code': -32600, 'message':"),
        AppServerError(
            "thread/resume failed: {'code': -32600, 'message': 'different invalid request'}"
        ),
    ],
)
def test_nonmatching_no_rollout_shapes_are_not_retried(
    monkeypatch: pytest.MonkeyPatch,
    failure: AppServerError,
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
            raise failure
        if method == "thread/loaded/list":
            loaded_calls += 1
            return {"data": ["parent"], "nextCursor": None}
        raise AssertionError(method)

    monkeypatch.setattr(BaseAppServerClient, "request", fake_request)
    monkeypatch.setattr(v8.time, "sleep", lambda _seconds: None)
    with pytest.raises(AppServerError):
        _client().request("thread/resume", {"threadId": CHILD})
    assert resume_calls == 1
    assert loaded_calls == 0


def test_mixed_conditions_exhaust_one_common_budget(
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
            if resume_calls % 2:
                raise NO_ROLLOUT_ERROR
            raise EMPTY_ROLLOUT_ERROR
        if method == "thread/loaded/list":
            loaded_calls += 1
            return {"data": ["parent"], "nextCursor": None}
        raise AssertionError(method)

    monkeypatch.setattr(BaseAppServerClient, "request", fake_request)
    monkeypatch.setattr(v8.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(v4, "RESUME_MAX_ATTEMPTS", 4)
    client = _client()
    with pytest.raises(MeasurementSurfaceBlocked, match="4 total attempts"):
        client.request("thread/resume", {"threadId": CHILD})
    assert resume_calls == 4
    assert loaded_calls == 3
    audit = v4._REATTACHMENT_AUDIT[-1]
    assert audit["attempt_count"] == 4
    assert audit["retry_count"] == 3
    assert audit["transient_error_classes"] == [
        "ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD",
        "EMPTY_ROLLOUT",
        "ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD",
        "EMPTY_ROLLOUT",
    ]


def test_parent_loss_stops_before_second_resume(monkeypatch: pytest.MonkeyPatch) -> None:
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
            raise NO_ROLLOUT_ERROR
        if method == "thread/loaded/list":
            events.append("loaded")
            return {"data": [], "nextCursor": None}
        raise AssertionError(method)

    monkeypatch.setattr(BaseAppServerClient, "request", fake_request)
    monkeypatch.setattr(v8.time, "sleep", lambda _seconds: events.append("sleep"))
    with pytest.raises(MeasurementSurfaceBlocked, match="parent lost residency"):
        _client().request("thread/resume", {"threadId": CHILD})
    assert resume_calls == 1
    assert events == ["resume:1", "sleep", "loaded"]


def test_unrelated_resume_error_fails_immediately(monkeypatch: pytest.MonkeyPatch) -> None:
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
        raise AppServerError(
            "thread/resume failed: {'code': -32600, 'message': 'different failure'}"
        )

    monkeypatch.setattr(BaseAppServerClient, "request", fake_request)
    with pytest.raises(AppServerError, match="different failure"):
        _client().request("thread/resume", {"threadId": CHILD})
    assert resume_calls == 1


def test_v8_identity_and_historical_boundary() -> None:
    assert v8.EVIDENCE_BRANCH.endswith("requalification-v8")
    assert v8.TELEMETRY_DEFAULT.as_posix().endswith("telemetry-v8.json")
    assert v8.HANDOFF_DEFAULT.as_posix().endswith("handoff-v8.json")
    assert v8.HISTORICAL_EVIDENCE_HEADS[-1] == v8.V7_TERMINAL_HEAD
    assert v4.RESUME_MAX_ATTEMPTS == 10
    assert v4.RESUME_RETRY_DELAY_SECONDS == 0.2
