# 🚀 От нуля до AI-ментора: Полный путь Backend-разработчика

*Изучаем программирование и backend-разработку через создание реального AI-ментора*

---

## Параллельно с лучшим курсом на планете: [Stepik.org "Поколение Python": курс для начинающих](https://stepik.org/course/58852/promo)

---

## Смотрите так же: [Мои другие проекты](https://github.com/mmdev2003?tab=repositories)

---

## 📞 Телеграм: @gommgo

---

## 🎯 О программе

Это комплексная программа для **полных новичков**, которая проведет вас от основ программирования до создания собственного AI-ментора. Каждая теоретическая тема будет сразу же показана на примерах из реального проекта.

### 🌟 Уникальность подхода:
- **Теория + Практика**: Изучили переменные → смотрим их в коде AI-ментора
- **От простого к сложному**: Начинаем с Hello World, заканчиваем микросервисами
- **Реальный проект**: Не учебные примеры, а production-ready система
- **Мгновенная применимость**: Видите, как знания работают в реальности

### 🏆 Результат через 6-8 месяцев:
- **Создадите собственного AI-ментора** с нуля
- **Поймете архитектуру** современных backend-систем
- **Освоите технологический стек**: Python, FastAPI, PostgreSQL, Docker, AI/LLM
- **Готовность к работе** Middle Backend Developer

---

## 📊 Структура обучения

```
🎓 ПОДХОД: Теория → Примеры в коде → Практика → Строим свой AI-ментор
⏱️ ДЛИТЕЛЬНОСТЬ: 24-32 недели (6-8 месяцев)
🔥 ИНТЕНСИВНОСТЬ: 20-25 часов в неделю
💡 ПРИНЦИП: Каждая тема сразу показывается на реальном коде
```

### Прогрессия обучения:

```
Неделя 1: Переменные в Python → Смотрим Config.py в AI-менторе
Неделя 5: Функции → Изучаем функции в сервисах AI-ментора  
Неделя 10: Классы → Анализируем классы репозиториев
Неделя 15: HTTP → Понимаем API эндпоинты
Неделя 20: Базы данных → Разбираем схему AI-ментора
Неделя 25: Финальный проект → Строим своего AI-ментора!
```

---

## 🗺️ Детальная карта обучения

## 🌱 ЭТАП 1: ОСНОВЫ ПРОГРАММИРОВАНИЯ (Недели 1-8)
*Изучаем Python и сразу видим примеры в коде AI-ментора*

### 📅 Неделя 1: Переменные, типы данных, ввод-вывод

**📚 Теория (3 дня):**
- Что такое переменные и зачем они нужны
- Типы данных: int, str, bool, float
- Ввод и вывод данных
- Операторы и выражения

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Смотрим internal/config/config.py
class Config:
    db_pass: str = os.environ.get('BACKEND_POSTGRES_PASSWORD')  ← Строковая переменная
    db_port: str = "5432"                                       ← Константа
    http_port: int = int(os.environ.get('BACKEND_PORT'))       ← Число
    
# Находим переменные в internal/common/const.py
class Roles:
    user = "user"           ← Строковые константы
    assistant = "assistant"
    system = "system"
```

**🛠️ Практические задания (2 дня):**
1. Создать свой файл config.py с настройками
2. Написать программу для ввода данных студента
3. Создать калькулятор оценок

### 📅 Неделя 2: Условия и логика

**📚 Теория (3 дня):**
- Условные операторы if, elif, else
- Логические операторы and, or, not
- Сравнения и булева логика

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Смотрим internal/service/chat/service.py
if student.current_expert == common.Experts.registrator:
    system_prompt = await self.prompt_generator.get_registrator_prompt()

if student.current_expert == common.Experts.interview:
    system_prompt = await self.prompt_generator.get_interview_expert_prompt(student_id)

# Анализируем логику в internal/controller/http/middlerware/middleware.py
if status_code >= 500:
    err = Exception("Internal server error")
    # обработка серверных ошибок
elif status_code >= 400:
    err = Exception("Client error")  
    # обработка клиентских ошибок
else:
    span.set_status(Status(StatusCode.OK))
```

