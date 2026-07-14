"""
Milestone 4 — Streamlit chat UI for RAG Document Q&A.

Run (from project root, venv active):
  streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is importable when Streamlit runs app.py
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

import src.config as config
from src.generate import answer_question
from src.ingest import list_pdfs
from src.retrieve import build_index, get_client

# Read settings from module (avoids stale partial imports)
CHROMA_DIR = config.CHROMA_DIR
COLLECTION_NAME = config.COLLECTION_NAME
DATA_DIR = config.DATA_DIR
LLM_MODEL = config.LLM_MODEL
LLM_PROVIDER = config.LLM_PROVIDER
MAX_DISTANCE = config.MAX_DISTANCE
TOP_K = config.TOP_K
XAI_API_KEY = getattr(config, "XAI_API_KEY", "") or ""
GEMINI_API_KEY = getattr(config, "GEMINI_API_KEY", "") or ""


st.set_page_config(
    page_title="RAG Doc Q&A",
    page_icon="📄",
    layout="wide",
)


def index_status() -> tuple[bool, int, str]:
    """Return (ok, count, message)."""
    try:
        client = get_client(CHROMA_DIR)
        col = client.get_collection(COLLECTION_NAME)
        n = col.count()
        if n == 0:
            return False, 0, "Index is empty — click **Rebuild index**."
        return True, n, f"Index ready · **{n}** chunks"
    except Exception:  # noqa: BLE001
        return False, 0, "No index found — click **Rebuild index**."


def render_citations(citations: list) -> None:
    if not citations:
        st.caption("No citations.")
        return
    with st.expander("Sources / citations", expanded=True):
        for i, c in enumerate(citations, start=1):
            dist = f"{c.distance:.4f}" if c.distance is not None else "n/a"
            st.markdown(
                f"**[{i}]** `{c.source_file}` · chunk `{c.chunk_index}` · distance `{dist}`"
            )
            st.caption(c.snippet)


def main() -> None:
    st.title("📄 RAG Document Q&A")
    st.caption(
        "Ask questions about your PDFs. Free by default (extractive mode). "
        "Optional free LLMs: Ollama or Gemini · paid: xAI Grok."
    )

    # ----- Sidebar -----
    with st.sidebar:
        st.header("Setup")
        ok, count, status_msg = index_status()
        if ok:
            st.success(status_msg)
        else:
            st.warning(status_msg)

        pdfs = list_pdfs(DATA_DIR)
        st.subheader("Documents")
        if pdfs:
            for p in pdfs:
                st.markdown(f"- `{p.name}`")
        else:
            st.info("No PDFs in `data/`. Run `python scripts/generate_sample_pdfs.py`.")

        st.subheader("Retrieval")
        top_k = st.slider("Top-k chunks", 1, 8, int(TOP_K))
        max_distance = st.number_input(
            "Max distance (weak retrieval cutoff)",
            min_value=0.1,
            max_value=2.0,
            value=float(MAX_DISTANCE),
            step=0.05,
            help="If the best chunk is farther than this, the app says it doesn't know.",
        )

        st.subheader("Index")
        if st.button("Rebuild index", type="primary", use_container_width=True):
            with st.spinner("Chunking PDFs and embedding into Chroma…"):
                try:
                    stats = build_index(DATA_DIR, reset=True)
                    st.success(
                        f"Indexed {stats['chunk_count']} chunks from "
                        f"{len(stats['by_source'])} file(s)."
                    )
                    st.rerun()
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Index failed: {exc}")

        st.divider()
        st.subheader("Answer mode (free options)")
        provider_labels = {
            "extractive": "Free — extractive (PDF text only, no API)",
            "ollama": "Free — Ollama (local LLM)",
            "gemini": "Free tier — Google Gemini API",
            "xai": "Paid — xAI Grok (needs credits)",
        }
        options = list(provider_labels.keys())
        default_idx = options.index(LLM_PROVIDER) if LLM_PROVIDER in options else 0
        provider = st.selectbox(
            "Provider",
            options=options,
            format_func=lambda k: provider_labels[k],
            index=default_idx,
            help="Extractive needs no key. Gemini: free key from Google AI Studio. "
            "Ollama: install locally. xAI needs paid credits.",
        )

        if provider == "extractive":
            st.success("Using **free extractive** mode — no credits needed.")
        elif provider == "ollama":
            st.info(
                "Requires [Ollama](https://ollama.com) running + "
                "`ollama pull llama3.2` (or set `OLLAMA_MODEL`)."
            )
        elif provider == "gemini":
            if GEMINI_API_KEY:
                st.success(f"Gemini key loaded · model `{LLM_MODEL}`")
            else:
                st.warning(
                    "Add free `GEMINI_API_KEY` in `.env` from "
                    "[aistudio.google.com/apikey](https://aistudio.google.com/apikey)"
                )
        elif provider == "xai":
            if XAI_API_KEY:
                st.warning(
                    f"xAI key present · model `{LLM_MODEL}` — **team needs credits** "
                    "or you'll fall back to extractive."
                )
            else:
                st.error("No `XAI_API_KEY` in `.env`. Prefer free modes above.")

        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.caption("Local demo · secrets stay in `.env` · never commit keys")

    # ----- Chat state -----
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome
    if not st.session_state.messages:
        st.info(
            "Try: *What timeout does ApiClient use?* · "
            "*What is Page Object Model?* · *What is RAG?*"
        )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("citations"):
                render_citations(msg["citations"])
            if msg.get("meta"):
                st.caption(msg["meta"])

    prompt = st.chat_input("Ask a question about your documents…")
    if not prompt:
        return

    # User bubble
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant
    with st.chat_message("assistant"):
        if not ok and count == 0:
            err = (
                "No vector index yet. Click **Rebuild index** in the sidebar, "
                "then ask again."
            )
            st.error(err)
            st.session_state.messages.append({"role": "assistant", "content": err})
            return

        with st.spinner("Retrieving context and generating answer…"):
            try:
                result = answer_question(
                    prompt,
                    top_k=top_k,
                    max_distance=max_distance,
                    provider=provider,
                )
            except Exception as exc:  # noqa: BLE001
                err = f"Could not answer: {exc}"
                st.error(err)
                st.session_state.messages.append(
                    {"role": "assistant", "content": err}
                )
                return

        if result.used_extractive_fallback and result.provider != "extractive":
            st.warning(
                f"LLM provider **{result.provider}** failed — showing document text instead. "
                f"{result.note or ''}"
            )
        elif result.provider == "extractive":
            st.info("Free **extractive** mode: answer is the best matching PDF passage.")
        st.markdown(result.answer)
        render_citations(result.citations)
        meta = (
            f"provider={result.provider} · used_llm={result.used_llm} · "
            f"weak_retrieval={result.weak_retrieval} · top_k={top_k}"
        )
        st.caption(meta)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result.answer,
                "citations": result.citations,
                "meta": meta,
            }
        )


if __name__ == "__main__":
    main()
