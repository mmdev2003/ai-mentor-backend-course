from fastapi import status
from fastapi.responses import JSONResponse
from opentelemetry.trace import StatusCode, SpanKind

from internal import interface
from .model import StudentResponse


class EduStudentController(interface.IEduStudentController):
    def __init__(
            self,
            tel: interface.ITelemetry,
            student_service: interface.IEduStudentService
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.student_service = student_service

    async def get_by_id(self, student_id: int):
        with self.tracer.start_as_current_span(
                "StudentController.get_student_by_id",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id
                }
        ) as span:
            try:
                student = await self.student_service.get_by_id(student_id)
                response = StudentResponse(
                    id=student.id,
                    account_id=student.account_id,
                    current_expert=student.current_expert,
                    current_topic=student.current_topic,
                    current_block=student.current_block,
                    current_chapter=student.current_chapter,
                    programming_experience=student.programming_experience,
                    education_background=student.education_background,
                    learning_goals=student.learning_goals,
                    career_goals=student.career_goals,
                    timeline=student.timeline,
                    learning_style=student.learning_style,
                    lesson_duration=student.lesson_duration,
                    preferred_difficulty=student.preferred_difficulty,
                    recommended_topics=student.recommended_topics,
                    recommended_blocks=student.recommended_blocks,
                    approved_topics=student.approved_topics,
                    approved_blocks=student.approved_blocks,
                    approved_chapters=student.approved_chapters,
                    assessment_score=student.assessment_score,
                    strong_areas=student.strong_areas,
                    weak_areas=student.weak_areas,
                    created_at=student.created_at,
                    updated_at=student.updated_at
                )

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=response.model_dump(),
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err