**🛠️ Практические задания (2 дня):**
1. Создать систему определения уровня студента
2. Написать валидатор данных пользователя
3. Сделать простого чат-бота с условиями

### 📅 Неделя 3: Циклы и итерации

**📚 Теория (3 дня):**
- Цикл for и его применение
- Цикл while и условия выхода
- Операторы break и continue
- Вложенные циклы

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Смотрим internal/service/chat/service.py
for command in commands:  ← Цикл по командам
    command_name = command.name
    params = command.params
    
    if command_name == "update_student_background":
        await self._update_student_background(student_id, background)

# Анализируем internal/model/sql_model.py  
create_queries = [
    "CREATE TABLE IF NOT EXISTS accounts (...)",
    "CREATE TABLE IF NOT EXISTS students (...)",
    # ... много запросов
]

# В main.py видим, как выполняются все запросы
await db.multi_query(model.create_queries)  ← Цикл внутри функции
```

**🛠️ Практические задания (2 дня):**
1. Создать систему обработки множественных команд
2. Написать генератор SQL-запросов в цикле
3. Сделать обработчик списка студентов

### 📅 Неделя 4: Списки, словари, множества

**📚 Теория (3 дня):**
- Работа со списками: добавление, удаление, поиск
- Словари: ключи, значения, методы
- Множества и их операции
- Comprehensions

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Смотрим internal/model/edu/student.py
@dataclass
class Student:
    # Словари для хранения данных
    current_topic: dict[int, str] = None           ← Словарь {id: name}
    approved_topics: dict[int, str] = field(default_factory=dict)
    strong_areas: list[str] = field(default_factory=list)  ← Список строк
    
# Анализируем internal/service/chat/service.py
commands = [common.Command(**command) for command in   ← List comprehension!
           response_data.get("metadata", {}).get("commands", [])]

# Смотрим работу со словарями в internal/repo/edu/student/repo.py
args = {
    'student_id': student_id,
    'programming_experience': background.get('programming_experience'),
    'education_background': background.get('education_background'),
    # ... словарь параметров
}
```

**🛠️ Практические задания (2 дня):**
1. Создать систему управления студентами через словари
2. Написать парсер команд с использованием списков
3. Сделать систему тегов через множества

### 📅 Неделя 5-6: Функции и модули

**📚 Теория (4 дня):**
- Определение и вызов функций
- Параметры и аргументы
- Возвращаемые значения
- Область видимости переменных
- Импорт модулей и пакетов
- Создание собственных модулей

**🔍 Примеры в коде AI-ментора (4 дня):**
```python
# Изучаем функции в internal/service/chat/service.py
async def send_message_to_expert(self, student_id: int, text: str) -> tuple[str, list[common.Command]]:
    """Обработка сообщений для эксперта"""  ← Документация функции
    # ... логика функции
    return user_message, commands  ← Возврат нескольких значений

# Смотрим приватные методы (инкапсуляция)
async def _parse_llm_response(self, response: str) -> dict:  ← Приватный метод
    try:
        # парсинг ответа
        parsed = json.loads(response)
        return parsed
    except json.JSONDecodeError as e:  ← Обработка ошибок
        # логирование ошибки
        
# Анализируем импорты в начале файлов
from internal import interface, common  ← Импорт внутренних модулей
from opentelemetry.trace import StatusCode, SpanKind  ← Внешние библиотеки
```

**🛠️ Практические задания (4 дня):**
1. Выделить общие функции в отдельный модуль
2. Создать систему валидации с функциями
3. Написать модуль для работы с конфигурацией
4. Сделать утилиты для обработки данных

### 📅 Неделя 7-8: Классы и объектно-ориентированное программирование

**📚 Теория (4 дня):**
- Классы и объекты
- Конструкторы и методы
- Наследование и полиморфизм
- Инкапсуляция и сокрытие данных
- Специальные методы (__init__, __str__ и др.)

