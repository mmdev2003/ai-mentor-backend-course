# Блок 4: Архитектурные стили и подходы

**Длительность:** 6-7 недель  
**Цель:** Понять различные способы организации крупных систем

---

## 📋 Содержание блока

```
┌─────────────────────────────────────────────────────────────┐
│                    АРХИТЕКТУРНЫЕ СТИЛИ                     │
├─────────────────────────────────────────────────────────────┤
│ 1. Эволюция архитектурных подходов                         │
│ 2. Монолитная архитектура                                  │
│ 3. Слоистая архитектура (Layered Architecture)             │
│ 4. Микросервисная архитектура                              │
│ 5. Event-Driven Architecture                               │
│ 6. Hexagonal Architecture (Ports and Adapters)             │
│ 7. Clean Architecture                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Глава 1: Эволюция архитектурных подходов

### 🕐 Временная линия развития архитектуры

```
1960s        1980s        1990s        2000s        2010s        2020s
  │            │            │            │            │            │
  ▼            ▼            ▼            ▼            ▼            ▼
Процедурное  Объектно-   Компонентное  SOA/ESB    Микросервисы  Serverless
программир.  ориентир.   программир.              Cloud-Native  Edge Computing
             
────────────────────────────────────────────────────────────────────────────
Монолиты ──────────────────▶ Распределенные системы ──────────────▶ Mesh
```

### 🎯 Ключевые драйверы изменений

**Технические факторы:**
- Рост сложности систем
- Увеличение нагрузки и данных
- Развитие инфраструктуры (облака, контейнеры)
- Новые требования к производительности

**Бизнес факторы:**
- Скорость разработки (Time to Market)
- Масштабируемость команд
- Независимые релизы
- Отказоустойчивость

### 📊 Сравнение подходов по эпохам

| Критерий | Процедурный | ООП | Компонентный | SOA | Микросервисы |
|----------|-------------|-----|--------------|-----|--------------|
| Сложность | Низкая | Средняя | Средняя | Высокая | Очень высокая |
| Масштабируемость | Низкая | Средняя | Средняя | Высокая | Очень высокая |
| Скорость разработки | Высокая | Средняя | Средняя | Низкая | Средняя |
| Поддерживаемость | Низкая | Средняя | Высокая | Средняя | Высокая |

---

## Глава 2: Монолитная архитектура

### 🏗️ Структура монолита

```
┌─────────────────────────────────────────┐
│              МОНОЛИТНОЕ ПРИЛОЖЕНИЕ      │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐ │
│  │        Presentation Layer           │ │
│  │  (Controllers, Views, API)          │ │
│  └─────────────────────────────────────┘ │
│  ┌─────────────────────────────────────┐ │
│  │         Business Layer              │ │
│  │    (Services, Domain Logic)         │ │
│  └─────────────────────────────────────┘ │
│  ┌─────────────────────────────────────┐ │
│  │          Data Layer                 │ │
│  │     (Repositories, ORM)             │ │
│  └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│          Единая База Данных             │
└─────────────────────────────────────────┘
```

### ✅ Преимущества монолитов

- **Простота разработки**: Все в одном месте
- **Простота тестирования**: End-to-end тесты проще
- **Простота деплоя**: Один артефакт для развертывания
- **Производительность**: Нет накладных расходов на сеть
- **ACID транзакции**: Легко обеспечить консистентность

### ❌ Недостатки монолитов

- **Сложность понимания**: Большая кодовая база
- **Технологическая привязка**: Сложно менять стек
- **Масштабирование**: Только вертикальное
- **Команды**: Конфликты при параллельной разработке
- **Развертывание**: Риск при каждом релизе

### 🎯 Когда выбирать монолит

```
┌─────────────────────────────────────────┐
│           МОНОЛИТ ПОДХОДИТ КОГДА:       │
├─────────────────────────────────────────┤
│ ✓ Команда < 10 человек                  │
│ ✓ Простая предметная область            │
│ ✓ Быстрый MVP                           │
│ ✓ Ограниченные ресурсы                  │
│ ✓ Неопределенные требования             │
│ ✓ Нет опыта с распределенными системами │
└─────────────────────────────────────────┘
```

### 🔧 Модульные монолиты

```
┌─────────────────────────────────────────────────────────────┐
│                   МОДУЛЬНЫЙ МОНОЛИТ                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   MODULE A  │  │   MODULE B  │  │   MODULE C  │         │
│  │             │  │             │  │             │         │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │         │
│  │ │   API   │ │  │ │   API   │ │  │ │   API   │ │         │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │         │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │         │
│  │ │Business │ │  │ │Business │ │  │ │Business │ │         │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │         │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │         │
│  │ │  Data   │ │  │ │  Data   │ │  │ │  Data   │ │         │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## Глава 3: Слоистая архитектура (Layered Architecture)

