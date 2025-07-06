from opentelemetry.trace import SpanKind, Status, StatusCode

from .query import *
from internal import model
from internal import interface


class ChatRepo(interface.IChatRepo):
    def __init__(self, tel: interface.ITelemetry, db: interface.IDB):
        self.db = db
        self.tracer = tel.tracer()

    async def create_chat(self, student_id: int) -> int:
        with self.tracer.start_as_current_span(
                "ChatRepo.create_chat",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                }
        ) as span:
            try:
                args = {'student_id': student_id}
                chat_id = await self.db.insert(create_chat, args)

                span.set_status(StatusCode.OK)
                return chat_id
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_chat_by_student_id(self, student_id: int) -> list[model.Chat]:
        with self.tracer.start_as_current_span(
                "ChatRepo.get_chat_by_student_id",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                }
        ) as span:
            try:
                args = {'student_id': student_id}
                rows = await self.db.select(get_chat_by_student_id, args)
                result = model.Chat.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def create_message(self, chat_id: int, role: str, text: str):
        with self.tracer.start_as_current_span(
                "ChatRepo.create_message",
                kind=SpanKind.INTERNAL,
                attributes={
                    "chat_id": chat_id,
                    "role": role,
                }
        ) as span:
            try:
                args = {
                    'chat_id': chat_id,
                    'role': role,
                    'text': text,
                }
                message_id = await self.db.insert(create_message, args)

                span.set_status(StatusCode.OK)
                return message_id
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_messages(self, chat_id: int) -> list[model.Message]:
        with self.tracer.start_as_current_span(
                "ChatRepo.get_messages",
                kind=SpanKind.INTERNAL,
                attributes={
                    "chat_id": chat_id,
                }
        ) as span:
            try:
                args = {'chat_id': chat_id}
                rows = await self.db.select(get_messages_by_chat_id, args)
                result = model.Message.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err