**🔍 Примеры в коде AI-ментора (4 дня):**
```python
# Изучаем класс в infrastructure/pg/pg.py
class PG(interface.IDB):  ← Наследование от интерфейса
    def __init__(self, tel: interface.ITelemetry, db_user, db_pass, db_host, db_port, db_name):
        self.pool = NewPool(db_user, db_pass, db_host, db_port, db_name)  ← Конструктор
        self.tracer = tel.tracer()
    
    async def insert(self, query: str, query_params: dict) -> int:  ← Метод класса
        # реализация вставки данных

# Анализируем dataclass в internal/model/edu/student.py
@dataclass  ← Декоратор для автогенерации методов
class Student:
    id: int
    account_id: int
    # ... поля класса
    
    @classmethod  ← Метод класса
    def serialize(cls, rows) -> list['Student']:
        return [cls(id=row.id, account_id=row.account_id, ...) for row in rows]

# Смотрим наследование в internal/service/chat/service.py  
class ChatService(interface.IChatService):  ← Реализует интерфейс
    def __init__(self, tel, llm_client, prompt_generator, ...):  ← Dependency Injection
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        # инициализация зависимостей
```

**🛠️ Практические задания (4 дня):**
1. Создать класс Student с методами управления
2. Написать систему логирования как класс
3. Сделать базовый класс для всех сервисов
4. Создать класс для валидации данных

---

## ⚙️ ЭТАП 2: ВЕБ-РАЗРАБОТКА И API (Недели 9-16)
*Изучаем веб-технологии через HTTP API AI-ментора*

### 📅 Неделя 9-10: HTTP и основы веб-разработки

**📚 Теория (4 дня):**
- Что такое HTTP протокол
- Методы запросов: GET, POST, PUT, DELETE
- Статус коды ответов
- Заголовки HTTP
- JSON формат данных

**🔍 Примеры в коде AI-ментора (4 дня):**
```python
# Изучаем HTTP обработчики в internal/app/http/app.py
def include_chat_handlers(app: FastAPI, chat_controller: interface.IChatController, prefix: str):
    app.add_api_route(
        prefix + "/chat/message/send",           ← URL эндпоинт
        chat_controller.send_message_to_expert,  ← Обработчик
        methods=["POST"],                        ← HTTP метод
        summary="Отправить сообщение регистратору",
        description="Отправляет сообщение регистратору"
    )

# Смотрим контроллер в internal/controller/http/handler/chat/handler.py
async def send_message_to_expert(self, body: SendMessageToExpert):
    # ... обработка запроса
    return JSONResponse(
        status_code=status.HTTP_200_OK,  ← HTTP статус код
        content=response.to_dict(),      ← JSON ответ
    )

# Анализируем модели запросов internal/controller/http/handler/chat/model.py
class SendMessageToExpert(BaseModel):  ← Pydantic модель для валидации
    student_id: int
    text: str
```

**🛠️ Практические задания (4 дня):**
1. Создать простой HTTP сервер
2. Написать эндпоинты для работы со студентами  
3. Сделать валидацию JSON запросов
4. Добавить обработку ошибок HTTP

### 📅 Неделя 11-12: FastAPI и создание REST API

**📚 Теория (4 дня):**
- Что такое REST архитектура
- Фреймворк FastAPI
- Роутинг и middleware
- Валидация данных с Pydantic
- Документация API

**🔍 Примеры в коде AI-ментора (4 дня):**
```python
# Изучаем создание приложения в internal/app/http/app.py
def NewHTTP(db, chat_controller, edu_student_controller, ...):
    app = FastAPI()  ← Создание FastAPI приложения
    include_middleware(app, http_middleware)  ← Подключение middleware
    
    # Подключение различных обработчиков
    include_chat_handlers(app, chat_controller, prefix)
    include_edu_student_handlers(app, edu_student_controller, prefix)
    return app

# Анализируем middleware в internal/controller/http/middlerware/middleware.py
@app.middleware("http")  ← Декоратор middleware
async def _trace_middleware01(request: Request, call_next: Callable):
    # обработка трейсов
    response = await call_next(request)
    # постобработка

# Смотрим контроллеры в internal/controller/http/handler/edu/student/handler.py
async def get_by_id(self, student_id: int):  ← Типизированные параметры
    student = await self.student_service.get_by_id(student_id)
    response = StudentResponse(...)  ← Pydantic модель ответа
    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())
```

**🛠️ Практические задания (4 дня):**
1. Создать FastAPI приложение с роутами
2. Добавить middleware для логирования
3. Написать CRUD операции для студентов
4. Сделать автодокументацию API

