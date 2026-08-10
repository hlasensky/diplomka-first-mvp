"""Fuzzy category lookup via embeddings.

The DuckDB category fetch, the HuggingFace embedding model and the in-memory vector store
are built lazily on first use (not at import time), keeping ``import diplomka`` cheap and
side-effect free.
"""

from functools import lru_cache

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from diplomka import config
from diplomka.db import connect


@lru_cache(maxsize=1)
def get_vectorstore() -> InMemoryVectorStore:
    """Build (once) an in-memory vector store over the distinct product categories."""
    with connect(read_only=True) as conn:
        all_db_categories = conn.execute("SELECT DISTINCT product_category_name FROM orders").fetchall()

    categories = [c for c in all_db_categories if c[0] is not None]
    cleaned = [c[0].strip().replace("_", " ") for c in categories]

    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    return InMemoryVectorStore.from_texts(
        cleaned,
        embedding=embeddings,
        metadatas=[{"original": c[0]} for c in categories],
    )


def lookup_categories(text: str, k: int = 3) -> list[tuple[str, float]]:
    """Return the ``k`` closest ``product_category_name`` values to ``text`` with scores."""
    query = text.strip().replace("_", " ")
    results = get_vectorstore().similarity_search_with_score(query, k=k)
    return [(doc.metadata["original"], score) for doc, score in results]
