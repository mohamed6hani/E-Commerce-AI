"""
Vector search helper.

This module provides functions to index product embeddings and search
for similar items based on query text.
"""

from typing import List, Dict, Any
import numpy as np

from .embedding_pipeline import EmbeddingPipeline


class SearchVectorizer:
    def __init__(self, pipeline: EmbeddingPipeline):
        self.pipeline = pipeline

    def index_products(self, products: List[Dict[str, Any]]) -> np.ndarray:
        """Generate embedding vectors for a list of products."""
        vectors = [self.pipeline.embed_product(p) for p in products]
        return np.stack(vectors, axis=0)

    def search(self, query: str, vectors: np.ndarray) -> List[int]:
        """Search for the most similar products to a text query.

        Returns the indices of products sorted by similarity.
        """
        qvec = self.pipeline.embed_text(query)
        qvec /= np.linalg.norm(qvec) or 1.0
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norm_vectors = vectors / np.maximum(norms, 1e-8)
        sims = norm_vectors @ qvec
        return sims.argsort()[::-1].tolist()