### 📅 Неделя 13: Асинхронное программирование

**📚 Теория (3 дня):**
- Что такое async/await
- Корутины и Event Loop
- Конкурентность vs параллелизм
- Работа с async библиотеками

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Изучаем async функции в internal/service/chat/service.py
async def send_message_to_expert(self, student_id: int, text: str):  ← async функция
    student = (await self.student_repo.get_by_id(student_id))[0]  ← await вызов
    
    chat = await self.chat_repo.get_chat_by_student_id(student_id)  ← Асинхронная БД
    
    # Получаем ответ от LLM асинхронно
    llm_response = await self.llm_client.generate(
        history=chat_history,
        system_prompt=system_prompt
    )

# Смотрим работу с БД в infrastructure/pg/pg.py
async def insert(self, query: str, query_params: dict) -> int:
    async with self.pool() as session:  ← Асинхронный контекст
        result = await session.execute(text(query), query_params)  ← await
        await session.commit()
```

**🛠️ Практические задания (2 дня):**
1. Переписать синхронный код в асинхронный
2. Создать параллельную обработку запросов
3. Добавить асинхронное логирование

### 📅 Неделя 14-15: Базы данных и ORM

**📚 Теория (4 дня):**
- SQL основы: SELECT, INSERT, UPDATE, DELETE
- Реляционные базы данных
- Индексы и оптимизация
- SQLAlchemy и работа с ORM
- Миграции БД

**🔍 Примеры в коде AI-ментора (3 дня):**
```python
# Изучаем SQL схемы в internal/model/sql_model.py
create_queries = [
    """
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,                    ← Первичный ключ
        account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,  ← Внешний ключ
        current_expert VARCHAR(50) DEFAULT 'registrator',
        approved_topics JSONB DEFAULT '{}'::jsonb,  ← JSONB для сложных данных
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """,
]

# Анализируем запросы в internal/repo/edu/student/query.py
get_student_by_id = """
SELECT 
    id, account_id, current_expert, current_topic, current_block,
    programming_experience, education_background, learning_goals
FROM students
WHERE id = :student_id;  ← Параметризованный запрос
"""

# Смотрим работу с БД в internal/repo/edu/student/repo.py
async def get_by_id(self, student_id: int) -> list[model.Student]:
    args = {'student_id': student_id}
    rows = await self.db.select(get_student_by_id, args)  ← Выполнение запроса
    result = model.Student.serialize(rows) if rows else []  ← Сериализация
```

**🛠️ Практические задания (3 дня):**
1. Создать схему БД для системы курсов
2. Написать CRUD операции с параметризованными запросами
3. Добавить индексы для оптимизации
4. Сделать миграции БД

### 📅 Неделя 16: Архитектура и паттерны

**📚 Теория (3 дня):**
- Clean Architecture принципы
- Repository Pattern
- Dependency Injection
- Interface Segregation
- Separation of Concerns

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Изучаем интерфейсы в internal/interface/chat/chat.py
class IChatService(Protocol):  ← Интерфейс сервиса
    async def send_message_to_expert(self, student_id: int, text: str): pass

class IChatRepo(Protocol):  ← Интерфейс репозитория
    async def create_chat(self, student_id: int) -> int: pass
    async def get_messages(self, chat_id: int) -> list[model.Message]: pass

# Анализируем Dependency Injection в main.py
# Создаем зависимости снизу вверх
db = PG(tel, cfg.db_user, cfg.db_pass, ...)      ← Инфраструктура
chat_repo = ChatRepo(tel, db)                     ← Репозиторий
chat_service = ChatService(tel, llm_client, ..., chat_repo)  ← Сервис
chat_controller = ChatController(tel, chat_service)          ← Контроллер

# Смотрим слои в internal/service/chat/service.py
class ChatService(interface.IChatService):  ← Реализует интерфейс
    def __init__(self, tel, llm_client, prompt_generator, student_repo, ...):
        # Все зависимости инжектятся через конструктор
```

**🛠️ Практические задания (2 дня):**
1. Выделить интерфейсы для всех компонентов
2. Создать слоистую архитектуру
3. Настроить DI контейнер

---

