"""Runtime profile abstraction for Agent Governance.

``consumer`` and ``source-maintainer`` are mutually exclusive active
profiles. Unsupported or ambiguous profile values are rejected rather than
routed with broader permissions.

Profiles are implementation context, not normative authority.  No profile
default grants source-maintenance permissions.
"""

from dataclasses import dataclass


class ProfileError(Exception):
    """Fail-closed profile-routing error."""


ACTIVE_PROFILES = frozenset({"consumer", "source-maintainer"})
DEFAULT_PROFILE = "consumer"


@dataclass(frozen=True)
class Profile:
    """Resolved operational profile.

    Profile identity selects an adapter boundary. Source-maintainer context
    still requires the explicit source-product signal validated by that
    adapter.
    """

    name: str

    @property
    def is_consumer(self) -> bool:
        return self.name == "consumer"

    @property
    def is_source_maintainer(self) -> bool:
        return self.name == "source-maintainer"

    @property
    def grants_source_maintenance(self) -> bool:
        return self.is_source_maintainer


def validate_profile(profile: object) -> Profile:
    """Validate a resolved profile against the active runtime identities."""

    if not isinstance(profile, Profile):
        raise ProfileError(f"profile must be a Profile instance, got {type(profile).__name__}")
    if not isinstance(profile.name, str) or profile.name not in ACTIVE_PROFILES:
        raise ProfileError(
            f"unsupported profile: {profile.name!r}; active profiles: {sorted(ACTIVE_PROFILES)}"
        )
    return profile


def resolve_profile(name: str | None = None) -> Profile:
    """Resolve a runtime profile by name.

    * ``None`` resolves to the default ``consumer`` profile.
    * Active profile names resolve to their :class:`Profile`.
    * Unsupported or ambiguous values raise :class:`ProfileError`.

    Fail-closed routing means rejected profiles never acquire broader
    permissions.
    """

    if name is None:
        name = DEFAULT_PROFILE
    if not isinstance(name, str) or not name:
        raise ProfileError(
            f"profile must be a non-empty string, got {name!r}; "
            f"active profiles: {sorted(ACTIVE_PROFILES)}"
        )
    return validate_profile(Profile(name=name))
