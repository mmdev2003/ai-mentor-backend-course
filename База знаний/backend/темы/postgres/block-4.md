# PostgreSQL Блок 4: Производительность и оптимизация

```
🎯 ЦЕЛЬ БЛОКА: Научиться создавать быстрые и эффективные запросы
⏱️ ПРОДОЛЖИТЕЛЬНОСТЬ: 2-3 недели
📊 СЛОЖНОСТЬ: Средний-Продвинутый уровень
```

---

## 📋 Содержание блока

```
┌─────────────────────────────────────────────────────────────┐
│  БЛОК 4: ПРОИЗВОДИТЕЛЬНОСТЬ И ОПТИМИЗАЦИЯ                  │
├─────────────────────────────────────────────────────────────┤
│  4.1 → Планы выполнения запросов            │ 4-5 дней      │
│  4.2 → Индексы: углубленное изучение        │ 5-6 дней      │
│  4.3 → Статистика и анализ                  │ 3-4 дня       │
│  4.4 → Оптимизация запросов                 │ 5-6 дней      │
│  4.5 → Партиционирование                    │ 4-5 дней      │
└─────────────────────────────────────────────────────────────┘
```

---

## 4.1 Планы выполнения запросов 🔍

### Что такое план выполнения?

План выполнения - это детальное описание того, как PostgreSQL будет выполнять ваш запрос.

```
ЗАПРОС → ПЛАНИРОВЩИК → ПЛАН ВЫПОЛНЕНИЯ → ИСПОЛНЕНИЕ → РЕЗУЛЬТАТ
   ↓           ↓              ↓             ↓           ↓
SELECT *    Анализ      [Seq Scan]     Чтение      Строки
FROM users  статистики  [Hash Join]    данных      данных
WHERE ...   индексов    [Sort]         с диска
```

### 🔧 Команды EXPLAIN

#### Базовый EXPLAIN
```sql
EXPLAIN 
SELECT c.customer_name, COUNT(*)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name;
```

**Результат:**
```
                                    QUERY PLAN
──────────────────────────────────────────────────────────────────
 HashAggregate  (cost=58.35..60.35 rows=200 width=64)
   Group Key: c.customer_name
   ->  Hash Join  (cost=22.50..53.35 rows=1000 width=64)
         Hash Cond: (o.customer_id = c.customer_id)
         ->  Seq Scan on orders o  (cost=0.00..18.10 rows=1000 width=4)
         ->  Hash  (cost=13.00..13.00 rows=200 width=68)
               ->  Seq Scan on customers c  (cost=0.00..13.00 rows=200 width=68)
```

#### EXPLAIN ANALYZE (с реальным выполнением)
```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT c.customer_name, COUNT(*)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name;
```

**Визуализация чтения плана:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Чтение плана СНИЗУ ВВЕРХ                │
├─────────────────────────────────────────────────────────────┤
│  HashAggregate ←── Группировка (самый верхний узел)        │
│       ↑                                                     │
│  Hash Join     ←── Соединение таблиц                       │
│    ↙     ↘                                                  │
│ Seq Scan    Hash                                            │
│ (orders)    (customers)  ←── Сканирование (листья дерева)  │
└─────────────────────────────────────────────────────────────┘
```

### 📊 Типы операций в планах

#### 🔍 Операции сканирования

```
┌──────────────────┬─────────────────────────────────────────┐
│   ТИП СКАНА      │              ОПИСАНИЕ                   │
├──────────────────┼─────────────────────────────────────────┤
│ Seq Scan         │ Последовательное чтение всей таблицы    │
│ Index Scan       │ Чтение через индекс + обращение к табл. │
│ Index Only Scan  │ Данные полностью из индекса             │
│ Bitmap Heap Scan │ Комбинированное сканирование            │
└──────────────────┴─────────────────────────────────────────┘
```

**Визуализация типов сканирования:**
```
Seq Scan:           Index Scan:         Index Only Scan:
┌─────────────┐     ┌─────┐             ┌─────┐
│ ████████████│     │Index│──┐          │Index│
│ ████████████│     └─────┘  │          │ All │
│ ████████████│              ↓          │Data │
│ Вся таблица │     ┌─────────────┐     │Here │
└─────────────┘     │ Table Heap  │     └─────┘
     Медленно       └─────────────┘        Быстро
                        Средне