### 🎂 Классическая трехуровневая архитектура

```
┌─────────────────────────────────────────────────────────┐
│                   КЛИЕНТСКИЕ ПРИЛОЖЕНИЯ                 │
│              (Web, Mobile, Desktop)                     │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/HTTPS
                  ▼
┌─────────────────────────────────────────────────────────┐
│                PRESENTATION TIER                        │
│              (Web Server, API Gateway)                 │
│  ┌─────────────────────────────────────────────────────┐│
│  │  Controllers │  Views  │  API Endpoints  │  DTOs   ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────┬───────────────────────────────────────┘
                  │ Function Calls
                  ▼
┌─────────────────────────────────────────────────────────┐
│                 BUSINESS TIER                           │
│               (Application Server)                      │
│  ┌─────────────────────────────────────────────────────┐│
│  │  Services  │  Domain Logic  │  Workflows  │  Rules ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────┬───────────────────────────────────────┘
                  │ SQL/NoSQL
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   DATA TIER                             │
│                (Database Server)                        │
│  ┌─────────────────────────────────────────────────────┐│
│  │  Tables  │  Views  │  Procedures  │  Triggers      ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

### 📋 Принципы слоистой архитектуры

1. **Односторонние зависимости**: Верхние слои зависят только от нижних
2. **Инкапсуляция**: Каждый слой скрывает детали реализации
3. **Разделение ответственности**: Каждый слой решает свои задачи
4. **Стандартизация**: Четкие интерфейсы между слоями

### 🔍 Детализация слоев

#### Presentation Layer
```
┌─────────────────────────────────────────┐
│           PRESENTATION LAYER            │
├─────────────────────────────────────────┤
│ Ответственности:                        │
│ • Обработка HTTP запросов               │
│ • Валидация входных данных              │
│ • Сериализация/десериализация           │
│ • Аутентификация и авторизация          │
│ • Логирование запросов                  │
│                                         │
│ Компоненты:                             │
│ • Controllers/Handlers                  │
│ • Middleware                            │
│ • DTO (Data Transfer Objects)           │
│ • Validators                            │
│ • Mappers                               │
└─────────────────────────────────────────┘
```

#### Business Layer
```
┌─────────────────────────────────────────┐
│            BUSINESS LAYER               │
├─────────────────────────────────────────┤
│ Ответственности:                        │
│ • Бизнес-логика приложения              │
│ • Оркестрация операций                  │
│ • Транзакции                            │
│ • Кэширование                           │
│ • Бизнес-правила                        │
│                                         │
│ Компоненты:                             │
│ • Services                              │
│ • Domain Models                         │
│ • Business Rules Engine                 │
│ • Workflow Manager                      │
│ • Cache Manager                         │
└─────────────────────────────────────────┘
```

#### Data Layer
```
┌─────────────────────────────────────────┐
│             DATA LAYER                  │
├─────────────────────────────────────────┤
│ Ответственности:                        │
│ • Доступ к данным                       │
│ • Персистентность                       │
│ • Запросы к БД                          │
│ • Миграции схемы                        │
│ • Оптимизация запросов                  │
│                                         │
│ Компоненты:                             │
│ • Repositories                          │
│ • Data Access Objects (DAO)             │
│ • ORM/ODM                               │
│ • Query Builders                        │
│ • Connection Pools                      │
└─────────────────────────────────────────┘
```

### ⚠️ Проблемы слоистой архитектуры

#### 1. **Sinkhole Anti-Pattern**
```
Request ──▶ Controller ──▶ Service ──▶ Repository ──▶ Database
                │              │            │
                │              │            │
               Pass          Pass         Pass
              Through       Through      Through
                │              │            │
                ▼              ▼            ▼
            No Logic      No Logic     No Logic
```

#### 2. **Tight Coupling между слоями**
```
┌─────────────┐    зависит от    ┌─────────────┐
│Presentation │ ──────────────▶  │  Business   │
└─────────────┘                  └─────────────┘
                                        │ зависит от
                                        ▼
                                 ┌─────────────┐
                                 │    Data     │
                                 └─────────────┘
```

#### 3. **Закон Деметры нарушается**
```java
// ПЛОХО - цепочка вызовов
customer.getOrder().getItems().get(0).getPrice()

