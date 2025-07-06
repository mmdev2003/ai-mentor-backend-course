# БЛОК 1: ОСНОВЫ И КОНЦЕПЦИИ
## От новичка до понимания фундаментальных принципов

---

```
🎯 ЦЕЛЬ БЛОКА: Понимание фундаментальных принципов асинхронного обмена сообщениями
⏱️ ПРОДОЛЖИТЕЛЬНОСТЬ: 3-4 недели
📚 ФОРМАТ: Теория + практические задания + анализ кейсов
```

---

# 📖 ГЛАВА 1.1: ВВЕДЕНИЕ В БРОКЕРЫ СООБЩЕНИЙ
## ⏱️ Время изучения: 1 неделя

---

### 🔄 История развития messaging систем

```
ЭВОЛЮЦИЯ ОБМЕНА СООБЩЕНИЯМИ:

1960s-1970s    │ Mainframe batch processing
               │ ──────────────────────────────
               │ ● Файловый обмен данными
               │ ● Batch jobs
               │ ● Централизованная обработка

1980s-1990s    │ Client-Server архитектура  
               │ ──────────────────────────────
               │ ● Прямые соединения
               │ ● RPC (Remote Procedure Calls)
               │ ● Tight coupling проблемы

2000s          │ Message-Oriented Middleware
               │ ──────────────────────────────
               │ ● JMS (Java Message Service)
               │ ● MSMQ, IBM MQ
               │ ● Стандартизация messaging

2010s-2020s    │ Distributed Streaming
               │ ──────────────────────────────
               │ ● Apache Kafka
               │ ● Cloud messaging
               │ ● Event-driven архитектуры
```

### ⚠️ Проблемы tight coupling в распределенных системах

#### БЕЗ БРОКЕРА СООБЩЕНИЙ:
```
Service A ──────────────► Service B
    │                        │
    ├──────────────► Service C
    │                        │
    └──────────────► Service D

❌ ПРОБЛЕМЫ:
├─ Прямые зависимости между сервисами
├─ Изменения в Service B влияют на Service A
├─ Сложность добавления новых сервисов
├─ Проблемы с масштабированием
└─ Отсутствие fault tolerance
```

#### С БРОКЕРОМ СООБЩЕНИЙ:
```
Service A ───┐
Service B ───┼──► MESSAGE BROKER ──┬──► Service X
Service C ───┘                     ├──► Service Y  
                                   └──► Service Z

✅ ПРЕИМУЩЕСТВА:
├─ Loose coupling между сервисами
├─ Независимое развитие и деплой
├─ Легкое добавление новых consumers
├─ Горизонтальное масштабирование
└─ Fault tolerance и resilience
```

### 🛠️ Как брокеры решают проблемы интеграции

```
ОСНОВНЫЕ ФУНКЦИИ MESSAGE BROKER:

┌─────────────────────────────────────────────────────┐
│                 MESSAGE BROKER                      │
├─────────────────────────────────────────────────────┤
│  🔄 ROUTING      │ Маршрутизация сообщений           │
│  📦 BUFFERING    │ Буферизация при пиковых нагрузках │
│  🔒 PERSISTENCE  │ Надежное хранение сообщений       │
│  ⚡ DELIVERY     │ Гарантии доставки                 │
│  🏗️ TRANSFORMATION │ Преобразование форматов        │
│  📊 MONITORING   │ Мониторинг и метрики              │
└─────────────────────────────────────────────────────┘
```

---

# 📋 ГЛАВА 1.2: ПАТТЕРНЫ ОБМЕНА СООБЩЕНИЯМИ
## ⏱️ Время изучения: 1 неделя

---

### 🎯 Point-to-Point (Очереди)

```
POINT-TO-POINT PATTERN:

Producer ───► [QUEUE] ───► Consumer
                │
                ├─ Один producer, один consumer
                ├─ Сообщение потребляется только один раз
                ├─ FIFO порядок обработки
                └─ Load balancing между consumers

АРХИТЕКТУРА:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Producer A  │───►│    QUEUE    │───►│ Consumer 1  │
├─────────────┤    │             │    ├─────────────┤
│ Producer B  │───►│ ┌─────────┐ │    │ Consumer 2  │
└─────────────┘    │ │ Msg 1   │ │    ├─────────────┤
                   │ │ Msg 2   │ │───►│ Consumer 3  │
                   │ │ Msg 3   │ │    │ (Competing) │
                   │ └─────────┘ │    └─────────────┘
                   └─────────────┘

✅ ИСПОЛЬЗОВАНИЕ:
├─ Task distribution
├─ Work queues
├─ Load balancing
└─ Background job processing
```

