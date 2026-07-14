"""
LinkedIn-ready professional themes for RAG Doc Q&A.

Designed for portfolio screenshots: clear hierarchy, restrained color,
high contrast text, and a product-quality SaaS aesthetic.
"""

from __future__ import annotations

from typing import Any

THEMES: dict[str, dict[str, Any]] = {
    "professional_dark": {
        "label": "Professional Dark",
        "description": "LinkedIn-ready dark product UI (recommended)",
        "bg": "#0c111b",
        "bg_mid": "#0f1520",
        "bg_end": "#121a27",
        "sidebar": "#0a0f18",
        "surface": "#151d2b",
        "surface_elevated": "#1a2436",
        "border": "#243044",
        "border_soft": "#1c2738",
        "text": "#f3f6fb",
        "text_secondary": "#c5d0e0",
        "text_muted": "#8b9bb0",
        "text_faint": "#5c6b82",
        "primary": "#6d7cff",
        "primary_hover": "#8b97ff",
        "primary_soft": "rgba(109, 124, 255, 0.12)",
        "primary_border": "rgba(109, 124, 255, 0.35)",
        "success": "#3ecf8e",
        "success_soft": "rgba(62, 207, 142, 0.12)",
        "warning": "#e8b339",
        "danger": "#f07178",
        "user_msg": "#1e2a4a",
        "bot_msg": "#151d2b",
        "hero_glow": "rgba(109, 124, 255, 0.08)",
        "shadow": "0 12px 40px rgba(0, 0, 0, 0.45)",
        "radius": "14px",
    },
    "professional_light": {
        "label": "Professional Light",
        "description": "Clean light SaaS — great for LinkedIn daytime screenshots",
        "bg": "#f4f6fa",
        "bg_mid": "#eef1f7",
        "bg_end": "#e8ecf4",
        "sidebar": "#ffffff",
        "surface": "#ffffff",
        "surface_elevated": "#ffffff",
        "border": "#d8dee9",
        "border_soft": "#e8edf5",
        "text": "#0f172a",
        "text_secondary": "#334155",
        "text_muted": "#64748b",
        "text_faint": "#94a3b8",
        "primary": "#4f46e5",
        "primary_hover": "#4338ca",
        "primary_soft": "rgba(79, 70, 229, 0.08)",
        "primary_border": "rgba(79, 70, 229, 0.28)",
        "success": "#059669",
        "success_soft": "rgba(5, 150, 105, 0.1)",
        "warning": "#d97706",
        "danger": "#dc2626",
        "user_msg": "#eef2ff",
        "bot_msg": "#ffffff",
        "hero_glow": "rgba(79, 70, 229, 0.06)",
        "shadow": "0 10px 30px rgba(15, 23, 42, 0.08)",
        "radius": "14px",
    },
    "executive_slate": {
        "label": "Executive Slate",
        "description": "Muted charcoal — serious, executive presence",
        "bg": "#12141a",
        "bg_mid": "#161922",
        "bg_end": "#1a1d27",
        "sidebar": "#0e1016",
        "surface": "#1c1f2a",
        "surface_elevated": "#222633",
        "border": "#2e3444",
        "border_soft": "#252a38",
        "text": "#f1f3f7",
        "text_secondary": "#c8ceda",
        "text_muted": "#9aa3b5",
        "text_faint": "#6b7385",
        "primary": "#a78bfa",
        "primary_hover": "#c4b5fd",
        "primary_soft": "rgba(167, 139, 250, 0.12)",
        "primary_border": "rgba(167, 139, 250, 0.35)",
        "success": "#34d399",
        "success_soft": "rgba(52, 211, 153, 0.12)",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "user_msg": "#2a2540",
        "bot_msg": "#1c1f2a",
        "hero_glow": "rgba(167, 139, 250, 0.07)",
        "shadow": "0 12px 40px rgba(0, 0, 0, 0.5)",
        "radius": "14px",
    },
}

DEFAULT_THEME = "professional_dark"


