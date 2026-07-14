"""
Streamlit chat UI for RAG Document Q&A (polished UI).

Run (from project root, venv active):
  streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

import src.config as config
from src.generate import answer_question
from src.ingest import list_pdfs
from src.retrieve import build_index, get_client

CHROMA_DIR = config.CHROMA_DIR
COLLECTION_NAME = config.COLLECTION_NAME
DATA_DIR = config.DATA_DIR
LLM_MODEL = config.LLM_MODEL
LLM_PROVIDER = config.LLM_PROVIDER
MAX_DISTANCE = config.MAX_DISTANCE
TOP_K = config.TOP_K
XAI_API_KEY = getattr(config, "XAI_API_KEY", "") or ""
GEMINI_API_KEY = getattr(config, "GEMINI_API_KEY", "") or ""

EXAMPLE_QUESTIONS = [
    "What timeout does ApiClient use?",
    "What is Page Object Model?",
    "What is RAG?",
    "How many automated tests are in the API suite?",
]

PROVIDER_LABELS = {
    "extractive": "Free · Extractive (PDF text)",
    "ollama": "Free · Ollama (local LLM)",
    "gemini": "Free tier · Google Gemini",
    "xai": "Paid · xAI Grok",
}


st.set_page_config(
    page_title="RAG Doc Q&A · Nilima",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        """
<style>
  /* ----- Global ----- */
  .stApp {
    background: linear-gradient(165deg, #0b1220 0%, #111827 45%, #0f172a 100%);
  }
  [data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
  }
  [data-testid="stSidebar"] * {
    color: #e2e8f0;
  }
  h1, h2, h3 {
    color: #f8fafc !important;
    letter-spacing: -0.02em;
  }
  p, label, .stMarkdown, .stCaption {
    color: #cbd5e1 !important;
  }

  /* ----- Hero ----- */
  .hero {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 55%, #1e1b4b 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.4rem 1.6rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
  }
  .hero-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #a5b4fc;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(129, 140, 248, 0.35);
    border-radius: 999px;
    padding: 0.25rem 0.7rem;
    margin-bottom: 0.65rem;
  }
  .hero h1 {
    margin: 0 0 0.35rem 0 !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #f8fafc !important;
  }
  .hero p {
    margin: 0 !important;
    color: #94a3b8 !important;
    font-size: 0.98rem;
    line-height: 1.5;
  }

  /* ----- Stat cards ----- */
  .stat-row {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin: 0.85rem 0 1.1rem 0;
  }
  .stat {
    flex: 1 1 140px;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    min-width: 120px;
  }
  .stat .label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 0.25rem;
  }
  .stat .value {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f1f5f9;
  }
  .stat .value.ok { color: #34d399; }
  .stat .value.warn { color: #fbbf24; }

  /* ----- Example chips ----- */
  .chip-label {
    font-size: 0.8rem;
    color: #94a3b8;
    margin: 0.5rem 0 0.4rem 0;
  }

  /* ----- Citation cards ----- */
  .cite-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-left: 3px solid #818cf8;
    border-radius: 10px;
    padding: 0.75rem 0.9rem;
    margin: 0.45rem 0;
  }
  .cite-card .meta {
    font-size: 0.8rem;
    color: #a5b4fc;
    font-weight: 600;
    margin-bottom: 0.3rem;
  }
  .cite-card .snip {
    font-size: 0.86rem;
    color: #cbd5e1;
    line-height: 1.45;
  }

  /* ----- Sidebar polish ----- */
  .side-section-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b !important;
    margin: 0.8rem 0 0.4rem 0;
  }
  .doc-pill {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.4rem 0.6rem;
    margin: 0.3rem 0;
    font-size: 0.8rem;
    color: #e2e8f0;
    word-break: break-all;
  }

  /* Hide default footer noise a bit */
  footer { visibility: hidden; }
  #MainMenu { visibility: hidden; }
</style>
        """,
        unsafe_allow_html=True,
    )


def index_status() -> tuple[bool, int, str]:
    try:
        client = get_client(CHROMA_DIR)
        col = client.get_collection(COLLECTION_NAME)
        n = col.count()
        if n == 0:
            return False, 0, "Empty — rebuild index"
        return True, n, f"{n} chunks ready"
    except Exception:  # noqa: BLE001
        return False, 0, "Not built yet"


def render_citations(citations: list) -> None:
    if not citations:
        st.caption("No citations returned.")
        return
    with st.expander(f"📎 Sources ({len(citations)})", expanded=True):
        for i, c in enumerate(citations, start=1):
            dist = f"{c.distance:.4f}" if c.distance is not None else "n/a"
            st.markdown(
                f"""
<div class="cite-card">
  <div class="meta">[{i}] {c.source_file} · chunk {c.chunk_index} · distance {dist}</div>
  <div class="snip">{c.snippet}</div>