### 📢 Publish-Subscribe (Топики)

```
PUBLISH-SUBSCRIBE PATTERN:

             ┌─► Consumer A
Publisher ───┤
             │   [TOPIC]
             │
             └─► Consumer B

АРХИТЕКТУРА:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Publisher 1 │───►│    TOPIC    │───►│Subscriber 1 │
├─────────────┤    │             │    ├─────────────┤
│ Publisher 2 │───►│ ┌─────────┐ │───►│Subscriber 2 │
└─────────────┘    │ │ Event 1 │ │    ├─────────────┤
                   │ │ Event 2 │ │───►│Subscriber 3 │
                   │ │ Event 3 │ │    │(Broadcast)  │
                   │ └─────────┘ │    └─────────────┘
                   └─────────────┘

✅ ИСПОЛЬЗОВАНИЕ:
├─ Event notifications
├─ Real-time updates
├─ Log aggregation
└─ Monitoring systems
```

### 🔄 Request-Reply Pattern

```
REQUEST-REPLY PATTERN:

Client ──Request──► [REQUEST QUEUE] ──► Service
   ▲                                       │
   │                                       ▼
   └─── [REPLY QUEUE] ◄────Response─── Service

АРХИТЕКТУРА:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───►│Request Queue│───►│   Service   │
│             │    └─────────────┘    │             │
│ Correlation │    ┌─────────────┐    │ Process &   │
│     ID      │◄───│ Reply Queue │◄───│   Reply     │
└─────────────┘    └─────────────┘    └─────────────┘

🔑 КЛЮЧЕВЫЕ ОСОБЕННОСТИ:
├─ Correlation ID для связи request/response
├─ Временные или персистентные reply queues
├─ Timeout handling
└─ Асинхронный request-response
```

### 🧭 Message Routing Patterns

```
CONTENT-BASED ROUTER:

Message ───► Router ─┬─► Queue A (Priority: High)
    │          │     ├─► Queue B (Type: Order)
    │          │     └─► Queue C (Region: EU)
    │          │
    └─ Routing ─┘
       Rules

RECIPIENT LIST:

Message ───► [LIST] ─┬─► Service A
                     ├─► Service B  
                     ├─► Service C
                     └─► Service D

SCATTER-GATHER:

Request ───► Scatter ─┬─► Service A ─┐
                      ├─► Service B ─┤
                      └─► Service C ─┘
                                     │
Response ◄── Gather ◄────────────────┘
```

### 📊 Сравнение паттернов

```
┌──────────────┬─────────────┬─────────────┬─────────────┐
│   PATTERN    │   COUPLING  │ SCALABILITY │   USE CASE  │
├──────────────┼─────────────┼─────────────┼─────────────┤
│Point-to-Point│   Medium    │    High     │ Work queues │
│ Pub/Sub      │     Low     │  Very High  │ Events      │
│Request-Reply │    High     │   Medium    │ RPC-like    │
│ Routing      │     Low     │    High     │ Integration │
└──────────────┴─────────────┴─────────────┴─────────────┘
```

---

# ⚡ ГЛАВА 1.3: СИНХРОННАЯ VS АСИНХРОННАЯ КОММУНИКАЦИЯ
## ⏱️ Время изучения: 1 неделя

---

### 🔒 Блокирующие и неблокирующие вызовы

```
СИНХРОННАЯ КОММУНИКАЦИЯ:

Thread 1: ──[Call]──►──[Wait]──►──[Response]──►──[Continue]──
                     ⏱️ Blocked Time

❌ ПРОБЛЕМЫ:
├─ Thread blocking
├─ Resource waste  
├─ Cascade failures
├─ Poor scalability
└─ Timeout issues

АСИНХРОННАЯ КОММУНИКАЦИЯ:

Thread 1: ──[Send]──►──[Continue other work]──►──[Callback]──
                                                      ▲
Message:  ──────────►──[Broker]──►──[Process]──►──────┘

✅ ПРЕИМУЩЕСТВА:  
├─ Non-blocking operations
├─ Better resource utilization
├─ Fault isolation
├─ Elastic scalability
└─ Higher throughput
```