```

#### 🔗 Операции соединения

```sql
-- Различные алгоритмы JOIN
-- 1. Nested Loop (вложенные циклы)
for each row in table1:
    for each row in table2:
        if join_condition: return row

-- 2. Hash Join (хеширование)
create hash_table from smaller_table
for each row in larger_table:
    lookup in hash_table

-- 3. Merge Join (сортировка-слияние)
sort table1 by join_key
sort table2 by join_key
merge sorted results
```

**Визуализация алгоритмов JOIN:**
```
Nested Loop:          Hash Join:           Merge Join:
┌─────┐               ┌─────┐              ┌─────┐ sort
│  A  │───┐           │  A  │──────┐       │  A  │───────┐
└─────┘   │           └─────┘      │       └─────┘       │
          ↓           ┌─────┐      ↓       ┌─────┐ sort  │
     ┌─────────┐      │  B  │──►[Hash]     │  B  │───────┤
     │  B loop │      └─────┘      │       └─────┘       ↓
     └─────────┘                   ↓                ┌─────────┐
                                [Join]              │  Merge  │
                                                    └─────────┘

Подходит для:         Подходит для:        Подходит для:
- Малые таблицы       - Средние таблицы    - Большие отсорт.
- Есть индексы        - Одна таблица       - таблицы
                        меньше другой
```

### ⚡ Анализ стоимости

```
cost=0.00..18.10 rows=1000 width=64
 ↑        ↑        ↑         ↑
 │        │        │         └─ Средняя ширина строки (байт)
 │        │        └─────────── Ожидаемое количество строк
 │        └──────────────────── Общая стоимость
 └───────────────────────────── Стоимость получения первой строки
```

### 🎯 Практический пример анализа

```sql
-- Медленный запрос
EXPLAIN ANALYZE
SELECT p.product_name, c.category_name, COUNT(*) as order_count
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN order_items oi ON p.product_id = oi.product_id
WHERE p.price > 100
GROUP BY p.product_name, c.category_name
HAVING COUNT(*) > 5
ORDER BY order_count DESC;
```

**Анализ проблем:**
```
┌─────────────────────────────────────────────────────────────┐
│ 🚨 КРАСНЫЕ ФЛАГИ В ПЛАНАХ ВЫПОЛНЕНИЯ:                      │
├─────────────────────────────────────────────────────────────┤
│ • Seq Scan на больших таблицах (>10k строк)               │
│ • Высокое actual_time vs estimated_time                    │
│ • Много строк отфильтровано (rows removed by filter)      │
│ • Nested Loop с большими таблицами                         │
│ • Sort операции с большим объемом данных                   │
│ • Hash операции с превышением work_mem                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 4.2 Индексы: углубленное изучение 📚

### Типы индексов в PostgreSQL

```
ИНДЕКСЫ В POSTGRESQL:
├── B-tree (по умолчанию) ─── Большинство случаев
├── Hash ─────────────────── Точные совпадения (=)
├── GiST ─────────────────── Геометрические данные
├── SP-GiST ──────────────── Разреженные данные
├── GIN ──────────────────── Составные значения (JSON, массивы)
└── BRIN ─────────────────── Очень большие таблицы
```

### 🌳 B-tree индексы (основные)

```sql
-- Создание B-tree индекса
CREATE INDEX idx_products_price ON products(price);
```

**Структура B-tree:**
```
                    [50|100]
                   /    |    \
              [25|35]  [75]  [125|150]
             /  |  \    |    /    |    \
        [10][30][40][85]  [110][140][200]
         |   |   |   |     |    |    |
        Data Data...      Data Data Data
```

**Когда использовать B-tree:**
```
✅ ПОДХОДИТ ДЛЯ:               ❌ НЕ ПОДХОДИТ ДЛЯ:
• =, <, <=, >, >=             • LIKE '%text%' (начинается не с начала)
• BETWEEN                     • Функции от столбца (без функц. индекса)
• IN                         • OR условия между разными столбцами
• ORDER BY                   • Очень редко используемые столбцы
• LIKE 'text%'              • Часто изменяемые данные
```

### 🔤 Hash индексы

```sql
-- Hash индекс для точных совпадений
CREATE INDEX idx_users_email_hash ON users USING HASH(email);
```

