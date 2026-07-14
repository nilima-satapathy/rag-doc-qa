# Deploy DocQ (M6) — Streamlit Community Cloud

Public demo so recruiters can try the app without installing Python.

## Prerequisites

- GitHub repo: [nilima-satapathy/rag-doc-qa](https://github.com/nilima-satapathy/rag-doc-qa)
- Free account: [share.streamlit.io](https://share.streamlit.io) (sign in with GitHub)
- Optional for LLM answers: free [Gemini API key](https://aistudio.google.com/apikey)

Default mode is **extractive** (no API key). The app **auto-builds** the vector index from `data/*.pdf` on first start.

## Deploy steps (about 5 minutes)

1. Open **[https://share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
2. Click **Create app** / **New app**.
3. Set:
   - **Repository:** `nilima-satapathy/rag-doc-qa`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy**. Wait for the build (first run may take a few minutes while dependencies install and the index builds).
5. Copy the public URL, e.g. `https://rag-doc-qa-xxxxx.streamlit.app`

## Optional secrets (Gemini / xAI)

In the Streamlit Cloud app → **Settings → Secrets**, paste:

```toml
# Free default — omit keys to stay extractive-only
RAG_LLM_PROVIDER = "extractive"

# Optional free Gemini
# RAG_LLM_PROVIDER = "gemini"
# GEMINI_API_KEY = "your-key-here"
# GEMINI_MODEL = "gemini-flash-lite-latest"

# Optional paid xAI
# RAG_LLM_PROVIDER = "xai"
# XAI_API_KEY = "xai-..."
```

Save and reboot the app if needed.

## After deploy

1. Open the public URL and ask: *What is RAG?*
2. Confirm the index pill shows chunks ready.
3. Paste the URL into the root `README.md` under **Live demo**.
4. Tag the release: `git tag -a milestone-6 -m "Project 3 Milestone 6 complete"`

## Local check before deploy

```powershell
cd Desktop\Code\rag-doc-qa
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Blank / index empty | Wait for first boot; or click **Rebuild index** in Settings |
| Gemini 429 | Use extractive, or `GEMINI_MODEL=gemini-flash-lite-latest` |
| Build fails on Cloud | Check logs; ensure `requirements.txt` and `app.py` are on `main` |
| Secrets not picked up | Use the TOML format above; reboot app |

## Why not commit `.chroma/`?

The vector store is regenerated on cold start from the sample PDFs. That keeps the repo small and avoids platform-specific binary index issues.
