# 🚀 Онбординг разработчика
## Как мы реально пишем код - Deep Dive в архитектуру

---

## 🎯 Введение

Этот документ не просто список принципов, а **полное погружение** в то, как мы реально строим системы. Каждый пример взят из продакшн-кода, каждый паттерн объяснен с контекстом.

**После изучения этого документа вы будете:**
- Понимать каждый слой нашей архитектуры
- Знать, где и как добавлять новую функциональность
- Писать код, который seamless интегрируется в существующую систему
- Понимать WHY мы делаем именно так

---

## 🏗️ Реальная архитектура проектов

### Анатомия проекта AI-Mentor

Давайте разберем **реальную структуру** нашего проекта:

```
ai-mentor-system/
├── infrastructure/                 # Все внешние интеграции
│   ├── pg/pg.py                   # PostgreSQL с трейсингом
│   ├── redis_client/              # Redis с connection pooling
│   ├── telemetry/                 # OpenTelemetry stack
│   │   ├── telemetry.py          # Инициализация мониторинга
│   │   ├── logger.py             # Structured logging
│   │   └── alertmanager.py       # Telegram алерты
│   ├── weedfs/weedfs.py          # Distributed file storage
│   └── docker/                    # Инфраструктура
├── internal/                      # Чистая бизнес-логика
│   ├── interface/                 # Контракты - сердце архитектуры
│   │   ├── general.py            # Базовые интерфейсы (DB, Logger, etc.)
│   │   ├── chat/chat.py          # Чат система
│   │   ├── edu/student.py        # Образовательная система
│   │   └── client/llm.py         # LLM интеграции
│   ├── model/                     # Доменные модели с сериализацией
│   │   ├── account/account.py
│   │   ├── chat/chat.py
│   │   ├── edu/student.py
│   │   └── sql_model.py          # DDL для всех таблиц
│   ├── repo/                      # Data Access Layer
│   │   ├── account/
│   │   │   ├── query.py          # SQL запросы
│   │   │   └── repo.py           # Реализация Repository
│   │   ├── chat/
│   │   └── edu/
│   ├── service/                   # Business Logic Layer
│   │   ├── chat/
│   │   │   ├── service.py        # Orchestration
│   │   │   ├── prompt.py         # LLM промпты
│   │   │   └── topic_formatter.py # Data formatting
│   │   └── edu/
│   ├── controller/               # Presentation Layer
│   │   └── http/
│   │       ├── handler/          # HTTP handlers
│   │       └── middleware/       # HTTP middleware
│   ├── config/config.py          # Environment configuration
│   └── common/                   # Shared utilities
├── pkg/                          # Переиспользуемые компоненты
│   └── client/external/openai/   # External API clients
├── docker-compose/               # Orchestration
│   ├── app.yaml                  # Application services
│   ├── db.yaml                   # Database services
│   └── monitoring.yaml           # Observability stack
├── env/                          # Environment configs
├── monitoring/                   # Monitoring configurations
└── main.py                       # Application bootstrap
```

### Почему именно такая структура?

**1. Четкое разделение ответственности:**
- `infrastructure/` - ВСЕ что касается внешнего мира
- `internal/` - ТОЛЬКО бизнес-логика
- `pkg/` - Переиспользуемые компоненты

**2. Dependency Rule:**
- `internal/` НЕ ЗНАЕТ про `infrastructure/`
- Все зависимости идут через интерфейсы
- Легко тестировать, легко менять реализации

---

## 🧱 Слои архитектуры - как это работает РЕАЛЬНО

### Layer 1: Interface Layer - Контракты системы

Это **самый важный слой** - все начинается здесь:

```python
# internal/interface/general.py - Базовые контракты
class ITelemetry(Protocol):
    @abstractmethod
    def tracer(self) -> Tracer: pass
    
    @abstractmethod
    def meter(self) -> Meter: pass
    
    @abstractmethod
    def logger(self) -> IOtelLogger: pass

class IDB(Protocol):
    @abstractmethod
    async def insert(self, query: str, query_params: dict) -> int: pass
    
    @abstractmethod
    async def select(self, query: str, query_params: dict) -> Sequence[Any]: pass
```

**Почему так?**
- Любой сервис может работать с любой БД
- Можем легко мокать для тестов
- Четко видны все операции системы

### Layer 2: Model Layer - Доменные сущности

```python
# internal/model/edu/student.py
@dataclass
class Student:
    id: int
    account_id: int
    
    # Контекст обучения
    current_expert: str = None
    current_topic: dict[int, str] = None
    current_block: dict[int, str] = None
    
    # Профиль студента
    programming_experience: str = None
    learning_goals: str = None
    
    # Прогресс
    approved_topics: dict[int, str] = field(default_factory=dict)
    assessment_score: int = None
    
    @classmethod
    def serialize(cls, rows) -> list['Student']:
        """Сериализация из результатов БД"""
        return [
            cls(
                id=row.id,
                account_id=row.account_id,
                current_expert=row.current_expert,
                # ... все поля
            )
            for row in rows
        ]
```

