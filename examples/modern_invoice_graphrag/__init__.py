"""Modern Neo4j invoice GraphRAG example."""

from .embeddings import DeterministicEmbedding
from .model import InvoiceRecord, records_from_rows

__all__ = ["DeterministicEmbedding", "InvoiceRecord", "records_from_rows"]