### 🎪 Event-driven архитектура

```
EVENT-DRIVEN ARCHITECTURE PATTERN:

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Service   │───►│    Event    │───►│   Service   │
│  Producer   │    │    Bus      │    │  Consumer   │
└─────────────┘    └─────┬───────┘    └─────────────┘
                         │
┌─────────────────────────┼─────────────────────────┐
│         EVENT FLOW      │                         │
├─────────────────────────┼─────────────────────────┤
│ 1. Something happens    │ 6. Event processed      │
│ 2. Event created        │ 7. New events generated │
│ 3. Event published      │ 8. Cascade continues    │
│ 4. Event routed         │ 9. System reacts        │
│ 5. Consumers notified   │ 10. State updated       │
└─────────────────────────┴─────────────────────────┘

ХАРАКТЕРИСТИКИ:
├─ Loose coupling
├─ Reactive systems
├─ Event sourcing
├─ CQRS compatibility
└─ Real-time processing
```

### 🔄 Eventual Consistency

```
STRONG CONSISTENCY vs EVENTUAL CONSISTENCY:

STRONG CONSISTENCY (Синхронная):
Database ──[Write]──► ✅ ──[Read]──► ✅ (Same data)
         ⏱️ Slow     ⏱️ Wait      ⏱️ Guaranteed

EVENTUAL CONSISTENCY (Асинхронная):
Database ──[Write]──► ✅ ──[Read]──► ⚠️ (Maybe stale)
         ⏱️ Fast    ⏱️ NoWait    ⏱️ Eventually consistent

TRADE-OFFS:
┌─────────────────┬─────────────────┬─────────────────┐
│   CONSISTENCY   │   AVAILABILITY  │  PARTITION TOL. │
├─────────────────┼─────────────────┼─────────────────┤
│ Strong (ACID)   │     Limited     │     Limited     │
│ Eventual (BASE) │      High       │      High       │
└─────────────────┴─────────────────┴─────────────────┘
```

### 🎭 CAP теорема в контексте messaging

```
CAP THEOREM APLICADO A MESSAGING:

    ┌─────────────────┐
    │   CONSISTENCY   │
    │  All nodes see  │  
    │  same data      │
    └─────────┬───────┘
              │
    ┌─────────┼───────┐
    │         │       │
    │    ┌────▼────┐  │
    │    │   CAP   │  │
    │    │ THEOREM │  │
    │    └────┬────┘  │
    │         │       │
    └─────────┼───────┘
              │
┌─────────────▼─┐   ┌─▼─────────────┐
│ AVAILABILITY  │   │   PARTITION   │
│ System remains│   │   TOLERANCE   │
│ operational   │   │ Works despite │
└───────────────┘   │ network fails │
                    └───────────────┘

MESSAGING SYSTEMS CHOICE:
├─ CP Systems: Strong consistency, may block
├─ AP Systems: Always available, eventual consistency  
└─ CA Systems: Only in perfect network (rare)
```

### 🏗️ Практические паттерны асинхронности

```
ASYNC PATTERNS В MESSAGING:

1. FIRE-AND-FORGET:
   Client ──[Send]──► Broker ──► Consumer
          └─[Continue]

2. REQUEST-ACKNOWLEDGE:
   Client ──[Send]──► Broker ──[Ack]──► Client
          └─[Wait for ack]──────────┘

3. SAGA PATTERN:
   Step1 ──► Step2 ──► Step3 ──► Success
     │       │         │
     ▼       ▼         ▼
   Comp1   Comp2     Comp3  (Compensation)

4. CIRCUIT BREAKER:
   ┌─ [CLOSED] ──failure──► [OPEN] ─┐
   │     │                    │    │
   │     ▼                    ▼    │
   │  Success               Timeout │
   │     │                    │    │
   └──── [HALF-OPEN] ◄─────────────┘
```

