# Cypher And GraphRAG Reference

## Safe Import Pattern

Use parameters and `UNWIND`:

```cypher
UNWIND $rows AS row
MERGE (invoice:Invoice {invoice_id: row.invoice_id})
SET invoice += row.invoice
WITH invoice, row
UNWIND row.people AS person
MERGE (p:Person {name: person.name})
MERGE (invoice)-[rel:HAS_PARTICIPANT {role: person.role}]->(p)
SET rel.updated_at = datetime();
```

Avoid string-concatenating user data into Cypher.

## Verification Queries

```cypher
MATCH (n) RETURN labels(n) AS labels, count(*) AS count ORDER BY count DESC;
MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count ORDER BY count DESC;
SHOW CONSTRAINTS;
SHOW INDEXES;
```

## Vector Index Pattern

Neo4j vector indexes are useful for semantic retrieval and GraphRAG-style workflows.

```cypher
CREATE VECTOR INDEX invoice_embedding_index IF NOT EXISTS
FOR (invoice:Invoice)
ON (invoice.embedding)
OPTIONS {indexConfig: {
  `vector.dimensions`: $dimensions,
  `vector.similarity_function`: "cosine"
}};
```

Search:

```cypher
CALL db.index.vector.queryNodes($index_name, $top_k, $embedding)
YIELD node, score
RETURN node.invoice_id AS invoice_id, node.search_text AS search_text, score
ORDER BY score DESC;
```

## GraphRAG Checklist

- Preserve graph structure first; do not replace relationships with text chunks.
- Build `search_text` from meaningful graph facts.
- Store embedding vectors on the node being retrieved.
- Return graph context around matched nodes, not just text.
- Use deterministic fake embeddings only for demos and tests.
- Use `neo4j-graphrag` or a real embedding provider for production semantic quality.

## Common Mistakes

- Using vector search for exact ID lookups.
- Creating a node for every spreadsheet cell.
- Loading full data before testing constraints on a sample.
- Running `MATCH (n) DETACH DELETE n` without explicit user confirmation.
- Mixing py2neo v3 and modern driver code in the same runtime path.
