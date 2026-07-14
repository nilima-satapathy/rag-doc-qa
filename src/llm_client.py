"""
LLM clients for free and paid providers.

Providers:
  extractive — no network call (handled in generate.py)
  ollama     — free local OpenAI-compatible API
  gemini     — Google AI Studio free tier
  xai        — SpaceXAI / Grok (needs credits)
"""

from __future__ import annotations

from openai import OpenAI

from src.config import (
    GEMINI_MODEL,
    LLM_MODEL,
    LLM_PROVIDER,
    XAI_BASE_URL,
    get_gemini_api_key,
    get_llm_provider,
    get_ollama_settings,
    get_xai_api_key,
    reload_env,
)


def chat_completion(
    *,
    system: str,
    user: str,
    model: str | None = None,
    temperature: float = 0.2,
    provider: str | None = None,
) -> str:
    """Single-turn chat; returns assistant text. Re-reads .env on every call."""
    reload_env()
    prov = (provider or get_llm_provider() or LLM_PROVIDER).strip().lower()

    if prov == "extractive":
        raise RuntimeError("extractive mode does not call an LLM")

    if prov == "ollama":
        base_url, ollama_model = get_ollama_settings()
        return _chat_openai_compatible(
            api_key="ollama",
            base_url=base_url,
            model=model or ollama_model or LLM_MODEL,
            system=system,
            user=user,
            temperature=temperature,
            provider_label="Ollama",
            hint="Install from https://ollama.com then run: ollama pull llama3.2",
        )

    if prov == "gemini":
        return _chat_gemini(
            system=system,
            user=user,
            model=model or GEMINI_MODEL or LLM_MODEL or "gemini-1.5-flash",
            temperature=temperature,
        )

    if prov == "xai":
        xai_key = get_xai_api_key()
        if not xai_key:
            raise RuntimeError(
                "XAI_API_KEY is not set. For free use, set RAG_LLM_PROVIDER=extractive "
                "or use ollama / gemini. See .env.example."
            )
        return _chat_openai_compatible(
            api_key=xai_key,
            base_url=XAI_BASE_URL or "https://api.x.ai/v1",
            model=model or LLM_MODEL or "grok-4.5",
            system=system,
            user=user,
            temperature=temperature,
            provider_label="xAI",
            hint="Add credits at https://console.x.ai or switch to a free provider.",
        )

    raise RuntimeError(
        f"Unknown RAG_LLM_PROVIDER={prov!r}. "
        "Use: extractive | ollama | gemini | xai"
    )


def _chat_openai_compatible(
    *,
    api_key: str,
    base_url: str,
    model: str,
    system: str,
    user: str,
    temperature: float,
    provider_label: str,
    hint: str,
) -> str:
    from openai import APIConnectionError, APIStatusError, PermissionDeniedError

    client = OpenAI(api_key=api_key, base_url=base_url)
    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
    except PermissionDeniedError as exc:
        raise RuntimeError(
            f"{provider_label} denied the request.\n{hint}\nDetails: {exc}"
        ) from exc
    except APIConnectionError as exc:
        raise RuntimeError(
            f"Could not reach {provider_label} at {base_url}.\n{hint}\nDetails: {exc}"
        ) from exc
    except APIStatusError as exc:
        raise RuntimeError(
            f"{provider_label} API error ({exc.status_code}): {exc}\n{hint}"
        ) from exc

    return (resp.choices[0].message.content or "").strip()


def _chat_gemini(
    *,
    system: str,
    user: str,
    model: str,
    temperature: float,
) -> str:
    key = get_gemini_api_key()
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set.\n"
            "1) Free key: https://aistudio.google.com/apikey\n"
            "2) Open file: rag-doc-qa/.env  (same folder as app.py)\n"
            "3) Add a line exactly like:\n"
            "   GEMINI_API_KEY=AIza...\n"
            "   RAG_LLM_PROVIDER=gemini\n"
            "4) Save file, stop Streamlit (Ctrl+C), run: streamlit run app.py\n"
            "Do NOT put the key only in the sidebar — it must be in .env"
        )

    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError(
            "google-generativeai is not installed. Run:\n"
            "  pip install google-generativeai"
        ) from exc

    genai.configure(api_key=key)
    gm = genai.GenerativeModel(
        model_name=model,
        system_instruction=system,
    )
    try:
        resp = gm.generate_content(
            user,
            generation_config={"temperature": temperature},
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        extra = ""
        if "429" in msg or "quota" in msg.lower() or "limit: 0" in msg:
            extra = (
                "\n\nThis is a QUOTA issue (not a wrong key).\n"
                "Try in .env:\n"
                "  GEMINI_MODEL=gemini-1.5-flash\n"
                "  or GEMINI_MODEL=gemini-2.0-flash-lite\n"
                "Or wait for free-tier reset, or use Answer mode: extractive (always free).\n"
                "Docs: https://ai.google.dev/gemini-api/docs/rate-limits"
            )
        raise RuntimeError(f"Gemini API error: {exc}{extra}") from exc

    text = getattr(resp, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
