from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class StudentResponse(BaseModel):
    id: int
    account_id: int

    # Текущий контекст
    current_expert: Optional[str] = None
    current_topic: Optional[Dict[int, str]] = None
    current_block: Optional[Dict[int, str]] = None
    current_chapter: Optional[Dict[int, str]] = None

    # Профиль студента
    programming_experience: Optional[str] = None
    education_background: Optional[str] = None
    learning_goals: Optional[str] = None
    career_goals: Optional[str] = None
    timeline: Optional[str] = None
    learning_style: Optional[str] = None
    lesson_duration: Optional[str] = None
    preferred_difficulty: Optional[str] = None

    # Рекомендации и прогресс
    recommended_topics: Optional[Dict[int, str]] = None
    recommended_blocks: Optional[Dict[int, str]] = None
    approved_topics: Optional[Dict[int, str]] = None
    approved_blocks: Optional[Dict[int, str]] = None
    approved_chapters: Optional[Dict[int, str]] = None

    # Оценка
    assessment_score: Optional[int] = None
    strong_areas: Optional[list[str]] = None
    weak_areas: Optional[list[str]] = None

    # Метаданные
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True