**Ключевые особенности:**
- `@dataclass` для автогенерации методов
- `serialize()` - статический метод для конвертации из БД
- Type hints для всех полей
- `field(default_factory=dict)` для мутабельных defaults

### Layer 3: Repository Layer - Доступ к данным

```python
# internal/repo/edu/student/repo.py
class StudentRepo(interface.IStudentRepo):
    def __init__(self, tel: interface.ITelemetry, db: interface.IDB):
        self.db = db
        self.tracer = tel.tracer()

    async def get_by_id(self, student_id: int) -> list[model.Student]:
        with self.tracer.start_as_current_span(
                "StudentRepo.get_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"student_id": student_id}
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
```

**Паттерн каждого метода Repository:**
1. **Трейсинг span** с attributes
2. **Try-catch** с proper error handling  
3. **Параметризованные запросы** (защита от SQL injection)
4. **Сериализация** через model.serialize()
5. **Логирование** результата в span

### Layer 4: Service Layer - Бизнес-логика

```python
# internal/service/chat/service.py
class ChatService(interface.IChatService):
    def __init__(
        self,
        tel: interface.ITelemetry,
        llm_client: interface.ILLMClient,
        prompt_generator: interface.IPromptGenerator,
        student_repo: interface.IStudentRepo,
        chat_repo: interface.IChatRepo,
    ):
        # Dependency Injection всех зависимостей
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.llm_client = llm_client
        # ...

    async def send_message_to_expert(self, student_id: int, text: str) -> tuple[str, list[common.Command]]:
        with self.tracer.start_as_current_span(
                "ChatService.send_message",
                kind=SpanKind.INTERNAL,
                attributes={"student_id": student_id}
        ) as span:
            try:
                # 1. Получаем контекст студента
                student = (await self.student_repo.get_by_id(student_id))[0]
                
                # 2. Работаем с чатом
                chat = await self._get_or_create_chat(student_id)
                await self.chat_repo.create_message(chat.id, Roles.user, text)
                
                # 3. Выбираем промпт на основе текущего эксперта
                system_prompt = await self._get_prompt_for_expert(student.current_expert, student_id)
                
                # 4. Получаем историю чата
                chat_history = await self.chat_repo.get_messages(chat.id)
                
                # 5. Генерируем ответ через LLM
                llm_response = await self.llm_client.generate(
                    history=chat_history,
                    system_prompt=system_prompt,
                    temperature=0.3
                )
                
                # 6. Парсим ответ и извлекаем команды
                response_data = await self._parse_llm_response(llm_response)
                commands = [Command(**cmd) for cmd in response_data.get("metadata", {}).get("commands", [])]
                
                # 7. Выполняем команды на основе эксперта
                await self._execute_commands_for_expert(student.current_expert, student_id, commands)
                
                span.set_status(StatusCode.OK)
                return response_data["user_message"], commands
                
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err
```

**Структура КАЖДОГО сервисного метода:**
1. **Span с контекстом** для distributed tracing
2. **Валидация входных данных**
3. **Orchestration** - координация между репозиториями
4. **Бизнес-логика** - решения на основе доменных правил
5. **Error handling** с детальным логированием

### Layer 5: Controller Layer - HTTP API

```python
# internal/controller/http/handler/chat/handler.py
class ChatController(interface.IChatController):
    def __init__(self, tel: interface.ITelemetry, chat_service: interface.IChatService):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.chat_service = chat_service

    async def send_message_to_expert(self, body: SendMessageToExpert):
        with self.tracer.start_as_current_span(
                "ChatController.send_message_to_expert",
                kind=SpanKind.INTERNAL,
                attributes={
                    "student_id": body.student_id,
                    "text": body.text
                }
        ) as span:
            try:
                user_message, commands = await self.chat_service.send_message_to_expert(
                    body.student_id,
                    body.text
                )

                response = SendMessageToExpertResponse(
                    user_message=user_message,
                    commands=commands
                )

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=response.to_dict(),
                )
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err
```

**Контроллер ТОЛЬКО:**
- Принимает HTTP запрос
- Валидирует через Pydantic модели
- Вызывает сервис
- Возвращает HTTP ответ
- Никакой бизнес-логики!

---

## 🔌 Dependency Injection - как мы собираем систему

### Bootstrap в main.py

