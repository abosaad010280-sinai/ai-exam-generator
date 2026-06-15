"""Data models and database schemas"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from app.core.config import settings
from app.core.logger import logger

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class Upload(Base):
    """Model for uploaded files"""
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True)
    original_filename = Column(String(255))
    file_type = Column(String(50))
    file_path = Column(String(500))
    content = Column(Text)
    upload_date = Column(DateTime, default=datetime.utcnow)
    file_size = Column(Integer)

    # Relationships
    exams = relationship("Exam", back_populates="upload")


class Exam(Base):
    """Model for generated exams"""
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"))
    subject_name = Column(String(255))
    grade_level = Column(String(100))
    exam_duration = Column(Integer)  # in minutes
    total_marks = Column(Float)
    num_questions = Column(Integer)
    question_types = Column(String(500))  # JSON string of selected types
    creation_date = Column(DateTime, default=datetime.utcnow)
    is_student_version = Column(Boolean, default=True)
    is_teacher_version = Column(Boolean, default=True)

    # Relationships
    upload = relationship("Upload", back_populates="exams")
    questions = relationship("Question", back_populates="exam")


class Question(Base):
    """Model for questions in question bank"""
    __tablename__ = "question_bank"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=True)
    question_text = Column(Text)
    question_type = Column(String(50))  # mcq, true_false, fill_blank, essay, practical
    subject = Column(String(255))
    difficulty_level = Column(String(50))  # easy, medium, hard
    options = Column(Text, nullable=True)  # JSON string for MCQ options
    correct_answer = Column(Text)
    explanation = Column(Text, nullable=True)
    creation_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    exam = relationship("Exam", back_populates="questions")


class ExamVersion(Base):
    """Model for different exam versions (A, B, C, D)"""
    __tablename__ = "exam_versions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    version_name = Column(String(10))  # A, B, C, D
    content = Column(Text)  # JSON content of the exam
    creation_date = Column(DateTime, default=datetime.utcnow)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database and create tables"""
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
