# Data Policy

This workbench is local-first and must not ingest private exports, credentials, model caches, logs, vector stores, or raw sensitive archives by default.

## Allowed Demo Inputs

- Synthetic demo documents created for workshops.
- Client-approved sample PDFs, DOCX, TXT, Markdown, CSV, XLSX, and HTML files.
- AIMM assessment exports that have been reviewed for sharing in the local workbench.

## Blocked By Default

- `05Chatgpt`
- ChatGPT or browser exports
- email exports
- `.env` files and credentials
- database files such as `.db`, `.sqlite`, and `.sqlite3`
- vector stores such as Chroma, FAISS, or `vectorstore`
- logs and audit trails
- installer folders and archives
- model caches and model files
- `Ollama`
- `Nodejs`
- `Chatbox`

The ingestion layer should reject these paths even if a user accidentally selects a parent folder.