def theme_options() -> dict[str, str]:
    return {k: v["label"] for k, v in THEMES.items()}


def build_css(theme_id: str) -> str:
    t = THEMES.get(theme_id, THEMES[DEFAULT_THEME])
    r = t["radius"]

    return f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {{
    --bg: {t["bg"]};
    --bg-mid: {t["bg_mid"]};
    --bg-end: {t["bg_end"]};
    --sidebar: {t["sidebar"]};
    --surface: {t["surface"]};
    --surface-2: {t["surface_elevated"]};
    --border: {t["border"]};
    --border-soft: {t["border_soft"]};
    --text: {t["text"]};
    --text-2: {t["text_secondary"]};
    --muted: {t["text_muted"]};
    --faint: {t["text_faint"]};
    --primary: {t["primary"]};
    --primary-hover: {t["primary_hover"]};
    --primary-soft: {t["primary_soft"]};
    --primary-border: {t["primary_border"]};
    --success: {t["success"]};
    --success-soft: {t["success_soft"]};
    --warning: {t["warning"]};
    --danger: {t["danger"]};
    --user-msg: {t["user_msg"]};
    --bot-msg: {t["bot_msg"]};
    --hero-glow: {t["hero_glow"]};
    --shadow: {t["shadow"]};
    --radius: {r};
    --font: "DM Sans", "Segoe UI", system-ui, sans-serif;
    --mono: "JetBrains Mono", ui-monospace, monospace;
    --fs-base: 17px;
    --fs-sm: 0.95rem;
    --fs-md: 1.05rem;
    --fs-lg: 1.15rem;
  }}

  html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: linear-gradient(165deg, var(--bg) 0%, var(--bg-mid) 50%, var(--bg-end) 100%) !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
    font-size: 18px !important;
  }}

  /* Force larger type across the whole app (high specificity) */
  .stApp, .stApp * {{
    font-size: inherit;
  }}
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] span,
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
  section.main p,
  section.main span,
  section.main label,
  section.main li,
  section.main div[data-testid="stMarkdownContainer"] p,
  section.main div[data-testid="stChatMessageContent"] p,
  section.main div[data-testid="stChatMessageContent"] li {{
    font-size: 1.12rem !important;
    line-height: 1.55 !important;
  }}
  section.main div[data-testid="stCaptionContainer"] p,
  section[data-testid="stSidebar"] .stCaption {{
    font-size: 1rem !important;
  }}
  section.main .stButton > button,
  section[data-testid="stSidebar"] .stButton > button {{
    font-size: 1.08rem !important;
    padding: 0.6rem 1.05rem !important;
    min-height: 2.75rem !important;
  }}
  section[data-testid="stSidebar"] h3 {{
    font-size: 1.5rem !important;
  }}
  div[data-baseweb="select"] > div {{
    font-size: 1.08rem !important;
    min-height: 2.85rem !important;
  }}
  [data-testid="stChatInput"] textarea {{
    font-size: 1.15rem !important;
    line-height: 1.5 !important;
  }}
  [data-testid="stExpander"] summary {{
    font-size: 1.12rem !important;
  }}

  .main .block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 2.25rem !important;
    max-width: 1120px !important;
  }}

  [data-testid="stHeader"] {{
    background: transparent !important;
  }}

  /* Sidebar */
  [data-testid="stSidebar"] {{
    background: var(--sidebar) !important;
    border-right: 1px solid var(--border) !important;
  }}
  [data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.2rem;
  }}
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] .stCaption {{
    color: var(--muted) !important;
    font-family: var(--font) !important;
  }}
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {{
    color: var(--text) !important;
    font-family: var(--font) !important;
    font-weight: 650 !important;
    letter-spacing: -0.02em;
  }}

  /* Typography */
  h1, h2, h3, h4 {{
    color: var(--text) !important;
    font-family: var(--font) !important;
    letter-spacing: -0.03em !important;
    font-weight: 650 !important;
  }}
  p, .stMarkdown, .stCaption {{
    font-family: var(--font) !important;
  }}
  code, pre {{
    font-family: var(--mono) !important;
    font-size: 0.84em !important;
  }}

  /* Widgets */
  .stTextInput input,
  .stNumberInput input,
  div[data-baseweb="select"] > div {{
    background-color: var(--surface) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    font-family: var(--font) !important;
  }}
  .stSlider label {{ color: var(--muted) !important; }}

  .stButton > button {{
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    color: var(--text) !important;
    font-weight: 600 !important;
    font-family: var(--font) !important;
    font-size: 0.9rem !important;
    letter-spacing: -0.01em;
    transition: border-color 0.15s ease, background 0.15s ease, transform 0.1s ease;
    box-shadow: none !important;
  }}
  .stButton > button:hover {{
    border-color: var(--primary-border) !important;
    background: var(--surface-2) !important;
  }}
  .stButton > button[kind="primary"] {{
    background: var(--primary) !important;
    border-color: var(--primary) !important;
    color: #ffffff !important;
  }}
  .stButton > button[kind="primary"]:hover {{
    background: var(--primary-hover) !important;
    border-color: var(--primary-hover) !important;
  }}

  /* Chat messages */
  [data-testid="stChatMessage"] {{
    background: var(--bot-msg) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 0.55rem 0.75rem !important;
    box-shadow: var(--shadow);
  }}
  [data-testid="stChatMessageContent"] {{
    color: var(--text-2) !important;
  }}

  /* Alerts */
  div[data-testid="stAlert"] {{
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    font-family: var(--font) !important;
  }}

  /* ===== Custom components ===== */
  /* ===== Site header / website title ===== */
  .app-topbar {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 1.35rem;
    padding: 0.5rem 0 1.25rem 0;
    border-bottom: 1px solid var(--border-soft);
  }}
  .app-logo {{
    display: flex;
    align-items: flex-start;
    gap: 0;
    flex: 1;
  }}
  .app-logo-text {{
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    width: 100%;
  }}
  /* DocQ = website title (no Streamlit link icon — not an h1) */
  .app-logo-text .title.docq-name {{
    margin: 0 !important;
    padding: 0 !important;
    font-size: 3.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.06em !important;
    line-height: 1.02 !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    background: none !important;
    font-family: var(--font) !important;
  }}
  .app-logo-text .title.docq-name .brand-accent {{
    color: var(--primary) !important;
    -webkit-text-fill-color: var(--primary) !important;
  }}
  .app-logo-text .domain {{
    font-size: 0.95rem !important;
    font-weight: 650;
    letter-spacing: 0.06em;
    text-transform: lowercase;
    color: var(--primary);
    margin-top: 0.25rem;
    font-family: var(--mono);
  }}
  .app-logo-text .sub {{
    font-size: 1.12rem !important;
    color: var(--muted);
    font-weight: 500;
    letter-spacing: -0.01em;
    margin-top: 0.4rem;
    max-width: 34rem;
    line-height: 1.45;
  }}
  /* About expander polish */
  div[data-testid="stExpander"] {{
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 0.85rem !important;
  }}
  div[data-testid="stExpander"] summary {{
    font-weight: 650 !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
  }}
  .status-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    font-weight: 650;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: var(--success);
    background: var(--success-soft);
    border: 1px solid rgba(62, 207, 142, 0.28);
    border-radius: 999px;
    padding: 0.45rem 0.9rem;
    white-space: nowrap;
  }}
  .status-pill .dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--success);
    box-shadow: 0 0 0 3px rgba(62, 207, 142, 0.2);
  }}
  .status-pill.warn {{
    color: var(--warning);
    background: rgba(232, 179, 57, 0.12);
    border-color: rgba(232, 179, 57, 0.3);
  }}
  .status-pill.warn .dot {{
    background: var(--warning);
    box-shadow: 0 0 0 3px rgba(232, 179, 57, 0.2);
  }}

  .hero {{
    position: relative;
    background:
      radial-gradient(600px 180px at 10% 0%, var(--hero-glow), transparent 60%),
      var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.35rem 1.5rem 1.25rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
    overflow: hidden;
  }}
  .hero-kicker {{
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--primary);
    background: var(--primary-soft);
    border: 1px solid var(--primary-border);
    border-radius: 999px;
    padding: 0.28rem 0.7rem;
    margin-bottom: 0.7rem;
  }}
  .hero h1 {{
    margin: 0 0 0.4rem 0 !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    letter-spacing: -0.035em !important;
    line-height: 1.2 !important;
  }}
  .hero p {{
    margin: 0 !important;
    color: var(--muted) !important;
    font-size: 0.95rem;
    line-height: 1.55;
    max-width: 640px;
    font-weight: 450;
  }}
  .hero-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 0.95rem;
  }}
  .hero-chip {{
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-2);
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.28rem 0.55rem;
    letter-spacing: -0.01em;
  }}

  .stat-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 0 0 1.15rem 0;
  }}
  @media (max-width: 900px) {{
    .stat-row {{ grid-template-columns: repeat(2, 1fr); }}
  }}
  .stat {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    box-shadow: var(--shadow);
  }}
  .stat .label {{
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--faint);
    margin-bottom: 0.3rem;
    font-weight: 700;
  }}
  .stat .value {{
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
    line-height: 1.25;
  }}
  .stat .value.ok {{ color: var(--success); }}
  .stat .value.warn {{ color: var(--warning); }}

  .section-label {{
    font-size: 0.78rem;
    font-weight: 650;
    color: var(--faint);
    letter-spacing: 0.02em;
    margin: 0.15rem 0 0.55rem 0;
  }}

  .cite-card {{
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--primary);
    border-radius: 0 10px 10px 0;
    padding: 0.7rem 0.85rem;
    margin: 0.45rem 0;
  }}
  .cite-card .meta {{
    font-size: 0.78rem;
    color: var(--primary);
    font-weight: 700;
    margin-bottom: 0.3rem;
    font-family: var(--mono);
    letter-spacing: -0.02em;
  }}
  .cite-card .snip {{
    font-size: 0.84rem;
    color: var(--muted);
    line-height: 1.5;
  }}

  .side-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.35rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--border-soft);
  }}
  .side-brand .mark {{
    width: 32px;
    height: 32px;
    border-radius: 9px;
    background: linear-gradient(145deg, var(--primary), #5563d6);
    display: grid;
    place-items: center;
    font-size: 14px;
  }}
  .side-brand .name {{
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--text) !important;
    letter-spacing: -0.02em;
  }}
  .side-brand .role {{
    font-size: 0.7rem;
    color: var(--faint) !important;
    font-weight: 500;
  }}

  .side-section-title {{
    font-size: 0.8rem;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: var(--faint) !important;
    margin: 1rem 0 0.45rem 0;
  }}
  .doc-pill {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.42rem 0.6rem;
    margin: 0.28rem 0;
    font-size: 0.9rem;
    color: var(--text-2);
    font-family: var(--mono);
    word-break: break-all;
    letter-spacing: -0.02em;
  }}
  .theme-hint {{
    font-size: 0.9rem;
    color: var(--faint) !important;
    margin: 0.2rem 0 0.4rem 0;
    line-height: 1.4;
  }}
  .side-footer {{
    margin-top: 1rem;
    padding-top: 0.85rem;
    border-top: 1px solid var(--border-soft);
    font-size: 0.88rem;
    color: var(--faint) !important;
    line-height: 1.45;
  }}
  [data-testid="stSidebar"] h3 {{
    font-size: 1.35rem !important;
  }}
  .cite-card .meta {{
    font-size: 0.88rem !important;
  }}
  .cite-card .snip {{
    font-size: 0.95rem !important;
  }}

  footer {{ visibility: hidden; }}
  #MainMenu {{ visibility: hidden; }}
  [data-testid="stToolbar"] {{ display: none !important; }}
</style>
"""