// ХОРОШО - делегирование
customer.getTotalOrderAmount()
```

---

## Глава 4: Микросервисная архитектура

### 🧩 Принципы микросервисов

```
┌─────────────────────────────────────────────────────────────┐
│                 ПРИНЦИПЫ МИКРОСЕРВИСОВ                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   SERVICE A  │  │   SERVICE B  │  │   SERVICE C  │      │
│  │              │  │              │  │              │      │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │      │
│  │  │Business│  │  │  │Business│  │  │  │Business│  │      │
│  │  │ Logic  │  │  │  │ Logic  │  │  │  │ Logic  │  │      │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │      │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │      │
│  │  │  API   │  │  │  │  API   │  │  │  │  API   │  │      │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │      │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │      │
│  │  │   DB   │  │  │  │   DB   │  │  │  │   DB   │  │      │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            │                                │
│              Асинхронная коммуникация                       │
│                   (REST/gRPC/Events)                        │
└─────────────────────────────────────────────────────────────┘
```

### 🎯 Ключевые характеристики

1. **Автономность**: Каждый сервис может разрабатываться и развертываться независимо
2. **Decentralized**: Нет центрального управления
3. **Single Responsibility**: Один сервис = одна бизнес-функция
4. **Technology Agnostic**: Разные технологии для разных сервисов
5. **Failure Isolation**: Сбой одного сервиса не влияет на другие

### 🔄 Декомпозиция монолита

#### Стратегии разбиения:

**1. По бизнес-доменам (Domain-Driven Design)**
```
МОНОЛИТ E-COMMERCE
┌─────────────────────────────────────────┐
│  User Management | Product Catalog      │
│  Order Processing | Payment            │
│  Inventory | Shipping | Notifications  │
└─────────────────────────────────────────┘
                    │
                    ▼ DECOMPOSITION
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│    User     │ │   Product   │ │    Order    │
│  Service    │ │   Service   │ │   Service   │
└─────────────┘ └─────────────┘ └─────────────┘
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Payment    │ │ Inventory   │ │  Shipping   │
│  Service    │ │  Service    │ │   Service   │
└─────────────┘ └─────────────┘ └─────────────┘
```

**2. Strangler Fig Pattern**
```
Phase 1: Монолит + Новый сервис
┌─────────────────┐    ┌─────────────┐
│    МОНОЛИТ      │    │   NEW       │
│                 │    │  SERVICE    │
│ ┌─────────────┐ │    │             │
│ │Old Function │ │    │             │
│ └─────────────┘ │    │             │
└─────────────────┘    └─────────────┘

Phase 2: Постепенная миграция
┌─────────────────┐    ┌─────────────┐
│    МОНОЛИТ      │    │   NEW       │
│ (уменьшается)   │───▶│  SERVICE    │
│                 │    │ (растет)    │
└─────────────────┘    └─────────────┘

Phase 3: Только микросервисы
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  SERVICE A  │ │  SERVICE B  │ │  SERVICE C  │
└─────────────┘ └─────────────┘ └─────────────┘
```

### 🌐 Межсервисное взаимодействие

#### Синхронное взаимодействие
```
┌─────────────┐     HTTP/REST      ┌─────────────┐
│  SERVICE A  │ ──────────────────▶│  SERVICE B  │
│             │◀──────────────────│             │
└─────────────┘    Response        └─────────────┘

┌─────────────┐      gRPC         ┌─────────────┐
│  SERVICE A  │ ──────────────────▶│  SERVICE B  │
│             │◀──────────────────│             │
└─────────────┘   Binary Proto    └─────────────┘
```

#### Асинхронное взаимодействие
```
                     Message Broker
                   ┌─────────────────┐
┌─────────────┐    │   ┌─────────┐   │    ┌─────────────┐
│  SERVICE A  │───▶│   │ QUEUE A │   │───▶│  SERVICE B  │
└─────────────┘    │   └─────────┘   │    └─────────────┘
                   │   ┌─────────┐   │    ┌─────────────┐
┌─────────────┐    │   │ QUEUE B │   │───▶│  SERVICE C  │
│  SERVICE D  │───▶│   └─────────┘   │    └─────────────┘
└─────────────┘    └─────────────────┘
```

### 💾 Управление данными

#### Database per Service
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   USER SERVICE  │    │ PRODUCT SERVICE │    │  ORDER SERVICE  │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │  User DB  │  │    │  │Product DB │  │    │  │ Order DB  │  │
│  │(PostgreSQL│  │    │  │ (MongoDB) │  │    │  │ (MySQL)   │  │
│  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Проблемы распределенных данных
```
ACID Транзакции ──────X────── Невозможны
                              