## 🤖 ЭТАП 3: AI И LLM ИНТЕГРАЦИЯ (Недели 17-20)
*Изучаем работу с искусственным интеллектом*

### 📅 Неделя 17: Основы работы с LLM

**📚 Теория (3 дня):**
- Что такое LLM (Large Language Models)
- OpenAI API и GPT модели
- Промпт инжиниринг
- Токены и ограничения
- Обработка ответов AI

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Изучаем LLM клиент в pkg/client/external/openai/client.py
class GPTClient(interface.ILLMClient):
    async def generate(self, history: list[model.Message], system_prompt: str = "", 
                      temperature: float = 0.5, llm_model: str = "gpt-4o-mini"):
        # Подготовка сообщений для OpenAI
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history:
            messages.append({"role": msg.role, "content": msg.text})
        
        # Вызов OpenAI API
        response = await self.client.chat.completions.create(
            model=llm_model,
            messages=messages,
            temperature=temperature
        )

# Анализируем промпты в internal/service/chat/prompt.py
async def get_registrator_prompt(self) -> str:
    prompt = f"""
КТО ТЫ:
Ты эксперт по приветствию и регистрации пользователя.

ФОРМАТ ТВОИХ ОТВЕТОВ:
Ты должен возвращать ответ в специальном JSON формате:
{{
    "user_message": "сообщение для студента",
    "metadata": {{ "commands": [...] }}
}}
"""
```

**🛠️ Практические задания (2 дня):**
1. Создать простого чат-бота с OpenAI
2. Написать систему промптов для разных задач
3. Добавить обработку ошибок API

### 📅 Неделя 18: Система AI-агентов

**📚 Теория (3 дня):**
- Концепция AI-агентов
- Система ролей и экспертов
- Переключение контекстов
- Управление состоянием диалога

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Изучаем экспертов в internal/common/const.py
class Experts:
    registrator = "registrator"  ← Эксперт по регистрации
    interview = "interview"      ← Эксперт по интервью  
    teacher = "teacher"          ← Преподаватель
    test = "test"               ← Эксперт по тестированию

# Анализируем переключение экспертов в internal/service/chat/service.py
if student.current_expert == common.Experts.registrator:
    system_prompt = await self.prompt_generator.get_registrator_prompt()
if student.current_expert == common.Experts.interview:
    system_prompt = await self.prompt_generator.get_interview_expert_prompt(student_id)

# Смотрим команды AI в internal/common/model.py
@dataclass
class Command:
    description: str  ← Описание действия
    name: str        ← Имя команды
    params: dict     ← Параметры выполнения
```

**🛠️ Практические задания (2 дня):**
1. Создать систему AI-агентов для разных задач
2. Написать менеджер переключения контекстов
3. Добавить систему команд

### 📅 Неделя 19: Обработка команд и интеграция

**📚 Теория (3 дня):**
- Парсинг JSON ответов от AI
- Валидация команд
- Выполнение системных действий
- Error handling в AI системах

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Изучаем парсинг ответов в internal/service/chat/service.py
async def _parse_llm_response(self, response: str) -> dict:
    try:
        # Убираем markdown форматирование
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
            
        parsed = json.loads(response)
        
        # Проверяем обязательные поля
        if "user_message" not in parsed:
            return {"user_message": "Ошибка обработки", "metadata": {"commands": []}}
            
    except json.JSONDecodeError as e:
        self.logger.error(f"Ошибка парсинга JSON: {e}")

# Анализируем выполнение команд
async def _execute_registrator_commands(self, student_id: int, commands: list[common.Command]):
    for command in commands:
        if command.name == "register_student":
            await self._register_student(**command.params)
        elif command.name == "switch_to_next_expert":
            await self._switch_expert(student_id, command.params.get("next_expert"))
