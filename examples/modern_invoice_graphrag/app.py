"""CLI for the modern Neo4j invoice GraphRAG example."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    from . import cypher
    from .embeddings import DeterministicEmbedding
    from .model import InvoiceRecord, records_from_rows
except ImportError:  # pragma: no cover - supports direct script execution
    import cypher  # type: ignore
    from embeddings import DeterministicEmbedding  # type: ignore
    from model import InvoiceRecord, records_from_rows  # type: ignore


DEFAULT_INDEX_NAME = "invoice_embedding_index"
DEFAULT_DIMENSIONS = 32


def read_rows(path: Path, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    elif suffix in {".xls", ".xlsx"}:
        try:
            import pandas as pd
        except ImportError as exc:
            raise RuntimeError(
                "Reading Excel files requires pandas and xlrd/openpyxl. "
                "Install examples/modern_invoice_graphrag/requirements-modern.txt."
            ) from exc
        rows = pd.read_excel(path, dtype=object).fillna("").to_dict("records")
    else:
        raise ValueError("Unsupported input file type: %s" % path.suffix)
    if limit is not None:
        return rows[:limit]
    return rows


def connect(uri: str, user: str, password: str):
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise RuntimeError(
            "The official Neo4j driver is required. Install it with: pip install neo4j"
        ) from exc
    return GraphDatabase.driver(uri, auth=(user, password))


def _execute(driver: Any, query: str, database: Optional[str] = None, **parameters: Any) -> Any:
    kwargs = dict(parameters)
    if database:
        kwargs["database_"] = database
    return driver.execute_query(query, **kwargs)


def ensure_schema(
    driver: Any,
    dimensions: int,
    index_name: str = DEFAULT_INDEX_NAME,
    similarity: str = "cosine",
    database: Optional[str] = None,
) -> None:
    for query in cypher.CONSTRAINT_QUERIES:
        _execute(driver, query, database=database)
    _execute(
        driver,
        cypher.CREATE_VECTOR_INDEX_QUERY.replace("invoice_embedding_index", index_name),
        database=database,
        dimensions=dimensions,
        similarity=similarity,
    )


def load_records(
    driver: Any,
    records: Iterable[InvoiceRecord],
    embedder: DeterministicEmbedding,
    database: Optional[str] = None,
) -> int:
    count = 0
    for record in records:
        payload = record.to_graph_payload(embedder.embed(record.search_text()))
        _execute(
            driver,
            cypher.UPSERT_INVOICE_QUERY,
            database=database,
            invoice=payload["invoice"],
            people=payload["people"],
        )
        count += 1
    return count


def search_invoices(
    driver: Any,
    query_text: str,
    embedder: DeterministicEmbedding,
    top_k: int = 5,
    index_name: str = DEFAULT_INDEX_NAME,
    database: Optional[str] = None,
) -> List[Dict[str, Any]]:
    result = _execute(
        driver,
        cypher.VECTOR_SEARCH_QUERY,
        database=database,
        index_name=index_name,
        top_k=top_k,
        embedding=embedder.embed(query_text),
    )
    records = getattr(result, "records", result[0] if isinstance(result, tuple) else result)
    return [dict(record) for record in records]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Modern Neo4j invoice GraphRAG example")
    parser.add_argument("--input", default="Invoice_data_Demo.xls", help="Excel or CSV input path")
    parser.add_argument("--limit", type=int, default=None, help="Limit rows for demos")
    parser.add_argument("--dimensions", type=int, default=DEFAULT_DIMENSIONS, help="Vector dimensions")
    parser.add_argument("--index-name", default=DEFAULT_INDEX_NAME, help="Neo4j vector index name")
    parser.add_argument("--database", default=os.getenv("NEO4J_DATABASE"), help="Neo4j database name")
    parser.add_argument("--uri", default=os.getenv("NEO4J_URI", "neo4j://localhost:7687"))
    parser.add_argument("--user", default=os.getenv("NEO4J_USER", "neo4j"))
    parser.add_argument("--password", default=os.getenv("NEO4J_PASSWORD", "password"))
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("dry-run", help="Print normalized records without connecting to Neo4j")
    subparsers.add_parser("load", help="Load invoice graph data into Neo4j")
    search = subparsers.add_parser("search", help="Run vector search against loaded invoices")
    search.add_argument("query", help="Natural-language search query")
    search.add_argument("--top-k", type=int, default=5)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    rows = read_rows(Path(args.input), limit=args.limit)
    records = records_from_rows(rows)
    embedder = DeterministicEmbedding(dimensions=args.dimensions)

    if args.command == "dry-run":
        preview = [record.to_graph_payload(embedder.embed(record.search_text())) for record in records]
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    driver = connect(args.uri, args.user, args.password)
    try:
        ensure_schema(driver, args.dimensions, args.index_name, database=args.database)
        if args.command == "load":
            count = load_records(driver, records, embedder, database=args.database)
            print("Loaded %s invoice records" % count)
            return 0
        if args.command == "search":
            results = search_invoices(
                driver,
                args.query,
                embedder,
                top_k=args.top_k,
                index_name=args.index_name,
                database=args.database,
            )
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return 0
    finally:
        driver.close()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