BASE (Eventually Consistent)
┌─────────────────────────────────────────┐
│ Basically Available                     │
│ Soft state                              │
│ Eventually consistent                   │
└─────────────────────────────────────────┘
```

### ✅ Преимущества микросервисов

- **Независимое развертывание**: Быстрые релизы
- **Технологическое разнообразие**: Лучший инструмент для задачи
- **Масштабирование**: Точечное масштабирование нагруженных сервисов
- **Отказоустойчивость**: Изоляция сбоев
- **Команды**: Небольшие автономные команды

### ❌ Недостатки микросервисов

- **Сложность**: Распределенные системы сложнее
- **Сетевые задержки**: Межсервисные вызовы
- **Консистентность данных**: Eventual consistency
- **Мониторинг**: Сложнее отслеживать запросы
- **Тестирование**: Интеграционное тестирование сложнее

---

## Глава 5: Event-Driven Architecture

### 📡 Основы событийной архитектуры

```
┌─────────────────────────────────────────────────────────────┐
│                EVENT-DRIVEN ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─────────────┐         EVENT BUS         ┌─────────────┐   │
│ │  PRODUCER   │──────┐                ┌───│  CONSUMER   │   │
│ │  SERVICE    │      │                │   │  SERVICE A  │   │
│ └─────────────┘      │                │   └─────────────┘   │
│                      ▼                ▲                     │
│ ┌─────────────┐ ┌─────────────────────────┐ ┌─────────────┐ │
│ │  PRODUCER   │▶│       MESSAGE        │◀│  CONSUMER   │ │
│ │  SERVICE    │ │        BROKER        │ │  SERVICE B  │ │
│ └─────────────┘ │   (Kafka, RabbitMQ)  │ └─────────────┘ │
│                 └─────────────────────────┘               │
│ ┌─────────────┐          ▲                ▼ ┌─────────────┐ │
│ │  PRODUCER   │──────────┘                └─│  CONSUMER   │ │
│ │  SERVICE    │                             │  SERVICE C  │ │
│ └─────────────┘                             └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 🎭 Паттерны событийной архитектуры

#### 1. **Publish-Subscribe**
```
                     TOPIC: OrderCreated
                   ┌─────────────────────┐
┌─────────────┐    │   Event: {          │    ┌─────────────┐
│    ORDER    │───▶│     orderId: 123    │───▶│  INVENTORY  │
│   SERVICE   │    │     userId: 456     │    │   SERVICE   │
└─────────────┘    │     amount: 100.0   │    └─────────────┘
                   │   }                 │            
                   └─────────────────────┘    ┌─────────────┐
                              │               │   EMAIL     │
                              └──────────────▶│   SERVICE   │
                                              └─────────────┘
                                                      │
                                              ┌─────────────┐
                                              │  ANALYTICS  │
                                              │   SERVICE   │
                                              └─────────────┘
```

#### 2. **Event Sourcing**
```
TRADITIONAL APPROACH                 EVENT SOURCING APPROACH
┌─────────────────┐                 ┌─────────────────────────┐
│   USER TABLE    │                 │     EVENT STORE         │
├─────────────────┤                 ├─────────────────────────┤
│ id | name | age │                 │ UserCreated: {          │
├─────────────────┤                 │   id: 1, name: "John"  │
│ 1  |John  | 25  │                 │ }                       │
└─────────────────┘                 │ UserAgeUpdated: {       │
       ▲                            │   id: 1, age: 25       │
       │ UPDATE                     │ }                       │
       │                            │ UserNameUpdated: {      │
   Current State                    │   id: 1, name: "Jane"  │
                                    │ }                       │
                                    └─────────────────────────┘
                                              │
                                              ▼ REPLAY
                                    ┌─────────────────────────┐
                                    │    CURRENT STATE        │
                                    │  id: 1, name: "Jane"   │
                                    │  age: 25                │
                                    └─────────────────────────┘
```

#### 3. **CQRS (Command Query Responsibility Segregation)**
```
┌─────────────────────────────────────────────────────────────┐
│                         CQRS                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WRITE SIDE (Commands)           READ SIDE (Queries)       │
│                                                             │
│ ┌─────────────┐                  ┌─────────────┐           │
│ │   CLIENT    │     Command      │   CLIENT    │           │
│ │             │─────────────────▶│             │           │
│ └─────────────┘                  └─────────────┘           │
│        │                                │                  │
│        ▼                                ▼                  │
│ ┌─────────────┐                  ┌─────────────┐           │
│ │  COMMAND    │                  │    QUERY    │           │
│ │  HANDLER    │                  │   HANDLER   │           │
│ └─────────────┘                  └─────────────┘           │
│        │                                │                  │
│        ▼                                ▼                  │
│ ┌─────────────┐     Events       ┌─────────────┐           │
│ │ WRITE MODEL │─────────────────▶│ READ MODEL  │           │
│ │(Normalized) │                  │(Denormalized│           │
│ └─────────────┘                  └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 🔄 Saga Pattern

Для управления распределенными транзакциями:

#### Choreography Saga
```
1. Order Service ──┐
                   ▼ OrderCreated Event
