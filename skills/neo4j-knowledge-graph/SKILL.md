---
name: neo4j-knowledge-graph
description: Use when designing, importing, querying, or modernizing Neo4j knowledge graphs from CSV, Excel, pandas, Cypher, py2neo, the official neo4j Python driver, vector indexes, or GraphRAG workflows.
---

# Neo4j Knowledge Graph

## Overview

Use this skill to turn tabular or semi-structured data into a Neo4j knowledge graph, then choose the right path: legacy py2neo compatibility, modern official-driver Cypher, or GraphRAG/vector search.

## Workflow

1. **Frame the graph task**
   - Identify the source data: CSV, Excel, pandas DataFrame, database export, API data, or existing Neo4j graph.
   - Ask what the user wants to do: import, model, query, migrate, visualize, or add GraphRAG.
   - Confirm Neo4j target: local Neo4j, Aura, legacy Neo4j 3.x, Neo4j 5+, or unknown.

2. **Profile data before modeling**
   - For CSV/Excel files, run `scripts/profile_table.py <path>` when local files are available.
   - Inspect columns, sample values, blank counts, likely identifiers, and repeated values.
   - Do not infer graph labels from one row only.

3. **Model the graph**
   - Use nouns for labels: `Invoice`, `Person`, `Company`, `Product`, `Location`.
   - Use verbs or role phrases for relationships: `ISSUED_BY`, `PAID_TO`, `HAS_PARTICIPANT`.
   - Choose stable IDs before writing Cypher.
   - Put frequently queried identifiers under uniqueness constraints.
   - Keep relationship properties for roles, timestamps, source rows, and confidence.

4. **Generate safe Cypher**
   - Prefer parameterized `MERGE` + `UNWIND` for imports.
   - Create constraints before loading data.
   - Avoid destructive commands unless the user explicitly asks and the target is confirmed.
   - For modern projects, prefer the official `neo4j` Python driver.
   - Use py2neo only when maintaining legacy Neo4j 3.x / py2neo v3 code.

5. **Add GraphRAG only when useful**
   - Use vector search when users need semantic retrieval, fuzzy matching, natural-language search, or RAG.
   - Build a clear `search_text` from graph facts.
   - Create a Neo4j vector index on the embedding property.
   - Use deterministic embeddings only for demos/tests; use `neo4j-graphrag` or a real embedding provider for production.

6. **Verify**
   - Dry-run on a small sample before loading the full dataset.
   - Report node/relationship counts, constraints, and index status.
   - Show representative Cypher queries users can run in Neo4j Browser.

## Resource Guide

- Read `references/modeling.md` for spreadsheet-to-graph modeling patterns.
- Read `references/cypher-and-graphrag.md` before writing import Cypher, vector index Cypher, or GraphRAG examples.
- Run `scripts/profile_table.py --help` for table profiling options.

## Output Shape

For a substantial task, return:

- graph model summary
- column-to-label/relationship mapping
- constraints and indexes
- import or migration steps
- verification queries
- risks and assumptions

For code changes, include tests or a dry-run path that does not require a live Neo4j instance.