**Визуализация Hash индекса:**
```
Значение → Hash функция → Bucket
┌─────────┐    ┌─────┐    ┌─────────┐
│'john@...'│───►│Hash │───►│ Bucket 1│
├─────────┤    └─────┘    ├─────────┤
│'mary@...'│───►         ►│ Bucket 2│
├─────────┤              ├─────────┤
│'bob@...' │───►         ►│ Bucket 3│
└─────────┘              └─────────┘

Только для оператора =
Очень быстрый поиск O(1)
```

### 🔍 GIN индексы (для составных данных)

```sql
-- GIN для JSON
CREATE INDEX idx_products_attributes_gin 
ON products USING GIN(attributes);

-- GIN для полнотекстового поиска
CREATE INDEX idx_products_search_gin 
ON products USING GIN(to_tsvector('english', product_name));

-- GIN для массивов
CREATE INDEX idx_tags_gin ON articles USING GIN(tags);
```

**Применение GIN:**
```sql
-- Поиск в JSON
SELECT * FROM products 
WHERE attributes @> '{"color": "red"}';

-- Поиск в массивах
SELECT * FROM articles 
WHERE tags && ARRAY['postgresql', 'database'];
```

### 📊 BRIN индексы (для больших таблиц)

```sql
-- BRIN для логов с временными метками
CREATE INDEX idx_logs_timestamp_brin 
ON logs USING BRIN(created_at);
```

**Структура BRIN:**
```
Физические блоки таблицы:
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Block 1-10  │ Block 11-20 │ Block 21-30 │ Block 31-40 │
│ 2024-01-01  │ 2024-01-02  │ 2024-01-03  │ 2024-01-04  │
│ to          │ to          │ to          │ to          │
│ 2024-01-01  │ 2024-01-02  │ 2024-01-03  │ 2024-01-04  │
└─────────────┴─────────────┴─────────────┴─────────────┘

BRIN индекс хранит только диапазоны:
┌─────────────────────────────────────────────────────────────┐
│ Блоки 1-10: MIN=2024-01-01, MAX=2024-01-01                 │
│ Блоки 11-20: MIN=2024-01-02, MAX=2024-01-02                │
│ Блоки 21-30: MIN=2024-01-03, MAX=2024-01-03                │
└─────────────────────────────────────────────────────────────┘
```

### 🎯 Составные и функциональные индексы

#### Составные индексы
```sql
-- Порядок столбцов ВАЖЕН!
CREATE INDEX idx_orders_customer_date 
ON orders(customer_id, order_date);

-- Этот индекс эффективен для:
-- ✅ WHERE customer_id = 123
-- ✅ WHERE customer_id = 123 AND order_date > '2024-01-01'
-- ❌ WHERE order_date > '2024-01-01' (только)
```

**Визуализация составного индекса:**
```
Индекс на (customer_id, order_date):

customer_id │ order_date │ Row Pointer
───────────┼────────────┼────────────
     1     │ 2024-01-01 │ ──►Row 1
     1     │ 2024-01-05 │ ──►Row 3
     1     │ 2024-01-10 │ ──►Row 7
     2     │ 2024-01-02 │ ──►Row 2
     2     │ 2024-01-08 │ ──►Row 5
```

#### Функциональные индексы
```sql
-- Индекс на результат функции
CREATE INDEX idx_users_lower_email 
ON users(lower(email));

-- Индекс на выражение
CREATE INDEX idx_orders_total_with_tax 
ON orders((total_amount * 1.2));

-- Частичный индекс
CREATE INDEX idx_active_users 
ON users(last_login) 
WHERE status = 'active';
```

### 📈 Мониторинг использования индексов

```sql
-- Статистика использования индексов
SELECT 
    indexrelname as index_name,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched,
    idx_scan as scans
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Неиспользуемые индексы
SELECT 
    indexrelname as index_name,
    relname as table_name,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes 
JOIN pg_index USING (indexrelid)
WHERE idx_scan = 0 
AND indisunique = false;
```

---

## 4.3 Статистика и анализ 📊

### Роль статистики в PostgreSQL

```
ПЛАНИРОВЩИК ЗАПРОСОВ
        ↓
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   СТАТИСТИКА    │───►│ ОЦЕНКА СТРОК    │───►│ ВЫБОР ПЛАНА     │
│                 │    │                 │    │                 │
│ • Кол-во строк  │    │ • Селективность │    │ • Seq vs Index  │
│ • Распределение │    │ • Join size     │    │ • Join алгоритм │
│ • Корреляция    │    │ • Sort cost     │    │ • Порядок Join  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔄 Команда ANALYZE

```sql
-- Обновить статистику для всех таблиц
ANALYZE;

