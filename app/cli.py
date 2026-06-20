from __future__ import annotations

import argparse
from pathlib import Path

from app.assessments.aimm_importer import import_aimm_records
from app.core.security import ensure_ingestion_allowed
from app.orchestrator.model_router import route_model
from app.reporting.report_builder import build_markdown_report


def main() -> None:
    parser = argparse.ArgumentParser(prog="enterprise-ai-governance-workbench")
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser("ingest")
    ingest.add_argument("--path", required=True)
    ask = sub.add_parser("ask")
    ask.add_argument("question")
    assess = sub.add_parser("assess")
    assess.add_argument("--file", required=True)
    report = sub.add_parser("report")
    report.add_argument("--type", default="readiness")
    sub.add_parser("eval")
    args = parser.parse_args()

    if args.command == "ingest":
        print(f"Allowed for ingestion: {ensure_ingestion_allowed(args.path)}")
    elif args.command == "ask":
        decision = route_model("document_qa")
        print(f"Route: {decision.local_cloud_decision} / {decision.selected_model}")
        print("Use the Streamlit Chat Workbench for grounded RAG answers in this phase.")
    elif args.command == "assess":
        records = import_aimm_records(args.file)
        print(f"Imported {len(records)} AIMM assessment record(s).")
    elif args.command == "report":
        path = build_markdown_report(args.type, {}, Path("data") / "reports")
        print(f"Wrote {path}")
    elif args.command == "eval":
        print("Run evaluation/run_eval.py for the current RAG evaluation harness.")


if __name__ == "__main__":
    main()