```

**🛠️ Практические задания (2 дня):**
1. Создать валидатор AI команд
2. Написать систему выполнения действий
3. Добавить логирование AI взаимодействий

### 📅 Неделя 20: Контекст и память системы

**📚 Теория (3 дня):**
- Управление контекстом диалога
- Сохранение истории
- Персонализация на основе данных
- Оптимизация токенов

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Изучаем управление контекстом в internal/service/chat/prompt.py
async def _format_student_context(self, student_id: int) -> str:
    students = await self.student_repo.get_by_id(student_id)
    student = students[0] if students else None
    
    return f"""ПРОФИЛЬ СТУДЕНТА:
- Опыт программирования: {student.programming_experience}
- Цели обучения: {student.learning_goals}
- Пройденные темы: {student.approved_topics}
- Сильные стороны: {student.strong_areas}
"""

# Анализируем сохранение истории в internal/repo/chat/repo.py
async def create_message(self, chat_id: int, role: str, text: str):
    args = {'chat_id': chat_id, 'role': role, 'text': text}
    message_id = await self.db.insert(create_message, args)

async def get_messages(self, chat_id: int) -> list[model.Message]:
    rows = await self.db.select(get_messages_by_chat_id, {'chat_id': chat_id})
    return model.Message.serialize(rows) if rows else []
```

**🛠️ Практические задания (2 дня):**
1. Создать систему управления контекстом
2. Написать персонализацию промптов
3. Оптимизировать использование токенов

---

## 🚀 ЭТАП 4: DEVOPS И РАЗВЕРТЫВАНИЕ (Недели 21-24)
*Изучаем современную инфраструктуру через проект*

### 📅 Неделя 21: Docker и контейнеризация

**📚 Теория (3 дня):**
- Что такое контейнеризация
- Docker образы и контейнеры
- Dockerfile best practices
- Docker Compose для multi-container

**🔍 Примеры в коде AI-ментора (2 дня):**
```dockerfile
# Изучаем Dockerfile в .github/Dockerfile
FROM python:3.12          ← Базовый образ

WORKDIR /root             ← Рабочая директория
COPY . .                  ← Копирование кода

RUN cd .github && pip install -r requirements.txt  ← Установка зависимостей
CMD python3 main.py http  ← Команда запуска
```

```yaml
# Анализируем docker-compose/app.yaml
services:
    backend:
        build:
            context: "../../ai-mentor-${BACKEND_CONTAINER_NAME}"
            dockerfile: ".github/Dockerfile"
        container_name: "${BACKEND_CONTAINER_NAME}"
        env_file:                    ← Файлы переменных окружения
            - "../env/${ENVIRONMENT}/.env"
        ports:
            - "${BACKEND_PORT}:${BACKEND_PORT}"  ← Проброс портов
        networks:
            - net                    ← Сеть контейнеров
```

**🛠️ Практические задания (2 дня):**
1. Создать Dockerfile для своего приложения
2. Настроить Docker Compose с БД
3. Оптимизировать размер образов

### 📅 Неделя 22: Мониторинг и логирование

**📚 Теория (3 дня):**
- Observability: логи, метрики, трейсы
- OpenTelemetry стандарт
- Structured logging
- Алертинг и уведомления

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Изучаем телеметрию в infrastructure/telemetry/telemetry.py
class Telemetry(interface.ITelemetry):
    def _setup_tracing(self, resource: Resource) -> None:
        otlp_exporter = OTLPSpanExporter(
            endpoint=f"http://{self.otlp_endpoint}",  ← Экспорт трейсов
            insecure=True
        )
        
        self._tracer_provider = TracerProvider(resource=resource, sampler=ALWAYS_ON)

# Анализируем структурированное логирование в infrastructure/telemetry/logger.py
def log(self, level: str, message: str, fields: dict = None) -> None:
    current_span = trace.get_current_span()
    if current_span and current_span.get_span_context().is_valid:
        trace_id = format(span_context.trace_id, '032x')  ← Trace ID
        attributes[common.TRACE_ID_KEY] = trace_id

# Смотрим алертинг в infrastructure/telemetry/alertmanger.py
async def __send_error_alert_to_tg(self, trace_id: str, span_id: str):
    log_link = f"{self.grafana_url}/explore?..."  ← Ссылка на логи
    trace_link = f"{self.grafana_url}/explore?..."  ← Ссылка на трейс
