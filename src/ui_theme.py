"""
Accessible UI themes for the Streamlit RAG app.

Color choices target WCAG AA contrast for body text on backgrounds.
"""

from __future__ import annotations

from typing import Any

# Theme catalog — tokens only (no Streamlit calls here)
THEMES: dict[str, dict[str, Any]] = {
    "dark": {
        "label": "Dark (default)",
        "description": "Low-glare dark UI for long sessions",
        "bg": "#0b1220",
        "bg_grad_mid": "#111827",
        "bg_grad_end": "#0f172a",
        "surface": "#1e293b",
        "surface_2": "#0f172a",
        "border": "#334155",
        "text": "#f1f5f9",
        "text_muted": "#94a3b8",
        "text_subtle": "#64748b",
        "primary": "#818cf8",
        "primary_soft": "rgba(129, 140, 248, 0.16)",
        "primary_border": "rgba(129, 140, 248, 0.4)",
        "success": "#34d399",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "hero_end": "#1e1b4b",
        "cite_accent": "#818cf8",
        "shadow": "rgba(0,0,0,0.35)",
        "input_bg": "#1e293b",
        "chip_bg": "#1e293b",
    },
    "light": {
        "label": "Light",
        "description": "Clean light theme with indigo accents",
        "bg": "#f8fafc",
        "bg_grad_mid": "#f1f5f9",
        "bg_grad_end": "#eef2ff",
        "surface": "#ffffff",
        "surface_2": "#f8fafc",
        "border": "#e2e8f0",
        "text": "#0f172a",
        "text_muted": "#475569",
        "text_subtle": "#64748b",
        "primary": "#4f46e5",
        "primary_soft": "rgba(79, 70, 229, 0.10)",
        "primary_border": "rgba(79, 70, 229, 0.35)",
        "success": "#059669",
        "warning": "#d97706",
        "danger": "#dc2626",
        "hero_end": "#e0e7ff",
        "cite_accent": "#4f46e5",
        "shadow": "rgba(15, 23, 42, 0.08)",
        "input_bg": "#ffffff",
        "chip_bg": "#ffffff",
    },
    "midnight": {
        "label": "Midnight teal",
        "description": "Cool professional dark with teal accents",
        "bg": "#0a1628",
        "bg_grad_mid": "#0c1a2e",
        "bg_grad_end": "#0b1f24",
        "surface": "#132337",
        "surface_2": "#0d1b2a",
        "border": "#1e3a4c",
        "text": "#e8f4f8",
        "text_muted": "#8ba3b5",
        "text_subtle": "#5c7a8a",
        "primary": "#2dd4bf",
        "primary_soft": "rgba(45, 212, 191, 0.14)",
        "primary_border": "rgba(45, 212, 191, 0.4)",
        "success": "#34d399",
        "warning": "#fbbf24",
        "danger": "#fb7185",
        "hero_end": "#0f3d3a",
        "cite_accent": "#2dd4bf",
        "shadow": "rgba(0,0,0,0.4)",
        "input_bg": "#132337",
        "chip_bg": "#132337",
    },
    "high_contrast": {
        "label": "High contrast",
        "description": "Maximum readability (WCAG AAA-oriented)",
        "bg": "#000000",
        "bg_grad_mid": "#000000",
        "bg_grad_end": "#0a0a0a",
        "surface": "#111111",
        "surface_2": "#000000",
        "border": "#ffffff",
        "text": "#ffffff",
        "text_muted": "#f5f5f5",
        "text_subtle": "#e5e5e5",
        "primary": "#ffff00",
        "primary_soft": "rgba(255, 255, 0, 0.12)",
        "primary_border": "#ffff00",
        "success": "#00ff00",
        "warning": "#ffcc00",
        "danger": "#ff4444",
        "hero_end": "#111111",
        "cite_accent": "#ffff00",
        "shadow": "rgba(255,255,255,0.12)",
        "input_bg": "#111111",
        "chip_bg": "#111111",
    },
}

DEFAULT_THEME = "dark"


def theme_options() -> dict[str, str]:
    """id -> label for selectboxes."""
    return {k: v["label"] for k, v in THEMES.items()}