2. Payment Service ──┐
                     ▼ PaymentProcessed Event  
3. Inventory Service ──┐
                       ▼ InventoryReserved Event
4. Shipping Service ──┐
                      ▼ OrderShipped Event
5. Order Service (Complete)

В случае ошибки:
   Compensation Events (откат операций)
```

#### Orchestration Saga
```
                    SAGA ORCHESTRATOR
                   ┌─────────────────┐
     ┌─────────────│  1. Process     │
     │             │     Payment     │◀──┐
     ▼             └─────────────────┘   │
┌─────────────┐           │              │
│  PAYMENT    │           ▼              │
│  SERVICE    │    ┌─────────────────┐   │
└─────────────┘    │  2. Reserve     │   │
     │             │     Inventory   │   │
     └────────────▶└─────────────────┘   │
           Success        │              │
                          ▼              │
                 ┌─────────────────┐     │
                 │  3. Ship Order  │─────┘
                 └─────────────────┘
```

### ⚡ Преимущества Event-Driven Architecture

- **Слабая связанность**: Сервисы не знают друг о друге
- **Масштабируемость**: Асинхронная обработка
- **Отказоустойчивость**: Буферизация сообщений
- **Аудит**: Полная история изменений (Event Sourcing)
- **Интеграция**: Легко добавлять новые потребители

### ⚠️ Вызовы Event-Driven Architecture

- **Eventual Consistency**: Данные не всегда консистентны
- **Сложность отладки**: Трудно отследить flow
- **Дублирование событий**: Idempotency обязательна
- **Порядок событий**: Может быть нарушен
- **Мониторинг**: Сложно отслеживать бизнес-процессы

---

## Глава 6: Hexagonal Architecture (Ports and Adapters)

### 🔷 Концепция Hexagonal Architecture

```
                 ┌─────────────────────────────────────┐
                 │         ВНЕШНИЙ МИР                 │
                 │                                     │
  ┌──────────────┤  ┌─────────────┐ ┌─────────────┐   │
  │   WEB UI     │  │    REST     │ │    CLI      │   │
  │   ADAPTER    │  │   ADAPTER   │ │   ADAPTER   │   │
  └──────────────┤  └─────────────┘ └─────────────┘   │
                 │         │               │          │
                 │    HTTP │               │ Commands │
                 └─────────┼───────────────┼──────────┘
                           │               │
          ┌────────────────┼───────────────┼────────────────┐
          │                ▼               ▼                │
          │        ┌─────────────┐ ┌─────────────┐         │
          │        │    PORT     │ │    PORT     │         │
          │        │ (Interface) │ │ (Interface) │         │
          │        └─────────────┘ └─────────────┘         │
          │                │               │                │
          │        ┌───────▼───────────────▼───────┐       │
          │        │                               │       │
          │        │        DOMAIN CORE            │       │
          │        │     (Business Logic)          │       │
          │        │                               │       │
          │        └───────┬───────────────┬───────┘       │
          │                │               │                │
          │        ┌─────────────┐ ┌─────────────┐         │
          │        │    PORT     │ │    PORT     │         │
          │        │ (Interface) │ │ (Interface) │         │
          │        └─────────────┘ └─────────────┘         │
          │                │               │                │
          └────────────────┼───────────────┼────────────────┘
                           │               │
                 ┌─────────▼───────────────▼──────────┐
                 │         │               │          │
                 │  ┌─────────────┐ ┌─────────────┐   │
                 │  │  DATABASE   │ │   EMAIL     │   │
                 │  │   ADAPTER   │ │   ADAPTER   │   │
                 │  └─────────────┘ └─────────────┘   │
                 │                                     │
                 │       ВНЕШНИЕ СИСТЕМЫ               │
                 └─────────────────────────────────────┘
```

### 🎯 Ключевые принципы

1. **Изоляция бизнес-логики**: Домен в центре, не зависит от внешних систем
2. **Порты и адаптеры**: Четкое разделение интерфейсов и реализаций
3. **Dependency Inversion**: Зависимости направлены внутрь
4. **Тестируемость**: Легко мокать внешние зависимости

### 🔌 Порты и Адаптеры

#### Driving Ports (Первичные)
```java
// PORT (Interface)
public interface OrderService {
    OrderId createOrder(CreateOrderCommand command);
    Order getOrder(OrderId orderId);
    void cancelOrder(OrderId orderId);
}

