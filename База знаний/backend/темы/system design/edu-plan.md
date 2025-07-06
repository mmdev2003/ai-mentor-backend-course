# System Design: Полный курс от новичка до эксперта

**Общая продолжительность:** 28-35 недель (7-9 месяцев)  
**Временные затраты:** 8-12 часов в неделю  
**Уровень:** От начинающего до эксперта

---

## Блок 1: Основы и фундамент
**Продолжительность:** 4-6 недель  
**Цель:** Заложить прочную теоретическую базу и понимание ключевых концепций

### Неделя 1-2: Введение в System Design
#### Глава 1.1: Что такое System Design и зачем он нужен
- **Теория (2 часа):**
  - Определение системного дизайна
  - Почему важно проектировать системы заранее
  - Стоимость изменений на разных этапах
  - Роль архитектора в команде

- **Практика (3 часа):**
  - Анализ архитектуры знакомых приложений (WhatsApp, Instagram)
  - Создание простой диаграммы компонентов веб-приложения

#### Глава 1.2: Основные принципы архитектуры систем
- **Теория (2 часа):**
  - SOLID принципы в контексте систем
  - Separation of Concerns
  - Single Responsibility на уровне сервисов
  - Loose coupling и High cohesion

- **Практика (3 часа):**
  - Рефакторинг монолитной схемы в модульную
  - Выделение ответственностей компонентов

### Неделя 3-4: Сетевые основы и базы данных
#### Глава 1.3: Клиент-серверная архитектура
- **Теория (2 часа):**
  - Модель клиент-сервер
  - Трехуровневая архитектура
  - Тонкий vs толстый клиент
  - Stateless vs Stateful подходы

- **Практика (3 часа):**
  - Проектирование REST API для простого CRUD приложения
  - Диаграмма взаимодействия клиент-сервер

#### Глава 1.4: Протоколы HTTP/HTTPS, TCP/UDP
- **Теория (3 часа):**
  - HTTP методы и статус коды
  - HTTPS и SSL/TLS
  - TCP vs UDP: когда что использовать
  - WebSockets для real-time коммуникации

- **Практика (2 часа):**
  - Анализ HTTP запросов в браузере
  - Проектирование API endpoints

### Неделя 5-6: Хранение данных
#### Глава 1.5: Базы данных: SQL vs NoSQL
- **Теория (3 часа):**
  - Реляционные БД: ACID свойства
  - NoSQL типы: Document, Key-Value, Column-family, Graph
  - CAP теорема (введение)
  - Когда выбирать SQL, когда NoSQL

- **Практика (3 часа):**
  - Проектирование схемы БД для блога
  - Сравнение решения в SQL и NoSQL

#### Глава 1.6: Кэширование: основы и стратегии
- **Теория (2 часа):**
  - Зачем нужно кэширование
  - Уровни кэширования
  - Cache-aside, Write-through, Write-behind
  - TTL и invalidation стратегии

- **Практика (2 часа):**
  - Проектирование кэширования для новостного сайта

### Контрольные задания блока 1:
1. **Проект:** Спроектировать архитектуру простого форума
   - Компоненты системы
   - API endpoints
   - Схема базы данных
   - Стратегия кэширования

2. **Теоретический тест:** 20 вопросов по основам

**Результат блока:** Понимание базовых концепций, умение объяснить архитектуру простых систем, создание первого системного дизайна

---

## Блок 2: Масштабирование и производительность
**Продолжительность:** 3-4 недели  
**Цель:** Научиться проектировать системы, выдерживающие высокие нагрузки

### Неделя 7-8: Стратегии масштабирования
#### Глава 2.1: Горизонтальное и вертикальное масштабирование
- **Теория (2 часа):**
  - Scale Up vs Scale Out
  - Когда достигается потолок вертикального масштабирования
  - Stateless архитектура для горизонтального масштабирования
  - Экономические аспекты масштабирования

- **Практика (3 часа):**
  - Расчет стоимости различных стратегий масштабирования
  - Планирование роста нагрузки

#### Глава 2.2: Load Balancing: алгоритмы и стратегии
- **Теория (3 часа):**
  - L4 vs L7 балансировка
  - Round Robin, Least Connections, IP Hash
  - Health checks и failover
  - Sticky sessions: плюсы и минусы

- **Практика (2 часа):**
  - Проектирование схемы балансировки для веб-приложения
  - Расчет пропускной способности

