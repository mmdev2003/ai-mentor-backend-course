from dataclasses import dataclass


class Roles:
    """Роли в системе чата"""
    user = "user"
    assistant = "assistant"
    system = "system"


class Experts:
    registrator = "registrator"
    interview = "interview"
    teacher = "teacher"
    test = "test"

TRACE_ID_KEY = "trace_id"
SPAN_ID_KEY = "span_id"
REQUEST_ID_KEY = "request_id"
EXTRA_LOG_FIELDS_KEY = "extra"
FILE_KEY = "file"
ERROR_KEY = "error"

HTTP_METHOD_KEY = "http.request.method"
HTTP_STATUS_KEY = "http.response.status_code"
HTTP_ROUTE_KEY = "http.route"
HTTP_REQUEST_DURATION_KEY = "http.server.request.duration"

CRM_SYSTEM_NAME_KEY = "crm.system.name"

TELEGRAM_USERBOT_USER_ID_KEY = "telegram.userbot.user_id"
TELEGRAM_UPDATE_TYPE_KEY = "telegram.update.type"
TELEGRAM_CHAT_ID_KEY = "telegram.chat.id"
TELEGRAM_USER_USERNAME_KEY = "telegram.user.username"
TELEGRAM_USER_MESSAGE_KEY = "telegram.user.message"
TELEGRAM_MESSAGE_ID_KEY = "telegram.message.id"
TELEGRAM_MESSAGE_DURATION_KEY = "telegram.message.duration"
TELEGRAM_MESSAGE_DIRECTION_KEY = "telegram.message.direction"
TELEGRAM_CHAT_TYPE_KEY = "telegram.chat.type"

REQUEST_DURATION_METRIC = "http.server.request.duration"
ACTIVE_REQUESTS_METRIC = "http.server.active_requests"
REQUEST_BODY_SIZE_METRIC = "http.server.request.body.size"
RESPONSE_BODY_SIZE_METRIC = "http.server.response.body.size"
OK_REQUEST_TOTAL_METRIC = "http.server.ok.request.total"
ERROR_REQUEST_TOTAL_METRIC = "http.server.error.request.total"

OK_MESSAGE_TOTAL_METRIC = "telegram.server.ok.message.total"
ERROR_MESSAGE_TOTAL_METRIC = "telegram.server.error.message.total"
OK_JOIN_CHAT_TOTAL_METRIC = "telegram.server.ok.join_chat.total"
ERROR_JOIN_CHAT_TOTAL_METRIC = "telegram.server.error.join_chat.total"
MESSAGE_DURATION_METRIC = "telegram.server.message.duration"
ACTIVE_MESSAGES_METRIC = "telegram.server.active_messages"

TRACE_ID_HEADER = "X-Trace-ID"
SPAN_ID_HEADER = "X-Span-ID"