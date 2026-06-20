from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrustScoreResult:
    score: int
    band: str
    human_review_required: bool
    factors: dict[str, float]
    warnings: list[str]


def calculate_trust_score(
    *,
    evidence_coverage: float,
    citation_quality: float,
    hallucination_risk: float,
    sensitive_exposure_risk: float,
    prompt_injection_risk: float,
    policy_conflict_risk: float,
    answer_completeness: float,
    retrieval_quality: float,
) -> TrustScoreResult:
    factors = {
        "evidence_coverage": _clamp(evidence_coverage),
        "citation_quality": _clamp(citation_quality),
        "hallucination_control": 1.0 - _clamp(hallucination_risk),
        "sensitive_information_control": 1.0 - _clamp(sensitive_exposure_risk),
        "prompt_injection_control": 1.0 - _clamp(prompt_injection_risk),
        "policy_conflict_control": 1.0 - _clamp(policy_conflict_risk),
        "answer_completeness": _clamp(answer_completeness),
        "retrieval_quality": _clamp(retrieval_quality),
    }
    weights = {
        "evidence_coverage": 0.2,
        "citation_quality": 0.18,
        "hallucination_control": 0.16,
        "sensitive_information_control": 0.12,
        "prompt_injection_control": 0.1,
        "policy_conflict_control": 0.1,
        "answer_completeness": 0.07,
        "retrieval_quality": 0.07,
    }
    score = round(sum(factors[key] * weight for key, weight in weights.items()) * 100)
    band = score_band(score)
    warnings = [key for key, value in factors.items() if value < 0.6]
    return TrustScoreResult(score=score, band=band, human_review_required=score < 85 or bool(warnings), factors=factors, warnings=warnings)


def score_band(score: int) -> str:
    if score >= 85:
        return "Trusted for executive review"
    if score >= 70:
        return "Usable with caution"
    if score >= 50:
        return "Requires human validation"
    return "Block or rewrite"


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