### Неделя 9: Масштабирование баз данных
#### Глава 2.3: Репликация баз данных
- **Теория (2 часа):**
  - Master-Slave репликация
  - Master-Master репликация
  - Read replicas и их использование
  - Eventual consistency в репликации

- **Практика (2 часа):**
  - Проектирование схемы репликации для высоконагруженного сайта

#### Глава 2.4: Шардирование данных
- **Теория (3 часа):**
  - Горизонтальное разбиение данных
  - Стратегии шардирования: по диапазону, по хэшу, по директории
  - Решение проблемы hot spots
  - Cross-shard запросы и их сложности

- **Практика (2 часа):**
  - Проектирование шардирования для социальной сети

### Неделя 10: Глобальное масштабирование
#### Глава 2.5: CDN и географическое распределение
- **Теория (2 часа):**
  - Content Delivery Networks
  - Edge caching и origin servers
  - Геолокационная маршрутизация
  - Static vs Dynamic content caching

- **Практика (2 часа):**
  - Планирование CDN стратегии для медиа-платформы

#### Глава 2.6: Мониторинг и метрики производительности
- **Теория (2 часа):**
  - Key Performance Indicators (KPI)
  - Latency, Throughput, Error Rate
  - Мониторинг инфраструктуры vs приложения
  - Alerting стратегии

- **Практика (3 часа):**
  - Разработка dashboard для мониторинга системы
  - Настройка alerts для критических метрик

### Контрольные задания блока 2:
1. **Проект:** Масштабирование форума до 1 млн пользователей
   - Стратегия масштабирования
   - Архитектура балансировки
   - План репликации и шардирования
   - Мониторинг план

2. **Кейс-стади:** Анализ падения производительности в существующей системе

**Результат блока:** Способность спроектировать масштабируемую архитектуру для миллионов пользователей, понимание bottlenecks и способов их решения

---

## Блок 3: Надежность и отказоустойчивость
**Продолжительность:** 3-4 недели  
**Цель:** Создавать системы, которые работают стабильно в условиях сбоев

### Неделя 11-12: Теория надежности
#### Глава 3.1: CAP теорема и компромиссы консистентности
- **Теория (3 часа):**
  - Consistency, Availability, Partition tolerance
  - Практические примеры CAP trade-offs
  - BASE vs ACID
  - Eventual consistency модели

- **Практика (2 часа):**
  - Анализ CAP выборов в реальных системах (Amazon, Google)
  - Проектирование системы с разными CAP приоритетами

#### Глава 3.2: Паттерны отказоустойчивости
- **Теория (3 часа):**
  - Circuit Breaker pattern
  - Retry logic с exponential backoff
  - Timeout configuration
  - Bulkhead pattern для изоляции ресурсов

- **Практика (3 часа):**
  - Реализация Circuit Breaker логики
  - Проектирование retry стратегий

### Неделя 13: Backup и Recovery
#### Глава 3.3: Резервное копирование и восстановление
- **Теория (2 часа):**
  - Стратегии backup: Full, Incremental, Differential
  - RTO и RPO метрики
  - Hot vs Cold backup
  - Cross-region backup стратегии

- **Практика (3 часа):**
  - Разработка backup стратегии для критической системы
  - Планирование процедуры восстановления

#### Глава 3.4: Disaster Recovery планирование
- **Теория (2 часа):**
  - Disaster Recovery vs Business Continuity
  - DR тестирование и планирование
  - Multi-region архитектуры
  - Failover vs Failback процедуры

- **Практика (2 часа):**
  - Создание DR плана для финансового приложения

### Неделя 14: Распределенная консистентность
#### Глава 3.5: Distributed consensus (Raft, Paxos)
- **Теория (4 часа):**
  - Проблема византийских генералов
  - Raft consensus algorithm
  - Paxos protocol основы
  - Leader election и log replication

- **Практика (2 часа):**
  - Моделирование Raft алгоритма
  - Анализ consensus в реальных системах

#### Глава 3.6: Eventual consistency и ACID
- **Теория (2 часа):**
  - Strong vs Eventual consistency
  - Conflict resolution стратегии
  - Vector clocks и logical timestamps
  - CRDT (Conflict-free Replicated Data Types)

- **Практика (2 часа):**
  - Проектирование eventually consistent системы

### Контрольные задания блока 3:
1. **Проект:** Проектирование отказоустойчивой системы онлайн-банкинга
   - Анализ точек отказа
   - Стратегии резервирования
   - DR план
   - Consistency требования