---

# 📚 ГЛАВА 1.4: ТЕРМИНОЛОГИЯ И БАЗОВЫЕ КОНЦЕПЦИИ
## ⏱️ Время изучения: 1 неделя

---

### 🏭 Основные компоненты

```
MESSAGING ECOSYSTEM COMPONENTS:

┌─────────────────────────────────────────────────────────┐
│                    MESSAGE BROKER                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   PRODUCER  │───►│    QUEUE    │───►│  CONSUMER   │  │
│  │  (Publisher)│    │   /TOPIC    │    │(Subscriber) │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                         │
│  🔧 BROKER SERVICES:                                    │
│  ├─ Routing Engine                                      │
│  ├─ Persistence Layer                                   │  
│  ├─ Management API                                      │
│  └─ Monitoring & Metrics                               │
└─────────────────────────────────────────────────────────┘

ОПРЕДЕЛЕНИЯ:
├─ PRODUCER: Создает и отправляет сообщения
├─ CONSUMER: Получает и обрабатывает сообщения
├─ BROKER: Посредник для маршрутизации сообщений
├─ MESSAGE: Единица данных для передачи
└─ DESTINATION: Место назначения (queue/topic)
```

### 📨 Структура и типы сообщений

```
MESSAGE STRUCTURE:

┌─────────────────────────────────────────────────────┐
│                    MESSAGE                          │
├─────────────────────────────────────────────────────┤
│  📋 HEADERS                                         │
│  ├─ Message-ID: unique identifier                   │
│  ├─ Timestamp: creation time                        │
│  ├─ Content-Type: application/json                  │
│  ├─ Priority: high/medium/low                       │
│  ├─ TTL: time to live                              │
│  └─ Custom headers                                  │
├─────────────────────────────────────────────────────┤
│  📦 PROPERTIES                                      │
│  ├─ Correlation-ID: for request/reply               │
│  ├─ Reply-To: destination for response              │
│  ├─ Delivery-Mode: persistent/non-persistent        │
│  └─ Routing-Key: for routing decisions              │
├─────────────────────────────────────────────────────┤
│  💾 PAYLOAD (BODY)                                  │
│  ├─ JSON: {"order": 123, "amount": 100}            │
│  ├─ XML: <order><id>123</id></order>               │
│  ├─ Binary: протоколы, файлы                       │
│  └─ Text: plain text messages                      │
└─────────────────────────────────────────────────────┘

MESSAGE TYPES:
├─ Command: "Create order", "Update inventory"
├─ Event: "Order created", "Payment processed"  
├─ Query: "Get order status", "List products"
└─ Document: Data transfer, file sharing
```

### 📬 Queues, Topics, Partitions

```
QUEUE CHARACTERISTICS:

[Producer] ──► [QUEUE] ──► [Consumer 1]
                │
                ├──────► [Consumer 2]
                │
                └──────► [Consumer 3]

СВОЙСТВА QUEUE:
├─ Point-to-point delivery
├─ Load balancing between consumers
├─ Message consumed only once
├─ FIFO ordering (usually)
└─ Persistent storage option

TOPIC CHARACTERISTICS:

[Publisher] ──► [TOPIC] ──┬──► [Subscriber 1]
                          ├──► [Subscriber 2]  
                          └──► [Subscriber 3]

СВОЙСТВА TOPIC:
├─ Publish-subscribe delivery
├─ Broadcasting to all subscribers
├─ Message consumed by all subscribers
├─ Multiple subscription options
└─ Filtering capabilities

PARTITIONS (Kafka-style):

TOPIC: "orders"
├─ Partition 0: [Msg1]──[Msg4]──[Msg7]──►
├─ Partition 1: [Msg2]──[Msg5]──[Msg8]──►
└─ Partition 2: [Msg3]──[Msg6]──[Msg9]──►

ПРЕИМУЩЕСТВА PARTITIONS:
├─ Parallel processing
├─ Scalability
├─ Ordering within partition
└─ Load distribution
```

### ✅ Acknowledgments и Delivery Semantics

