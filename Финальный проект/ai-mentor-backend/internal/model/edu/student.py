from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Student:
    id: int
    account_id: int

    current_expert: str = None
    current_topic: dict[int, str] = None
    current_block: dict[int, str] = None
    current_chapter: dict[int, str] = None

    programming_experience: str = None
    education_background: str = None

    # Цели
    learning_goals: str = None
    career_goals: str = None
    timeline: str = None

    # Предпочтения
    learning_style: str = None
    lesson_duration: str = None
    preferred_difficulty: str = None

    # {id: name} тем в порядке изучения
    recommended_topics: dict[int, str] = field(default_factory=dict)
    # {id: name} блоков в порядке изучения
    recommended_blocks: dict[int, str] = field(default_factory=dict)

    # {id: name} тем, которые уже изучены
    approved_topics: dict[int, str] = field(default_factory=dict)
    # {id: name} блоков, которые уже изучены
    approved_blocks: dict[int, str] = field(default_factory=dict)
    # {id: name} глав, которые уже изучены
    approved_chapters: dict[int, str] = field(default_factory=dict)

    # Оценка уровня
    # 0-100
    assessment_score: int = None
    strong_areas: list[str] = field(default_factory=list)
    weak_areas: list[str] = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def serialize(cls, rows) -> list['Student']:
        """Сериализация из результатов БД"""
        return [
            cls(
                id=row.id,
                account_id=row.account_id,
                current_expert=row.current_expert,
                current_topic=row.current_topic,
                current_block=row.current_block,
                current_chapter=row.current_chapter,
                programming_experience=row.programming_experience,
                education_background=row.education_background,
                learning_goals=row.learning_goals,
                career_goals=row.career_goals,
                timeline=row.timeline,
                learning_style=row.learning_style,
                lesson_duration=row.lesson_duration,
                preferred_difficulty=row.preferred_difficulty,
                recommended_topics=row.recommended_topics,
                recommended_blocks=row.recommended_blocks,
                approved_topics=row.approved_topics,
                approved_blocks=row.approved_blocks,
                approved_chapters=row.approved_chapters,
                assessment_score=row.assessment_score,
                strong_areas=row.strong_areas,
                weak_areas=row.weak_areas,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]
