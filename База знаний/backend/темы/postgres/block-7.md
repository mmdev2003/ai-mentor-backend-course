# 🚀 Блок 7: Экспертные возможности PostgreSQL

---

**🎯 Цель:** Освоить продвинутые функции PostgreSQL  
**⏱️ Продолжительность:** 3-4 недели  
**📊 Сложность:** Эксперт  
**🔧 Предварительные требования:** Завершение блоков 1-6

---

## 📋 Содержание блока

```
7.1 JSON и JSONB ................................. 5-6 дней
7.2 Полнотекстовый поиск ......................... 4-5 дней  
7.3 Расширения PostgreSQL ....................... 4-5 дней
7.4 Сложные типы данных ......................... 4-5 дней
7.5 Интеграция и Foreign Data Wrappers ......... 4-5 дней
7.6 Продвинутые техники ......................... 5-6 дней
```

---

## 📖 Глава 7.1: JSON и JSONB

**⏱️ Продолжительность:** 5-6 дней  
**🎯 Цель:** Освоить работу с JSON данными в PostgreSQL

### 🔍 Теоретическая часть

#### Различия между JSON и JSONB

```
┌─────────────────┬────────────────────┬────────────────────┐
│    Аспект       │        JSON        │       JSONB        │
├─────────────────┼────────────────────┼────────────────────┤
│ Хранение        │ Текстовый формат   │ Бинарный формат    │
│ Производит.     │ Медленнее          │ Быстрее            │
│ Индексы         │ Не поддерживает    │ Поддерживает GIN   │
│ Порядок ключей  │ Сохраняется        │ Не гарантируется   │
│ Дубли ключей    │ Сохраняются        │ Удаляются          │
│ Размер          │ Больше             │ Меньше             │
└─────────────────┴────────────────────┴────────────────────┘
```

#### Основные операторы для работы с JSON

```sql
-- Операторы доступа
->    -- Получить значение JSON по ключу/индексу (возвращает JSON)
->>   -- Получить значение JSON по ключу/индексу (возвращает TEXT)
#>    -- Получить значение JSON по пути (возвращает JSON)
#>>   -- Получить значение JSON по пути (возвращает TEXT)

-- Операторы проверки
?     -- Существует ли ключ верхнего уровня?
?|    -- Существует ли любой из ключей?
?&    -- Существуют ли все ключи?
@>    -- Содержит ли левый JSON правый?
<@    -- Содержится ли левый JSON в правом?
```

### 💻 Практические примеры

#### Создание таблицы с JSON данными

```sql
-- Создаем таблицу для хранения информации о продуктах
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Вставляем тестовые данные
INSERT INTO products (name, details) VALUES 
('Smartphone', '{"brand": "Apple", "model": "iPhone 14", "specs": {"ram": "6GB", "storage": "128GB"}, "colors": ["black", "white", "red"], "price": 999}'),
('Laptop', '{"brand": "Dell", "model": "XPS 13", "specs": {"ram": "16GB", "storage": "512GB", "cpu": "Intel i7"}, "colors": ["silver", "black"], "price": 1299}'),
('Tablet', '{"brand": "Samsung", "model": "Galaxy Tab S8", "specs": {"ram": "8GB", "storage": "256GB"}, "colors": ["gray", "pink"], "price": 699}');
```

#### Базовые операции с JSON

```sql
-- Получение значений по ключу
SELECT name, details->'brand' as brand FROM products;
SELECT name, details->>'brand' as brand_text FROM products;

-- Работа с вложенными объектами
SELECT name, details#>'{specs,ram}' as ram FROM products;
SELECT name, details#>>'{specs,ram}' as ram_text FROM products;

-- Работа с массивами
SELECT name, details->'colors' as colors FROM products;
SELECT name, details->'colors'->0 as first_color FROM products;
```

#### Поиск и фильтрация

```sql
-- Поиск по ключу
SELECT * FROM products WHERE details ? 'brand';

-- Поиск по значению
SELECT * FROM products WHERE details->>'brand' = 'Apple';

-- Поиск по цене
SELECT * FROM products WHERE (details->>'price')::numeric > 800;

-- Проверка содержания
SELECT * FROM products WHERE details @> '{"brand": "Apple"}';

-- Поиск в массиве
SELECT * FROM products WHERE details->'colors' ? 'black';
```

#### Агрегатные функции для JSON

```sql
-- json_agg - агрегация в JSON массив
SELECT json_agg(name) as product_names FROM products;

-- json_object_agg - агрегация в JSON объект
SELECT json_object_agg(name, details->>'price') as price_list FROM products;

-- jsonb_agg с группировкой
SELECT 
    details->>'brand' as brand,
    jsonb_agg(name) as products
FROM products 
GROUP BY details->>'brand';
```

