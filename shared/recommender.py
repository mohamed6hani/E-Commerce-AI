"""
Simple vector-based recommendation engine.

Given a set of product vectors and a query vector, the engine
computes cosine similarity and returns the indices of the most similar
items.
"""

from typing import List
import numpy as np


class RecommenderEngine:
    def __init__(self, product_vectors: np.ndarray):
        # Store normalised product vectors
        norms = np.linalg.norm(product_vectors, axis=1, keepdims=True)
        self.product_vectors = product_vectors / np.maximum(norms, 1e-8)

    def recommend(self, query_vector: np.ndarray, top_k: int = 5) -> List[int]:
        """Return indices of top_k most similar products to the query.

        Args:
            query_vector: A normalised vector representing the query.
            top_k: Number of recommendations to return.

        Returns:
            List of indices into the product vector array.
        """
        # Ensure the query is normalised
        q = query_vector / (np.linalg.norm(query_vector) or 1.0)
        sims = self.product_vectors @ q
        return sims.argsort()[::-1][:top_k].tolist()