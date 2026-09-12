"""Provider-free Freeze I guard for T023 v17."""
from __future__ import annotations
import json
from .harness import validate_freeze_i

def main() -> int:
    print(json.dumps(validate_freeze_i(), indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