-- Обновить статистику для конкретной таблицы
ANALYZE products;

-- Обновить статистику для конкретных столбцов
ANALYZE products(price, category_id);
```

### 📋 Просмотр статистики

```sql
-- Основная статистика таблицы
SELECT 
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables;

-- Статистика по столбцам
SELECT 
    attname as column_name,
    n_distinct,           -- Количество уникальных значений
    most_common_vals,     -- Самые частые значения
    most_common_freqs,    -- Частоты самых частых значений
    correlation           -- Корреляция с физическим порядком
FROM pg_stats 
WHERE tablename = 'products';
```

**Визуализация корреляции:**
```
Высокая корреляция (0.9):        Низкая корреляция (0.1):
Физический порядок = Логический   Физический ≠ Логический

┌─────┬─────┬─────┬─────┐        ┌─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │        │  3  │  1  │  4  │  2  │
├─────┼─────┼─────┼─────┤        ├─────┼─────┼─────┼─────┤
│  5  │  6  │  7  │  8  │        │  7  │  5  │  8  │  6  │
└─────┴─────┴─────┴─────┘        └─────┴─────┴─────┴─────┘

Index Scan эффективен            Index Scan неэффективен
(последовательное чтение)         (случайное чтение)
```

### ⚙️ Настройка сбора статистики

```sql
-- Увеличить количество записей для статистики
ALTER TABLE products ALTER COLUMN price SET STATISTICS 1000;

-- Настроить автоматическое обновление статистики
-- В postgresql.conf:
-- autovacuum_analyze_scale_factor = 0.1  -- 10% изменений
-- autovacuum_analyze_threshold = 50      -- минимум 50 строк
```

---

## 4.4 Оптимизация запросов ⚡

### 🎯 Основные принципы оптимизации

```
ИЕРАРХИЯ ОПТИМИЗАЦИИ:
1. 📊 Правильная структура данных и индексы
2. 🔍 Эффективные WHERE условия
3. 🔗 Оптимальный порядок JOIN
4. 📈 Минимизация объема данных
5. ⚙️ Настройка параметров сервера
```

### 🔍 Оптимизация WHERE условий

#### ✅ Эффективные паттерны
```sql
-- ✅ Используйте индексы
SELECT * FROM products WHERE category_id = 5;

-- ✅ Диапазоны с индексами
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';

-- ✅ Префиксный поиск
SELECT * FROM customers WHERE customer_name LIKE 'John%';
```

#### ❌ Неэффективные паттерны
```sql
-- ❌ Функции в WHERE (без функционального индекса)
SELECT * FROM customers WHERE UPPER(customer_name) = 'JOHN';

-- ❌ Поиск в середине строки
SELECT * FROM customers WHERE customer_name LIKE '%john%';

-- ❌ OR между разными столбцами
SELECT * FROM products WHERE price > 100 OR category_id = 5;

-- ❌ Неравенство с NULL
SELECT * FROM orders WHERE customer_id != 123; -- не найдет NULL
```

### 🔄 Переписывание запросов

#### Пример 1: OR → UNION
```sql
-- ❌ Медленно
SELECT * FROM products 
WHERE price > 1000 OR category_id IN (1,2,3);

-- ✅ Быстрее
SELECT * FROM products WHERE price > 1000
UNION
SELECT * FROM products WHERE category_id IN (1,2,3);
```

#### Пример 2: EXISTS vs IN
```sql
-- ❌ Может быть медленно с большими подзапросами
SELECT * FROM customers c
WHERE c.customer_id IN (
    SELECT o.customer_id FROM orders o WHERE o.total_amount > 1000
);

-- ✅ Обычно быстрее
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id AND o.total_amount > 1000
);
```

#### Пример 3: Избегание подзапросов
```sql
-- ❌ Коррелированный подзапрос
SELECT c.customer_name,
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count
FROM customers c;