```
DELIVERY GUARANTEES:

1. AT-MOST-ONCE (0 или 1 раз):
   Producer ──► Broker ──► Consumer
            ❌ No ack     ✅ Fast
   ⚠️ Возможна потеря сообщений

2. AT-LEAST-ONCE (1 или более раз):
   Producer ──► Broker ──► Consumer
            ✅ Ack       ✅ Reliable
   ⚠️ Возможны дубликаты

3. EXACTLY-ONCE (ровно 1 раз):
   Producer ──► Broker ──► Consumer
            ✅ Ack + Dedup ⏱️ Slow
   ✅ Идемпотентность

ACKNOWLEDGMENT PATTERNS:

AUTO-ACK:
Consumer ──[Receive]──► ✅ (Auto ack) ──[Process]
⚡ Fast, ⚠️ Risk of message loss

MANUAL-ACK:
Consumer ──[Receive]──[Process]──[Ack]──► ✅  
🛡️ Safe, ⏱️ Slower

CLIENT-ACK:  
Consumer ──[Receive]──[Process]──[Business Logic]──[Ack]──► ✅
🎯 Control, 💼 Business logic dependent
```

### 💀 Dead Letter Queues

```
DEAD LETTER QUEUE PATTERN:

Normal Flow:
Producer ──► [MAIN QUEUE] ──► Consumer ──► ✅ Success

Error Flow:
Producer ──► [MAIN QUEUE] ──► Consumer ──► ❌ Failure
                │                            │
                │     (Max retries)          │
                └──────[DLQ]◄─────────────────┘

DLQ ARCHITECTURE:
┌─────────────────────────────────────────────────────┐
│                MAIN QUEUE                           │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐               │
│  │Msg1 │  │Msg2 │  │Msg3 │  │Msg4 │  ──► Consumer │
│  └─────┘  └─────┘  └─────┘  └─────┘               │
└─────────────────────────────────────────────────────┘
                     │
                     ▼ (After retries)
┌─────────────────────────────────────────────────────┐
│                DEAD LETTER QUEUE                    │
│  ┌─────┐  ┌─────┐                                   │
│  │Msg2 │  │Msg5 │  ──► Manual Investigation        │
│  └─────┘  └─────┘                                   │
└─────────────────────────────────────────────────────┘

DLQ ИСПОЛЬЗОВАНИЕ:
├─ Poison message handling
├─ Debugging failed messages
├─ Manual reprocessing  
├─ Audit trail
└─ System resilience
```

---

# 🎯 ПРАКТИЧЕСКИЕ ЗАДАНИЯ БЛОКА 1

---

## 📝 ЗАДАНИЕ 1: Анализ архитектурных паттернов

```
СЦЕНАРИЙ: ИНТЕРНЕТ-МАГАЗИН

Компоненты системы:
├─ Web Frontend
├─ Order Service  
├─ Payment Service
├─ Inventory Service
├─ Notification Service
├─ Analytics Service
└─ Shipping Service

ЗАДАЧИ:
1. Спроектируйте архитектуру БЕЗ message broker
2. Определите проблемы tight coupling
3. Перепроектируйте С message broker
4. Выберите подходящие messaging patterns
5. Определите типы delivery guarantees
```

## 📊 ЗАДАНИЕ 2: Сравнительная таблица

```
СОЗДАЙТЕ СРАВНИТЕЛЬНУЮ ТАБЛИЦУ:

┌──────────────┬──────────┬──────────┬──────────┬──────────┐
│   PATTERN    │ COUPLING │RELIABILITY│ LATENCY  │USE CASES │
├──────────────┼──────────┼──────────┼──────────┼──────────┤
│Point-to-Point│    ?     │    ?     │    ?     │    ?     │
│ Pub/Sub      │    ?     │    ?     │    ?     │    ?     │
│Request-Reply │    ?     │    ?     │    ?     │    ?     │  
│ Routing      │    ?     │    ?     │    ?     │    ?     │
└──────────────┴──────────┴──────────┴──────────┴──────────┘

ЗАПОЛНИТЕ ТАБЛИЦУ И ОБОСНУЙТЕ ВЫБОР
```

## 🔧 ЗАДАНИЕ 3: Проектирование messaging flow

