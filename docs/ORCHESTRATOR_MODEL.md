# Orchestrator Model

`app/orchestrator/model_router.py` chooses local-first routing based on task type, privacy sensitivity, cost sensitivity, context length, speed requirement, and whether external APIs are explicitly enabled.

Supported task types:

- document_qa
- executive_summary
- risk_assessment
- governance_mapping
- technical_architecture
- proposal_drafting
- assessment_analysis
- code_analysis
