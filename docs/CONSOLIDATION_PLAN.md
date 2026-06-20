# Consolidation Plan

## Target Product

Private Enterprise Knowledge & Governance Workbench.

## Source App Decisions

| Source | Classification | Decision |
| --- | --- | --- |
| enterprise-knowledge-assistant | Reuse directly | Seed workbench, preserve working RAG, observability, guardrails, and Streamlit UI. |
| Second-Brain-RAG | Use as design reference only | Reuse UX/Ollama-first ideas only. Do not import uploaded documents or Chroma DB. |
| Local-RAG-Pipeline | Refactor and reuse | Reuse CLI/package/cache/reranking concepts. Do not import archives or runtime data. |
| 05Chatgpt | Do not import | Private ChatGPT export. Keep offline, excluded, and never indexed by default. |
| LLM-TrustGuard-Chatbox-Addon | Refactor and reuse | Port scoring/detector concepts into `app/governance/trust_score.py`. Do not import DB/logs. |
| llm-orchestrator | Refactor and reuse | Port local/cloud, cost, privacy, and task routing concepts into `app/orchestrator/model_router.py`. Do not import `.env`. |
| AIMM-Windows-App | Refactor and reuse | Support importing reviewed JSON/CSV/XLSX assessment outputs through `app/assessments/aimm_importer.py`. |

## Migration Sequence

1. Establish target folder and privacy exclusions.
2. Generate legacy inventory using safe path/dependency scanning.
3. Preserve working RAG and wrap it with unified module paths.
4. Add TrustGuard scoring, model router, AIMM importer, and reporting builder.
5. Add tests and run compile/test verification.
6. Only after validation, manually review retirement of duplicate RAG apps. No deletion is part of this phase.
