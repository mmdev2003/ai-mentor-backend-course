from fastapi import FastAPI

from internal import interface
from internal import model


def NewHTTP(
        db: interface.IDB,
        chat_controller: interface.IChatController,
        edu_student_controller: interface.IEduStudentController,
        edu_topic_controller: interface.IEduTopicController,
        http_middleware: interface.IHttpMiddleware,
        prefix: str
):
    app = FastAPI()
    include_middleware(app, http_middleware)

    include_db_handler(app, db, prefix)
    include_chat_handlers(app, chat_controller, prefix)
    include_edu_student_handlers(app, edu_student_controller, prefix)
    include_edu_topic_handlers(app, edu_topic_controller, prefix)

    return app


def include_middleware(
        app: FastAPI,
        http_middleware: interface.IHttpMiddleware
):
    http_middleware.logger_middleware03(app)
    http_middleware.metrics_middleware02(app)
    http_middleware.trace_middleware01(app)


def include_chat_handlers(
        app: FastAPI,
        chat_controller: interface.IChatController,
        prefix: str
):
    app.add_api_route(
        prefix + "/chat/message/send",
        chat_controller.send_message_to_expert,
        methods=["POST"],
        summary="Отправить сообщение регистратору",
        description="Отправляет сообщение регистратору"
    )

def include_edu_topic_handlers(
        app: FastAPI,
        edu_topic_controller: interface.IEduTopicController,
        prefix: str
):
    app.add_api_route(
        prefix + "/edu/topic/download/{edu_content_type}/{file_id}",
        edu_topic_controller.download_topic_content,
        methods=["GET"],
    )

    app.add_api_route(
        prefix + "/edu/block/download/{file_id}",
        edu_topic_controller.download_block_content,
        methods=["GET"],
    )


def include_edu_student_handlers(
        app: FastAPI,
        edu_student_controller: interface.IEduStudentController,
        prefix: str
):
    app.add_api_route(
        prefix + "/edu/student/{student_id}",
        edu_student_controller.get_by_id,
        methods=["GET"],
    )


def include_db_handler(app: FastAPI, db: interface.IDB, prefix: str):
    app.add_api_route(prefix + "/table/create", create_table_handler(db), methods=["GET"])
    app.add_api_route(prefix + "/table/drop", drop_table_handler(db), methods=["GET"])


def create_table_handler(db: interface.IDB):
    async def create_table():
        try:
            await db.multi_query(model.create_queries)
        except Exception as err:
            raise err

    return create_table


def drop_table_handler(db: interface.IDB):
    async def delete_table():
        try:
            await db.multi_query(model.drop_queries)
        except Exception as err:
            raise err

    return delete_table
