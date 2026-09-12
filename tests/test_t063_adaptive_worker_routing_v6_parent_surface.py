from __future__ import annotations

from typing import Any

import pytest

from evals.adaptive_worker_routing_v3.app_server import Notification
from evals.adaptive_worker_routing_v3.config import ExecutionInvalid
from evals.adaptive_worker_routing_v6 import runner as v6


class _FakeClient:
    def __init__(self, notifications: list[Notification]) -> None:
        self._notifications = tuple(notifications)

    def notifications(self) -> tuple[Notification, ...]:
        return self._notifications


def _activity(
    *,
    item_id: str = "activity-1",
    child_id: str = "child-1",
    task_name: str = "t063-p1",
) -> dict[str, Any]:
    return {
        "id": item_id,
        "type": "subAgentActivity",
        "kind": "Started",
        "agentThreadId": child_id,
        "agentPath": f"agents/{task_name}",
    }


def _notification(
    method: str,
    item: dict[str, Any],
    *,
    parent_id: str = "parent-1",
    turn_id: str = "parent-turn-1",
) -> Notification:
    return Notification(
        method=method,
        params={"threadId": parent_id, "turnId": turn_id, "item": item},
    )


def _parent_turn(*items: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "parent-turn-1",
        "status": "completed",
        "items": [
            *items,
            {"id": "message-1", "type": "agentMessage", "text": "PARENT_SPAWNED"},
        ],
    }


def _install_context(notifications: list[Notification]) -> None:
    v6._PARENT_CONTEXT_BY_CHILD["child-1"] = v6._ParentSurfaceContext(
        client=_FakeClient(notifications),  # type: ignore[arg-type]
        parent_id="parent-1",
        parent_turn_id="parent-turn-1",
        start_index=0,
        spawn_item_id="activity-1",
    )


@pytest.fixture(autouse=True)
def _clear_context() -> None:
    v6._PARENT_CONTEXT_BY_CHILD.clear()


def test_live_started_receipt_can_be_absent_from_completed_snapshot() -> None:
    activity = _activity()
    _install_context(
        [
            _notification("item/started", activity),
            _notification("item/completed", dict(activity)),
        ]
    )

    v6._validate_parent_surface_v6(
        _parent_turn(),
        child_id="child-1",
        expected_task_name="t063-p1",
    )


def test_started_and_completed_notifications_are_deduplicated_by_item_id() -> None:
    activity = _activity()
    _install_context(
        [
            _notification("item/started", activity),
            _notification("item/completed", dict(activity)),
            _notification(
                "item/started",
                _activity(item_id="activity-other", child_id="child-2"),
            ),
        ]
    )

    with pytest.raises(ExecutionInvalid, match="live parent spawn activity count mismatch"):
        v6._validate_parent_surface_v6(
            _parent_turn(),
            child_id="child-1",
            expected_task_name="t063-p1",
        )


def test_notifications_from_other_parent_turns_are_ignored() -> None:
    activity = _activity()
    _install_context(
        [
            _notification(
                "item/started",
                _activity(item_id="other", child_id="child-2"),
                parent_id="other-parent",
                turn_id="other-turn",
            ),
            _notification("item/started", activity),
        ]
    )

    v6._validate_parent_surface_v6(
        _parent_turn(),
        child_id="child-1",
        expected_task_name="t063-p1",
    )


def test_missing_correlated_activity_blocks() -> None:
    _install_context([])

    with pytest.raises(ExecutionInvalid, match="live parent spawn activity count mismatch"):
        v6._validate_parent_surface_v6(
            _parent_turn(),
            child_id="child-1",
            expected_task_name="t063-p1",
        )


def test_wrong_child_or_task_blocks() -> None:
    _install_context([_notification("item/started", _activity(child_id="child-2"))])

    with pytest.raises(ExecutionInvalid, match="live parent spawn activity count mismatch"):
        v6._validate_parent_surface_v6(
            _parent_turn(),
            child_id="child-1",
            expected_task_name="t063-p1",
        )


def test_forbidden_live_parent_item_blocks() -> None:
    activity = _activity()
    command = {"id": "cmd-1", "type": "commandExecution", "command": "git status"}
    _install_context(
        [
            _notification("item/started", activity),
            _notification("item/started", command),
        ]
    )

    with pytest.raises(ExecutionInvalid, match="forbidden live item types"):
        v6._validate_parent_surface_v6(
            _parent_turn(),
            child_id="child-1",
            expected_task_name="t063-p1",
        )


def test_forbidden_completed_parent_item_blocks() -> None:
    _install_context([_notification("item/started", _activity())])
    command = {"id": "cmd-1", "type": "commandExecution", "command": "git status"}

    with pytest.raises(ExecutionInvalid, match="forbidden completed item types"):
        v6._validate_parent_surface_v6(
            _parent_turn(command),
            child_id="child-1",
            expected_task_name="t063-p1",
        )


def test_contradictory_completed_activity_blocks() -> None:
    _install_context([_notification("item/started", _activity())])
    contradictory = _activity(item_id="activity-2", child_id="child-2")

    with pytest.raises(ExecutionInvalid, match="contradicts live spawn correlation"):
        v6._validate_parent_surface_v6(
            _parent_turn(contradictory),
            child_id="child-1",
            expected_task_name="t063-p1",
        )


def test_final_parent_response_is_still_required() -> None:
    _install_context([_notification("item/started", _activity())])
    parent_turn = {
        "id": "parent-turn-1",
        "status": "completed",
        "items": [{"id": "message-1", "type": "agentMessage", "text": "drift"}],
    }

    with pytest.raises(ExecutionInvalid, match="final response drift"):
        v6._validate_parent_surface_v6(
            parent_turn,
            child_id="child-1",
            expected_task_name="t063-p1",
        )