```python
# main.py - Сборка всей системы
def main():
    # 1. Конфигурация
    cfg = Config()
    
    # 2. Инфраструктура (внешние зависимости)
    alert_manager = AlertManager(cfg.alert_tg_bot_token, ...)
    tel = Telemetry(cfg.log_level, cfg.environment, ...)
    db = PG(tel, cfg.db_user, cfg.db_pass, ...)
    storage = Weed(cfg.weed_master_host, cfg.weed_master_port)
    llm_client = GPTClient(tel, cfg.openai_api_key)
    
    # 3. Репозитории (Data Access)
    account_repo = AccountRepo(tel, db)
    student_repo = StudentRepo(tel, db)
    chat_repo = ChatRepo(tel, db)
    topic_repo = TopicRepo(tel, db, storage)
    
    # 4. Сервисы (Business Logic)
    prompt_generator = PromptGenerator(tel, student_repo, topic_repo)
    chat_service = ChatService(tel, llm_client, prompt_generator, student_repo, topic_repo, chat_repo, account_repo)
    
    # 5. Контроллеры (Presentation)
    chat_controller = ChatController(tel, chat_service)
    
    # 6. HTTP приложение
    http_app = NewHTTP(db, chat_controller, ...)
```

**Принцип инъекции зависимостей:**
- **Снизу вверх**: infrastructure → repo → service → controller
- **Через интерфейсы**: каждый слой знает только о контрактах
- **Единая точка сборки**: main.py знает обо всем

---

## 🗄️ Работа с базой данных - реальные примеры

### SQL как код

```python
# internal/repo/edu/student/query.py
create_student = """
INSERT INTO students (
    account_id, 
    current_expert,
    created_at, 
    updated_at
)
VALUES (:account_id, 'registrator', NOW(), NOW())
RETURNING id;
"""

get_student_by_id = """
SELECT 
    id, account_id, current_expert, current_topic, current_block, current_chapter,
    programming_experience, education_background, learning_goals, career_goals, timeline,
    learning_style, lesson_duration, preferred_difficulty, recommended_topics, recommended_blocks,
    approved_topics, approved_blocks, approved_chapters, assessment_score, strong_areas, weak_areas,
    created_at, updated_at
FROM students
WHERE id = :student_id;
"""

update_student_background = """
UPDATE students
SET 
    programming_experience = COALESCE(:programming_experience, programming_experience),
    education_background = COALESCE(:education_background, education_background),
    -- используем COALESCE для optional updates
    updated_at = NOW()
WHERE id = :student_id;
"""
```

**Принципы SQL:**
- **Параметризованные запросы** - защита от SQL injection
- **COALESCE** для optional updates
- **RETURNING** для получения ID после INSERT
- **Explicit column lists** - не используем SELECT *

### JSONB для сложных структур

```python
# Работа с JSONB полями
add_topic_to_approved = """
UPDATE students
SET 
    approved_topics = COALESCE(approved_topics, '{}'::jsonb) || jsonb_build_object(:topic_id::text, :topic_name),
    updated_at = NOW()
WHERE id = :student_id;
"""

# В Python коде
async def update_student_background(self, student_id: int, background: dict):
    args = {
        'student_id': student_id,
        'recommended_topics': json.dumps(background.get('recommended_topics')) if background.get('recommended_topics') else None,
        # Конвертируем dict в JSON строку для PostgreSQL
    }
    await self.db.update(update_student_background, args)
```

### Database schema as code

```python
# internal/model/sql_model.py - Весь DDL в коде
create_queries = [
    """
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
        
        current_expert VARCHAR(50) DEFAULT 'registrator',
        current_topic JSONB DEFAULT '{}'::jsonb,
        current_block JSONB DEFAULT '{}'::jsonb,
        
        programming_experience TEXT,
        education_background TEXT,
        
        recommended_topics JSONB DEFAULT '{}'::jsonb,
        approved_topics JSONB DEFAULT '{}'::jsonb,
        
        assessment_score INTEGER CHECK (assessment_score >= 0 AND assessment_score <= 100),
        strong_areas JSONB DEFAULT '[]'::jsonb,
        
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """,
    # Индексы
    "CREATE INDEX IF NOT EXISTS idx_students_account_id ON students(account_id);",
]
```

---

## 🎭 Observability - как мы видим систему

### Structured Logging

```python
# infrastructure/telemetry/logger.py
class OtelLogger(interface.IOtelLogger):
    def log(self, level: str, message: str, fields: dict = None) -> None:
        # Получаем информацию о файле
        file_info = self._get_caller_info(3)
        attributes = {common.FILE_KEY: file_info}

        # Добавляем extra поля
        if fields:
            attributes.update(self._extract_extra_params(fields))

        # Получаем trace context
        current_span = trace.get_current_span()
        if current_span and current_span.get_span_context().is_valid:
            span_context = current_span.get_span_context()
            trace_id = format(span_context.trace_id, '032x')
            span_id = format(span_context.span_id, '016x')
            
            attributes[common.TRACE_ID_KEY] = trace_id
            attributes[common.SPAN_ID_KEY] = span_id

            # Автоматические алерты при ERROR
            if level == "ERROR" and self.alert_manager:
                self.alert_manager.send_error_alert(trace_id, span_id)

        self.logger.log(log_level, f"{self.service_name} | {message}", extra=attributes)
```

**Каждый лог содержит:**
- Service name
- Trace ID и Span ID
- Файл и строка откуда вызван
- Structured fields
- Автоматические алерты при ошибках

