"""Embedding helpers for the modern Neo4j example."""

from __future__ import annotations

import hashlib
from typing import Iterable, List


class DeterministicEmbedding:
    """Small deterministic embedder for demos and tests.

    This is not a semantic production embedder. It gives stable vectors without
    API keys so the example can be tested offline.
    """

    def __init__(self, dimensions: int = 32, salt: str = "invoice-graphrag-demo") -> None:
        if dimensions < 1:
            raise ValueError("dimensions must be positive")
        self.dimensions = dimensions
        self.salt = salt

    def embed(self, text: str) -> List[float]:
        values = []
        counter = 0
        while len(values) < self.dimensions:
            seed = "%s:%s:%s" % (self.salt, text, counter)
            digest = hashlib.blake2b(seed.encode("utf-8"), digest_size=32).digest()
            for byte in digest:
                values.append(round((byte / 127.5) - 1.0, 6))
                if len(values) == self.dimensions:
                    break
            counter += 1
        return values

    def embed_many(self, texts: Iterable[str]) -> List[List[float]]:
        return [self.embed(text) for text in texts]