2. **Симуляция:** Моделирование сценариев отказов и recovery

**Результат блока:** Умение проектировать высоконадежные системы с минимальным временем простоя, понимание trade-offs в distributed systems

---

## Блок 4: Микросервисы и распределенные системы
**Продолжительность:** 4-5 недель  
**Цель:** Освоить современные подходы к архитектуре сложных систем

### Неделя 15-16: Микросервисная архитектура
#### Глава 4.1: Монолит vs Микросервисы: когда что выбирать
- **Теория (3 часа):**
  - Conway's Law и организационные аспекты
  - Плюсы и минусы микросервисов
  - Критерии для декомпозиции
  - Микросервисы anti-patterns

- **Практика (3 часа):**
  - Декомпозиция монолитного приложения
  - Определение границ сервисов

#### Глава 4.2: Service discovery и коммуникация между сервисами
- **Теория (2 часа):**
  - Client-side vs Server-side discovery
  - Service registry паттерны
  - Health checking и circuit breaking
  - Синхронная vs асинхронная коммуникация

- **Практика (3 часа):**
  - Проектирование service mesh архитектуры
  - Настройка service discovery

### Неделя 17: API Management
#### Глава 4.3: API Gateway и управление трафиком
- **Теория (2 часа):**
  - API Gateway responsibilities
  - Rate limiting и throttling
  - Authentication и authorization
  - Request/Response transformation

- **Практика (3 часа):**
  - Проектирование API Gateway для микросервисов
  - Настройка routing и security правил

### Неделя 18: Event-driven архитектура
#### Глава 4.4: Event-driven архитектура и message queues
- **Теория (3 часа):**
  - Event sourcing и CQRS
  - Message brokers: Kafka, RabbitMQ, AWS SQS
  - Pub/Sub vs Point-to-Point
  - Event ordering и exactly-once delivery

- **Практика (3 часа):**
  - Проектирование event-driven системы для e-commerce
  - Выбор message broker для разных сценариев

#### Глава 4.5: Distributed transactions и Saga pattern
- **Теория (3 часа):**
  - Проблемы распределенных транзакций
  - Two-Phase Commit и его ограничения
  - Saga pattern: Choreography vs Orchestration
  - Compensating actions

- **Практика (2 часа):**
  - Проектирование Saga для процесса заказа
  - Handling failures в распределенных транзакциях

### Неделя 19: Containerization и оркестрация
#### Глава 4.6: Containerization и оркестрация (Docker, Kubernetes)
- **Теория (3 часа):**
  - Контейнеризация vs виртуализация
  - Docker ecosystem
  - Kubernetes архитектура
  - Service mesh (Istio, Linkerd)

- **Практика (3 часа):**
  - Проектирование Kubernetes деплоймента
  - Настройка service mesh для микросервисов

### Контрольные задания блока 4:
1. **Масштабный проект:** Микросервисная архитектура для онлайн-магазина
   - Декомпозиция на сервисы
   - API Gateway дизайн
   - Event-driven взаимодействия
   - Deployment стратегия

2. **Сравнительный анализ:** Монолит vs микросервисы для конкретного бизнес-случая

**Результат блока:** Способность спроектировать сложную микросервисную архитектуру, понимание современных паттернов и инструментов

---

## Блок 5: Безопасность и аутентификация
**Продолжительность:** 2-3 недели  
**Цель:** Обеспечить безопасность проектируемых систем

### Неделя 20-21: Основы безопасности
#### Глава 5.1: Основы информационной безопасности в системах
- **Теория (3 часа):**
  - CIA triad: Confidentiality, Integrity, Availability
  - Threat modeling
  - OWASP Top 10
  - Defense in depth стратегия

- **Практика (2 часа):**
  - Threat modeling для веб-приложения
  - Security checklist разработка

#### Глава 5.2: Аутентификация и авторизация
- **Теория (3 часа):**
  - Authentication vs Authorization
  - OAuth 2.0 и OpenID Connect flows
  - JWT токены: структура и использование
  - Single Sign-On (SSO) архитектуры

- **Практика (3 часа):**
  - Проектирование OAuth2 flow
  - JWT implementation стратегия

### Неделя 22: Защита данных и инфраструктуры
#### Глава 5.3: Encryption: данных в покое и в передаче
- **Теория (2 часа):**
  - Symmetric vs Asymmetric encryption
  - TLS/SSL implementation
  - Database encryption стратегии
  - Key management systems