// ADAPTER (REST Controller)
@RestController
public class OrderController {
    private final OrderService orderService;
    
    @PostMapping("/orders")
    public ResponseEntity<OrderDto> createOrder(@RequestBody CreateOrderDto dto) {
        CreateOrderCommand command = mapper.toCommand(dto);
        OrderId orderId = orderService.createOrder(command);
        return ResponseEntity.ok(mapper.toDto(orderId));
    }
}
```

#### Driven Ports (Вторичные)
```java
// PORT (Interface)
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId orderId);
    List<Order> findByUserId(UserId userId);
}

// ADAPTER (JPA Implementation)
@Repository
public class JpaOrderRepository implements OrderRepository {
    private final JpaOrderEntityRepository jpaRepository;
    
    @Override
    public void save(Order order) {
        OrderEntity entity = mapper.toEntity(order);
        jpaRepository.save(entity);
    }
    
    @Override
    public Optional<Order> findById(OrderId orderId) {
        return jpaRepository.findById(orderId.getValue())
                .map(mapper::toDomain);
    }
}
```

### 🏗️ Структура проекта

```
src/
├── main/
│   ├── java/
│   │   ├── domain/                    # DOMAIN CORE
│   │   │   ├── model/                 # Entities, Value Objects
│   │   │   ├── service/               # Domain Services
│   │   │   └── port/                  # Interfaces
│   │   │       ├── in/                # Driving Ports
│   │   │       └── out/               # Driven Ports
│   │   │
│   │   └── adapter/                   # ADAPTERS
│   │       ├── in/                    # Driving Adapters
│   │       │   ├── web/               # REST Controllers
│   │       │   ├── cli/               # Command Line
│   │       │   └── messaging/         # Message Consumers
│   │       │
│   │       └── out/                   # Driven Adapters
│   │           ├── persistence/       # Database
│   │           ├── messaging/         # Message Producers
│   │           └── external/          # External APIs
│   │
│   └── resources/
└── test/
```

### 🧪 Тестирование

#### Unit Tests (Domain Core)
```java
class OrderServiceTest {
    
    // Мокаем только порты, не адаптеры
    @Mock
    private OrderRepository orderRepository;
    
    @Mock
    private PaymentService paymentService;
    
    @InjectMocks
    private OrderService orderService;
    
    @Test
    void shouldCreateOrderSuccessfully() {
        // Тестируем только бизнес-логику
        // Внешние зависимости замоканы
    }
}
```

#### Integration Tests (Adapters)
```java
@SpringBootTest
@Testcontainers
class OrderControllerIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13");
    
    @Test
    void shouldCreateOrderThroughRestApi() {
        // Тестируем полный flow через REST API
        // с реальной базой данных
    }
}
```

---

## Глава 7: Clean Architecture

### 🎯 Принципы Clean Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLEAN ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    ┌─────────────────────────────────────────────────┐     │
│    │                FRAMEWORKS                       │     │
│    │              & DRIVERS                          │     │
│    │        (Web, DB, External APIs)                 │     │
│    │  ┌─────────────────────────────────────────┐   │     │
│    │  │           INTERFACE                     │   │     │
│    │  │          ADAPTERS                       │   │     │
│    │  │      (Controllers, Gateways)            │   │     │
│    │  │  ┌─────────────────────────────────┐   │   │     │
│    │  │  │        APPLICATION              │   │   │     │
│    │  │  │       BUSINESS RULES            │   │   │     │
│    │  │  │     (Use Cases)                 │   │   │     │
│    │  │  │  ┌─────────────────────────┐   │   │   │     │
│    │  │  │  │     ENTERPRISE          │   │   │   │     │
│    │  │  │  │   BUSINESS RULES        │   │   │   │     │
│    │  │  │  │    (Entities)           │   │   │   │     │
│    │  │  │  └─────────────────────────┘   │   │   │     │
│    │  │  └─────────────────────────────────┘   │   │     │
│    │  └─────────────────────────────────────────┘   │     │
│    └─────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘

              DEPENDENCY RULE: Внутрь только! ───────▶
```

### 📋 Dependency Rule

**Зависимости могут указывать только ВНУТРЬ:**

```
Frameworks ────▶ Interface Adapters ────▶ Use Cases ────▶ Entities
   (DB, Web)        (Controllers)         (Business)      (Domain)
```

**НИКОГДА НЕ НАОБОРОТ!**

### 🏛️ Слои Clean Architecture