```
СЦЕНАРИЙ: СИСТЕМА МОНИТОРИНГА IoT

Требования:
├─ 10,000 IoT устройств отправляют данные каждую минуту
├─ Real-time dashboard обновления
├─ Alerts при критических значениях  
├─ Historical data storage
├─ Analytics и ML processing
└─ 99.9% availability

СПРОЕКТИРУЙТЕ:
1. Messaging topology
2. Выбор patterns для каждого flow
3. Delivery guarantees для каждого сценария
4. Error handling strategy
5. Scaling approach
```

---

# 🧠 КОНТРОЛЬНЫЕ ВОПРОСЫ БЛОКА 1

```
📝 ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ:

1. Объясните разницу между Message Queue и Message Topic
2. Когда следует использовать синхронную, а когда асинхронную коммуникацию?
3. Что такое CAP теорема и как она применима к messaging?
4. Опишите три типа delivery guarantees и их trade-offs
5. Что такое Dead Letter Queue и когда его использовать?

🛠️ ПРАКТИЧЕСКИЕ ВОПРОСЫ:

6. Как спроектировать fault-tolerant messaging систему?
7. Какие паттерны использовать для Order Processing workflow?
8. Как обеспечить ordering сообщений в distributed системе?
9. Как реализовать Request-Reply pattern асинхронно?
10. Какие метрики важны для monitoring messaging системы?

🎯 СЦЕНАРНЫЕ ВОПРОСЫ:

11. Банковская система: какие guarantees нужны для transfer операций?
12. Social media: как реализовать real-time notifications?
13. E-commerce: как обработать Black Friday traffic spike?
14. IoT система: как обработать миллионы events в секунду?
15. Microservices: как обеспечить data consistency между сервисами?
```

---

# ✅ РЕЗУЛЬТАТЫ ИЗУЧЕНИЯ БЛОКА 1

После успешного завершения блока 1 вы должны:

```
🎯 ПОНИМАТЬ:
├─ Фундаментальные принципы messaging
├─ Различия между синхронной и асинхронной коммуникацией
├─ Основные messaging patterns и их применение
├─ Trade-offs различных подходов к messaging
├─ Важность delivery guarantees и consistency
└─ Роль messaging в distributed systems

🛠️ УМЕТЬ:
├─ Анализировать требования для выбора messaging pattern
├─ Проектировать messaging топологии
├─ Определять подходящие delivery guarantees
├─ Создавать fault-tolerant messaging архитектуры
├─ Выбирать между различными подходами к consistency
└─ Планировать error handling strategies

📊 ПРИМЕНЯТЬ:
├─ Messaging patterns в реальных проектах
├─ Принципы loose coupling в архитектуре
├─ Event-driven архитектурные подходы
├─ Best practices для reliability и performance
├─ Monitoring и troubleshooting подходы
└─ Scalability planning для messaging систем
```

---

# 🚀 ПОДГОТОВКА К БЛОКУ 2

```
📚 СЛЕДУЮЩИЙ БЛОК: ПОПУЛЯРНЫЕ РЕШЕНИЯ И ИХ ОСОБЕННОСТИ

ПРЕДВАРИТЕЛЬНАЯ ПОДГОТОВКА:
├─ Установите Docker для практических работ
├─ Изучите основы Java/Python для work с brokers
├─ Подготовьте dev environment
├─ Изучите основы network protocols (TCP, HTTP)
└─ Ознакомьтесь с Linux command line

ТЕМЫ БЛОКА 2:
├─ Apache Kafka deep dive
├─ RabbitMQ и AMQP protocol
├─ Amazon SQS и cloud messaging
├─ Redis Pub/Sub и Apache Pulsar
└─ Сравнительный анализ решений

🎯 ЦЕЛЬ: Практическое освоение популярных message brokers
```

---

```
📈 ОБЩИЙ ПРОГРЕСС ПРОГРАММЫ:
[████░░░░░░░░░░░░░░░░] 14% завершено (1/7 блоков)

СТАТУС БЛОКА 1: ✅ ЗАВЕРШЕН
├─ Глава 1.1: Введение в брокеры сообщений ✅
├─ Глава 1.2: Паттерны обмена сообщениями ✅  
├─ Глава 1.3: Синхронная vs асинхронная коммуникация ✅
└─ Глава 1.4: Терминология и базовые концепции ✅
```