"""LLM factory. Selects the chat backend from config and caches a single instance."""

import json
from functools import cache
from typing import cast

from langchain_core.language_models import BaseChatModel, LanguageModelInput
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.runnables import Runnable, RunnableLambda
from pydantic import BaseModel

from diplomka import config


@cache
def get_llm(model: str | None = None) -> BaseChatModel:
    """Cached chat model for the configured backend (``ollama``, ``anthropic``, or ``openrouter``).

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


def get_structured_llm[SchemaT: BaseModel](
    schema: type[SchemaT], model: str | None = None
) -> Runnable[LanguageModelInput, SchemaT]:
    """``get_llm(model).with_structured_output(schema)`` with the method that is reliable per backend.

    - Ollama: ``json_schema`` - Ollama constrains decoding to the schema (``format=``), so even
      small local models always produce parseable JSON with the right field names. Unlike a tool
      definition, ``format=`` never shows the model the field descriptions, so the schema is also
      added to the system prompt.
    - Others: ``function_calling`` - ``ChatOpenAI`` prefers OpenAI's strict ``json_schema``
      response format, which most non-OpenAI models routed through OpenRouter don't honor
      properly (they echo plain text back instead, breaking parsing). Tool-calling is the one
      method broadly supported there.
    """
    if config.LLM_BACKEND == "ollama":
        hint = f"Respond only with a JSON object matching this JSON schema:\n{json.dumps(schema.model_json_schema())}"
        structured = RunnableLambda(lambda messages: _with_system_hint(messages, hint)) | get_llm(
            model
        ).with_structured_output(schema, method="json_schema")
    else:
        structured = get_llm(model).with_structured_output(schema, method="function_calling")
    return cast("Runnable[LanguageModelInput, SchemaT]", structured)


def _with_system_hint(messages: list[BaseMessage], hint: str) -> list[BaseMessage]:
    """Append ``hint`` to the leading system message (or add one) - some chat templates
    handle only a single system message at the start."""
    if messages and isinstance(messages[0], SystemMessage):
        return [SystemMessage(content=f"{messages[0].content}\n\n{hint}"), *messages[1:]]
    return [SystemMessage(content=hint), *messages]
