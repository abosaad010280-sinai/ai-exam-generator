"""Question bank management service"""

from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.config import settings
from app.core.logger import logger


class QuestionBankManager:
    """Manage and search question bank"""

    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calculate similarity between two texts using TF-IDF"""
        try:
            vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
            vectors = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0

    @staticmethod
    def is_duplicate(question_text: str, existing_questions: List[str]) -> bool:
        """Check if question is a duplicate of existing questions"""
        for existing_question in existing_questions:
            similarity = QuestionBankManager.calculate_similarity(
                question_text,
                existing_question
            )
            if similarity >= settings.SIMILARITY_THRESHOLD:
                logger.warning(f"Duplicate question detected with similarity: {similarity}")
                return True
        return False
