from __future__ import annotations

from typing import Any

from .models import NormalizedAlert


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def normalize_wazuh_alert(alert: dict[str, Any]) -> NormalizedAlert:
    """Convert one raw Wazuh alert object into the backend's stable schema."""

    rule = _dict(alert.get("rule"))
    agent = _dict(alert.get("agent"))
    mitre = _dict(rule.get("mitre"))

    data = _dict(alert.get("data"))
    win = _dict(data.get("win"))
    system = _dict(win.get("system"))
    eventdata = _dict(win.get("eventdata"))

    return NormalizedAlert(
        alert_id=str(alert["id"]) if alert.get("id") is not None else None,
        timestamp=str(alert["timestamp"]) if alert.get("timestamp") is not None else None,
        rule_id=str(rule["id"]) if rule.get("id") is not None else None,
        rule_level=_int(rule.get("level")),
        rule_description=(
            str(rule["description"]) if rule.get("description") is not None else None
        ),
        groups=_list(rule.get("groups")),
        mitre_ids=_list(mitre.get("id")),
        mitre_tactics=_list(mitre.get("tactic")),
        mitre_techniques=_list(mitre.get("technique")),
        agent_id=str(agent["id"]) if agent.get("id") is not None else None,
        agent_name=str(agent["name"]) if agent.get("name") is not None else None,
        agent_ip=str(agent["ip"]) if agent.get("ip") is not None else None,
        event_provider=(
            str(system["providerName"]) if system.get("providerName") is not None else None
        ),
        event_id=str(system["eventID"]) if system.get("eventID") is not None else None,
        event_channel=(
            str(system["channel"]) if system.get("channel") is not None else None
        ),
        computer=str(system["computer"]) if system.get("computer") is not None else None,
        user=str(eventdata["user"]) if eventdata.get("user") is not None else None,
        image=str(eventdata["image"]) if eventdata.get("image") is not None else None,
        command_line=(
            str(eventdata["commandLine"])
            if eventdata.get("commandLine") is not None
            else None
        ),
        process_guid=(
            str(eventdata["processGuid"])
            if eventdata.get("processGuid") is not None
            else None
        ),
        process_id=(
            str(eventdata["processId"])
            if eventdata.get("processId") is not None
            else None
        ),
        parent_image=(
            str(eventdata["parentImage"])
            if eventdata.get("parentImage") is not None
            else None
        ),
        parent_command_line=(
            str(eventdata["parentCommandLine"])
            if eventdata.get("parentCommandLine") is not None
            else None
        ),
        parent_process_guid=(
            str(eventdata["parentProcessGuid"])
            if eventdata.get("parentProcessGuid") is not None
            else None
        ),
        parent_process_id=(
            str(eventdata["parentProcessId"])
            if eventdata.get("parentProcessId") is not None
            else None
        ),
        source_ip=(
            str(eventdata["sourceIp"]) if eventdata.get("sourceIp") is not None else None
        ),
        source_port=(
            str(eventdata["sourcePort"])
            if eventdata.get("sourcePort") is not None
            else None
        ),
        destination_ip=(
            str(eventdata["destinationIp"])
            if eventdata.get("destinationIp") is not None
            else None
        ),
        destination_port=(
            str(eventdata["destinationPort"])
            if eventdata.get("destinationPort") is not None
            else None
        ),
    )
