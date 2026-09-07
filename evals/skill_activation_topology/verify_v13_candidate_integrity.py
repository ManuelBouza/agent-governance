"""Compatibility entrypoint delegating to the current T061 v14 candidate guard."""

from __future__ import annotations

from verify_v14_candidate_integrity import main

if __name__ == "__main__":
    raise SystemExit(main())