### Distributed Tracing

```python
# Каждая операция в span
async def get_by_id(self, student_id: int) -> list[model.Student]:
    with self.tracer.start_as_current_span(
            "StudentRepo.get_by_id",
            kind=SpanKind.INTERNAL,  # CLIENT для внешних вызовов
            attributes={
                "student_id": student_id,
                "operation": "database.select"
            }
    ) as span:
        try:
            # Business logic
            span.add_event("Executing SQL query", {
                "query": "get_student_by_id",
                "table": "students"
            })
            
            result = await self.db.select(get_student_by_id, args)
            
            span.set_attributes({
                "result.count": len(result),
                "result.found": len(result) > 0
            })
            
            span.set_status(StatusCode.OK)
            return result
        except Exception as err:
            span.record_exception(err)
            span.set_status(StatusCode.ERROR, str(err))
            raise err
```

### Metrics и Alerts

```python
# internal/controller/http/middleware/middleware.py
class HttpMiddleware:
    def metrics_middleware02(self, app: FastAPI):
        # Создаем метрики
        ok_request_counter = self.meter.create_counter(
            name="http.server.ok.request.total",
            description="Total count of successful HTTP requests"
        )
        
        request_duration = self.meter.create_histogram(
            name="http.server.request.duration",
            description="HTTP request duration in seconds"
        )

        @app.middleware("http")
        async def _metrics_middleware(request: Request, call_next):
            start_time = time.time()
            
            # Attributes для группировки метрик
            attrs = {
                "method": request.method,
                "endpoint": request.url.path,
                "trace_id": request.state.trace_id
            }
            
            try:
                response = await call_next(request)
                duration = time.time() - start_time
                
                attrs["status_code"] = response.status_code
                
                # Записываем метрики
                if response.status_code < 400:
                    ok_request_counter.add(1, attributes=attrs)
                else:
                    error_request_counter.add(1, attributes=attrs)
                
                request_duration.record(duration, attributes=attrs)
                
                return response
            except Exception as err:
                # Метрики для ошибок
                error_request_counter.add(1, attributes={**attrs, "error": str(err)})
                raise
```

### Alert Manager

```python
# infrastructure/telemetry/alertmanager.py
class AlertManager:
    async def __send_error_alert_to_tg(self, trace_id: str, span_id: str):
        # Создаем ссылки на Grafana
        log_link = f"{self.grafana_url}/explore?...&trace_id={trace_id}"
        trace_link = f"{self.grafana_url}/explore?...&query={trace_id}"
        
        text = f"""🚨 Ошибка в {self.service_name}
TraceID: {trace_id}
SpanID: {span_id}"""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Логи", url=log_link)],
            [InlineKeyboardButton(text="🔍 Трейс", url=trace_link)]
        ])

        await self.bot.send_message(
            self.alert_tg_chat_id,
            text,
            reply_markup=keyboard
        )
```

---

## 🤖 AI Integration - LLM как часть архитектуры

### LLM Client

```python
# pkg/client/external/openai/client.py
class GPTClient(interface.ILLMClient):
    async def generate(
        self,
        history: list[model.Message],
        system_prompt: str = "",
        temperature: float = 0.5,
        llm_model: str = "gpt-4o-mini",
        base64img: str = None
    ) -> str:
        with self.tracer.start_as_current_span("GPTClient.generate", kind=SpanKind.CLIENT) as span:
            try:
                # Формируем историю для OpenAI
                messages = [
                    {"role": "system", "content": system_prompt},
                    *[{"role": msg.role, "content": msg.text} for msg in history]
                ]
                
                # Добавляем изображение если есть
                if base64img:
                    messages[-1]["content"] = [
                        {"type": "text", "text": messages[-1]["content"]},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64img}"}}
                    ]

                response = await self.client.chat.completions.create(
                    model=llm_model,
                    messages=messages,
                    temperature=temperature,
                )
                
                span.set_attributes({
                    "llm.model": llm_model,
                    "llm.temperature": temperature,
                    "llm.input_tokens": len(str(messages)),
                    "llm.output_tokens": len(response.choices[0].message.content)
                })
                
                return response.choices[0].message.content
            except Exception as err:
                span.record_exception(err)
                raise
```

### Prompt Engineering как код

