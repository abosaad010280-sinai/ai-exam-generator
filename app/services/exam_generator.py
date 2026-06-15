"""Exam generation service"""

from typing import List, Dict, Any
from app.services.ai_service import AIService
from app.core.logger import logger


class ExamGenerator:
    """Generate exams with various question types"""

    def __init__(self):
        self.ai_service = AIService()

    async def generate_exam(
        self,
        content: str,
        num_questions: int,
        question_types: List[str],
        subject: str
    ) -> Dict[str, Any]:
        """Generate an exam with specified question types"""
        try:
            exam_questions = []

            # Calculate questions per type
            questions_per_type = num_questions // len(question_types)
            remainder = num_questions % len(question_types)

            for idx, q_type in enumerate(question_types):
                # Add remainder to last type
                count = questions_per_type + (1 if idx == len(question_types) - 1 else 0)

                if q_type == "mcq":
                    questions = await self.ai_service.generate_mcq_questions(
                        content, count, subject
                    )
                    exam_questions.extend(questions)

                elif q_type == "true_false":
                    questions = await self.ai_service.generate_true_false_questions(
                        content, count, subject
                    )
                    exam_questions.extend(questions)

            logger.info(f"Exam generated with {len(exam_questions)} questions")
            return {"questions": exam_questions}

        except Exception as e:
            logger.error(f"Error generating exam: {e}")
            raise
