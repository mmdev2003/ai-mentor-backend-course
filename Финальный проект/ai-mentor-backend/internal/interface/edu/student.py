from abc import abstractmethod
from typing import Protocol, Optional
from internal import model


class IEduStudentController(Protocol):
    @abstractmethod
    async def get_by_id(self, student_id: int): pass


class IEduStudentService(Protocol):
    @abstractmethod
    async def get_by_id(self, student_id: int) -> model.Student: pass


class IStudentRepo(Protocol):
    @abstractmethod
    async def create_student(self, account_id: int) -> int: pass

    @abstractmethod
    async def get_by_id(self, student_id: int) -> list[model.Student]: pass

    @abstractmethod
    async def update_student_background(self, student_id: int, background: dict): pass

    @abstractmethod
    async def change_current_expert(self, student_id: int, expert_name: str): pass

    @abstractmethod
    async def add_topic_to_approved_topics(self, student_id: int, topic_id: int, topic_name: str): pass

    @abstractmethod
    async def add_block_to_approved_blocks(self, student_id: int, block_id: int, block_name: str): pass

    @abstractmethod
    async def add_chapter_to_approved_chapters(self, student_id: int, chapter_id: int, chapter_name: str): pass
