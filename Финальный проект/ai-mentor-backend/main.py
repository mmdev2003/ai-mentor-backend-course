import uvicorn

# External dependencies
from infrastructure.pg.pg import PG
from infrastructure.weedfs.weedfs import Weed
from pkg.client.external.openai.client import GPTClient
from infrastructure.telemetry.telemetry import Telemetry, AlertManager

# Repositories
from internal.repo.account.repo import AccountRepo
from internal.repo.edu.student.repo import StudentRepo
from internal.repo.chat.repo import ChatRepo
from internal.repo.edu.topic.repo import TopicRepo

# Services
from internal.service.edu.student.service import EduStudentService
from internal.service.edu.topic.service import EduTopicService
from internal.service.chat.service import ChatService
from internal.service.chat.prompt import PromptGenerator

# Controllers
from internal.controller.http.handler.chat.handler import ChatController
from internal.controller.http.handler.edu.topic.handler import EduTopicController
from internal.controller.http.handler.edu.student.handler import EduStudentController
from internal.controller.http.middlerware.middleware import HttpMiddleware

# App
from internal.app.http.app import NewHTTP

# Config
from internal.config.config import Config

# Инициализация конфигурации
cfg = Config()

alert_manager = AlertManager(
    cfg.alert_tg_bot_token,
    cfg.service_name,
    cfg.alert_tg_chat_id,
    cfg.alert_tg_chat_thread_id,
    cfg.grafana_url,
    cfg.monitoring_redis_host,
    cfg.monitoring_redis_port,
    cfg.monitoring_redis_db,
    cfg.monitoring_redis_password
)

# Инициализация телеметрии
tel = Telemetry(
    cfg.log_level,
    cfg.root_path,
    cfg.environment,
    cfg.service_name,
    cfg.service_version,
    cfg.otlp_host,
    cfg.otlp_port,
    alert_manager
)

# Инициализация базы данных
db = PG(
    tel,
    cfg.db_user,
    cfg.db_pass,
    cfg.db_host,
    cfg.db_port,
    cfg.db_name
)

storage = Weed(cfg.weed_master_host, cfg.weed_master_port)

# Инициализация LLM клиента
llm_client = GPTClient(
    tel,
    cfg.openai_api_key
)

# Инициализация репозиториев
account_repo = AccountRepo(tel, db)
student_repo = StudentRepo(tel, db)
chat_repo = ChatRepo(tel, db)
edu_topic_repo = TopicRepo(tel, db, storage)

# Инициализация сервисов
prompt_generator = PromptGenerator(
    tel,
    student_repo,
    edu_topic_repo
)

chat_service = ChatService(
    tel,
    llm_client,
    prompt_generator,
    student_repo,
    edu_topic_repo,
    chat_repo,
    account_repo
)

edu_topic_service = EduTopicService(tel, edu_topic_repo)
edu_student_service = EduStudentService(tel, student_repo)

# Инициализация middleware
http_middleware = HttpMiddleware(
    tel,
    cfg.prefix
)

# Инициализация контроллеров
chat_controller = ChatController(
    tel,
    chat_service
)

edu_topic_controller = EduTopicController(
    tel,
    edu_topic_service
)

edu_student_controller = EduStudentController(
    tel,
    edu_student_service
)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='For choice app')
    parser.add_argument(
        'app',
        type=str,
        help='Option: "http, parse_edu_content"'
    )
    args = parser.parse_args()

    if args.app == "http":
        # Создание HTTP приложения
        http_app = NewHTTP(
            db,
            chat_controller,
            edu_student_controller,
            edu_topic_controller,
            http_middleware,
            cfg.prefix
        )

        # Запуск сервера
        uvicorn.run(
            http_app,
            host='0.0.0.0',
            port=cfg.http_port,
            loop='asyncio',
            access_log=False
        )
