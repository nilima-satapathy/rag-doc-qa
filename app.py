"""
RAG Document Q&A — professional Streamlit UI (LinkedIn / portfolio ready).

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
    page_title="DocQ — Document Q&A",
    page_icon="📄",
    layout="wide",
    # Left Settings panel starts open; user can collapse/expand anytime
    initial_sidebar_state="expanded",
    menu_items={
        "About": "DocQ — RAG document Q&A by Nilima Satapathy",
    },
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
    with st.expander(f"Sources · {len(citations)} retrieved", expanded=True):
        for i, c in enumerate(citations, start=1):
            dist = f"{c.distance:.3f}" if c.distance is not None else "n/a"
            snip = (c.snippet or "").replace("<", "&lt;").replace(">", "&gt;")
            st.markdown(
                f"""
<div class="cite-card">
  <div class="meta">[{i}] {c.source_file}  ·  chunk {c.chunk_index}  ·  d={dist}</div>
  <div class="snip">{snip}</div>
</div>
                """,
                unsafe_allow_html=True,
            )


def provider_status_message(provider: str) -> None:
    gemini_key = config.get_gemini_api_key()
    xai_key = config.get_xai_api_key()

    if provider == "extractive":
        st.success("Free mode — matching PDF passages (no API).")
    elif provider == "ollama":
        st.info("Requires local Ollama (`ollama pull llama3.2`).")
    elif provider == "gemini":
        if gemini_key:
            st.success(f"Gemini connected · `{config.GEMINI_MODEL}`")
        else:
            st.error(
                "Add `GEMINI_API_KEY` to `.env`, then restart Streamlit.  \n"
                "[Get free key](https://aistudio.google.com/apikey)"
            )
    elif provider == "xai":
        if xai_key:
            st.warning("xAI key set — needs credits, else falls back.")
        else:
            st.error("No XAI key — use Gemini or Extractive.")


def main() -> None:
    theme_id = init_theme()
    apply_theme(theme_id)

    ok, count, status_msg = index_status()
    pdfs = list_pdfs(DATA_DIR)
    options_map = theme_options()

    # ---------- Left Settings panel (native Streamlit sidebar) ----------
    # Expand: click » when panel is closed (top-left).
    # Collapse: click « in the Settings header area (Streamlit control).
    with st.sidebar:
        st.markdown(
            """
<div style="
  display:flex; align-items:center; justify-content:space-between;
  gap:10px; margin:0 0 0.85rem 0; padding-bottom:0.65rem;
  border-bottom:1px solid rgba(128,128,128,0.25);
">
  <div style="font-size:1.45rem; font-weight:800; letter-spacing:-0.03em;">
    Settings
  </div>
  <div style="
    font-size:0.72rem; font-weight:650; letter-spacing:0.04em;
    text-transform:uppercase; opacity:0.65; white-space:nowrap;
  " title="Use « at the top of this panel to collapse">« collapse</div>