```

**🛠️ Практические задания (2 дня):**
1. Настроить логирование с трейсами
2. Создать дашборды в Grafana
3. Настроить алерты в Telegram

### 📅 Неделя 23: Конфигурация и переменные окружения

**📚 Теория (3 дня):**
- 12-Factor App принципы
- Environment variables
- Конфигурация для разных окружений
- Секреты и безопасность

**🔍 Примеры в коде AI-ментора (2 дня):**
```python
# Изучаем конфигурацию в internal/config/config.py
class Config:
    # База данных
    db_pass: str = os.environ.get('BACKEND_POSTGRES_PASSWORD')
    db_user: str = os.environ.get('BACKEND_POSTGRES_USER')
    
    # API ключи
    openai_api_key: str = os.environ.get('OPEN_AI_API_KEY')
    
    # Алерты
    alert_tg_bot_token: str = os.environ.get('ALERT_TG_BOT_TOKEN')
```

```bash
# Анализируем env/dev/.env.app
BACKEND_CONTAINER_NAME=backend
BACKEND_PORT=8000
BACKEND_PREFIX=/api/ai-mentor

FRONTEND_CONTAINER_NAME=frontend  
FRONTEND_PORT=3000
```

**🛠️ Практические задания (2 дня):**
1. Создать конфигурацию для dev/prod
2. Настроить безопасное хранение секретов
3. Добавить валидацию конфигурации

### 📅 Неделя 24: Развертывание и CI/CD

**📚 Теория (3 дня):**
- Автоматизация развертывания
- Makefile и скрипты
- Мониторинг инфраструктуры
- Backup и восстановление

**🔍 Примеры в коде AI-ментора (2 дня):**
```makefile
# Изучаем Makefile
build-all: set-env-to-config-template
	@docker compose -f ./docker-compose/db.yaml up -d --build
	sleep 20
	@docker compose -f ./docker-compose/monitoring.yaml up -d --build  
	sleep 20
	@docker compose -f ./docker-compose/app.yaml up -d --build

rebuild-all: update-all build-all  ← Обновление и пересборка

update-all:
	@git pull
	@cd ../ai-mentor-backend/ && git pull
	@cd ../ai-mentor-frontend/ && git pull