#### Модификация JSON данных

```sql
-- Добавление нового ключа
UPDATE products 
SET details = details || '{"warranty": "2 years"}'
WHERE details->>'brand' = 'Apple';

-- Обновление существующего значения
UPDATE products 
SET details = jsonb_set(details, '{price}', '899')
WHERE name = 'Smartphone';

-- Удаление ключа
UPDATE products 
SET details = details - 'warranty'
WHERE id = 1;

-- Сложная модификация вложенных объектов
UPDATE products 
SET details = jsonb_set(details, '{specs,ram}', '"8GB"')
WHERE details->>'brand' = 'Samsung';
```

#### Индексы для JSON

```sql
-- GIN индекс для всего JSONB документа
CREATE INDEX idx_products_details ON products USING GIN (details);

-- Индекс для конкретного пути
CREATE INDEX idx_products_brand ON products USING BTREE ((details->>'brand'));

-- Индекс для числовых значений
CREATE INDEX idx_products_price ON products USING BTREE (((details->>'price')::numeric));

-- Проверка использования индекса
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM products WHERE details @> '{"brand": "Apple"}';
```

---

## 🔍 Глава 7.2: Полнотекстовый поиск

**⏱️ Продолжительность:** 4-5 дней  
**🎯 Цель:** Реализовать эффективный полнотекстовый поиск

### 🔍 Теоретическая часть

#### Архитектура полнотекстового поиска

```
┌─────────────────────────────────────────────────────────┐
│                  Полнотекстовый поиск                   │
├─────────────────────┬───────────────────────────────────┤
│     Документ        │          Обработка               │
│   (исходный текст)  │                                   │
├─────────────────────┼───────────────────────────────────┤
│ "PostgreSQL это     │ 1. Парсинг → токены               │
│  мощная СУБД для    │ 2. Нормализация → лексемы         │
│  работы с данными"  │ 3. Создание tsvector              │
├─────────────────────┼───────────────────────────────────┤
│     tsvector        │ 'postgresql':1 'мощн':2 'субд':3  │
│  (поисковый вектор) │ 'работ':5 'данн':7                │
├─────────────────────┼───────────────────────────────────┤
│     tsquery         │ postgresql & (мощная | данные)    │
│  (поисковый запрос) │                                   │
└─────────────────────┴───────────────────────────────────┘
```

#### Основные функции и операторы

```sql
-- Создание tsvector
to_tsvector(config, document)

-- Создание tsquery  
to_tsquery(config, query)
plainto_tsquery(config, query)
phraseto_tsquery(config, query)

-- Операторы поиска
@@    -- Соответствие между tsvector и tsquery
||    -- Конкатенация tsvector
&&    -- И (AND) для tsquery
||    -- ИЛИ (OR) для tsquery  
!!    -- НЕ (NOT) для tsquery
<->   -- Следует за (phrase search)
```

### 💻 Практические примеры

#### Создание таблицы для полнотекстового поиска

```sql
-- Создаем таблицу статей блога
CREATE TABLE blog_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100),
    tags VARCHAR(200),
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector
);

-- Вставляем тестовые данные
INSERT INTO blog_posts (title, content, author, tags) VALUES 
('Введение в PostgreSQL', 
 'PostgreSQL это мощная объектно-реляционная система управления базами данных. Она поддерживает SQL стандарт и предлагает множество продвинутых функций для работы с данными.',
 'Иван Петров', 'postgresql, database, sql'),
 
('Оптимизация запросов в PostgreSQL',
 'Производительность базы данных критически важна для любого приложения. В этой статье мы рассмотрим основные техники оптимизации SQL запросов в PostgreSQL.',
 'Мария Сидорова', 'optimization, performance, sql'),
 
('JSON в PostgreSQL', 
 'PostgreSQL предоставляет отличную поддержку для работы с JSON данными. Вы можете хранить, индексировать и запрашивать JSON документы эффективно.',
 'Алексей Козлов', 'json, jsonb, nosql');
```

#### Создание поисковых векторов

```sql
-- Обновляем поисковые векторы
UPDATE blog_posts SET search_vector = 
    to_tsvector('russian', title || ' ' || content || ' ' || tags);

-- Проверяем созданные векторы
SELECT title, search_vector FROM blog_posts LIMIT 1;
```

#### Базовые поисковые запросы

```sql
-- Простой поиск
SELECT title, author 
FROM blog_posts 
WHERE search_vector @@ to_tsquery('russian', 'PostgreSQL');

-- Поиск с несколькими словами (И)
SELECT title, author 
FROM blog_posts 
WHERE search_vector @@ to_tsquery('russian', 'PostgreSQL & данные');

-- Поиск с альтернативами (ИЛИ)
SELECT title, author 
FROM blog_posts 
WHERE search_vector @@ to_tsquery('russian', 'PostgreSQL | MySQL');

-- Поиск фразы
SELECT title, author 
FROM blog_posts 
WHERE search_vector @@ phraseto_tsquery('russian', 'база данных');
```