-- ✅ JOIN с агрегацией
SELECT c.customer_name, COALESCE(o.order_count, 0) as order_count
FROM customers c
LEFT JOIN (
    SELECT customer_id, COUNT(*) as order_count
    FROM orders
    GROUP BY customer_id
) o ON c.customer_id = o.customer_id;
```

### 🔗 Оптимизация JOIN операций

```sql
-- ✅ Порядок JOIN: от маленьких к большим
SELECT p.product_name, c.category_name, COUNT(*)
FROM categories c                    -- Маленькая таблица
JOIN products p ON c.category_id = p.category_id
JOIN order_items oi ON p.product_id = oi.product_id  -- Большая
GROUP BY p.product_name, c.category_name;
```

**Визуализация порядка JOIN:**
```
Плохой порядок:                   Хороший порядок:
┌─────────────┐                   ┌─────────────┐
│ orders      │ 1M строк          │ categories  │ 10 строк
│     ↓       │                   │     ↓       │
│ ┌─────────┐ │                   │ ┌─────────┐ │
│ │products │ │ 10K строк         │ │products │ │ 100 строк
│ └─────────┘ │                   │ └─────────┘ │
│     ↓       │                   │     ↓       │
│ ┌─────────┐ │                   │ ┌─────────┐ │
│ │categori.│ │ 10 строк          │ │orders   │ │ 1K строк
│ └─────────┘ │                   │ └─────────┘ │
└─────────────┘                   └─────────────┘
Результат: 1M × 10K операций      Результат: 10 × 100 операций
```

### 📊 Оптимизация агрегации

```sql
-- ✅ Фильтрация перед агрегацией
SELECT category_id, AVG(price)
FROM products
WHERE price > 10  -- Фильтр ДО агрегации
GROUP BY category_id
HAVING AVG(price) < 1000;  -- Фильтр ПОСЛЕ агрегации

-- ✅ Частичные индексы для частых фильтров
CREATE INDEX idx_expensive_products 
ON products(category_id) 
WHERE price > 100;
```

---

## 4.5 Партиционирование 🗂️

### Что такое партиционирование?

Партиционирование - это разделение большой таблицы на несколько физически отдельных, но логически связанных частей.

```
БОЛЬШАЯ ТАБЛИЦА (100M строк)
            ↓
    ПАРТИЦИОНИРОВАНИЕ
            ↓
