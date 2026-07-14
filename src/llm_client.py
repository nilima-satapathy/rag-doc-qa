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
    GEMINI_API_KEY,
    GEMINI_MODEL,
    LLM_MODEL,
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    XAI_API_KEY,
    XAI_BASE_URL,
)


def chat_completion(
    *,
    system: str,
    user: str,
    model: str | None = None,
    temperature: float = 0.2,
    provider: str | None = None,
) -> str:
    """Single-turn chat; returns assistant text."""
    prov = (provider or LLM_PROVIDER).strip().lower()

    if prov == "extractive":
        raise RuntimeError("extractive mode does not call an LLM")

    if prov == "ollama":
        return _chat_openai_compatible(
            api_key=os_getenv_dummy_key(),
            base_url=OLLAMA_BASE_URL,
            model=model or OLLAMA_MODEL or LLM_MODEL,
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
            model=model or GEMINI_MODEL or LLM_MODEL,
            temperature=temperature,
        )

    if prov == "xai":
        if not XAI_API_KEY:
            raise RuntimeError(
                "XAI_API_KEY is not set. For free use, set RAG_LLM_PROVIDER=extractive "
                "or use ollama / gemini. See .env.example."
            )
        return _chat_openai_compatible(
            api_key=XAI_API_KEY,
            base_url=XAI_BASE_URL,
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


def os_getenv_dummy_key() -> str:
    # Ollama ignores the key but OpenAI client requires a non-empty string
    return "ollama"


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
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not set.\n"
            "1) Free key: https://aistudio.google.com/apikey\n"
            "2) Put GEMINI_API_KEY=... in .env\n"
            "3) Set RAG_LLM_PROVIDER=gemini"
        )

    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError(
            "google-generativeai is not installed. Run:\n"
            "  pip install google-generativeai"
        ) from exc

    genai.configure(api_key=GEMINI_API_KEY)
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
        raise RuntimeError(
            f"Gemini API error: {exc}\n"
            "Check your free key at https://aistudio.google.com/apikey"
        ) from exc

    text = getattr(resp, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