```python
# internal/service/chat/prompt.py
class PromptGenerator(interface.IPromptGenerator):
    async def get_registrator_prompt(self) -> str:
        formatted_content = await self._format_all_content_metadata()
        
        return f"""
КТО ТЫ:
Ты эксперт по приветствию и регистрации пользователя.

{formatted_content}

ФОРМАТ ОТВЕТОВ:
Ты ДОЛЖЕН возвращать ответ в JSON формате:
```json
{{
    "user_message": "Сообщение для студента",
    "metadata": {{
        "commands": [
            {{
                "description": "Описание действия",
                "name": "register_student", 
                "params": {{"login": "...", "password": "..."}}
            }}
        ]
    }}
}}
```

КОМАНДЫ:
- register_student: {{"login": str, "password": str}}
- switch_to_next_expert: {{"next_expert": str}}

ПОМНИ: Возвращай ТОЛЬКО валидный JSON!
"""

    async def _format_all_content_metadata(self) -> str:
        # Получаем все данные из БД
        topics = await self.topic_repo.get_all_topic()
        blocks = await self.topic_repo.get_all_block()
        chapters = await self.topic_repo.get_all_chapter()
        
        # Форматируем в удобную структуру
        formatter = EducationDataFormatter(topics, blocks, chapters)
        return formatter.to_hierarchical_json()
```

### Command Pattern для LLM Actions

```python
# internal/common/model.py
@dataclass
class Command:
    description: str
    name: str
    params: dict

    def to_dict(self):
        return {
            "name": self.name,
            "params": self.params,
            "description": self.description
        }

# internal/service/chat/service.py
async def _execute_registrator_commands(self, student_id: int, commands: list[Command]):
    for command in commands:
        match command.name:
            case "register_student":
                await self._register_student(**command.params)
            case "login_student":
                await self._login_student(**command.params)
            case "switch_to_next_expert":
                await self._switch_expert(student_id, command.params["next_expert"])
            case _:
                self.logger.warning(f"Unknown command: {command.name}")
```

---

## 🐳 Infrastructure as Code

### Docker Compose Orchestration

```yaml
# docker-compose/app.yaml
services:
    backend:
        build:
            context: "../../ai-mentor-backend"
            dockerfile: ".github/Dockerfile"
        container_name: "${BACKEND_CONTAINER_NAME}"
        env_file:
            - "../env/${ENVIRONMENT}/.env"
            - "../env/${ENVIRONMENT}/.env.app"
            - "../env/${ENVIRONMENT}/.env.db"
            - "../env/${ENVIRONMENT}/.env.monitoring"
        ports:
            - "${BACKEND_PORT}:${BACKEND_PORT}"
        restart: unless-stopped
        networks:
            - net
        depends_on:
            - backend-db
            - redis-monitoring
```

### Environment Management

```python
# internal/config/config.py
class Config:
    # Database
    db_pass: str = os.environ.get('BACKEND_POSTGRES_PASSWORD')
    db_user: str = os.environ.get('BACKEND_POSTGRES_USER')
    db_host: str = os.environ.get('BACKEND_POSTGRES_HOST')
    
    # Monitoring
    otlp_host: str = os.environ.get("OTEL_COLLECTOR_HOST")
    grafana_url: str = os.environ.get('GRAFANA_URL')
    
    # External APIs
    openai_api_key: str = os.environ.get('OPENAI_API_KEY')
```

### Makefile для операций

```makefile
# Makefile
.PHONY: deploy build-all stop-all update-all rebuild-all

set-dev-env:
	@export $(cat env/dev/.env env/dev/.env.app env/dev/.env.db env/dev/.env.monitoring | xargs)

build-all: set-env-to-config-template
	@docker compose -f ./docker-compose/db.yaml up -d --build
	sleep 20
	@docker compose -f ./docker-compose/monitoring.yaml up -d --build
	sleep 20
	@docker compose -f ./docker-compose/app.yaml up -d --build

rebuild-app: update-all set-env-to-config-template
	@docker compose -f ./docker-compose/app.yaml down
	@docker compose -f ./docker-compose/app.yaml up -d --build
```

---

## 🔄 Разработка Flow - TBD в действии

### Git Workflow

```bash
# 1. Синхронизация с main
git checkout main
git pull origin main

# 2. Создание ветки с префиксом типа задачи
git checkout -b feature/TASK-123-add-student-authentication
# или
git checkout -b bugfix/TASK-124-fix-chat-message-encoding
# или  
git checkout -b refactor/TASK-125-optimize-database-queries

# 3. Разработка с частыми коммитами
git add internal/service/auth/
git commit -m "feat(auth): add student JWT authentication

- Implement JWT token generation
- Add password hashing with bcrypt  
- Create authentication middleware
- Add unit tests for auth service

Relates to TASK-123"

# 4. Промежуточные коммиты
git add internal/controller/http/handler/auth/
git commit -m "feat(auth): add HTTP authentication endpoints

- POST /auth/login endpoint
- POST /auth/refresh endpoint  
- GET /auth/verify endpoint
- Add request/response models

Relates to TASK-123"

# 5. Push и PR
git push origin feature/TASK-123-add-student-authentication
# Создаем PR в GitHub
```

### Commit Message Convention

```
<type>(<scope>): <description>

<body>

<footer>
```

**Types:**
- `feat`: новая функциональность
- `fix`: исправление бага
- `refactor`: рефакторинг без изменения API
- `perf`: улучшение производительности
- `test`: добавление тестов
- `docs`: обновление документации
- `chore`: обновление инфраструктуры

