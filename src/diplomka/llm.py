"""LLM factory. Selects the chat backend from config and caches a single instance."""

from functools import lru_cache

from langchain_core.language_models import BaseChatModel

from diplomka import config


def build_llm() -> BaseChatModel:
    """Construct the chat model for the configured backend (``ollama`` or ``anthropic``)."""
    if config.LLM_BACKEND == "anthropic":
        from langchain_anthropic import ChatAnthropic

        # pyright's pydantic-constructor synthesis picks the by-alias overload here and
        # complains about these by-name kwargs, even though ChatAnthropic accepts both
        # (validate_by_alias=True, populate_by_name=True) - false positive, works at runtime.
        return ChatAnthropic(model=config.ANTHROPIC_MODEL, temperature=0, max_tokens=1000)  # pyright: ignore[reportCallIssue]

    from langchain_ollama import ChatOllama

    return ChatOllama(model=config.OLLAMA_MODEL, temperature=0)


@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    """Return a process-wide cached chat model, built on first use."""
    return build_llm()
