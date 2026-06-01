# Modern Invoice GraphRAG Example

[English](README.md) | [Simplified Chinese](README.zh-CN.md)

This example updates the original Excel-to-Neo4j idea for the current Neo4j application stack:

- official `neo4j` Python driver instead of legacy py2neo
- Neo4j 5+/2026 vector indexes
- GraphRAG-style semantic retrieval over invoice records
- optional `neo4j-graphrag` integration for production embeddings

The legacy py2neo v3 scripts remain unchanged. This folder is an additive modern path for users who want to build current Neo4j applications from the same invoice dataset concept.

## Why This Exists

The original project demonstrates how to load Excel invoice data into Neo4j as a graph. Modern Neo4j applications often combine graph structure with vector search and GraphRAG. This example shows that upgrade path without forcing existing users to abandon the legacy baseline.

## Files

- `model.py`: normalizes legacy invoice spreadsheet rows into `InvoiceRecord` objects.
- `embeddings.py`: provides a deterministic local embedder for demos and tests.
- `cypher.py`: contains constraints, vector index creation, upsert, and vector search Cypher.
- `app.py`: CLI for dry-run, loading, and searching.
- `sample_invoice_rows.csv`: small keyless sample that runs without pandas.
- `requirements-modern.txt`: modern Neo4j driver and Excel-reading dependencies.
- `requirements-graphrag-openai.txt`: optional production GraphRAG embedding stack.

## Requirements

For the modern Neo4j path:

- Python >=3.10
- Neo4j 5.18+ or Neo4j Aura
- `pip install -r examples/modern_invoice_graphrag/requirements-modern.txt`

For production-quality embeddings:

```bash
pip install -r examples/modern_invoice_graphrag/requirements-graphrag-openai.txt
```

The default deterministic embedder is intentionally local and keyless. It is useful for demos, tests, and repository CI, but it is not a semantic production embedding model.

## Quick Dry Run

Run without Neo4j or external APIs:

```bash
python -m examples.modern_invoice_graphrag.app \
  --input examples/modern_invoice_graphrag/sample_invoice_rows.csv \
  --limit 2 \
  dry-run
```

This prints graph-ready invoice payloads with deterministic vectors.

## Run With Neo4j

Start Neo4j locally, for example:

```bash
docker run --rm \
  --name neo4j-invoice-demo \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

Load sample data:

```bash
export NEO4J_URI=neo4j://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=password

python -m examples.modern_invoice_graphrag.app \
  --input examples/modern_invoice_graphrag/sample_invoice_rows.csv \
  load
```

Search invoices:

```bash
python -m examples.modern_invoice_graphrag.app \
  search "invoice reviewed by Wang Min from Shandong"
```

## Use The Original Excel File

The repository-level `Invoice_data_Demo.xls` can also be used:

```bash
python -m examples.modern_invoice_graphrag.app \
  --input Invoice_data_Demo.xls \
  --limit 10 \
  dry-run
```

Reading `.xls` files requires pandas and `xlrd`.

## Production GraphRAG Path

For real semantic search, replace `DeterministicEmbedding` with an embedder from `neo4j-graphrag`, for example an OpenAI embedder. Keep the rest of the flow the same:

1. normalize invoice rows
2. build graph payloads
3. create constraints and vector index
4. upsert invoice nodes with embedding vectors
5. query with `db.index.vector.queryNodes`

This keeps the example understandable while pointing users toward Neo4j's current GraphRAG ecosystem.

## Official References

- Neo4j Python Driver: https://neo4j.com/docs/python-manual/current/
- Neo4j vector indexes: https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/
- Neo4j GraphRAG for Python: https://neo4j.com/docs/neo4j-graphrag-python/current/

## Testing

From the repository root:

```bash
python -m unittest discover -s tests/modern_invoice_graphrag -v
```
