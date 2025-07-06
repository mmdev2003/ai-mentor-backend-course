from fastapi.responses import StreamingResponse
from opentelemetry.trace import StatusCode, SpanKind

from internal import interface


class EduTopicController(interface.IEduTopicController):
    def __init__(
            self,
            tel: interface.ITelemetry,
            edu_topic_service: interface.IEduTopicService,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.edu_topic_service = edu_topic_service

    async def download_topic_content(self, edu_content_type: str, topic_id: int):
        with self.tracer.start_as_current_span(
                "EduChatController.download_topic_content",
                kind=SpanKind.INTERNAL,
                attributes={
                    "edu_content_type": edu_content_type,
                    "topic_id": topic_id
                }
        ) as span:
            try:
                file, content_type = await self.edu_topic_service.download_topic_content(
                    edu_content_type,
                    topic_id
                )
                headers = {
                    "Content-Type": content_type,
                }
                return StreamingResponse(
                    content=file,
                    headers=headers
                )
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def download_block_content(self, block_id: int):
        with self.tracer.start_as_current_span(
                "EduChatController.download_block_content",
                kind=SpanKind.INTERNAL,
                attributes={
                    "block_id": block_id,
                }
        ) as span:
            try:
                file, content_type = await self.edu_topic_service.download_block_content(
                    block_id
                )
                headers = {
                    "Content-Type": content_type,
                }
                return StreamingResponse(
                    content=file,
                    headers=headers
                )
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err
