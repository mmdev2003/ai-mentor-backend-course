from abc import abstractmethod
from typing import Protocol

from internal.controller.http.handler.chat.model import *
from internal import model, common


class IChatController(Protocol):
    async def send_message_to_expert(self, body: SendMessageToExpert): pass


class IChatService(Protocol):
    async def send_message_to_expert(self, student_id: int, text: str) -> tuple[str, list[common.Command]]: pass


class IChatRepo(Protocol):

    @abstractmethod
    async def create_chat(self, student_id: int) -> int: pass

    @abstractmethod
    async def get_chat_by_student_id(self, student_id: int) -> list[model.Chat]: pass

    @abstractmethod
    async def create_message(self, chat_id: int, role: str, text: str): pass

    @abstractmethod
    async def get_messages(self, chat_id: int) -> list[model.Message]: pass


class IPromptGenerator(Protocol):
    @abstractmethod
    async def get_registrator_prompt(self) -> str: pass

    @abstractmethod
    async def get_interview_expert_prompt(self, student_id: int) -> str: pass

    @abstractmethod
    async def get_teacher_prompt(self, student_id: int) -> str: pass

    @abstractmethod
    async def get_test_expert_prompt(self, student_id: int) -> str: pass