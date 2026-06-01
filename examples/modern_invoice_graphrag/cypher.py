"""Cypher statements for the modern Neo4j invoice example."""

CONSTRAINT_QUERIES = [
    """
    CREATE CONSTRAINT invoice_id_unique IF NOT EXISTS
    FOR (invoice:Invoice)
    REQUIRE invoice.invoice_id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT person_name_unique IF NOT EXISTS
    FOR (person:Person)
    REQUIRE person.name IS UNIQUE
    """,
]

CREATE_VECTOR_INDEX_QUERY = """
CREATE VECTOR INDEX invoice_embedding_index IF NOT EXISTS
FOR (invoice:Invoice)
ON (invoice.embedding)
OPTIONS {indexConfig: {
  `vector.dimensions`: $dimensions,
  `vector.similarity_function`: $similarity
}}
"""

UPSERT_INVOICE_QUERY = """
MERGE (invoice:Invoice {invoice_id: $invoice.invoice_id})
SET invoice += $invoice
WITH invoice
UNWIND $people AS person
MERGE (p:Person {name: person.name})
MERGE (invoice)-[rel:HAS_PARTICIPANT {role: person.role}]->(p)
SET rel.updated_at = datetime()
"""

VECTOR_SEARCH_QUERY = """
CALL db.index.vector.queryNodes($index_name, $top_k, $embedding)
YIELD node, score
RETURN
  node.invoice_id AS invoice_id,
  node.invoice_name AS invoice_name,
  node.invoice_code AS invoice_code,
  node.invoice_number AS invoice_number,
  node.amount AS amount,
  node.search_text AS search_text,
  score
ORDER BY score DESC
"""