┌─────────┬─────────┬─────────┬─────────┐
│Партиция │Партиция │Партиция │Партиция │
│   Q1    │   Q2    │   Q3    │   Q4    │
│ 25M строк│ 25M строк│ 25M строк│ 25M строк│
└─────────┴─────────┴─────────┴─────────┘
```

### 🗓️ Партиционирование по диапазону (Range)

```sql
-- Создание родительской таблицы
CREATE TABLE orders (
    order_id SERIAL,
    customer_id INTEGER,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Создание партиций
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE orders_2024_q3 PARTITION OF orders
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE orders_2024_q4 PARTITION OF orders
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');
```

**Визуализация Range партиционирования:**
```
        orders (родительская таблица)
               ↓ PARTITION BY RANGE (order_date)
┌──────────────────────────────────────────────────────────┐
│ orders_2024_q1 │ orders_2024_q2 │ orders_2024_q3 │ ... │
│ 2024-01-01     │ 2024-04-01     │ 2024-07-01     │     │
│     TO         │     TO         │     TO         │     │
│ 2024-04-01     │ 2024-07-01     │ 2024-10-01     │     │
└──────────────────────────────────────────────────────────┘

Запрос: WHERE order_date = '2024-02-15'
         ↓ Partition Pruning
    Сканируется только orders_2024_q1
```

### 📝 Партиционирование по списку (List)

```sql
-- Партиционирование по региону
CREATE TABLE sales (
    sale_id SERIAL,
    region VARCHAR(50) NOT NULL,
    sale_date DATE,
    amount DECIMAL(10,2)
) PARTITION BY LIST (region);

CREATE TABLE sales_north PARTITION OF sales
    FOR VALUES IN ('North', 'Northeast', 'Northwest');

CREATE TABLE sales_south PARTITION OF sales
    FOR VALUES IN ('South', 'Southeast', 'Southwest');

CREATE TABLE sales_international PARTITION OF sales
    FOR VALUES IN ('Europe', 'Asia', 'Australia');
```

### #️⃣ Партиционирование по хешу (Hash)

```sql
-- Равномерное распределение данных
CREATE TABLE user_sessions (
    session_id BIGSERIAL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP,
    data JSONB
) PARTITION BY HASH (user_id);

CREATE TABLE user_sessions_0 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE user_sessions_1 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE user_sessions_2 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE user_sessions_3 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

**Визуализация Hash партиционирования:**
```
user_id → HASH(user_id) % 4 → Партиция

user_id: 1001 → hash % 4 = 1 → user_sessions_1
user_id: 1002 → hash % 4 = 2 → user_sessions_2  
user_id: 1003 → hash % 4 = 3 → user_sessions_3
user_id: 1004 → hash % 4 = 0 → user_sessions_0

Равномерное распределение данных между партициями
```

### 🔍 Partition Pruning (Исключение партиций)

```sql
-- Проверка исключения партиций
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-02-01' AND '2024-02-28';
```

**Результат с partition pruning:**
```
Append  (cost=0.00..41.88 rows=11 width=20) (actual time=0.012..0.014 rows=5 loops=1)
  ->  Seq Scan on orders_2024_q1  (cost=0.00..41.88 rows=11 width=20) (actual time=0.011..0.013 rows=5 loops=1)
       Filter: ((order_date >= '2024-02-01'::date) AND (order_date <= '2024-02-28'::date))

Buffers: shared hit=1
Planning time: 1.131 ms
Execution time: 0.043 ms

Обратите внимание: сканируется только одна партиция!
```

### 🔧 Обслуживание партиций

```sql
-- Добавление новой партиции
CREATE TABLE orders_2025_q1 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

-- Удаление старой партиции
DROP TABLE orders_2023_q1;

-- Автоматическое создание партиций (расширение pg_partman)
-- Detach партиции для архивирования
ALTER TABLE orders DETACH PARTITION orders_2023_q1;
```

### 📊 Мониторинг партиций

```sql
-- Размеры партиций
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE tablename LIKE 'orders_%'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Количество строк в партициях
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserted_rows,
    n_live_tup as live_rows
FROM pg_stat_user_tables 
WHERE relname LIKE 'orders_%';
```

---

## 🎯 Практические задания

### Задание 1: Анализ медленного запроса
```sql
-- Оптимизируйте этот запрос:
SELECT c.customer_name, p.product_name, SUM(oi.quantity * oi.price)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id  
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
  AND p.category_id IN (1, 2, 3, 4, 5)
GROUP BY c.customer_name, p.product_name
HAVING SUM(oi.quantity * oi.price) > 1000
ORDER BY SUM(oi.quantity * oi.price) DESC;
```

**Шаги для оптимизации:**
1. Выполните EXPLAIN ANALYZE
2. Определите узкие места
3. Создайте необходимые индексы
4. Переместите фильтры WHERE в подзапросы при необходимости

### Задание 2: Партиционирование таблицы логов
```sql
-- Создайте партиционированную таблицу для системных логов
-- Требования:
-- • Партиционирование по месяцам
-- • Автоматическое исключение старых партиций
-- • Оптимальные индексы для каждой партиции
```

### Задание 3: Оптимизация индексов
```sql
-- Найдите неиспользуемые индексы в вашей БД
-- Предложите план оптимизации индексной стратегии
```

---

## ✅ Чек-лист освоения блока

```
□ Умею читать и анализировать планы выполнения
□ Понимаю различия между типами индексов
□ Знаю когда использовать каждый тип индекса
□ Умею оптимизировать WHERE условия
□ Понимаю принципы эффективного JOIN
□ Знаю основы партиционирования
□ Умею настраивать сбор статистики
□ Могу выявлять и устранять узкие места в запросах
```

---

## 🔧 Инструменты для анализа производительности

```
┌─────────────────────────────────────────────────────────────┐
│                    ИНСТРУМЕНТЫ                              │
├─────────────────┬───────────────────────────────────────────┤
│ pg_stat_*       │ Встроенная статистика PostgreSQL         │
│ EXPLAIN ANALYZE │ Анализ планов выполнения                  │
│ pgbench         │ Нагрузочное тестирование                  │
│ pg_stat_statements │ Анализ самых медленных запросов        │
│ pgAdmin         │ Графический интерфейс мониторинга         │
│ DataGrip        │ IDE с анализом производительности         │
└─────────────────┴───────────────────────────────────────────┘
```

---

## 🚀 Следующий блок

**Блок 5: Программирование в PostgreSQL**
- Введение в PL/pgSQL
- Функции и процедуры
- Триггеры и их применение

```
🎓 РЕЗУЛЬТАТ БЛОКА 4:
Способность анализировать и оптимизировать производительность БД,
умение работать с большими объемами данных
```