#### Ранжирование результатов

```sql
-- Функция ts_rank для ранжирования
SELECT 
    title,
    author,
    ts_rank(search_vector, to_tsquery('russian', 'PostgreSQL')) as rank
FROM blog_posts 
WHERE search_vector @@ to_tsquery('russian', 'PostgreSQL')
ORDER BY rank DESC;

-- Улучшенное ранжирование с ts_rank_cd
SELECT 
    title,
    author,
    ts_rank_cd(search_vector, to_tsquery('russian', 'PostgreSQL & база')) as rank
FROM blog_posts 
WHERE search_vector @@ to_tsquery('russian', 'PostgreSQL & база')
ORDER BY rank DESC;

-- Выделение найденных слов
SELECT 
    title,
    ts_headline('russian', content, to_tsquery('russian', 'PostgreSQL'), 
                'MaxWords=20, MinWords=5') as headline
FROM blog_posts 
WHERE search_vector @@ to_tsquery('russian', 'PostgreSQL');
```

#### Создание индексов для полнотекстового поиска

```sql
-- GIN индекс для tsvector
CREATE INDEX idx_blog_search ON blog_posts USING GIN (search_vector);

-- Функциональный индекс для динамического поиска
CREATE INDEX idx_blog_content_search ON blog_posts 
USING GIN (to_tsvector('russian', title || ' ' || content));

-- Проверка использования индекса
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM blog_posts 
WHERE search_vector @@ to_tsquery('russian', 'PostgreSQL');
```

#### Автоматическое обновление поисковых векторов

```sql
-- Функция для обновления поискового вектора
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('russian', 
        COALESCE(NEW.title, '') || ' ' || 
        COALESCE(NEW.content, '') || ' ' || 
        COALESCE(NEW.tags, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для автоматического обновления
CREATE TRIGGER trigger_update_search_vector
    BEFORE INSERT OR UPDATE ON blog_posts
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();
```

---

## 🧩 Глава 7.3: Расширения PostgreSQL

**⏱️ Продолжительность:** 4-5 дней  
**🎯 Цель:** Освоить работу с расширениями PostgreSQL

### 🔍 Популярные расширения

```
┌─────────────────┬──────────────────────────────────────────┐
│   Расширение    │                Назначение                │
├─────────────────┼──────────────────────────────────────────┤
│ PostGIS         │ Геопространственные данные               │
│ pgcrypto        │ Криптографические функции                │
│ uuid-ossp       │ Генерация UUID                           │
│ hstore          │ Ключ-значение в одном поле               │
│ pg_stat_state   │ Расширенная статистика                   │
│ pg_trgm         │ Поиск по триграммам                      │
│ fuzzystrmatch   │ Нечеткое сравнение строк                 │
│ citext          │ Нечувствительный к регистру текст        │
│ ltree           │ Иерархические структуры                  │
│ pg_partman      │ Управление партициями                    │
└─────────────────┴──────────────────────────────────────────┘
```

### 💻 Практические примеры

#### Работа с UUID

```sql
-- Установка расширения
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Просмотр доступных функций
\dx+ uuid-ossp

-- Создание таблицы с UUID
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Вставка данных
INSERT INTO users (username, email) VALUES 
('user1', 'user1@example.com'),
('user2', 'user2@example.com');

-- Генерация различных типов UUID
SELECT 
    uuid_generate_v1() as uuid_v1,
    uuid_generate_v4() as uuid_v4,
    uuid_nil() as uuid_nil;
```

#### Криптография с pgcrypto

```sql
-- Установка расширения
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Хеширование паролей
CREATE TABLE user_accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Функция для регистрации пользователя
CREATE OR REPLACE FUNCTION register_user(
    p_username VARCHAR(50),
    p_password TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    INSERT INTO user_accounts (username, password_hash)
    VALUES (p_username, crypt(p_password, gen_salt('bf', 8)));
    RETURN TRUE;
EXCEPTION
    WHEN unique_violation THEN
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Функция для проверки пароля
CREATE OR REPLACE FUNCTION check_password(
    p_username VARCHAR(50),
    p_password TEXT
) RETURNS BOOLEAN AS $$
DECLARE
    stored_hash TEXT;
BEGIN
    SELECT password_hash INTO stored_hash 
    FROM user_accounts 
    WHERE username = p_username;
    
    IF stored_hash IS NULL THEN
        RETURN FALSE;
    END IF;
    
    RETURN stored_hash = crypt(p_password, stored_hash);
END;
$$ LANGUAGE plpgsql;

-- Использование
SELECT register_user('john_doe', 'secret123');
SELECT check_password('john_doe', 'secret123'); -- TRUE
SELECT check_password('john_doe', 'wrong');     -- FALSE
```