**Scopes:** auth, chat, edu, repo, service, controller, infrastructure

### Code Review Checklist

**Обязательные проверки:**
- [ ] Все методы имеют типизацию
- [ ] Добавлены spans для tracing
- [ ] Обработка ошибок с proper logging
- [ ] SQL запросы параметризованы
- [ ] Нет хардкода в коде
- [ ] Добавлены/обновлены тесты
- [ ] Документация обновлена

**Архитектурные проверки:**
- [ ] Dependency injection соблюден
- [ ] Интерфейсы используются правильно
- [ ] Слои не нарушают boundaries
- [ ] Нет circular dependencies

---

## 🧪 Testing Strategy

### Unit Testing

```python
# tests/service/test_chat_service.py
import pytest
from unittest.mock import AsyncMock
from internal.service.chat.service import ChatService
from internal.interface import IChatRepo, IStudentRepo, ILLMClient

@pytest.fixture
def mock_repos():
    return {
        'chat_repo': AsyncMock(spec=IChatRepo),
        'student_repo': AsyncMock(spec=IStudentRepo),
        'llm_client': AsyncMock(spec=ILLMClient),
    }

@pytest.mark.asyncio
async def test_send_message_creates_chat_if_not_exists(mock_repos):
    # Arrange
    mock_repos['chat_repo'].get_chat_by_student_id.return_value = []
    mock_repos['chat_repo'].create_chat.return_value = 1
    
    service = ChatService(**mock_repos)
    
    # Act
    await service.send_message_to_expert(1, "Hello")
    
    # Assert
    mock_repos['chat_repo'].create_chat.assert_called_once_with(1)
```

### Integration Testing

```python
# tests/integration/test_student_repo.py
@pytest.mark.asyncio
async def test_student_repo_full_cycle():
    async with get_test_db() as db:
        repo = StudentRepo(mock_telemetry, db)
        
        # Create
        student_id = await repo.create_student(account_id=1)
        assert student_id > 0
        
        # Read
        students = await repo.get_by_id(student_id)
        assert len(students) == 1
        assert students[0].current_expert == "registrator"
        
        # Update
        await repo.update_student_background(student_id, {
            "programming_experience": "Beginner"
        })
        
        # Verify update
        updated_students = await repo.get_by_id(student_id)
        assert updated_students[0].programming_experience == "Beginner"
```

---

## 🛡️ Security Best Practices

### Input Validation

```python
# internal/controller/http/handler/chat/model.py
class SendMessageToExpert(BaseModel):
    student_id: int = Field(..., gt=0, description="ID студента")
    text: str = Field(..., min_length=1, max_length=5000, description="Текст сообщения")
    
    @validator('text')
    def validate_text(cls, v):
        # Очищаем от лишних пробелов
        v = v.strip()
        if not v:
            raise ValueError('Сообщение не может быть пустым')
        return v
    
    @validator('student_id')
    def validate_student_id(cls, v):
        if v <= 0:
            raise ValueError('Student ID должен быть положительным числом')
        return v
```

### SQL Injection Prevention

```python
# ✅ Правильно - параметризованные запросы
get_student_by_id = """
SELECT id, account_id, current_expert
FROM students
WHERE id = :student_id AND account_id = :account_id;
"""

async def get_student(self, student_id: int, account_id: int):
    params = {
        'student_id': student_id,
        'account_id': account_id
    }
    return await self.db.select(get_student_by_id, params)

# ❌ НИКОГДА не делайте так
query = f"SELECT * FROM students WHERE id = {student_id}"  # SQL Injection!
```

### Sensitive Data Handling

```python
# internal/config/config.py
class Config:
    # ✅ Через environment variables
    openai_api_key: str = os.environ.get('OPENAI_API_KEY')
    db_password: str = os.environ.get('BACKEND_POSTGRES_PASSWORD')
    
    def __repr__(self):
        # ✅ Маскируем секреты в логах
        return f"Config(db_host={self.db_host}, openai_key=***masked***)"

# В логах
self.logger.info("Инициализация LLM клиента", {
    "model": model_name,
    "temperature": temperature,
    # ❌ НЕ логируем API ключи
    # "api_key": self.api_key,  # ОПАСНО!
})
```

---

## 🚀 Performance Optimization

### Database Optimization

```python
# Connection pooling
async_engine = create_async_engine(
    f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}",
    echo=False,
    future=True,
    pool_size=15,        # Размер пула соединений
    max_overflow=15,     # Дополнительные соединения при нагрузке
    pool_recycle=300     # Переиспользование соединений
)

# Оптимизированные запросы
get_student_with_chat = """
SELECT 
    s.id, s.account_id, s.current_expert,
    c.id as chat_id, c.created_at as chat_created
FROM students s
LEFT JOIN chats c ON s.id = c.student_id
WHERE s.id = :student_id;
"""
```

### Async Best Practices