</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p class="side-section-title">Appearance</p>',
            unsafe_allow_html=True,
        )

        theme_keys = list(options_map.keys())
        theme_index = theme_keys.index(theme_id) if theme_id in theme_keys else 0
        new_theme = st.selectbox(
            "Theme",
            options=theme_keys,
            format_func=lambda k: options_map[k],
            index=theme_index,
            label_visibility="collapsed",
            key="theme_select",
        )
        if new_theme != st.session_state.ui_theme:
            st.session_state.ui_theme = new_theme
            st.rerun()
        st.markdown(
            f'<p class="theme-hint">{THEMES[new_theme]["description"]}</p>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p class="side-section-title">System</p>',
            unsafe_allow_html=True,
        )
        if ok:
            st.success(status_msg)
        else:
            st.warning(status_msg)

        st.markdown(
            '<p class="side-section-title">Knowledge base</p>',
            unsafe_allow_html=True,
        )
        if pdfs:
            pdf_names = [p.name for p in pdfs]
            st.selectbox(
                "Knowledge base",
                options=pdf_names,
                index=0,
                label_visibility="collapsed",
                key="kb_select",
                help="PDFs currently indexed from the data/ folder.",
            )
            st.caption(f"{len(pdf_names)} document(s) available")
        else:
            st.info("No PDFs in data/")

        st.markdown(
            '<p class="side-section-title">Retrieval</p>',
            unsafe_allow_html=True,
        )
        top_k = st.slider("Top‑k chunks", 1, 8, int(TOP_K))
        max_distance = st.slider(
            "Max distance",
            0.3,
            1.5,
            min(max(float(MAX_DISTANCE), 0.3), 1.5),
            0.05,
            help="Stricter (lower) → more “I don’t know” when weak match.",
        )

        if st.button("Rebuild index", type="primary", use_container_width=True):
            with st.spinner("Indexing PDFs…"):
                try:
                    stats = build_index(DATA_DIR, reset=True)
                    st.success(
                        f"Indexed {stats['chunk_count']} chunks · "
                        f"{len(stats['by_source'])} files"
                    )
                    st.rerun()
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Index failed: {exc}")

        st.markdown(
            '<p class="side-section-title">Answer engine</p>',
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

        if st.button("Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown(
            """
<div class="side-footer">
  Built by <strong>Nilima Satapathy</strong><br/>
  AI Test · SDET · GenAI Quality<br/>
  <a href="https://github.com/nilima-satapathy/rag-doc-qa" target="_blank">github.com/nilima-satapathy/rag-doc-qa</a>
</div>
            """,
            unsafe_allow_html=True,
        )

    # ---------- Main site header (inline styles so Streamlit cannot override) ----------
    pill_bg = "rgba(62, 207, 142, 0.14)" if ok else "rgba(232, 179, 57, 0.14)"
    pill_color = "#3ecf8e" if ok else "#e8b339"
    st.markdown(
        f"""
<div style="
  display:flex; align-items:flex-start; justify-content:space-between;
  gap:20px; margin:0 0 1.4rem 0; padding:0.25rem 0 1.2rem 0;
  border-bottom:1px solid rgba(128,128,128,0.25);
">
  <div>
    <div role="heading" aria-level="1" style="
      margin:0; padding:0;
      font-size:3.6rem; font-weight:800; line-height:1.05;
      letter-spacing:-0.06em; font-family:DM Sans, Segoe UI, system-ui, sans-serif;
    ">
      <span style="color:inherit;">Doc</span><span style="color:#6d7cff;">Q</span>
    </div>
    <div style="
      margin-top:0.35rem; font-size:1rem; font-weight:650;
      letter-spacing:0.06em; text-transform:lowercase;
      color:#6d7cff; font-family:JetBrains Mono, Consolas, monospace;
    ">docq.app · document Q&amp;A</div>
    <div style="
      margin-top:0.45rem; font-size:1.15rem; font-weight:500;
      line-height:1.45; max-width:36rem; opacity:0.85;
      font-family:DM Sans, Segoe UI, system-ui, sans-serif;
    ">Your documents, searchable answers — every reply includes sources</div>
  </div>
  <div style="
    display:inline-flex; align-items:center; gap:8px; white-space:nowrap;
    font-size:0.9rem; font-weight:700; letter-spacing:0.04em; text-transform:uppercase;
    color:{pill_color}; background:{pill_bg}; border:1px solid {pill_color}55;
    border-radius:999px; padding:0.5rem 0.95rem; margin-top:0.35rem;
  ">
    <span style="
      width:8px; height:8px; border-radius:50%; background:{pill_color};
      box-shadow:0 0 0 3px {pill_color}33; display:inline-block;
    "></span>
    {status_msg}
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    # About panel — collapsed by default; click to expand
    with st.expander("About DocQ · what this app is", expanded=False):
        st.markdown(
            """
**DocQ** is a retrieval-augmented document Q&A app (RAG).

Upload or index PDFs, ask questions in natural language, and get answers grounded in your files — with **citations** so you can verify every claim.

| | |
|--|--|
| **What it does** | PDF ingest → chunk → vector search → grounded answer + sources |
| **Stack** | Python · Chroma · Streamlit · Gemini / Extractive / Ollama |
| **Eval** | Retrieval hit@3 **13/13** on the in-corpus golden set |
| **Built by** | Nilima Satapathy · AI Test / SDET / GenAI Quality |
| **Repo** | [github.com/nilima-satapathy/rag-doc-qa](https://github.com/nilima-satapathy/rag-doc-qa) |

**Portfolio note:** Project 3 on the public AI career journey — designed to demonstrate product-quality GenAI + test-engineering craft for hiring managers.
            """
        )
        st.caption(
            "Project 3 · Portfolio · GenAI Quality  ·  Python · Chroma · Gemini · Streamlit"
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
    <div class="label">Corpus</div>
    <div class="value">{len(pdfs)} PDF{'s' if len(pdfs) != 1 else ''}</div>
  </div>
  <div class="stat">
    <div class="label">Engine</div>
    <div class="value" style="font-size:0.98rem">{provider_short}</div>
  </div>
  <div class="stat">
    <div class="label">Theme</div>
    <div class="value" style="font-size:0.95rem">{theme_label}</div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown(
            '<p class="section-label">Quick prompts</p>',
            unsafe_allow_html=True,
        )
        cols = st.columns(2)
        for i, q in enumerate(EXAMPLE_QUESTIONS):
            with cols[i % 2]:
                if st.button(q, key=f"ex_{i}", use_container_width=True):
                    st.session_state._pending_prompt = q
                    st.rerun()

    for msg in st.session_state.messages:
        avatar = "◉" if msg["role"] == "user" else "◆"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg.get("citations"):
                render_citations(msg["citations"])
            if msg.get("meta"):
                st.caption(msg["meta"])

    prompt = st.session_state.pop("_pending_prompt", None) or st.chat_input(
        "Ask a question about your knowledge base…"
    )
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="◉"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="◆"):
        if not ok and count == 0:
            err = "Index not ready. Use **Rebuild index** in the sidebar, then retry."
            st.error(err)
            st.session_state.messages.append({"role": "assistant", "content": err})
            return

        with st.spinner("Retrieving context and composing answer…"):
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
                f"Engine **{result.provider}** unavailable — showing document extract. "
                f"{result.note or ''}"
            )
        elif result.provider == "extractive":
            st.info("Extractive mode: best matching passage from your PDFs.")
        elif result.weak_retrieval:
            st.warning("Weak retrieval match — answer may be incomplete.")

        st.markdown(result.answer)
        render_citations(result.citations)
        meta = (
            f"{result.provider} · llm={result.used_llm} · "
            f"top_k={top_k} · {theme_id}"
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
