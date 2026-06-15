"""Exam generation routes"""

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.logger import logger
from app.models import get_db, Upload as UploadModel, Exam as ExamModel, Question
from app.services.exam_generator import ExamGenerator
from datetime import datetime

router = APIRouter(prefix="/api/exams", tags=["exams"])
exam_generator = ExamGenerator()


@router.post("/generate")
async def generate_exam(
    upload_id: int,
    subject_name: str,
    grade_level: str,
    num_questions: int,
    question_types: List[str],
    exam_duration: int,
    db: Session = get_db()
):
    """Generate exam from uploaded file"""
    try:
        # Get upload
        upload = next(db).query(UploadModel).filter(UploadModel.id == upload_id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Upload not found")

        # Generate exam questions
        exam_result = await exam_generator.generate_exam(
            upload.content,
            num_questions,
            question_types,
            subject_name
        )

        # Save exam to database
        exam = ExamModel(
            upload_id=upload_id,
            subject_name=subject_name,
            grade_level=grade_level,
            exam_duration=exam_duration,
            total_marks=num_questions * 2,
            num_questions=len(exam_result["questions"]),
            question_types=",".join(question_types),
            creation_date=datetime.utcnow()
        )
        next(db).add(exam)
        next(db).commit()
        next(db).refresh(exam)

        # Save questions
        for q in exam_result["questions"]:
            question = Question(
                exam_id=exam.id,
                question_text=q.get("text"),
                question_type=q.get("type", "mcq"),
                subject=subject_name,
                difficulty_level=q.get("difficulty", "medium"),
                options=str(q.get("options", [])),
                correct_answer=q.get("correct_answer"),
                explanation=q.get("explanation", "")
            )
            next(db).add(question)

        next(db).commit()

        logger.info(f"Exam generated with ID: {exam.id}")
        return {
            "success": True,
            "exam_id": exam.id,
            "num_questions": exam.num_questions,
            "total_marks": exam.total_marks,
            "questions": exam_result["questions"]
        }

    except Exception as e:
        logger.error(f"Error generating exam: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preview/{exam_id}")
async def preview_exam(exam_id: int, db: Session = get_db()):
    """Preview exam questions"""
    try:
        exam = next(db).query(ExamModel).filter(ExamModel.id == exam_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        questions = next(db).query(Question).filter(Question.exam_id == exam_id).all()

        return {
            "success": True,
            "exam": {
                "id": exam.id,
                "subject_name": exam.subject_name,
                "grade_level": exam.grade_level,
                "num_questions": exam.num_questions,
                "total_marks": exam.total_marks,
                "exam_duration": exam.exam_duration
            },
            "questions": [
                {
                    "id": q.id,
                    "text": q.question_text,
                    "type": q.question_type,
                    "difficulty": q.difficulty_level,
                    "options": eval(q.options) if q.options else []
                }
                for q in questions
            ]
        }

    except Exception as e:
        logger.error(f"Error previewing exam: {e}")
        raise HTTPException(status_code=500, detail=str(e))
