"""Runtime profile abstraction for Agent Governance.

``consumer`` is the only active profile.  Unsupported or ambiguous profile
values are rejected rather than routed with broader permissions.

Profiles are implementation context, not normative authority.  No profile
default grants source-maintenance permissions.
"""

from dataclasses import dataclass


class ProfileError(Exception):
    """Fail-closed profile-routing error."""


ACTIVE_PROFILES = frozenset({"consumer"})
DEFAULT_PROFILE = "consumer"


@dataclass(frozen=True)
class Profile:
    """Resolved operational profile.

    ``consumer`` is the only active profile.  The ``source-maintainer``
    profile is reserved for T022 and is not active in T021.
    """

    name: str

    @property
    def is_consumer(self) -> bool:
        return self.name == "consumer"

    @property
    def is_source_maintainer(self) -> bool:
        return False

    @property
    def grants_source_maintenance(self) -> bool:
        return False


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
    if name not in ACTIVE_PROFILES:
        raise ProfileError(
            f"unsupported profile: {name!r}; active profiles: {sorted(ACTIVE_PROFILES)}"
        )
    return Profile(name=name)