```python
# ✅ Правильно - параллельные запросы
async def get_student_context(self, student_id: int):
    # Запросы выполняются параллельно
    student_task = self.student_repo.get_by_id(student_id)
    chat_task = self.chat_repo.get_chat_by_student_id(student_id)
    topics_task = self.topic_repo.get_all_topic()
    
    student, chat, topics = await asyncio.gather(
        student_task, 
        chat_task, 
        topics_task
    )
    return self._format_context(student, chat, topics)

# ❌ Неправильно - последовательные запросы
async def get_student_context_slow(self, student_id: int):
    student = await self.student_repo.get_by_id(student_id)  # Ждем
    chat = await self.chat_repo.get_chat_by_student_id(student_id)  # Ждем 
    topics = await self.topic_repo.get_all_topic()  # Ждем
    return self._format_context(student, chat, topics)
```

### Caching Strategy

```python
# Redis для кэширования
class StudentService:
    async def get_student_profile(self, student_id: int) -> Student:
        # Проверяем кэш
        cached = await self.redis.get(f"student:profile:{student_id}")
        if cached:
            return Student.model_validate_json(cached)
        
        # Загружаем из БД
        student = await self.student_repo.get_by_id(student_id)
        
        # Кэшируем на 5 минут
        await self.redis.set(
            f"student:profile:{student_id}",
            student.model_dump_json(),
            ttl=300
        )
        
        return student
```

---

## 📊 Monitoring Deep Dive

### Custom Metrics

```python
# internal/service/chat/service.py
class ChatService:
    def __init__(self, tel: ITelemetry, ...):
        self.meter = tel.meter()
        
        # Бизнес-метрики
        self.messages_counter = self.meter.create_counter(
            name="chat.messages.total",
            description="Total messages processed"
        )
        
        self.llm_calls_duration = self.meter.create_histogram(
            name="chat.llm.duration",
            description="LLM call duration in seconds"
        )
        
        self.expert_switches = self.meter.create_counter(
            name="chat.expert.switches",
            description="Expert switches count"
        )

    async def send_message_to_expert(self, student_id: int, text: str):
        # Метрики сообщений
        self.messages_counter.add(1, attributes={
            "student_id": str(student_id),
            "expert": student.current_expert,
            "message_length": len(text)
        })
        
        # Метрики LLM вызовов
        start_time = time.time()
        llm_response = await self.llm_client.generate(...)
        duration = time.time() - start_time
        
        self.llm_calls_duration.record(duration, attributes={
            "model": "gpt-4o-mini",
            "expert": student.current_expert
        })
```

### Health Checks

```python
# internal/controller/http/handler/health.py
class HealthController:
    async def health_check(self):
        checks = {
            "database": await self._check_database(),
            "redis": await self._check_redis(),
            "llm_api": await self._check_llm_api(),
            "file_storage": await self._check_file_storage()
        }
        
        all_healthy = all(checks.values())
        status_code = 200 if all_healthy else 503
        
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "healthy" if all_healthy else "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "checks": checks
            }
        )
    
    async def _check_database(self) -> bool:
        try:
            await self.db.select("SELECT 1", {})
            return True
        except Exception:
            return False
```

---

## 🎯 Advanced Patterns

### Event-Driven Architecture

```python
# internal/common/events.py
@dataclass
class StudentRegisteredEvent:
    student_id: int
    account_id: int
    timestamp: datetime

@dataclass 
class ExpertSwitchedEvent:
    student_id: int
    from_expert: str
    to_expert: str
    timestamp: datetime

# internal/service/chat/service.py
class ChatService:
    async def _switch_expert(self, student_id: int, next_expert: str):
        current_expert = await self._get_current_expert(student_id)
        
        # Обновляем БД
        await self.student_repo.change_current_expert(student_id, next_expert)
        
        # Публикуем событие
        event = ExpertSwitchedEvent(
            student_id=student_id,
            from_expert=current_expert,
            to_expert=next_expert,
            timestamp=datetime.utcnow()
        )
        await self.event_publisher.publish("expert.switched", event)
```

### Circuit Breaker Pattern

```python
# pkg/circuit_breaker.py
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    async def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenException()

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

# Использование
class LLMService:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=30)
    
    async def generate_response(self, prompt: str):
        return await self.circuit_breaker.call(
            self.llm_client.generate,
            prompt=prompt
        )
```

---

## 📋 Checklist для новой функциональности

### 1. Планирование (День 1)
- [ ] Понять бизнес-требования
- [ ] Определить затрагиваемые слои архитектуры  
- [ ] Выбрать паттерны для реализации
- [ ] Спроектировать API контракты
- [ ] Создать задачу в канбан доске

### 2. Database Layer (День 1-2)
- [ ] Обновить `sql_model.py` если нужны новые таблицы
- [ ] Добавить миграции в `create_queries`
- [ ] Создать модели в `internal/model/`
- [ ] Добавить методы сериализации
- [ ] Написать SQL запросы в `query.py`

