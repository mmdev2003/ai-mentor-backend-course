from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Topic:
    id: int

    name: str
    intro_file_id: str = None
    edu_plan_file_id: str = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "intro_file_id": self.intro_file_id,
            "edu_plan_file_id": self.edu_plan_file_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def serialize(cls, rows) -> list:
        return [
            cls(
                id=row.id,
                name=row.name,
                intro_file_id=row.intro_file_id,
                edu_plan_file_id=row.edu_plan_file_id,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]


@dataclass
class Block:
    id: int
    topic_id: int

    name: str
    content_file_id: str = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "name": self.name,
            "content_file_id": self.content_file_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def serialize(cls, rows) -> list:
        return [
            cls(
                id=row.id,
                topic_id=row.topic_id,
                name=row.name,
                content_file_id=row.content_file_id,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]


@dataclass
class Chapter:
    id: int
    topic_id: int
    block_id: int

    name: str
    content_file_id: str = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "block_id": self.block_id,
            "name": self.name,
            "content_file_id": self.content_file_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def serialize(cls, rows) -> list:
        return [
            cls(
                id=row.id,
                topic_id=row.topic_id,
                block_id=row.block_id,
                name=row.name,
                content_file_id=row.content_file_id,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]