def build_css(theme_id: str) -> str:
    """Return full CSS string for the selected theme."""
    t = THEMES.get(theme_id, THEMES[DEFAULT_THEME])

    return f"""
<style>
  :root {{
    --bg: {t["bg"]};
    --bg-mid: {t["bg_grad_mid"]};
    --bg-end: {t["bg_grad_end"]};
    --surface: {t["surface"]};
    --surface-2: {t["surface_2"]};
    --border: {t["border"]};
    --text: {t["text"]};
    --text-muted: {t["text_muted"]};
    --text-subtle: {t["text_subtle"]};
    --primary: {t["primary"]};
    --primary-soft: {t["primary_soft"]};
    --primary-border: {t["primary_border"]};
    --success: {t["success"]};
    --warning: {t["warning"]};
    --danger: {t["danger"]};
    --hero-end: {t["hero_end"]};
    --cite: {t["cite_accent"]};
    --shadow: {t["shadow"]};
    --input-bg: {t["input_bg"]};
    --chip-bg: {t["chip_bg"]};
  }}

  html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: linear-gradient(165deg, var(--bg) 0%, var(--bg-mid) 48%, var(--bg-end) 100%) !important;
    color: var(--text) !important;
  }}

  [data-testid="stHeader"] {{
    background: transparent !important;
  }}

  [data-testid="stSidebar"] {{
    background: var(--surface-2) !important;
    border-right: 1px solid var(--border) !important;
  }}
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] span {{
    color: var(--text-muted) !important;
  }}

  h1, h2, h3, h4 {{
    color: var(--text) !important;
    letter-spacing: -0.02em;
  }}

  p, label, .stMarkdown, .stCaption, span {{
    color: var(--text-muted) !important;
  }}

  /* Inputs / widgets */
  .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {{
    background-color: var(--input-bg) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
  }}
  .stSlider label {{ color: var(--text-muted) !important; }}

  /* Buttons */
  .stButton > button {{
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    color: var(--text) !important;
    font-weight: 600 !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
  }}
  .stButton > button:hover {{
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 1px var(--primary-border);
  }}
  .stButton > button[kind="primary"] {{
    background: var(--primary-soft) !important;
    border-color: var(--primary-border) !important;
    color: var(--text) !important;
  }}

  /* Chat */
  [data-testid="stChatMessage"] {{
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 0.35rem 0.5rem !important;
  }}

  /* Hero */
  .hero {{
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 50%, var(--hero-end) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.35rem 1.5rem 1.15rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 12px 36px var(--shadow);
  }}
  .hero-badge {{
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--primary);
    background: var(--primary-soft);
    border: 1px solid var(--primary-border);
    border-radius: 999px;
    padding: 0.28rem 0.75rem;
    margin-bottom: 0.6rem;
  }}
  .hero h1 {{
    margin: 0 0 0.35rem 0 !important;
    font-size: 1.7rem !important;
    font-weight: 750 !important;
    color: var(--text) !important;
  }}
  .hero p {{
    margin: 0 !important;
    color: var(--text-muted) !important;
    font-size: 0.96rem;
    line-height: 1.55;
  }}

  /* Stats */
  .stat-row {{
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin: 0.75rem 0 1rem 0;
  }}
  .stat {{
    flex: 1 1 130px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.8rem 0.95rem;
    min-width: 110px;
    box-shadow: 0 4px 14px var(--shadow);
  }}
  .stat .label {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-subtle);
    margin-bottom: 0.25rem;
    font-weight: 600;
  }}
  .stat .value {{
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
  }}
  .stat .value.ok {{ color: var(--success); }}
  .stat .value.warn {{ color: var(--warning); }}

  .chip-label {{
    font-size: 0.8rem;
    color: var(--text-subtle);
    margin: 0.35rem 0 0.45rem 0;
    font-weight: 600;
  }}

  .cite-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--cite);
    border-radius: 10px;
    padding: 0.7rem 0.85rem;
    margin: 0.4rem 0;
  }}
  .cite-card .meta {{
    font-size: 0.8rem;
    color: var(--primary);
    font-weight: 700;
    margin-bottom: 0.28rem;
  }}
  .cite-card .snip {{
    font-size: 0.86rem;
    color: var(--text-muted);
    line-height: 1.45;
  }}

  .side-section-title {{
    font-size: 0.72rem;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--text-subtle) !important;
    margin: 0.85rem 0 0.4rem 0;
  }}
  .doc-pill {{
    background: var(--chip-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.4rem 0.6rem;
    margin: 0.3rem 0;
    font-size: 0.8rem;
    color: var(--text);
    word-break: break-all;
  }}
  .theme-hint {{
    font-size: 0.78rem;
    color: var(--text-subtle) !important;
    margin-top: 0.25rem;
  }}

  footer {{ visibility: hidden; }}
  #MainMenu {{ visibility: hidden; }}
</style>
"""
