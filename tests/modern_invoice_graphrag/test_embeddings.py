import unittest

from examples.modern_invoice_graphrag.embeddings import DeterministicEmbedding


class DeterministicEmbeddingTests(unittest.TestCase):
    def test_deterministic_embedding_returns_requested_dimensions(self):
        embedder = DeterministicEmbedding(dimensions=12)

        vector = embedder.embed("invoice from shandong reviewed by wang min")

        self.assertEqual(len(vector), 12)
        self.assertTrue(all(isinstance(value, float) for value in vector))
        self.assertTrue(all(-1.0 <= value <= 1.0 for value in vector))

    def test_deterministic_embedding_is_repeatable(self):
        embedder = DeterministicEmbedding(dimensions=8)

        self.assertEqual(embedder.embed("same text"), embedder.embed("same text"))
        self.assertNotEqual(embedder.embed("same text"), embedder.embed("different text"))

    def test_embed_many_preserves_order(self):
        embedder = DeterministicEmbedding(dimensions=4)

        vectors = embedder.embed_many(["alpha", "beta", "alpha"])

        self.assertEqual(len(vectors), 3)
        self.assertNotEqual(vectors[0], vectors[1])
        self.assertEqual(vectors[0], vectors[2])


if __name__ == "__main__":
    unittest.main()