- **Практика (2 часа):**
  - Проектирование encryption стратегии
  - Key rotation планирование

#### Глава 5.4: Rate limiting и защита от DDoS
- **Теория (2 часа):**
  - Rate limiting алгоритмы
  - DDoS types и защита
  - Web Application Firewall (WAF)
  - Captcha и bot detection

- **Практика (2 часа):**
  - Настройка rate limiting для API
  - DDoS protection планирование

#### Глава 5.5: Security by design принципы
- **Теория (2 часа):**
  - Principle of least privilege
  - Zero trust architecture
  - Security controls в CI/CD
  - Vulnerability management

- **Практика (2 часа):**
  - Security architecture review
  - DevSecOps pipeline дизайн

### Контрольные задания блока 5:
1. **Security audit:** Анализ безопасности существующей архитектуры
2. **Проект:** Secure by design архитектура для финтех приложения

**Результат блока:** Умение встраивать безопасность в архитектуру с самого начала, понимание современных security practices

---

## Блок 6: Проектирование конкретных систем
**Продолжительность:** 5-6 недель  
**Цель:** Применить знания на практике через разбор реальных кейсов

### Неделя 23: Социальные системы
#### Глава 6.1: Проектирование социальной сети (Twitter/Facebook)
- **Практический проект (8 часов):**
  - Требования и ограничения
  - User service и профили
  - Feed generation алгоритмы
  - Timeline архитектуры
  - Media storage и CDN
  - Notifications система
  - Analytics и trending

- **Дополнительные задачи:**
  - Масштабирование до 1 млрд пользователей
  - Real-time обновления
  - Content moderation

### Неделя 24: Коммуникационные системы
#### Глава 6.2: Система чатов и мессенджеров
- **Практический проект (8 часов):**
  - Real-time messaging архитектура
  - WebSocket vs Server-Sent Events
  - Message delivery guarantees
  - Group chats и каналы
  - File sharing и media
  - End-to-end encryption
  - Presence и статусы

- **Дополнительные задачи:**
  - Message history и search
  - Push notifications
  - Cross-platform синхронизация

### Неделя 25: Медиа платформы
#### Глава 6.3: Видеостриминг платформа (YouTube/Netflix)
- **Практический проект (8 часов):**
  - Video upload и processing pipeline
  - Adaptive bitrate streaming
  - CDN стратегия для видео
  - Recommendation engine
  - Content management система
  - DRM и security
  - Analytics и viewing статистика

- **Дополнительные задачи:**
  - Live streaming архитектура
  - Global content distribution
  - Monetization система

### Неделя 26: E-commerce системы
#### Глава 6.4: E-commerce платформа
- **Практический проект (8 часов):**
  - Product catalog и inventory
  - Shopping cart и checkout
  - Payment processing integration
  - Order management система
  - Shipping и logistics
  - Reviews и ratings
  - Fraud detection

- **Дополнительные задачи:**
  - Personalization engine
  - Multi-vendor marketplace
  - International expansion

### Неделя 27: Поисковые системы
#### Глава 6.5: Поисковая система
- **Практический проект (8 часов):**
  - Web crawler архитектура
  - Indexing система
  - Search ranking алгоритмы
  - Query processing
  - Результаты caching
  - Auto-suggestions
  - Search analytics

- **Дополнительные задачи:**
  - Image и video search
  - Real-time indexing
  - Personalized results

### Неделя 28: Transportation и финансовые системы
#### Глава 6.6: Ride-sharing сервис (Uber/Lyft)
- **Практический проект (4 часа):**
  - Location tracking и GPS
  - Matching алгоритм водитель-пассажир
  - Dynamic pricing
  - Real-time trip tracking
  - Payment processing
  - Driver management
  - Safety features

#### Глава 6.7: Финансовая система и платежи
- **Практический проект (4 часа):**
  - Account management
  - Transaction processing
  - Fraud detection система
  - Compliance и audit trails
  - Real-time балансы
  - International transfers
  - Security и encryption

### Контрольные задания блока 6:
1. **Портфолио проектов:** 7 детально проработанных system designs
2. **Презентация:** Защита одного из проектов перед "техническим комитетом"
3. **Peer review:** Анализ проектов других участников

**Результат блока:** Портфолио из 6-7 детально проработанных системных дизайнов, практический опыт решения real-world задач

---

## Блок 7: Экспертный уровень и лидерство
**Продолжительность:** 3-4 недели  
**Цель:** Развить навыки архитектурного лидерства и принятия стратегических решений