#### Нечеткий поиск с pg_trgm

```sql
-- Установка расширения
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Создание таблицы товаров
CREATE TABLE products_search (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT
);

INSERT INTO products_search (name, description) VALUES 
('iPhone 14 Pro', 'Смартфон Apple с камерой 48 МП'),
('Samsung Galaxy S23', 'Флагманский Android смартфон'),
('MacBook Pro 16', 'Ноутбук Apple для профессионалов'),
('Dell XPS 13', 'Ультрабук с процессором Intel');

-- Создание индекса для триграмм
CREATE INDEX idx_products_name_trgm ON products_search 
USING GIN (name gin_trgm_ops);

-- Нечеткий поиск по названию
SELECT name, similarity(name, 'iphone') as sim
FROM products_search
WHERE name % 'iphone'
ORDER BY sim DESC;

-- Поиск с пороговым значением
SET pg_trgm.similarity_threshold = 0.3;

SELECT name, similarity(name, 'macbok') as sim
FROM products_search
WHERE name % 'macbok'
ORDER BY sim DESC;
```

#### Работа с hstore

```sql
-- Установка расширения
CREATE EXTENSION IF NOT EXISTS hstore;

-- Создание таблицы с hstore
CREATE TABLE product_attributes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    attributes hstore
);

-- Вставка данных
INSERT INTO product_attributes (name, attributes) VALUES 
('Laptop', 'brand=>Dell, ram=>16GB, ssd=>512GB, color=>black'),
('Phone', 'brand=>Apple, model=>iPhone14, storage=>128GB, color=>blue');

-- Поиск по атрибутам
SELECT name FROM product_attributes 
WHERE attributes ? 'brand';

SELECT name FROM product_attributes 
WHERE attributes->'brand' = 'Apple';

SELECT name FROM product_attributes 
WHERE attributes @> 'brand=>Dell';

-- Обновление атрибутов
UPDATE product_attributes 
SET attributes = attributes || 'warranty=>2years'::hstore
WHERE name = 'Laptop';

-- Создание индекса для hstore
CREATE INDEX idx_product_attributes ON product_attributes 
USING GIN (attributes);
```

---

## 🏗️ Глава 7.4: Сложные типы данных

**⏱️ Продолжительность:** 4-5 дней  
**🎯 Цель:** Освоить работу со сложными типами данных

### 🔍 Типы данных

```
┌─────────────────┬──────────────────────────────────────────┐
│      Тип        │              Описание                    │
├─────────────────┼──────────────────────────────────────────┤
│ Массивы         │ Одномерные и многомерные массивы         │
│ Составные типы  │ Пользовательские структуры данных        │
│ Enum типы       │ Перечисления с ограниченным набором      │
│ Range типы      │ Диапазоны значений                       │
│ Домены          │ Пользовательские типы с ограничениями   │
└─────────────────┴──────────────────────────────────────────┘
```

### 💻 Практические примеры

#### Работа с массивами

```sql
-- Создание таблицы с массивами
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    tags TEXT[],
    ratings INTEGER[],
    metadata JSONB
);

-- Вставка данных с массивами
INSERT INTO articles (title, tags, ratings) VALUES 
('PostgreSQL Tutorial', ARRAY['database', 'sql', 'tutorial'], ARRAY[5, 4, 5, 3]),
('Python для начинающих', ARRAY['python', 'programming', 'beginner'], ARRAY[4, 5, 4]);

-- Альтернативный синтаксис вставки
INSERT INTO articles (title, tags, ratings) VALUES 
('JavaScript Guide', '{"javascript", "web", "frontend"}', '{3, 4, 5, 5, 2}');

-- Операции с массивами
SELECT title, array_length(tags, 1) as tag_count FROM articles;

SELECT title FROM articles WHERE 'sql' = ANY(tags);

SELECT title FROM articles WHERE tags @> ARRAY['database'];

-- Добавление элемента в массив
UPDATE articles 
SET tags = array_append(tags, 'advanced')
WHERE title = 'PostgreSQL Tutorial';

-- Удаление элемента из массива
UPDATE articles 
SET tags = array_remove(tags, 'beginner')
WHERE title = 'Python для начинающих';

-- Агрегация массивов
SELECT array_agg(DISTINCT tag) as all_tags
FROM articles, unnest(tags) as tag;
```

#### Создание составных типов

