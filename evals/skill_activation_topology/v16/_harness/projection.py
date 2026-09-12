"""Topology-independent capability truth -> topology-specific activation projection."""
from __future__ import annotations
from collections.abc import Iterable
from typing import Any
from .models import CAPABILITIES, CANDIDATES, HarnessError

def validate_topologies(topologies: dict[str, Any]) -> None:
    if topologies.get("topology_revision") != "MG1-T023-TOPOLOGIES-v4":
        raise HarnessError("unexpected topology revision")
    if tuple(topologies.get("candidates", {})) != CANDIDATES:
        raise HarnessError("candidate set/order must be B2/F2/G3")
    expected_caps = set(CAPABILITIES)
    for candidate_id in CANDIDATES:
        mapping = topologies["candidates"][candidate_id]["capability_to_entrypoints"]
        if set(mapping) != expected_caps:
            raise HarnessError(f"{candidate_id}: capability mapping drift")
        for capability, entrypoints in mapping.items():
            if not entrypoints or not all(isinstance(item, str) and item for item in entrypoints):
                raise HarnessError(f"{candidate_id}/{capability}: invalid entrypoints")

def project_capabilities(topologies: dict[str, Any], candidate_id: str, capabilities: Iterable[str]) -> frozenset[str]:
    validate_topologies(topologies)
    if candidate_id not in CANDIDATES:
        raise HarnessError(f"unknown candidate: {candidate_id}")
    caps = set(capabilities)
    unknown = caps - set(CAPABILITIES)
    if unknown:
        raise HarnessError(f"unknown capabilities: {sorted(unknown)}")
    mapping = topologies["candidates"][candidate_id]["capability_to_entrypoints"]
    return frozenset(entrypoint for capability in caps for entrypoint in mapping[capability])
