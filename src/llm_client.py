"""
Thin LLM client for SpaceXAI (xAI OpenAI-compatible API).

Env:
  XAI_API_KEY   — required for M3+
  XAI_BASE_URL  — default https://api.x.ai/v1
  RAG_LLM_MODEL — default grok-4.5
"""

from __future__ import annotations

from openai import OpenAI

from src.config import LLM_MODEL, XAI_API_KEY, XAI_BASE_URL


def get_llm_client() -> OpenAI:
    if not XAI_API_KEY:
        raise RuntimeError(
            "XAI_API_KEY is not set.\n"
            "1) Copy .env.example to .env\n"
            "2) Put your key: XAI_API_KEY=...\n"
            "   (create a key at https://console.x.ai )\n"
        )
    return OpenAI(api_key=XAI_API_KEY, base_url=XAI_BASE_URL)


def chat_completion(
    *,
    system: str,
    user: str,
    model: str | None = None,
    temperature: float = 0.2,
) -> str:
    """Single-turn chat; returns assistant text."""
    from openai import APIStatusError, PermissionDeniedError

    client = get_llm_client()
    try:
        resp = client.chat.completions.create(
            model=model or LLM_MODEL,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
    except PermissionDeniedError as exc:
        raise RuntimeError(
            "xAI API denied the request (often: no credits/license on the team).\n"
            "Add credits at https://console.x.ai then retry.\n"
            f"Details: {exc}"
        ) from exc
    except APIStatusError as exc:
        raise RuntimeError(f"xAI API error ({exc.status_code}): {exc}") from exc

    content = resp.choices[0].message.content
    return (content or "").strip()