### 3. Repository Layer (День 2)
- [ ] Создать интерфейс в `internal/interface/`
- [ ] Реализовать Repository с трейсингом
- [ ] Добавить proper error handling
- [ ] Написать unit тесты для Repository
- [ ] Проверить SQL injection защиту

### 4. Service Layer (День 2-3)
- [ ] Создать интерфейс сервиса
- [ ] Реализовать бизнес-логику
- [ ] Добавить валидацию данных
- [ ] Интегрировать с другими сервисами
- [ ] Добавить метрики и логирование
- [ ] Написать unit тесты

### 5. Controller Layer (День 3)
- [ ] Создать Pydantic модели запросов/ответов
- [ ] Реализовать HTTP handler
- [ ] Добавить валидацию входных данных
- [ ] Интегрировать с middleware
- [ ] Написать integration тесты

### 6. Infrastructure (День 4)
- [ ] Обновить `main.py` для DI
- [ ] Добавить конфигурацию если нужно
- [ ] Обновить Docker конфигурацию
- [ ] Добавить мониторинг и алерты
- [ ] Протестировать в Docker окружении

### 7. Documentation & Deploy (День 4-5)
- [ ] Обновить API документацию
- [ ] Добавить примеры использования
- [ ] Создать PR с детальным описанием
- [ ] Пройти code review
- [ ] Задеплоить и проверить мониторинг

---

## 🔍 Debugging Guide

### Локальная отладка

```bash
# 1. Запуск с отладкой
docker-compose -f docker-compose/db.yaml up -d
python main.py http

# 2. Просмотр логов в real-time
docker logs -f backend
docker logs -f grafana

# 3. Подключение к БД
docker exec -it backend-postgres psql -U backend-user -d backend

# 4. Проверка Redis
docker exec -it monitoring-redis redis-cli
> keys *
> get "student:1"
```

### Мониторинг в продакшне

```bash
# Grafana Explore queries
# Логи конкретного trace
{service_name="backend"} | trace_id="0123456789abcdef"

# Ошибки за последний час
{service_name="backend"} | level="ERROR" | __error__=""

# Медленные запросы
{service_name="backend"} | json | http_request_duration > 1.0

# Метрики в VictoriaMetrics
# Количество запросов в секунду
rate(http_server_ok_request_total[1m])

# P95 latency
histogram_quantile(0.95, rate(http_server_request_duration_bucket[5m]))
```

### Common Issues & Solutions

**1. Высокий latency:**
```python
# Добавить профилирование
with self.tracer.start_as_current_span("slow_operation") as span:
    start_time = time.time()
    result = await slow_function()
    duration = time.time() - start_time
    
    span.set_attributes({
        "operation.duration": duration,
        "operation.result_count": len(result)
    })
    
    if duration > 1.0:  # Логируем медленные операции
        self.logger.warning("Slow operation detected", {
            "operation": "slow_function",
            "duration": duration,
            "threshold": 1.0
        })
```

**2. Memory leaks:**
```python
# Проверить закрытие соединений
async def cleanup_resources(self):
    try:
        if self.db_pool:
            await self.db_pool.close()
        if self.redis_client:
            await self.redis_client.close()
    except Exception as e:
        self.logger.error("Error during cleanup", {"error": str(e)})
```

**3. Database deadlocks:**
```python
# Добавить retry логику
async def update_with_retry(self, query: str, params: dict, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return await self.db.update(query, params)
        except asyncpg.DeadlockDetectedError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(0.1 * (2 ** attempt))  # Exponential backoff
```

---

## 🎓 Заключение

Теперь вы знаете **КАК РЕАЛЬНО** устроен код в нашей компании:

### Что вы освоили:
✅ **Архитектуру слоями** - interface → model → repo → service → controller  
✅ **Dependency Injection** - как собираются зависимости в main.py  
✅ **Observability** - трейсинг, метрики, логирование, алерты  
✅ **Database patterns** - Repository, параметризованные запросы, JSONB  
✅ **AI Integration** - LLM как часть архитектуры, Command pattern  
✅ **Infrastructure** - Docker, конфигурация, мониторинг  
✅ **Development Flow** - TBD, канбан, code review  

### Следующие шаги:
1. **Склонируйте** AI-mentor проект
2. **Запустите** через `make build-all`
3. **Изучите** код в порядке: interface → model → repo → service → controller
4. **Возьмите** первую задачу из канбана
5. **Реализуйте** по чеклисту выше

### Помните принципы:
- **Type Safety First** - типизация везде
- **Observability by Design** - каждая операция traced
- **Clean Architecture** - четкие boundaries между слоями
- **Fail Fast** - валидация на входе, обработка ошибок везде
- **Infrastructure as Code** - все в Git, ничего ручного

**Добро пожаловать в команду! 🚀**

---

*Документ обновлен: декабрь 2024*  
*Версия: 2.0*  
*Авторы: Engineering Team*