```sql
-- Создание составного типа для адреса
CREATE TYPE address_type AS (
    street VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    postal_code VARCHAR(20)
);

-- Создание составного типа для контакта
CREATE TYPE contact_type AS (
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(100)
);

-- Таблица с составными типами
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address address_type,
    contact contact_type,
    founded_year INTEGER
);

-- Вставка данных
INSERT INTO companies (name, address, contact, founded_year) VALUES 
('TechCorp', 
 ROW('123 Tech Street', 'San Francisco', 'USA', '94102')::address_type,
 ROW('+1-555-0123', 'info@techcorp.com', 'www.techcorp.com')::contact_type,
 2010);

-- Доступ к полям составного типа
SELECT name, (address).city, (contact).email FROM companies;

-- Обновление составного типа
UPDATE companies 
SET address.street = '456 New Tech Ave'
WHERE name = 'TechCorp';
```

#### Enum типы

```sql
-- Создание enum типа для статуса заказа
CREATE TYPE order_status AS ENUM (
    'pending', 'processing', 'shipped', 'delivered', 'cancelled'
);

-- Создание enum типа для приоритета
CREATE TYPE priority_level AS ENUM (
    'low', 'medium', 'high', 'critical'
);

-- Таблица заказов с enum
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    status order_status DEFAULT 'pending',
    priority priority_level DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Вставка данных
INSERT INTO orders (order_number, status, priority) VALUES 
('ORD-001', 'processing', 'high'),
('ORD-002', 'pending', 'low'),
('ORD-003', 'shipped', 'medium');

-- Запросы с enum
SELECT * FROM orders WHERE status = 'processing';

-- Сравнение enum (они упорядочены!)
SELECT * FROM orders WHERE priority >= 'medium';

-- Изменение enum типа (добавление значения)
ALTER TYPE order_status ADD VALUE 'returned' AFTER 'delivered';
```

#### Range типы

```sql
-- Создание таблицы с range типами
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date_range daterange,
    time_range tsrange,
    price_range numrange
);

-- Вставка данных с диапазонами
INSERT INTO events (name, date_range, time_range, price_range) VALUES 
('Tech Conference', '[2024-03-15, 2024-03-17)', 
 '[2024-03-15 09:00, 2024-03-15 18:00)', '[100, 500]'),
('Workshop', '[2024-03-20, 2024-03-20]',
 '[2024-03-20 10:00, 2024-03-20 16:00)', '[50, 150)');

-- Операции с диапазонами
SELECT name FROM events 
WHERE date_range @> '2024-03-16'::date;

-- Пересечение диапазонов
SELECT name FROM events 
WHERE daterange('2024-03-10', '2024-03-20') && date_range;

-- Объединение диапазонов
SELECT name, date_range + daterange('2024-03-18', '2024-03-19') as extended_range
FROM events WHERE name = 'Tech Conference';

-- Эксклюзивные ограничения с диапазонами
CREATE TABLE room_bookings (
    id SERIAL PRIMARY KEY,
    room_number INTEGER,
    booking_period tsrange,
    EXCLUDE USING GIST (room_number WITH =, booking_period WITH &&)
);
```

#### Создание доменов

```sql
-- Домен для email адресов
CREATE DOMAIN email_type AS VARCHAR(100)
CHECK (VALUE ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Домен для положительных чисел
CREATE DOMAIN positive_integer AS INTEGER
CHECK (VALUE > 0);

-- Домен для процентов
CREATE DOMAIN percentage AS NUMERIC(5,2)
CHECK (VALUE >= 0 AND VALUE <= 100);

-- Таблица с доменами
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email email_type UNIQUE NOT NULL,
    age positive_integer,
    performance_rating percentage
);

-- Вставка корректных данных
INSERT INTO employees (name, email, age, performance_rating) VALUES 
('John Doe', 'john.doe@company.com', 30, 85.5);

-- Попытка вставки некорректных данных (вызовет ошибку)
-- INSERT INTO employees (name, email, age) VALUES 
-- ('Jane Smith', 'invalid-email', -5);
```

---

## 🔗 Глава 7.5: Интеграция и Foreign Data Wrappers

**⏱️ Продолжительность:** 4-5 дней  
**🎯 Цель:** Научиться интегрировать PostgreSQL с внешними системами

### 🔍 Архитектура FDW

```
┌─────────────────────────────────────────────────────────┐
│                PostgreSQL сервер                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Локальная │  │  Внешняя    │  │  Внешняя    │      │
│  │   таблица   │  │  таблица 1  │  │  таблица 2  │      │
│  └─────────────┘  └─────┬───────┘  └─────┬───────┘      │
│                         │                │              │
│  ┌─────────────────────┼────────────────┼──────────┐    │
│  │        FDW          │                │          │    │
│  │   (Foreign Data     │                │          │    │
│  │     Wrapper)        │                │          │    │
│  └─────────────────────┼────────────────┼──────────┘    │
└─────────────────────────┼────────────────┼───────────────┘
                          │                │
         ┌────────────────┼────────────────┼───────────────┐
         │                ▼                ▼               │
         │     ┌─────────────────┐  ┌─────────────────┐    │
         │     │   PostgreSQL    │  │      MySQL      │    │
         │     │     Server      │  │     Server      │    │
         │     │   (удаленный)   │  │                 │    │
         │     └─────────────────┘  └─────────────────┘    │
         │                                                 │
         │            Внешние источники данных             │
         └─────────────────────────────────────────────────┘
```

