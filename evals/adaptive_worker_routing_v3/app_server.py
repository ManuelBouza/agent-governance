"""Minimal stdlib JSON-RPC client for the Codex App Server."""

from __future__ import annotations

import contextlib
import json
import queue
import subprocess
import threading
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

Json = dict[str, Any]


class AppServerError(RuntimeError):
    """Fail-closed App Server transport/protocol error."""


@dataclass(frozen=True)
class Notification:
    method: str
    params: Json


class AppServerClient:
    """Line-delimited JSON-RPC client for ``codex app-server --listen stdio://``."""

    def __init__(
        self,
        codex_bin: Path,
        *,
        cwd: Path,
        config_overrides: tuple[str, ...] = (),
    ) -> None:
        self.codex_bin = codex_bin
        self.cwd = cwd
        self.config_overrides = config_overrides
        self._proc: subprocess.Popen[str] | None = None
        self._pending: dict[str, queue.Queue[Json]] = {}
        self._pending_lock = threading.Lock()
        self._notifications: list[Notification] = []
        self._notification_cond = threading.Condition()
        self._reader_error: BaseException | None = None
        self._reader_thread: threading.Thread | None = None
        self._stderr_lines: list[str] = []
        self._stderr_thread: threading.Thread | None = None

    def __enter__(self) -> AppServerClient:
        self.start()
        return self

    def __exit__(self, _exc_type: object, _exc: object, _tb: object) -> None:
        self.close()

    @property
    def stderr_tail(self) -> str:
        return "\n".join(self._stderr_lines[-40:])

    def start(self) -> None:
        if self._proc is not None:
            return
        args = [str(self.codex_bin)]
        for override in self.config_overrides:
            args.extend(["--config", override])
        args.extend(["app-server", "--listen", "stdio://"])
        self._proc = subprocess.Popen(
            args,
            cwd=self.cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        if self._proc.stdin is None or self._proc.stdout is None or self._proc.stderr is None:
            raise AppServerError("app-server stdio pipes unavailable")
        self._reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._reader_thread.start()
        self._stderr_thread = threading.Thread(target=self._stderr_loop, daemon=True)
        self._stderr_thread.start()

    def close(self) -> None:
        proc = self._proc
        self._proc = None
        if proc is None:
            return
        if proc.stdin is not None:
            with contextlib.suppress(OSError):
                proc.stdin.close()
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            proc.kill()
        if self._reader_thread is not None:
            self._reader_thread.join(timeout=0.5)
        if self._stderr_thread is not None:
            self._stderr_thread.join(timeout=0.5)

    def initialize(self) -> Json:
        result = self.request(
            "initialize",
            {
                "clientInfo": {
                    "name": "agent-governance-t063-v3",
                    "title": "Agent Governance T063 v3 Harness",
                    "version": "1",
                },
                "capabilities": {"experimentalApi": True},
            },
        )
        self.notify("initialized")
        return result

    def request(self, method: str, params: Json | None = None, *, timeout: float = 30.0) -> Json:
        self._raise_reader_error()
        request_id = str(uuid.uuid4())
        waiter: queue.Queue[Json] = queue.Queue(maxsize=1)
        with self._pending_lock:
            self._pending[request_id] = waiter
        payload: Json = {"id": request_id, "method": method}
        if params is not None:
            payload["params"] = params
        try:
            self._write(payload)
            try:
                response = waiter.get(timeout=timeout)
            except queue.Empty as exc:
                raise AppServerError(f"{method} timed out after {timeout:.1f}s") from exc
        finally:
            with self._pending_lock:
                self._pending.pop(request_id, None)
        if "error" in response:
            raise AppServerError(f"{method} failed: {response['error']!r}")
        result = response.get("result")
        if not isinstance(result, dict):
            raise AppServerError(f"{method} result is not an object: {result!r}")
        return result

    def notify(self, method: str, params: Json | None = None) -> None:
        payload: Json = {"method": method}
        if params is not None:
            payload["params"] = params
        self._write(payload)

    def notifications(self) -> tuple[Notification, ...]:
        with self._notification_cond:
            return tuple(self._notifications)

    def wait_for_notification(
        self,
        predicate: Callable[[Notification], bool],
        *,
        start_index: int = 0,
        timeout: float = 300.0,
    ) -> tuple[int, Notification]:
        deadline = time.monotonic() + timeout
        with self._notification_cond:
            index = start_index
            while True:
                while index < len(self._notifications):
                    item = self._notifications[index]
                    index += 1
                    if predicate(item):
                        return index, item
                self._raise_reader_error()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise AppServerError(f"notification wait timed out after {timeout:.1f}s")
                self._notification_cond.wait(timeout=min(remaining, 0.5))

    def _write(self, payload: Json) -> None:
        proc = self._proc
        if proc is None or proc.stdin is None:
            raise AppServerError("app-server is not running")
        try:
            proc.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
            proc.stdin.flush()
        except OSError as exc:
            raise AppServerError(f"failed writing app-server request: {exc}") from exc

    def _reader_loop(self) -> None:
        proc = self._proc
        if proc is None or proc.stdout is None:
            return
        try:
            for raw in proc.stdout:
                line = raw.strip()
                if not line:
                    continue
                message = json.loads(line)
                if not isinstance(message, dict):
                    continue
                request_id = message.get("id")
                if request_id is not None:
                    with self._pending_lock:
                        waiter = self._pending.get(str(request_id))
                    if waiter is not None:
                        waiter.put(message)
                    continue
                method = message.get("method")
                params = message.get("params")
                if isinstance(method, str) and isinstance(params, dict):
                    with self._notification_cond:
                        self._notifications.append(Notification(method=method, params=params))
                        self._notification_cond.notify_all()
        except BaseException as exc:  # pragma: no cover
            self._reader_error = exc
            with self._notification_cond:
                self._notification_cond.notify_all()

    def _stderr_loop(self) -> None:
        proc = self._proc
        if proc is None or proc.stderr is None:
            return
        for raw in proc.stderr:
            self._stderr_lines.append(raw.rstrip())
            if len(self._stderr_lines) > 400:
                del self._stderr_lines[:200]

    def _raise_reader_error(self) -> None:
        if self._reader_error is not None:
            raise AppServerError(
                f"app-server reader failed: {self._reader_error}"
            ) from self._reader_error
