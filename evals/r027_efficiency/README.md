# T066 R027/R028 efficiency screening — Freeze A

Fresh provider-free Stage 5 materialization on the v2 scientific branch. It freezes nine matched pairs / eighteen scored arms and contains no scored model output. The abandoned v1 branch is non-authoritative and must not be consumed.

Provider-free checks:

- `python evals/r027_efficiency/integrity.py`
- `python evals/r027_efficiency/fixture_generator.py <scratch-dir>`
- `pytest -q tests/test_r027_efficiency_freeze.py`

Live execution remains blocked until the separate Human launch gate and live runtime/account/usage/instruction preflight are satisfied.