### 💻 Практические примеры

#### postgres_fdw - подключение к другому PostgreSQL

```sql
-- Установка расширения
CREATE EXTENSION postgres_fdw;

-- Создание сервера (подключение к внешней БД)
CREATE SERVER remote_db
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'remote-server.example.com', port '5432', dbname 'production_db');

-- Создание маппинга пользователя
CREATE USER MAPPING FOR current_user
SERVER remote_db
OPTIONS (user 'readonly_user', password 'secret_password');

-- Создание внешней таблицы
CREATE FOREIGN TABLE remote_orders (
    id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20)
) SERVER remote_db
OPTIONS (schema_name 'public', table_name 'orders');

-- Импорт схемы целиком
IMPORT FOREIGN SCHEMA public 
FROM SERVER remote_db 
INTO remote_schema;

-- Использование внешних таблиц
SELECT status, COUNT(*), SUM(total_amount)
FROM remote_orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY status;

-- Объединение локальных и внешних данных
SELECT 
    l.customer_name,
    r.order_date,
    r.total_amount
FROM local_customers l
JOIN remote_orders r ON l.id = r.customer_id
WHERE r.order_date >= '2024-01-01';
```

#### file_fdw - работа с файлами

```sql
-- Установка расширения
CREATE EXTENSION file_fdw;

-- Создание сервера для файлов
CREATE SERVER file_server
FOREIGN DATA WRAPPER file_fdw;

-- Создание внешней таблицы для CSV файла
CREATE FOREIGN TABLE sales_data (
    sale_date DATE,
    product_name VARCHAR(100),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)
) SERVER file_server
OPTIONS (filename '/path/to/sales_data.csv', format 'csv', header 'true');

-- Чтение данных из файла
SELECT 
    product_name,
    SUM(quantity) as total_quantity,
    SUM(total_amount) as total_revenue
FROM sales_data
GROUP BY product_name
ORDER BY total_revenue DESC;

-- Создание внешней таблицы для лог файла
CREATE FOREIGN TABLE access_logs (
    log_line TEXT
) SERVER file_server
OPTIONS (filename '/var/log/application.log', format 'text');

-- Анализ логов
SELECT 
    SUBSTRING(log_line FROM '\[(.*?)\]') as timestamp,
    CASE 
        WHEN log_line LIKE '%ERROR%' THEN 'ERROR'
        WHEN log_line LIKE '%WARN%' THEN 'WARNING'
        ELSE 'INFO'
    END as log_level
FROM access_logs
WHERE log_line LIKE '%2024-03%';
```

#### Создание собственного FDW (концептуально)

```sql
-- Пример концептуального FDW для REST API
-- (требует написания кода на C или использования существующих решений)

-- 1. Создание расширения FDW
CREATE FOREIGN DATA WRAPPER rest_fdw
HANDLER rest_fdw_handler
VALIDATOR rest_fdw_validator;

-- 2. Создание сервера для REST API
CREATE SERVER api_server
FOREIGN DATA WRAPPER rest_fdw
OPTIONS (
    base_url 'https://api.example.com',
    api_key 'your_api_key_here',
    timeout '30'
);

-- 3. Создание внешней таблицы для API endpoint
CREATE FOREIGN TABLE api_users (
    id INTEGER,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP
) SERVER api_server
OPTIONS (endpoint '/users', method 'GET');

-- Использование (как обычную таблицу)
SELECT * FROM api_users WHERE name LIKE '%John%';
```

---

## ⚡ Глава 7.6: Продвинутые техники

**⏱️ Продолжительность:** 5-6 дней  
**🎯 Цель:** Освоить экспертные техники PostgreSQL

### 💻 Практические примеры

#### Lateral Join

