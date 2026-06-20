from __future__ import annotations

from dataclasses import dataclass


HIGH_PRIVACY_TASKS = {"proposal_drafting", "assessment_analysis", "code_analysis", "governance_mapping"}
TASK_TYPES = {
    "document_qa",
    "executive_summary",
    "risk_assessment",
    "governance_mapping",
    "technical_architecture",
    "proposal_drafting",
    "assessment_analysis",
    "code_analysis",
}


@dataclass(frozen=True)
class RoutingDecision:
    task_type: str
    selected_model: str
    local_cloud_decision: str
    reason: str
    estimated_cost: str
    privacy_level: str
    fallback_model: str
    blocked: bool = False


def route_model(
    task_type: str,
    *,
    privacy_sensitive: bool = True,
    external_api_enabled: bool = False,
    context_length: int = 0,
    speed_required: bool = False,
    cost_sensitive: bool = True,
) -> RoutingDecision:
    task = task_type if task_type in TASK_TYPES else "document_qa"
    privacy_level = "high" if privacy_sensitive or task in HIGH_PRIVACY_TASKS else "standard"
    if privacy_level == "high" and not external_api_enabled:
        return RoutingDecision(task, "qwen2.5:7b", "local", "High privacy task; cloud disabled by default.", "0", privacy_level, "extractive")
    if privacy_level == "high" and external_api_enabled:
        return RoutingDecision(task, "qwen2.5:7b", "local", "High privacy task; local preferred even when external APIs are configured.", "0", privacy_level, "human_review")
    if cost_sensitive or not external_api_enabled:
        return RoutingDecision(task, "qwen2.5:7b", "local", "Cost-sensitive or external API disabled.", "0", privacy_level, "extractive")
    if context_length > 24000 and not privacy_sensitive:
        return RoutingDecision(task, "configured-external-long-context", "cloud_optional", "Long context and non-sensitive task; requires explicit config.", "estimate_required", privacy_level, "qwen2.5:7b")
    if speed_required:
        return RoutingDecision(task, "configured-fast-model", "cloud_optional", "Speed requested for non-sensitive task; requires explicit config.", "estimate_required", privacy_level, "qwen2.5:7b")
    return RoutingDecision(task, "qwen2.5:7b", "local", "Default local-first routing.", "0", privacy_level, "extractive")
