"""LLM factory. Selects the chat backend from config and caches a single instance."""

from functools import lru_cache
from typing import TypeVar, cast

from langchain_core.language_models import BaseChatModel, LanguageModelInput
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from diplomka import config

SchemaT = TypeVar("SchemaT", bound=BaseModel)


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
            # Some OpenRouter-routed providers (e.g. Anthropic models via Amazon Bedrock)
            # reject the `parallel_tool_calls` param that with_structured_output sends for
            # single-tool "function_calling" mode - never send it, for any model here.
            disabled_params={"parallel_tool_calls": None},
        )

    from langchain_ollama import ChatOllama

    return ChatOllama(model=model or config.OLLAMA_MODEL, temperature=0)


@lru_cache(maxsize=None)
def get_llm(model: str | None = None) -> BaseChatModel:
    """Return a cached chat model for ``model`` (or the backend's configured default), built on first use."""
    return build_llm(model)


def get_structured_llm(schema: type[SchemaT], model: str | None = None) -> Runnable[LanguageModelInput, SchemaT]:
    """``get_llm(model).with_structured_output(schema)``, forced onto tool-calling.

    The default structured-output method varies by backend - ``ChatOpenAI`` prefers OpenAI's
    strict ``json_schema`` response format, which most non-OpenAI models routed through
    OpenRouter don't honor properly (they echo plain text back instead, breaking parsing).
    ``function_calling`` is the one method broadly supported across backends and models.
    """
    structured = get_llm(model).with_structured_output(schema, method="function_calling")
    return cast("Runnable[LanguageModelInput, SchemaT]", structured)
