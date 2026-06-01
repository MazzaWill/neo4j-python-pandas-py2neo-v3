import unittest

from examples.modern_invoice_graphrag import cypher


class CypherTests(unittest.TestCase):
    def test_constraint_queries_cover_invoice_and_person_identity(self):
        joined = "\n".join(cypher.CONSTRAINT_QUERIES)

        self.assertIn("Invoice", joined)
        self.assertIn("invoice_id", joined)
        self.assertIn("Person", joined)
        self.assertIn("name", joined)

    def test_vector_index_query_uses_modern_neo4j_vector_index_syntax(self):
        query = cypher.CREATE_VECTOR_INDEX_QUERY

        self.assertIn("CREATE VECTOR INDEX", query)
        self.assertIn("IF NOT EXISTS", query)
        self.assertIn("vector.dimensions", query)
        self.assertIn("vector.similarity_function", query)
        self.assertIn("$dimensions", query)

    def test_upsert_query_merges_invoices_people_and_relationship_roles(self):
        query = cypher.UPSERT_INVOICE_QUERY

        self.assertIn("MERGE (invoice:Invoice", query)
        self.assertIn("UNWIND $people AS person", query)
        self.assertIn("MERGE (p:Person", query)
        self.assertIn("HAS_PARTICIPANT", query)

    def test_vector_search_query_uses_index_query_nodes(self):
        query = cypher.VECTOR_SEARCH_QUERY

        self.assertIn("db.index.vector.queryNodes", query)
        self.assertIn("$index_name", query)
        self.assertIn("$embedding", query)
        self.assertIn("$top_k", query)


if __name__ == "__main__":
    unittest.main()
