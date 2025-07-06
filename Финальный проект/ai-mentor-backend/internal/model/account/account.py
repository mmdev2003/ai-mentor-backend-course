from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Account:
    id: int

    login: str
    password: str

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def serialize(cls, rows) -> list['Account']:
        return [
            cls(
                id=row.id,
                login=row.login,
                password=row.password,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]