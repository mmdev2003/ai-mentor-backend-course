from opentelemetry.trace import StatusCode, SpanKind

from internal import interface, model

class EduStudentService(interface.IEduStudentService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            student_repo: interface.IStudentRepo
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.student_repo = student_repo

    async def get_by_id(self, student_id: int) -> model.Student:
        with self.tracer.start_as_current_span(
                "IEduStudentService.get_student_by_id",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": student_id
                }
        ) as span:
            try:
                student = await self.student_repo.get_by_id(student_id)
                if not student:
                    raise ValueError(f"Student with id {student_id} not found")
                else:
                    return student[0]
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err