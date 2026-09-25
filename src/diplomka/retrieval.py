"""Fuzzy lookup of dimension-level values via embeddings.

For a level with a known domain (``domain: from_data`` in the semantic layer) the vector store
indexes its values from DuckDB plus every glossary term/synonym that maps to one of them, so
both "beauty products" -> ``beleza_saude`` and "swarm cell" -> ``queencell`` resolve.

The embedding model and the per-level vector stores are built lazily on first use (not at
import time), keeping ``import diplomka`` cheap and side-effect free.
"""

from functools import cache, lru_cache

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from diplomka import config
from diplomka.schema import LAYER, get_domains


def _clean(text: str) -> str:
    return text.strip().replace("_", " ")


@lru_cache(maxsize=1)
def _embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)


@cache
def get_vectorstore(level: str) -> InMemoryVectorStore | None:
    """Build (once) an in-memory vector store over the values of ``level``; None if it has no domain."""
    values = get_domains().get(level)
    if not values:
        return None

    texts = [(_clean(v), v) for v in sorted(values)]
    for entry in LAYER.glossary:
        target = entry["maps_to"]
        if target.get("level") == level and str(target.get("value")) in values:
            texts.extend((_clean(term), str(target["value"])) for term in [entry["term"], *entry.get("synonyms", [])])

    return InMemoryVectorStore.from_texts(
        [text for text, _ in texts],
        embedding=_embeddings(),
        metadatas=[{"original": original} for _, original in texts],
    )


def lookup_values(level: str, text: str, k: int = 3) -> list[tuple[str, float]]:
    """Return up to ``k`` distinct values of ``level`` closest to ``text``, with scores (best first)."""
    store = get_vectorstore(level)
    if store is None:
        return []
    candidates: dict[str, float] = {}
    # glossary synonyms can map several texts to one value - fetch extra and keep each value's best score
    for doc, score in store.similarity_search_with_score(_clean(text), k=k * 3):
        original = doc.metadata["original"]
        candidates[original] = max(score, candidates.get(original, score))
    return sorted(candidates.items(), key=lambda item: item[1], reverse=True)[:k]