</div>
                """,
                unsafe_allow_html=True,
            )


def provider_status_message(provider: str) -> None:
    if provider == "extractive":
        st.success("Free mode — answers from matching PDF text (no API cost).")
    elif provider == "ollama":
        st.info("Needs Ollama running locally (`ollama pull llama3.2`).")
    elif provider == "gemini":
        if GEMINI_API_KEY:
            st.success(f"Gemini ready · model `{LLM_MODEL}`")
        else:
            st.warning(
                "Add free `GEMINI_API_KEY` in `.env` → "
                "[aistudio.google.com/apikey](https://aistudio.google.com/apikey)"
            )
    elif provider == "xai":
        if XAI_API_KEY:
            st.warning("xAI key set — needs **credits** or falls back to extractive.")
        else:
            st.error("No XAI key — prefer free modes above.")


def main() -> None:
    inject_css()

    ok, count, status_msg = index_status()
    pdfs = list_pdfs(DATA_DIR)

    # ----- Sidebar -----
    with st.sidebar:
        st.markdown("### ⚙️ Control panel")
        st.markdown(
            '<p class="side-section-title">Index health</p>',
            unsafe_allow_html=True,
        )
        if ok:
            st.success(status_msg)
        else:
            st.warning(status_msg)

        st.markdown(
            '<p class="side-section-title">Documents in data/</p>',
            unsafe_allow_html=True,
        )
        if pdfs:
            for p in pdfs:
                st.markdown(
                    f'<div class="doc-pill">📄 {p.name}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No PDFs. Run `python scripts/generate_sample_pdfs.py`.")

        st.markdown(
            '<p class="side-section-title">Retrieval</p>',
            unsafe_allow_html=True,
        )
        top_k = st.slider("Top‑k chunks", 1, 8, int(TOP_K))
        max_distance = st.slider(
            "Max distance (stricter = lower)",
            min_value=0.3,
            max_value=1.5,
            value=min(max(float(MAX_DISTANCE), 0.3), 1.5),
            step=0.05,
            help="If the best chunk is farther than this, answer is “I don’t know”.",
        )

        st.markdown(
            '<p class="side-section-title">Index actions</p>',
            unsafe_allow_html=True,
        )
        if st.button("🔄 Rebuild index", type="primary", use_container_width=True):
            with st.spinner("Chunking PDFs and embedding into Chroma…"):
                try:
                    stats = build_index(DATA_DIR, reset=True)
                    st.success(
                        f"Indexed **{stats['chunk_count']}** chunks from "
                        f"**{len(stats['by_source'])}** file(s)."
                    )
                    st.rerun()
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Index failed: {exc}")

        st.markdown(
            '<p class="side-section-title">Answer mode</p>',
            unsafe_allow_html=True,
        )
        options = list(PROVIDER_LABELS.keys())
        default_idx = options.index(LLM_PROVIDER) if LLM_PROVIDER in options else 0
        provider = st.selectbox(
            "Provider",
            options=options,
            format_func=lambda k: PROVIDER_LABELS[k],
            index=default_idx,
            label_visibility="collapsed",
        )
        provider_status_message(provider)

        st.markdown(
            '<p class="side-section-title">Chat</p>',
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with c2:
            st.caption("Local demo")

        st.markdown("---")
        st.caption(
            "Built by **Nilima Satapathy** · "
            "[GitHub](https://github.com/nilima-satapathy/rag-doc-qa) · "
            "secrets stay in `.env`"
        )

    # ----- Main hero -----
    st.markdown(
        """
<div class="hero">
  <div class="hero-badge">Project 3 · RAG portfolio</div>
  <h1>📄 Document Q&amp;A</h1>
  <p>
    Ask questions about your PDFs. The app retrieves the best matching chunks,
    then answers with citations — free extractive mode by default, or Gemini / Ollama / Grok.
  </p>
</div>
        """,
        unsafe_allow_html=True,
    )

    # Stat cards
    provider_short = PROVIDER_LABELS.get(provider, provider).split("·")[-1].strip()
    st.markdown(
        f"""
<div class="stat-row">
  <div class="stat">
    <div class="label">Index</div>
    <div class="value {'ok' if ok else 'warn'}">{status_msg}</div>
  </div>
  <div class="stat">
    <div class="label">Documents</div>
    <div class="value">{len(pdfs)} PDF{'s' if len(pdfs) != 1 else ''}</div>
  </div>
  <div class="stat">
    <div class="label">Answer mode</div>
    <div class="value" style="font-size:1rem;">{provider_short}</div>
  </div>
  <div class="stat">
    <div class="label">Top‑k</div>
    <div class="value">{top_k}</div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    # ----- Chat state -----
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Example question buttons (only when chat empty)
    if not st.session_state.messages:
        st.markdown(
            '<p class="chip-label">Try an example question</p>',
            unsafe_allow_html=True,
        )
        cols = st.columns(2)
        for i, q in enumerate(EXAMPLE_QUESTIONS):
            with cols[i % 2]:
                if st.button(q, key=f"ex_{i}", use_container_width=True):
                    st.session_state._pending_prompt = q
                    st.rerun()

    # History
    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg.get("citations"):
                render_citations(msg["citations"])
            if msg.get("meta"):
                st.caption(msg["meta"])

    # Pending example click or chat input
    prompt = st.session_state.pop("_pending_prompt", None) or st.chat_input(
        "Ask anything about your indexed PDFs…"
    )
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        if not ok and count == 0:
            err = (
                "No vector index yet. Click **Rebuild index** in the sidebar, "
                "then ask again."
            )
            st.error(err)
            st.session_state.messages.append({"role": "assistant", "content": err})
            return

        with st.spinner("Searching your documents and building an answer…"):
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
                f"Provider **{result.provider}** failed — showing document text instead. "
                f"{result.note or ''}"
            )
        elif result.provider == "extractive":
            st.info("Extractive mode: best matching passage from your PDFs.")
        elif result.weak_retrieval:
            st.warning("Weak retrieval — answer may be “I don’t know”.")

        st.markdown(result.answer)
        render_citations(result.citations)
        meta = (
            f"provider={result.provider} · llm={result.used_llm} · "
            f"weak={result.weak_retrieval} · top_k={top_k}"
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