```sql
-- Создание тестовых данных
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE employees_advanced (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    salary DECIMAL(10,2),
    hire_date DATE
);

INSERT INTO departments (name) VALUES 
('Engineering'), ('Sales'), ('Marketing'), ('HR');

INSERT INTO employees_advanced (name, department_id, salary, hire_date) VALUES 
('Alice Johnson', 1, 75000, '2020-01-15'),
('Bob Smith', 1, 80000, '2019-03-20'),
('Carol Davis', 1, 70000, '2021-06-10'),
('David Wilson', 2, 60000, '2020-08-05'),
('Eve Brown', 2, 65000, '2019-11-12'),
('Frank Miller', 3, 55000, '2021-02-28');

-- LATERAL JOIN для получения топ-2 сотрудников по зарплате в каждом отделе
SELECT d.name as department, e.name as employee, e.salary
FROM departments d,
LATERAL (
    SELECT name, salary
    FROM employees_advanced ea
    WHERE ea.department_id = d.id
    ORDER BY salary DESC
    LIMIT 2
) e;

-- LATERAL JOIN с агрегатными функциями
SELECT 
    d.name as department,
    stats.avg_salary,
    stats.max_salary,
    stats.employee_count
FROM departments d,
LATERAL (
    SELECT 
        AVG(salary) as avg_salary,
        MAX(salary) as max_salary,
        COUNT(*) as employee_count
    FROM employees_advanced ea
    WHERE ea.department_id = d.id
) stats
WHERE stats.employee_count > 0;
```

#### Материализованные представления

```sql
-- Создание материализованного представления
CREATE MATERIALIZED VIEW department_stats AS
SELECT 
    d.name as department_name,
    COUNT(e.id) as employee_count,
    AVG(e.salary) as avg_salary,
    MIN(e.salary) as min_salary,
    MAX(e.salary) as max_salary,
    SUM(e.salary) as total_salary_cost
FROM departments d
LEFT JOIN employees_advanced e ON d.id = e.department_id
GROUP BY d.id, d.name;

-- Создание индекса для материализованного представления
CREATE INDEX idx_dept_stats_name ON department_stats (department_name);

-- Использование материализованного представления
SELECT * FROM department_stats 
WHERE avg_salary > 60000
ORDER BY avg_salary DESC;

-- Обновление материализованного представления
REFRESH MATERIALIZED VIEW department_stats;

-- Конкурентное обновление (не блокирует чтение)
REFRESH MATERIALIZED VIEW CONCURRENTLY department_stats;

-- Автоматическое обновление через функцию и триггер
CREATE OR REPLACE FUNCTION refresh_department_stats()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY department_stats;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_refresh_dept_stats
    AFTER INSERT OR UPDATE OR DELETE ON employees_advanced
    FOR EACH STATEMENT EXECUTE FUNCTION refresh_department_stats();
```

#### Advisory Locks

```sql
-- Функция с использованием advisory lock
CREATE OR REPLACE FUNCTION process_daily_reports()
RETURNS BOOLEAN AS $$
BEGIN
    -- Попытка получить блокировку
    IF NOT pg_try_advisory_lock(12345) THEN
        RAISE NOTICE 'Process already running, skipping...';
        RETURN FALSE;
    END IF;
    
    -- Выполнение работы
    RAISE NOTICE 'Starting daily report processing...';
    PERFORM pg_sleep(5); -- Имитация долгой работы
    
    -- Освобождение блокировки
    PERFORM pg_advisory_unlock(12345);
    
    RAISE NOTICE 'Daily report processing completed.';
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Тестирование advisory locks
SELECT process_daily_reports();

-- Проверка активных блокировок
SELECT 
    locktype,
    classid,
    objid,
    mode,
    granted,
    pid
FROM pg_locks 
WHERE locktype = 'advisory';
```

#### LISTEN/NOTIFY для асинхронных уведомлений

```sql
-- Функция для отправки уведомлений
CREATE OR REPLACE FUNCTION notify_new_order()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('new_order', 
        json_build_object(
            'order_id', NEW.id,
            'customer_id', NEW.customer_id,
            'total_amount', NEW.total_amount
        )::text
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера для уведомлений
CREATE TRIGGER trigger_notify_new_order
    AFTER INSERT ON remote_orders
    FOR EACH ROW EXECUTE FUNCTION notify_new_order();

-- В приложении или другой сессии:
-- LISTEN new_order;

-- Отправка кастомного уведомления
SELECT pg_notify('custom_channel', 'Custom message here');

-- Функция для обработки уведомлений в PL/pgSQL
CREATE OR REPLACE FUNCTION process_notifications()
RETURNS VOID AS $$
DECLARE
    notification RECORD;
BEGIN
    -- Подписка на канал
    LISTEN new_order;
    
    -- Обработка уведомлений (в реальном приложении это бесконечный цикл)
    FOR notification IN 
        SELECT pg_notification_to_json(payload) as data
        FROM pg_notify_queue 
        WHERE channel = 'new_order'
    LOOP
        RAISE NOTICE 'Received notification: %', notification.data;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

#### Групповые множества (GROUPING SETS)

```sql
-- Продвинутая группировка с GROUPING SETS
SELECT 
    d.name as department,
    EXTRACT(YEAR FROM e.hire_date) as hire_year,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM departments d