```

```bash
# Анализируем установочные скрипты infrastructure/docker/install.sh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
apt install docker-ce docker-ce-cli containerd.io -y  ← Установка Docker
```

**🛠️ Практические задания (2 дня):**
1. Создать автоматизированное развертывание
2. Настроить мониторинг инфраструктуры
3. Сделать бэкап системы

---

## 🎓 ЭТАП 5: ФИНАЛЬНЫЙ ПРОЕКТ (Недели 25-32)
*Создаем собственного AI-ментора с нуля!*

### 📅 Неделя 25-26: Планирование и архитектура

**🎯 Цель:** Спроектировать архитектуру собственного AI-ментора

**📋 Задачи:**
1. **Анализ требований**
   - Определить функциональность системы
   - Выбрать технологический стек
   - Спланировать API эндпоинты

2. **Проектирование архитектуры**
   - Нарисовать диаграммы компонентов
   - Спроектировать схему БД
   - Определить интерфейсы и зависимости

3. **Настройка проекта**
   - Создать структуру каталогов
   - Настроить Docker окружение
   - Подготовить CI/CD pipeline

### 📅 Неделя 27-28: Backend и API

**🎯 Цель:** Создать backend с REST API

**📋 Задачи:**
1. **Инфраструктурный слой**
   ```python
   # Создаем свои версии компонентов
   infrastructure/
   ├── database/db.py      ← Подключение к PostgreSQL
   ├── cache/redis.py      ← Кэширование
   ├── storage/files.py    ← Файловое хранилище
   └── telemetry/          ← Мониторинг
   ```

2. **Бизнес-логика**
   ```python
   internal/
   ├── interface/          ← Определяем интерфейсы
   ├── model/             ← Доменные модели
   ├── repo/              ← Репозитории данных
   ├── service/           ← Бизнес-логика
   └── controller/        ← HTTP контроллеры
   ```

3. **HTTP API**
   - Создать FastAPI приложение
   - Добавить middleware
   - Настроить валидацию

### 📅 Неделя 29-30: AI интеграция

**🎯 Цель:** Интегрировать LLM и создать систему AI-агентов

**📋 Задачи:**
1. **LLM клиент**
   - Подключить OpenAI API
   - Создать систему промптов
   - Добавить обработку ошибок

2. **AI-агенты**
   - Создать экспертов для разных задач
   - Настроить переключение контекстов
   - Добавить систему команд

3. **Персонализация**
   - Создать профили пользователей
   - Добавить адаптивные промпты
   - Настроить сохранение контекста

### 📅 Неделя 31: DevOps и развертывание

**🎯 Цель:** Развернуть систему в production

**📋 Задачи:**
1. **Контейнеризация**
   - Создать Dockerfile
   - Настроить Docker Compose
   - Оптимизировать образы

2. **Мониторинг**
   - Настроить логирование
   - Добавить метрики
   - Создать дашборды

3. **Развертывание**
   - Настроить сервер
   - Автоматизировать деплой
   - Настроить домен и SSL

### 📅 Неделя 32: Тестирование и документация

**🎯 Цель:** Завершить проект и подготовить к демонстрации

**📋 Задачи:**
1. **Тестирование**
   - Unit тесты для всех компонентов
   - Integration тесты API
   - Load testing системы

2. **Документация**
   - API документация
   - Архитектурная документация
   - Руководство по развертыванию

3. **Демонстрация**
   - Презентация проекта
   - Live demo системы
   - Анализ полученного опыта

---

## 🏆 Результат обучения

### 💼 Что вы будете уметь:

**🔧 Технические навыки:**
- Программирование на Python (продвинутый уровень)
- Создание REST API с FastAPI
- Работа с PostgreSQL и SQL
- Асинхронное программирование
- Docker и контейнеризация
- Системы мониторинга и логирования

**🤖 AI/ML навыки:**
- Интеграция с LLM (GPT, Claude и др.)
- Промпт инжиниринг
- Создание AI-агентов
- Обработка natural language

**🏗️ Архитектурные навыки:**
- Clean Architecture
- Микросервисная архитектура
- Design patterns
- Dependency Injection
- SOLID принципы

**⚙️ DevOps навыки:**
- CI/CD pipelines
- Infrastructure as Code
- Мониторинг и алертинг
- Развертывание и масштабирование

### 🎯 Карьерные перспективы:

```
После программы вы готовы к позициям:
├── Middle Backend Developer     (200-350k ₽)
├── Senior Python Developer     (300-500k ₽) 
├── AI/ML Engineer              (350-600k ₽)
├── Solutions Architect         (500-800k ₽)
└── Tech Lead                   (600k+ ₽)
```

### 📁 Портфолио проекты:

1. **Собственный AI-ментор** - флагманский проект
2. **REST API сервисы** - различные бизнес-логики
3. **Микросервисная архитектура** - distributed systems
4. **DevOps pipeline** - полная автоматизация
5. **Мониторинг система** - observability stack

---

## 🚀 Начинаем путешествие!

### ✅ Что нужно для старта:

**💻 Технические требования:**
- Компьютер с 8+ ГБ RAM
- Стабильный интернет
- Возможность установки Docker

**🧠 Личные качества:**
- Мотивация изучать новое
- Готовность тратить 20-25 часов в неделю
- Английский язык для чтения документации

**📚 Подготовка:**
1. Установите Python 3.11+
2. Настройте IDE (VS Code или PyCharm)
3. Создайте аккаунт на GitHub
4. Зарегистрируйтесь в OpenAI для API

### 🎯 Ваш первый шаг:

**СЕГОДНЯ** начинайте с недели 1 - изучения переменных в Python. Напишите свой первый "Hello World", а затем найдите переменные в коде AI-ментора. 

**Помните:** каждая строчка кода, которую вы изучите в AI-менторе, приближает вас к созданию собственной AI-системы!

---

## 📞 Поддержка и сообщество

- **Менторская поддержка**: Персональная помощь на сложных этапах
- **Code review**: Проверка вашего кода экспертами
- **Сообщество**: Telegram чат для обмена опытом
- **Еженедельные созвоны**: Разбор сложных вопросов

---

**🎉 Добро пожаловать в захватывающий мир создания AI-систем! Ваш путь от новичка до создателя собственного AI-ментора начинается прямо сейчас! 🤖**

*От переменных Python до production AI-системы - каждый шаг приближает вас к будущему технологий!*