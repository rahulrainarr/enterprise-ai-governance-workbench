import csv

from app.assessments.aimm_importer import import_aimm_records
from app.governance.trust_score import calculate_trust_score
from app.orchestrator.model_router import route_model
from app.reporting.report_builder import build_markdown_report


def test_trust_score_requires_review_for_weak_controls():
    result = calculate_trust_score(
        evidence_coverage=0.4,
        citation_quality=0.5,
        hallucination_risk=0.5,
        sensitive_exposure_risk=0.1,
        prompt_injection_risk=0.0,
        policy_conflict_risk=0.2,
        answer_completeness=0.7,
        retrieval_quality=0.5,
    )
    assert result.score < 85
    assert result.human_review_required


def test_router_stays_local_for_proposal_work():
    decision = route_model("proposal_drafting", privacy_sensitive=True, external_api_enabled=True)
    assert decision.local_cloud_decision == "local"
    assert decision.privacy_level == "high"


def test_aimm_csv_import_and_report(tmp_path):
    csv_path = tmp_path / "assessment.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["organization_name", "industry", "data_readiness_score"])
        writer.writeheader()
        writer.writerow({"organization_name": "DemoCo", "industry": "Telecom", "data_readiness_score": "72"})
    records = import_aimm_records(csv_path)
    assert records[0].organization_name == "DemoCo"
    report = build_markdown_report("readiness", {"executive_summary": "Demo summary"}, tmp_path)
    assert report.exists()