JOIN employees_advanced e ON d.id = e.department_id
GROUP BY GROUPING SETS (
    (d.name, EXTRACT(YEAR FROM e.hire_date)), -- По отделам и годам
    (d.name),                                 -- Только по отделам
    (EXTRACT(YEAR FROM e.hire_date)),        -- Только по годам
    ()                                       -- Общий итог
)
ORDER BY d.name NULLS LAST, hire_year NULLS LAST;

-- ROLLUP для иерархической группировки
SELECT 
    d.name as department,
    EXTRACT(YEAR FROM e.hire_date) as hire_year,
    COUNT(*) as employee_count,
    SUM(salary) as total_salary
FROM departments d
JOIN employees_advanced e ON d.id = e.department_id
GROUP BY ROLLUP (d.name, EXTRACT(YEAR FROM e.hire_date))
ORDER BY d.name NULLS LAST, hire_year NULLS LAST;

-- CUBE для всех возможных комбинаций
SELECT 
    d.name as department,
    CASE WHEN salary >= 70000 THEN 'High' ELSE 'Standard' END as salary_tier,
    COUNT(*) as employee_count
FROM departments d
JOIN employees_advanced e ON d.id = e.department_id
GROUP BY CUBE (d.name, CASE WHEN salary >= 70000 THEN 'High' ELSE 'Standard' END)
ORDER BY d.name NULLS LAST, salary_tier NULLS LAST;
```

---

## 🎯 Практические задания блока 7

### 📝 Задание 1: JSON интернет-магазин (2 дня)
```
Создайте систему интернет-магазина с использованием JSONB:
- Таблица products с характеристиками в JSONB
- Поиск товаров по характеристикам  
- Фильтрация по цене, бренду, категории
- Агрегация данных по брендам и категориям
- Создание соответствующих индексов
```

### 📝 Задание 2: Система поиска документов (2 дня)
```
Реализуйте полнотекстовый поиск для документов:
- База документов с заголовками и содержимым
- Автоматическое обновление поисковых векторов
- Ранжирование результатов поиска
- Выделение найденных фрагментов
- Поиск по категориям и тегам
```

### 📝 Задание 3: Система мониторинга с расширениями (1 день)
```
Создайте систему мониторинга используя:
- UUID для идентификаторов
- hstore для метрик
- Криптографию для хеширования данных
- Триграммы для поиска по именам серверов
```

### 📝 Задание 4: Сложные типы для HR системы (1 день)
```
Разработайте HR систему с использованием:
- Составных типов для адресов и контактов
- Enum для статусов сотрудников
- Range типов для периодов работы
- Массивов для навыков и сертификатов
- Доменов для проверки данных
```

### 📝 Задание 5: Интеграция систем через FDW (1-2 дня)
```
Создайте интеграцию между системами:
- Подключение к внешней БД через postgres_fdw
- Чтение данных из CSV файлов через file_fdw
- Объединение локальных и внешних данных
- Создание отчетов на основе интегрированных данных
```

---

## ✅ Результаты блока 7

После завершения блока 7 вы будете владеть:

### 🎯 **Экспертными навыками:**
- Работа с JSON/JSONB для NoSQL сценариев
- Реализация полнотекстового поиска любой сложности  
- Использование и создание расширений PostgreSQL
- Проектирование сложных типов данных
- Интеграция с внешними системами через FDW
- Применение продвинутых техник оптимизации

### 🏆 **Практический опыт:**
- 5+ реальных проектов с экспертными возможностями
- Портфолио интеграционных решений
- Опыт создания высокопроизводительных поисковых систем

### 🚀 **Карьерные перспективы:**
- **Senior Database Developer** - разработка сложных БД решений
- **Database Architect** - проектирование корпоративных архитектур  
- **Data Integration Specialist** - интеграция разнородных систем
- **PostgreSQL Expert/Consultant** - консультирование по сложным задачам

---

## 📖 Дополнительные ресурсы

### **Документация:**
- [PostgreSQL JSON Functions](https://www.postgresql.org/docs/current/functions-json.html)
- [Full Text Search](https://www.postgresql.org/docs/current/textsearch.html)
- [Extensions](https://www.postgresql.org/docs/current/external-extensions.html)
- [Foreign Data Wrappers](https://www.postgresql.org/docs/current/fdwhandler.html)

### **Инструменты:**
- pgAdmin 4 для администрирования
- PostGIS для геоданных
- pg_trgm для нечеткого поиска
- FDW библиотеки для различных систем

---

**🎊 Поздравляем с завершением экспертного блока PostgreSQL!**  
*Теперь вы владеете всеми продвинутыми возможностями PostgreSQL и готовы решать самые сложные задачи в области баз данных.*