import io
from opentelemetry.trace import StatusCode, SpanKind

from internal import interface


class EduTopicService(interface.IEduTopicService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            topic_repo: interface.ITopicRepo,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.topic_repo = topic_repo

    async def download_topic_content(self, edu_content_type: str, topic_id: int) -> tuple[io.BytesIO, str]:
        with self.tracer.start_as_current_span(
                "EduTopicService.download_topic_content",
                kind=SpanKind.INTERNAL,
                attributes={"edu_content_type": edu_content_type, "topic_id": topic_id}
        ) as span:
            try:

                topic = (await self.topic_repo.get_topic_by_id(topic_id))[0]

                if edu_content_type == "edu-plan":
                    file, content_type = await self.topic_repo.download_file(
                        topic.edu_plan_file_id,
                        topic.name
                    )
                else:
                    file, content_type = await self.topic_repo.download_file(
                        topic.intro_file_id,
                        topic.name
                    )

                return file, content_type

            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def download_block_content(self, block_id: int) -> tuple[io.BytesIO, str]:
            with self.tracer.start_as_current_span(
                    "EduTopicService.download_block_content",
                    kind=SpanKind.INTERNAL,
                    attributes={"block_id": block_id}
            ) as span:
                try:
                    block = (await self.topic_repo.get_block_by_id(block_id))[0]
                    file, content_type = await self.topic_repo.download_file(
                        block.content_file_id,
                        block.name
                    )

                    return file, content_type

                except Exception as err:
                    span.record_exception(err)
                    span.set_status(StatusCode.ERROR, str(err))
                    raise err
