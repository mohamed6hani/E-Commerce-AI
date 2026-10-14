"""
Sentiment analysis placeholder.

This module provides a simplistic sentiment analysis function.  In a
production system you would likely use a fine‑tuned transformer model
for this task.
"""

from typing import Iterable


class SentimentAnalyzer:
    POSITIVE_WORDS = {"good", "great", "excellent", "love", "amazing", "happy", "satisfied"}
    NEGATIVE_WORDS = {"bad", "terrible", "poor", "hate", "disappointed", "sad", "unsatisfied"}

    def analyse(self, texts: Iterable[str]) -> float:
        """Return a sentiment score between -1.0 (negative) and 1.0 (positive).

        The score is computed as the difference between positive and
        negative word counts divided by the total number of words.
        """
        pos = 0
        neg = 0
        total = 0
        for text in texts:
            for word in str(text).lower().split():
                total += 1
                if word in self.POSITIVE_WORDS:
                    pos += 1
                elif word in self.NEGATIVE_WORDS:
                    neg += 1
        if total == 0:
            return 0.0
        return (pos - neg) / total