"""
Embedding pipeline for generating vector representations of text and product data.

This module wraps the SentenceTransformer model from the
`sentence_transformers` library to produce normalised embeddings.  It
can embed arbitrary strings or structured product objects.
"""

from typing import Dict, Any

import numpy as np
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None  # type: ignore


class EmbeddingPipeline:
    def __init__(self):
        """Initialise the embedding model."""
        if SentenceTransformer is None:
            raise ImportError(
                "sentence_transformers not installed. Please install it to use the embedding pipeline."
            )
        # Use a compact model for faster inference
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text: str) -> np.ndarray:
        """Embed a single text string into a normalised vector."""
        vec = self.model.encode(text)
        return vec / np.linalg.norm(vec)

    def embed_product(self, product: Dict[str, Any]) -> np.ndarray:
        """Create an embedding for a product by concatenating its title, description and category."""
        parts = [product.get("title", ""), product.get("description", ""), product.get("category", "")]
        return self.embed_text(" ".join(str(p) for p in parts))