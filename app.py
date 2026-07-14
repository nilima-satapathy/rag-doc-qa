"""
Streamlit chat UI for RAG Document Q&A.

Features:
  - Accessible multi-theme design (light / dark / midnight / high contrast)
  - Theme picker in Settings (persists for the browser session)
  - Chat + citations + index controls

Run:
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
from src.ui_theme import DEFAULT_THEME, THEMES, build_css, theme_options

CHROMA_DIR = config.CHROMA_DIR
COLLECTION_NAME = config.COLLECTION_NAME
DATA_DIR = config.DATA_DIR
LLM_MODEL = config.LLM_MODEL
LLM_PROVIDER = config.LLM_PROVIDER
MAX_DISTANCE = config.MAX_DISTANCE
TOP_K = config.TOP_K

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


def init_theme() -> str:
    if "ui_theme" not in st.session_state:
        st.session_state.ui_theme = DEFAULT_THEME
    theme_id = st.session_state.ui_theme
    if theme_id not in THEMES:
        theme_id = DEFAULT_THEME
        st.session_state.ui_theme = theme_id
    return theme_id


def apply_theme(theme_id: str) -> None:
    st.markdown(build_css(theme_id), unsafe_allow_html=True)


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
            # Escape not needed for our controlled snippets; keep simple
            snip = (c.snippet or "").replace("<", "&lt;").replace(">", "&gt;")
            st.markdown(
                f"""
<div class="cite-card">
  <div class="meta">[{i}] {c.source_file} · chunk {c.chunk_index} · distance {dist}</div>
  <div class="snip">{snip}</div>
</div>
                """,
                unsafe_allow_html=True,
            )


def provider_status_message(provider: str) -> None:
    # Re-read .env every sidebar render so a saved key shows up after refresh
    gemini_key = config.get_gemini_api_key()
    xai_key = config.get_xai_api_key()

    if provider == "extractive":
        st.success("Free mode — answers from matching PDF text (no API cost).")
    elif provider == "ollama":
        st.info("Needs Ollama running locally (`ollama pull llama3.2`).")
    elif provider == "gemini":
        if gemini_key:
            st.success(
                f"Gemini key loaded ({len(gemini_key)} chars) · "
                f"model `{config.GEMINI_MODEL}`"
            )
        else:
            st.error(
                "**GEMINI_API_KEY not found in `.env`.**  \n"
                "File must be: `rag-doc-qa/.env` (next to `app.py`).  \n"
                "Line must be exactly: `GEMINI_API_KEY=AIza...`  \n"
                "Then **restart** Streamlit (Ctrl+C → `streamlit run app.py`)."
            )
    elif provider == "xai":
        if xai_key:
            st.warning("xAI key set — needs **credits** or falls back to extractive.")
        else:
            st.error("No XAI key — prefer free modes above.")


def main() -> None:
    theme_id = init_theme()
    apply_theme(theme_id)

    ok, count, status_msg = index_status()
    pdfs = list_pdfs(DATA_DIR)
    options_map = theme_options()

    # ----- Sidebar -----
    with st.sidebar:
        st.markdown("### ⚙️ Settings")

        # ---- Appearance / theme ----
        st.markdown(
            '<p class="side-section-title">Appearance</p>',
            unsafe_allow_html=True,
        )
        theme_keys = list(options_map.keys())
        try:
            theme_index = theme_keys.index(theme_id)
        except ValueError:
            theme_index = 0

        new_theme = st.selectbox(
            "Page theme",
            options=theme_keys,
            format_func=lambda k: options_map[k],
            index=theme_index,
            help="Colors follow accessible contrast standards. High contrast is best for low vision.",
        )
        if new_theme != st.session_state.ui_theme:
            st.session_state.ui_theme = new_theme
            st.rerun()

        st.markdown(
            f'<p class="theme-hint">{THEMES[new_theme]["description"]}</p>',
            unsafe_allow_html=True,
        )

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
        prov_options = list(PROVIDER_LABELS.keys())
        default_idx = (
            prov_options.index(LLM_PROVIDER) if LLM_PROVIDER in prov_options else 0
        )
        provider = st.selectbox(
            "Provider",
            options=prov_options,
            format_func=lambda k: PROVIDER_LABELS[k],
            index=default_idx,
            label_visibility="collapsed",
        )
        provider_status_message(provider)

        st.markdown(
            '<p class="side-section-title">Chat</p>',
            unsafe_allow_html=True,
        )
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.caption(
            "Built by **Nilima Satapathy** · "
            "[GitHub](https://github.com/nilima-satapathy/rag-doc-qa) · "
            "Theme applies for this browser session"
        )

    # ----- Main hero -----
    st.markdown(
        """
<div class="hero">
  <div class="hero-badge">Project 3 · RAG portfolio</div>
  <h1>📄 Document Q&amp;A</h1>
  <p>
    Ask questions about your PDFs. Retrieval finds the best chunks; answers include citations.
    Change the page theme anytime in <strong>Settings → Appearance</strong>.
  </p>
</div>
        """,
        unsafe_allow_html=True,
    )

    provider_short = PROVIDER_LABELS.get(provider, provider).split("·")[-1].strip()
    theme_label = options_map.get(theme_id, theme_id)
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
    <div class="label">Theme</div>
    <div class="value" style="font-size:0.95rem;">{theme_label}</div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    # ----- Chat state -----
    if "messages" not in st.session_state:
        st.session_state.messages = []

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

    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg.get("citations"):
                render_citations(msg["citations"])
            if msg.get("meta"):
                st.caption(msg["meta"])

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
            f"weak={result.weak_retrieval} · top_k={top_k} · theme={theme_id}"
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
