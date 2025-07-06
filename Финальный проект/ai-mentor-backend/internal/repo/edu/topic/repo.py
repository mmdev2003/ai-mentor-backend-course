import io

from opentelemetry.trace import SpanKind, Status, StatusCode

from .query import *
from internal import model
from internal import interface


class TopicRepo(interface.ITopicRepo):
    def __init__(self, tel: interface.ITelemetry, db: interface.IDB, storage: interface.IStorage):
        self.db = db
        self.storage = storage
        self.tracer = tel.tracer()

    # Topic methods
    async def get_topic_by_id(self, topic_id: int) -> list[model.Topic]:
        with self.tracer.start_as_current_span(
                "TopicRepo.get_topic_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"topic_id": topic_id}
        ) as span:
            try:
                args = {'topic_id': topic_id}
                rows = await self.db.select(get_topic_by_id, args)
                result = model.Topic.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_all_topic(self) -> list[model.Topic]:
        with self.tracer.start_as_current_span(
                "TopicRepo.get_all_topic",
                kind=SpanKind.INTERNAL
        ) as span:
            try:
                rows = await self.db.select(get_all_topics, {})
                result = model.Topic.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    # Block methods
    async def get_block_by_id(self, block_id: int) -> list[model.Block]:
        with self.tracer.start_as_current_span(
                "TopicRepo.get_block_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"block_id": block_id}
        ) as span:
            try:
                args = {'block_id': block_id}
                rows = await self.db.select(get_block_by_id, args)
                result = model.Block.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_all_block(self) -> list[model.Block]:
        with self.tracer.start_as_current_span(
                "TopicRepo.get_all_block",
                kind=SpanKind.INTERNAL
        ) as span:
            try:
                rows = await self.db.select(get_all_blocks, {})
                result = model.Block.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    # Chapter methods
    async def get_chapter_by_id(self, chapter_id: int) -> list[model.Chapter]:
        with self.tracer.start_as_current_span(
                "TopicRepo.get_chapter_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"chapter_id": chapter_id}
        ) as span:
            try:
                args = {'chapter_id': chapter_id}
                rows = await self.db.select(get_chapter_by_id, args)
                result = model.Chapter.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_all_chapter(self) -> list[model.Chapter]:
        with self.tracer.start_as_current_span(
                "TopicRepo.get_all_chapter",
                kind=SpanKind.INTERNAL
        ) as span:
            try:
                rows = await self.db.select(get_all_chapters, {})
                result = model.Chapter.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    # Student progress methods
    async def update_current_topic(self, student_id: int, topic_id: int, topic_name: str):
        with self.tracer.start_as_current_span(
                "TopicRepo.update_current_topic",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                    "topic_id": topic_id
                }
        ) as span:
            try:
                args = {
                    'student_id': student_id,
                    'topic_id': str(topic_id),
                    'topic_name': topic_name,
                }
                await self.db.update(update_current_topic, args)
                span.set_status(StatusCode.OK)
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def update_current_block(self, student_id: int, block_id: int, block_name: str):
        with self.tracer.start_as_current_span(
                "TopicRepo.update_current_block",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                    "block_id": block_id
                }
        ) as span:
            try:
                args = {
                    'student_id': student_id,
                    'block_id': str(block_id),
                    'block_name': block_name,
                }
                await self.db.update(update_current_block, args)
                span.set_status(StatusCode.OK)
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def update_current_chapter(self, student_id: int, chapter_id: int, chapter_name: str):
        with self.tracer.start_as_current_span(
                "TopicRepo.update_current_chapter",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                    "chapter_id": chapter_id
                }
        ) as span:
            try:
                args = {
                    'student_id': student_id,
                    'chapter_id': str(chapter_id),
                    'chapter_name': chapter_name,
                }
                await self.db.update(update_current_chapter, args)
                span.set_status(StatusCode.OK)
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def create_topic(self, name: str, intro_file_id: str, edu_plan_file_id: str) -> int:
        with self.tracer.start_as_current_span(
                "TopicRepo.create_topic",
                kind=SpanKind.INTERNAL,
                attributes={"name": name}
        ) as span:
            try:
                args = {
                    'name': name,
                    'intro_file_id': intro_file_id,
                    'edu_plan_file_id': edu_plan_file_id
                }
                topic_id = await self.db.insert(create_topic, args)

                span.set_status(StatusCode.OK)
                return topic_id
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def create_block(self, topic_id: int, name: str, content_file_id: str) -> int:
        with self.tracer.start_as_current_span(
                "TopicRepo.create_block",
                kind=SpanKind.INTERNAL,
                attributes={"topic_id": topic_id, "name": name}
        ) as span:
            try:
                args = {
                    'topic_id': topic_id,
                    'name': name,
                    'content_file_id': content_file_id
                }
                block_id = await self.db.insert(create_block, args)

                span.set_status(StatusCode.OK)
                return block_id
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def create_chapter(self, topic_id: int, block_id: int, name: str, content_file_id: str) -> int:
        with self.tracer.start_as_current_span(
                "TopicRepo.create_chapter",
                kind=SpanKind.INTERNAL,
                attributes={"topic_id": topic_id, "block_id": block_id, "name": name}
        ) as span:
            try:
                args = {
                    'topic_id': topic_id,
                    'block_id': block_id,
                    'name': name,
                    'content_file_id': content_file_id
                }
                chapter_id = await self.db.insert(create_chapter, args)

                span.set_status(StatusCode.OK)
                return chapter_id
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err


    async def upload_file(self, file: io.BytesIO, file_name: str) -> str:
        response = self.storage.upload(file, file_name)
        return response.fid

    async def download_file(self, file_id: str, file_name: str) -> tuple[io.BytesIO, str]:
        file, content_type = self.storage.download(file_id, file_name)
        return file, content_type