### Неделя 29-30: Архитектурное лидерство
#### Глава 7.1: Technology decision making и trade-off анализ
- **Теория (3 часа):**
  - Decision frameworks (TOGAF, ADR)
  - Technical debt quantification
  - ROI анализ для технических решений
  - Stakeholder management

- **Практика (4 часа):**
  - Создание Architecture Decision Records
  - Trade-off анализ для migration проекта
  - Презентация технических решений бизнесу

#### Глава 7.2: Архитектурные ревью и код-ревью на системном уровне
- **Теория (2 часа):**
  - Architecture review процессы
  - Quality gates и checkpoints
  - Design review best practices
  - Collaborative architecture

- **Практика (3 часа):**
  - Проведение architecture review
  - Разработка review checklist
  - Peer architecture review session

### Неделя 31: Legacy и эволюция
#### Глава 7.3: Technical debt management
- **Теория (2 часа):**
  - Technical debt типы и измерение
  - Refactoring vs rewriting стратегии
  - Debt prioritization frameworks
  - Communication с management

- **Практика (3 часа):**
  - Technical debt audit
  - Refactoring roadmap создание
  - Business case для debt reduction

#### Глава 7.4: Организация команд вокруг архитектуры (Conway's Law)
- **Теория (2 часа):**
  - Conway's Law в практике
  - Team topologies
  - Communication patterns
  - Scaling engineering organizations

- **Практика (2 часа):**
  - Organizational design для микросервисов
  - Team interaction mapping

### Неделя 32: Эволюция и карьера
#### Глава 7.5: Эволюция архитектуры и legacy системы
- **Теория (3 часа):**
  - Strangler Fig pattern
  - Blue-green deployments
  - Feature flags для migration
  - Zero-downtime migration стратегии

- **Практика (3 часа):**
  - Migration plan для legacy системы
  - Risk assessment и mitigation

#### Глава 7.6: Подготовка к system design интервью
- **Теория (2 часа):**
  - Структура system design интервью
  - Типичные вопросы и подходы
  - Коммуникация во время интервью
  - Red flags и best practices

- **Практика (4 часа):**
  - Mock interviews
  - Whiteboarding practice
  - Case study презентации
  - Interview feedback анализ

### Итоговые задания блока 7:
1. **Capstone проект:** Архитектурная стратегия для компании на 3 года
2. **Лидерство симуляция:** Ведение архитектурного комитета
3. **Менторинг:** Обучение junior разработчика system design основам
4. **Mock interview:** Проведение system design интервью

**Результат блока:** Готовность к роли Senior/Staff/Principal Engineer, способность проводить архитектурные интервью, лидерские навыки в технической области

---

## Итоговая оценка и сертификация

### Финальный проект (Неделя 33-35)
**Комплексный проект:** Создание архитектуры для стартапа с нуля
- Бизнес-требования анализ
- Technology strategy
- Architecture roadmap на 2 года
- Team organization план
- Risk assessment
- Budget planning
- Implementation phases

### Оценочные критерии:
- **Техническая глубина:** Использование продвинутых концепций
- **Бизнес понимание:** Alignment с бизнес целями
- **Коммуникация:** Качество презентации и документации
- **Практичность:** Реализуемость предложенных решений
- **Инновации:** Использование современных подходов

### Итоговый результат программы:
**Комплексная экспертиза в области системного дизайна** с возможностью:
- Проектировать системы любой сложности и масштаба
- Принимать обоснованные архитектурные решения
- Руководить техническими командами
- Проводить архитектурные интервью
- Консультировать по вопросам технической стратегии
- Развивать архитектурную культуру в организации

---

## Ресурсы для изучения

### Книги:
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Building Microservices" - Sam Newman
- "System Design Interview" - Alex Xu
- "Clean Architecture" - Robert Martin
- "Release It!" - Michael Nygard

### Онлайн ресурсы:
- High Scalability blog
- AWS Architecture Center
- Google Cloud Architecture Framework
- System Design Primer (GitHub)
- Engineering blogs крупных компаний

### Практические инструменты:
- Draw.io для диаграмм
- Miro для collaborative design
- Lucidchart для архитектурных схем
- AWS Well-Architected Tool
- Docker и Kubernetes для практики

### Сообщества:
- Reddit r/ExperiencedDevs
- Hacker News
- Software Architecture Slack communities
- Local meetups по архитектуре и DevOps