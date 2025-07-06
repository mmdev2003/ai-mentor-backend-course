import json
from opentelemetry.trace import SpanKind, StatusCode

from .query import *
from internal import model
from internal import interface


class StudentRepo(interface.IStudentRepo):
    def __init__(self, tel: interface.ITelemetry, db: interface.IDB):
        self.db = db
        self.tracer = tel.tracer()

    async def create_student(self, account_id: int) -> int:
        with self.tracer.start_as_current_span(
                "StudentRepo.create_student",
                kind=SpanKind.INTERNAL,
                attributes={
                    "account_id": account_id,
                }
        ) as span:
            try:
                args = {'account_id': account_id}
                student_id = await self.db.insert(create_student, args)

                span.set_status(StatusCode.OK)
                return student_id
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_by_id(self, student_id: int) -> list[model.Student]:
        with self.tracer.start_as_current_span(
                "StudentRepo.get_by_id",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                }
        ) as span:
            try:
                args = {'student_id': student_id}
                rows = await self.db.select(get_student_by_id, args)
                result = model.Student.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def update_student_background(self, student_id: int, background: dict):
        with self.tracer.start_as_current_span(
                "StudentRepo.update_student_background",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                }
        ) as span:
            try:
                # Конвертируем JSON поля в строки для PostgreSQL
                args = {
                    'student_id': student_id,
                    'programming_experience': background.get('programming_experience'),
                    'education_background': background.get('education_background'),
                    'learning_goals': background.get('learning_goals'),
                    'career_goals': background.get('career_goals'),
                    'timeline': background.get('timeline'),
                    'learning_style': background.get('learning_style'),
                    'lesson_duration': background.get('lesson_duration'),
                    'preferred_difficulty': background.get('preferred_difficulty'),
                    'recommended_topics': json.dumps(background.get('recommended_topics')) if background.get(
                        'recommended_topics') else None,
                    'recommended_blocks': json.dumps(background.get('recommended_blocks')) if background.get(
                        'recommended_blocks') else None,
                    'approved_topics': json.dumps(background.get('approved_topics')) if background.get(
                        'approved_topics') else None,
                    'approved_blocks': json.dumps(background.get('approved_blocks')) if background.get(
                        'approved_blocks') else None,
                    'approved_chapters': json.dumps(background.get('approved_chapters')) if background.get(
                        'approved_chapters') else None,
                    'assessment_score': background.get('assessment_score'),
                    'strong_areas': json.dumps(background.get('strong_areas')) if background.get(
                        'strong_areas') else None,
                    'weak_areas': json.dumps(background.get('weak_areas')) if background.get('weak_areas') else None,
                }

                await self.db.update(update_student_background, args)
                span.set_status(StatusCode.OK)
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def change_current_expert(self, student_id: int, expert_name: str):
        with self.tracer.start_as_current_span(
                "StudentRepo.change_current_expert",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                    "expert_name": expert_name,
                }
        ) as span:
            try:
                args = {
                    'student_id': student_id,
                    'expert_name': expert_name,
                }
                await self.db.update(change_current_expert, args)
                span.set_status(StatusCode.OK)
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def add_topic_to_approved_topics(self, student_id: int, topic_id: int, topic_name: str):
        with self.tracer.start_as_current_span(
                "StudentRepo.add_topic_to_approved_topics",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                    "topic_id": topic_id,
                }
        ) as span:
            try:
                args = {
                    'student_id': student_id,
                    'topic_id': str(topic_id),
                    'topic_name': topic_name,
                }
                await self.db.update(add_topic_to_approved, args)
                span.set_status(StatusCode.OK)
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def add_block_to_approved_blocks(self, student_id: int, block_id: int, block_name: str):
        with self.tracer.start_as_current_span(
                "StudentRepo.add_block_to_approved_blocks",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                    "block_id": block_id,
                }
        ) as span:
            try:
                args = {
                    'student_id': student_id,
                    'block_id': str(block_id),
                    'block_name': block_name,
                }
                await self.db.update(add_block_to_approved, args)
                span.set_status(StatusCode.OK)
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def add_chapter_to_approved_chapters(self, student_id: int, chapter_id: int, chapter_name: str):
        with self.tracer.start_as_current_span(
                "StudentRepo.add_chapter_to_approved_chapters",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id,
                    "chapter_id": chapter_id,
                }
        ) as span:
            try:
                args = {
                    'student_id': student_id,
                    'chapter_id': str(chapter_id),
                    'chapter_name': chapter_name,
                }
                await self.db.update(add_chapter_to_approved, args)
                span.set_status(StatusCode.OK)
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err