#### 1. **Entities (Enterprise Business Rules)**
```java
// Чистая бизнес-логика, не зависит ни от чего
public class Order {
    private OrderId id;
    private UserId userId;
    private List<OrderItem> items;
    private OrderStatus status;
    private Money totalAmount;
    
    public void addItem(Product product, int quantity) {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Cannot modify confirmed order");
        }
        items.add(new OrderItem(product, quantity));
        recalculateTotal();
    }
    
    public void confirm() {
        if (items.isEmpty()) {
            throw new IllegalStateException("Cannot confirm empty order");
        }
        if (totalAmount.isZero()) {
            throw new IllegalStateException("Cannot confirm zero amount order");
        }
        status = OrderStatus.CONFIRMED;
    }
    
    private void recalculateTotal() {
        totalAmount = items.stream()
            .map(OrderItem::getSubtotal)
            .reduce(Money.ZERO, Money::add);
    }
}
```

#### 2. **Use Cases (Application Business Rules)**
```java
// Оркестрация бизнес-логики
public class CreateOrderUseCase {
    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;
    private final PaymentService paymentService;
    private final OrderConfirmationEmailSender emailSender;
    
    public OrderId execute(CreateOrderCommand command) {
        // 1. Валидация
        User user = validateUserExists(command.getUserId());
        List<Product> products = validateProductsExist(command.getItems());
        
        // 2. Создание заказа (бизнес-логика в Entity)
        Order order = new Order(user.getId());
        command.getItems().forEach(item -> {
            Product product = findProduct(products, item.getProductId());
            order.addItem(product, item.getQuantity());
        });
        
        // 3. Подтверждение заказа
        order.confirm();
        
        // 4. Сохранение
        orderRepository.save(order);
        
        // 5. Побочные эффекты
        paymentService.createPaymentRequest(order);
        emailSender.sendConfirmation(order);
        
        return order.getId();
    }
}
```

#### 3. **Interface Adapters**
```java
// Контроллер - адаптер между веб-слоем и use case
@RestController
public class OrderController {
    private final CreateOrderUseCase createOrderUseCase;
    
    @PostMapping("/orders")
    public ResponseEntity<OrderResponse> createOrder(
            @RequestBody CreateOrderRequest request) {
        
        // Преобразование DTO в команду
        CreateOrderCommand command = CreateOrderCommand.builder()
            .userId(UserId.of(request.getUserId()))
            .items(request.getItems().stream()
                .map(this::toOrderItem)
                .collect(toList()))
            .build();
        
        // Выполнение use case
        OrderId orderId = createOrderUseCase.execute(command);
        
        // Преобразование результата в DTO
        return ResponseEntity.ok(
            OrderResponse.builder()
                .orderId(orderId.getValue())
                .build()
        );
    }
}

// Repository - адаптер между use case и базой данных
@Repository
public class JpaOrderRepository implements OrderRepository {
    
    @Override
    public void save(Order order) {
        OrderEntity entity = orderMapper.toEntity(order);
        jpaRepository.save(entity);
    }
    
    @Override
    public Optional<Order> findById(OrderId orderId) {
        return jpaRepository.findById(orderId.getValue())
            .map(orderMapper::toDomain);
    }
}
```

#### 4. **Frameworks & Drivers**
```java
// Конфигурация Spring
@Configuration
public class OrderConfiguration {
    
    @Bean
    public CreateOrderUseCase createOrderUseCase(
            OrderRepository orderRepository,
            ProductRepository productRepository,
            PaymentService paymentService,
            OrderConfirmationEmailSender emailSender) {
        
        return new CreateOrderUseCase(
            orderRepository,
            productRepository, 
            paymentService,
            emailSender
        );
    }
}
```

### 🔄 Data Flow в Clean Architecture

```
1. REQUEST
   HTTP Request ──▶ Controller (Interface Adapter)
                           │
                           ▼
2. COMMAND/QUERY  
   DTO ──▶ Command/Query Object ──▶ Use Case (Application Layer)
                                          │
                                          ▼
3. BUSINESS LOGIC
   Use Case ──▶ Entity (Enterprise Layer) ──▶ Business Rules
        │                                           │
        ▼                                           ▼
4. DATA ACCESS                                  SIDE EFFECTS
   Repository Interface ──▶ Repository Impl     Email Service
        │                      │                     │
        ▼                      ▼                     ▼
   Database Entity ──▶ Database              External API
```

### 🧪 Тестирование в Clean Architecture

#### Testing Pyramid
```
                    ┌─────────────┐
                    │   E2E TESTS │ ◀── Мало, дорогие
                    └─────────────┘
                 ┌─────────────────────┐
                 │ INTEGRATION TESTS   │ ◀── Средне
                 └─────────────────────┘
            ┌─────────────────────────────────┐
            │        UNIT TESTS               │ ◀── Много, быстрые
            └─────────────────────────────────┘
```

