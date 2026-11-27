# Onboarding Buddy — Streamlit client

This is a presentation layer for the existing FastAPI application. It does not
replace the API, database, ingestion pipeline, retriever, or LLM integration.

## Run locally

1. Start the existing backend from the `server/` directory using its configured
   virtual environment and `.env` file:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
   ```

2. In a second terminal, install the client dependencies and start Streamlit:

   ```bash
   cd client
   python -m venv .venv
   # Windows: .venv\\Scripts\\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```

3. Open the local URL printed by Streamlit (normally `http://localhost:8501`).

The client defaults to `http://localhost:8080`. To change it, set the
`API_BASE_URL` environment variable or add it to `.streamlit/secrets.toml`:

```toml
API_BASE_URL = "http://localhost:8080"
```

## Current API constraints

- The existing message response model exposes `content` but no sender/role.
- The current retrieval pipeline stores generated assistant responses; it does
  not store the user prompt as a message. User turns are therefore kept in
  Streamlit session state for the active browser session and cannot be fully
  reconstructed after a refresh or from another browser.
- The current API has no document-list endpoint, so the sidebar supports
  document ingestion but does not claim to show an indexed-document inventory.
- The current API does not expose a delete-document route or streaming response.

These limitations are intentionally not addressed in this UI-only change.
