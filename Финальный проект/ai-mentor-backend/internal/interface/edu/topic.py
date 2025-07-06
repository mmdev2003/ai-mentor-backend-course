import io
from abc import abstractmethod
from typing import Protocol

from internal import model
from internal.controller.http.handler.edu.topic.model import *


class IEduTopicController(Protocol):
    @abstractmethod
    async def download_topic_content(self, edu_content_type: str, topic_id: int): pass

    @abstractmethod
    async def download_block_content(self, block_id: int): pass


class IEduTopicService(Protocol):
    @abstractmethod
    async def download_topic_content(self, edu_content_type: str, topic_id: int) -> tuple[io.BytesIO, str]: pass

    @abstractmethod
    async def download_block_content(self, block_id: int) -> tuple[io.BytesIO, str]: pass


class ITopicRepo(Protocol):
    @abstractmethod
    async def create_topic(self, name: str, intro_file_id: str, edu_plan_file_id: str) -> int: pass

    @abstractmethod
    async def create_block(self, topic_id: int, name: str, content_file_id: str) -> int: pass

    @abstractmethod
    async def create_chapter(self, topic_id: int, block_id: int, name: str, content_file_id: str) -> int: pass

    @abstractmethod
    async def update_current_topic(self, student_id: int, topic_id: int, topic_name: str): pass

    @abstractmethod
    async def update_current_block(self, student_id: int, block_id: int, block_name: str): pass

    @abstractmethod
    async def update_current_chapter(self, student_id: int, chapter_id: int, chapter_name: str): pass

    @abstractmethod
    async def get_topic_by_id(self, topic_id: int) -> list[model.Topic]: pass

    @abstractmethod
    async def get_block_by_id(self, block_id: int) -> list[model.Block]: pass

    @abstractmethod
    async def get_chapter_by_id(self, chapter_id: int) -> list[model.Chapter]: pass

    @abstractmethod
    async def get_all_topic(self) -> list[model.Topic]: pass

    @abstractmethod
    async def get_all_block(self) -> list[model.Block]: pass

    @abstractmethod
    async def get_all_chapter(self) -> list[model.Chapter]: pass

    @abstractmethod
    async def upload_file(self, file: io.BytesIO, file_name: str) -> str: pass

    @abstractmethod
    async def download_file(self, file_id: str, file_name: str) -> tuple[io.BytesIO, str]: pass