**Unit Tests - Entities и Use Cases:**
```java
class OrderTest {
    @Test
    void shouldCalculateTotalCorrectly() {
        Order order = new Order(UserId.of("user1"));
        Product product = new Product("Product1", Money.of(10.0));
        
        order.addItem(product, 2);
        
        assertThat(order.getTotalAmount()).isEqualTo(Money.of(20.0));
    }
}

class CreateOrderUseCaseTest {
    @Mock private OrderRepository orderRepository;
    @Mock private ProductRepository productRepository; 
    @InjectMocks private CreateOrderUseCase useCase;
    
    @Test
    void shouldCreateOrderSuccessfully() {
        // Тест бизнес-логики без внешних зависимостей
    }
}
```

### ✅ Преимущества Clean Architecture

- **Независимость от фреймворков**: Легко заменить Spring на что-то другое
- **Тестируемость**: Бизнес-логика легко тестируется
- **Независимость от UI**: Можно добавить GraphQL, gRPC
- **Независимость от DB**: Легко мигрировать с PostgreSQL на MongoDB
- **Независимость от внешних систем**: Легко мокать

### ⚠️ Вызовы Clean Architecture

- **Сложность**: Много слоев и абстракций
- **Overhead**: Для простых CRUD операций может быть избыточно
- **Learning Curve**: Требует понимания принципов
- **Производительность**: Дополнительные мапинги между слоями

---

## 🎯 Практические задания

### Задание 1: Анализ архитектурного стиля
Проанализируйте существующее приложение и определите:
- Какой архитектурный стиль используется?
- Какие принципы соблюдаются/нарушаются?
- Какие проблемы можно выявить?
- Какие улучшения можно предложить?

### Задание 2: Проектирование системы
Спроектируйте архитектуру для интернет-магазина:
- Выберите подходящий архитектурный стиль
- Обоснуйте свой выбор
- Опишите компоненты системы
- Покажите взаимодействие между компонентами

### Задание 3: Миграция архитектуры
Предложите план миграции монолитного приложения к микросервисам:
- Определите границы сервисов
- Выберите стратегию миграции
- Опишите этапы перехода
- Учтите риски и способы их митигации

### Задание 4: Реализация Clean Architecture
Реализуйте простое приложение для управления задачами (TODO) используя принципы Clean Architecture:
- Создайте слоистую структуру
- Реализуйте Dependency Rule
- Напишите unit и integration тесты
- Продемонстрируйте независимость от фреймворков

---

## 📊 Сравнительная таблица архитектурных стилей

| Критерий | Монолит | Слоистая | Микросервисы | Event-Driven | Hexagonal | Clean |
|----------|---------|----------|--------------|--------------|-----------|-------|
| **Сложность разработки** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Сложность эксплуатации** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Масштабируемость** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Производительность** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Тестируемость** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Гибкость технологий** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Время выхода на рынок** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 🏁 Чек-лист завершения блока

### ✅ Теоретические знания
- [ ] Понимаю эволюцию архитектурных подходов
- [ ] Знаю преимущества и недостатки каждого стиля
- [ ] Могу обосновать выбор архитектуры для проекта
- [ ] Понимаю принципы декомпозиции систем

### ✅ Практические навыки
- [ ] Могу спроектировать монолитную архитектуру
- [ ] Умею проектировать микросервисные системы
- [ ] Понимаю принципы событийной архитектуры
- [ ] Могу применить Hexagonal Architecture
- [ ] Владею принципами Clean Architecture

### ✅ Проектные навыки
- [ ] Могу провести анализ существующей архитектуры
- [ ] Умею планировать миграцию между архитектурными стилями
- [ ] Могу документировать архитектурные решения
- [ ] Понимаю trade-offs разных подходов

---

## 📚 Рекомендуемая литература

1. **"Clean Architecture"** - Robert C. Martin
2. **"Building Microservices"** - Sam Newman  
3. **"Patterns of Enterprise Application Architecture"** - Martin Fowler
4. **"Implementing Domain-Driven Design"** - Vaughn Vernon
5. **"Microservices Patterns"** - Chris Richardson

---

## 🎯 Итоговый результат блока

По завершении этого блока вы будете способны:

**🔍 Анализировать** существующие архитектуры и выявлять их сильные и слабые стороны

**🏗️ Проектировать** системы в различных архитектурных стилях в зависимости от требований

**⚖️ Принимать** обоснованные решения о выборе архитектурного подхода

**🔄 Планировать** миграцию между различными архитектурными стилями

**📋 Применять** архитектурные паттерны для решения конкретных проблем

---

**Время изучения:** 6-7 недель  
**Следующий блок:** Управление зависимостями и модульность