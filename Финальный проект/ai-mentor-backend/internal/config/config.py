import os

class Config:
    db_pass: str = os.environ.get('BACKEND_POSTGRES_PASSWORD')
    db_user: str = os.environ.get('BACKEND_POSTGRES_USER')
    db_name: str = os.environ.get('BACKEND_POSTGRES_DB_NAME')
    db_host: str = os.environ.get('BACKEND_POSTGRES_HOST')
    db_port: str = "5432"

    http_port: int = int(os.environ.get('BACKEND_PORT'))
    prefix = os.environ.get('BACKEND_PREFIX')
    service_name = "backend"

    root_path = "/app"
    service_version = "0.0.1"
    otlp_host: str = os.environ.get("OTEL_COLLECTOR_HOST")
    otlp_port: int = os.environ.get("OTEL_COLLECTOR_GRPC_PORT")

    openai_api_key: str = os.environ.get('OPEN_AI_API_KEY')

    environment = os.environ.get('ENVIRONMENT')
    log_level = os.environ.get('LOG_LEVEL')

    alert_tg_bot_token: str = os.environ.get('ALERT_TG_BOT_TOKEN')
    alert_tg_chat_id: int = int(os.environ.get('ALERT_TG_CHAT_ID'))
    alert_tg_chat_thread_id: int = int(os.environ.get('ALERT_TG_CHAT_THREAD_ID'))
    grafana_url: str = os.environ.get('GRAFANA_URL')

    monitoring_redis_host: str = os.environ.get('MONITORING_REDIS_HOST')
    monitoring_redis_port: int = int(os.environ.get('MONITORING_REDIS_PORT'))
    monitoring_redis_db: int = int(os.environ.get('MONITORING_DEDUPLICATE_ERROR_ALERT_REDIS_DB'))
    monitoring_redis_password: str = os.environ.get('MONITORING_REDIS_PASSWORD')

    weed_master_host: str = os.environ.get('WEED_MASTER_CONTAINER_NAME')
    weed_master_port: int = int(os.environ.get('WEED_MASTER_PORT'))