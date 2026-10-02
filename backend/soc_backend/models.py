from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class NormalizedAlert:
    """Stable internal representation of a Wazuh alert."""

    alert_id: str | None
    timestamp: str | None

    rule_id: str | None
    rule_level: int
    rule_description: str | None
    groups: list[str] = field(default_factory=list)

    mitre_ids: list[str] = field(default_factory=list)
    mitre_tactics: list[str] = field(default_factory=list)
    mitre_techniques: list[str] = field(default_factory=list)

    agent_id: str | None = None
    agent_name: str | None = None
    agent_ip: str | None = None

    event_provider: str | None = None
    event_id: str | None = None
    event_channel: str | None = None
    computer: str | None = None

    user: str | None = None
    image: str | None = None
    command_line: str | None = None
    process_guid: str | None = None
    process_id: str | None = None
    parent_image: str | None = None
    parent_command_line: str | None = None
    parent_process_guid: str | None = None
    parent_process_id: str | None = None

    source_ip: str | None = None
    source_port: str | None = None
    destination_ip: str | None = None
    destination_port: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
