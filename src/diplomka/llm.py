"""LLM factory. Selects the chat backend from config and caches a single instance."""

from functools import lru_cache

from langchain_core.language_models import BaseChatModel

from diplomka import config


def build_llm(model: str | None = None) -> BaseChatModel:
    """Construct the chat model for the configured backend (``ollama``, ``anthropic``, or ``openrouter``).

    ``model`` overrides the backend's configured default - used to switch OpenRouter models
    at runtime (e.g. from a UI picker) without touching the ``ollama``/``anthropic`` backends.
    """
    if config.LLM_BACKEND == "anthropic":
        from langchain_anthropic import ChatAnthropic

        # pyright's pydantic-constructor synthesis picks the by-alias overload here and
        # complains about these by-name kwargs, even though ChatAnthropic accepts both
        # (validate_by_alias=True, populate_by_name=True) - false positive, works at runtime.
        return ChatAnthropic(model=model or config.ANTHROPIC_MODEL, temperature=0, max_tokens=1000)  # pyright: ignore[reportCallIssue]

    if config.LLM_BACKEND == "openrouter":
        from langchain_openai import ChatOpenAI
        from pydantic import SecretStr

        return ChatOpenAI(
            model=model or config.OPENROUTER_MODEL,
            api_key=SecretStr(config.OPENROUTER_API_KEY) if config.OPENROUTER_API_KEY else None,
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
        )

    from langchain_ollama import ChatOllama

    return ChatOllama(model=model or config.OLLAMA_MODEL, temperature=0)


@lru_cache(maxsize=None)
def get_llm(model: str | None = None) -> BaseChatModel:
    """Return a cached chat model for ``model`` (or the backend's configured default), built on first use."""
    return build_llm(model)
