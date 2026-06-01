# Modeling Reference

## Column Triage

Classify columns before choosing labels:

| Column type | Graph treatment |
| --- | --- |
| Stable ID, code, number | Unique key or indexed property |
| Repeated category | Node label or property depending on query needs |
| Person/company/place name | Usually a node if reused across rows |
| Amount/date/status | Usually a property |
| Free text | Property; may contribute to `search_text` for vector search |
| Source metadata | Property such as `source_file`, `source_row`, `ingested_at` |

## Label And Relationship Rules

- Labels should be durable business concepts, not raw column names.
- Relationship types should describe the fact between entities.
- Avoid making every spreadsheet cell a node. Promote values to nodes only when users query, join, or traverse through them.
- Keep original source columns in a `raw` map only when traceability matters and data volume is manageable.

## Invoice Example

Spreadsheet columns:

- `发票名称`
- `发票代码`
- `发票号码`
- `价税合计（小写）`
- `收款人`
- `复核`
- `开票人`

Graph model:

- `(:Invoice {invoice_id, invoice_name, invoice_code, invoice_number, amount, source_row})`
- `(:Person {name})`
- `(invoice)-[:HAS_PARTICIPANT {role: "payee"}]->(person)`
- `(invoice)-[:HAS_PARTICIPANT {role: "reviewer"}]->(person)`
- `(invoice)-[:HAS_PARTICIPANT {role: "drawer"}]->(person)`

Constraints:

```cypher
CREATE CONSTRAINT invoice_id_unique IF NOT EXISTS
FOR (invoice:Invoice)
REQUIRE invoice.invoice_id IS UNIQUE;

CREATE CONSTRAINT person_name_unique IF NOT EXISTS
FOR (person:Person)
REQUIRE person.name IS UNIQUE;
```

## Migration Guidance

- Keep py2neo v3 examples isolated when supporting Neo4j 3.x learners.
- For new applications, use the official `neo4j` Python driver.
- For semantic retrieval, add embeddings and vector indexes as an additive path, not as a replacement for graph structure.
