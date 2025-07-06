from fastapi import status
from fastapi.responses import JSONResponse
from opentelemetry.trace import StatusCode, SpanKind

from internal import interface
from .model import *


class ChatController(interface.IChatController):
    def __init__(
            self,
            tel: interface.ITelemetry,
            chat_service: interface.IChatService
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.chat_service = chat_service

    async def send_message_to_expert(self, body: SendMessageToExpert):
        with self.tracer.start_as_current_span(
                "EduChatController.send_message_to_expert",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": body.student_id,
                    "text": body.text
                }
        ) as span:
            try:
                user_message, commands = await self.chat_service.send_message_to_expert(
                    body.student_id,
                    body.text
                )

                response = SendMessageToExpertResponse(
                    user_message=user_message,
                    commands=commands
                )

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=response.to_dict(),
                )
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err