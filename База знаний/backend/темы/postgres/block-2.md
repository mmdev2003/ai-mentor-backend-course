# 🏗️ БЛОК 2: СТРУКТУРА ДАННЫХ И МОДИФИКАЦИЯ

```
🎯 ЦЕЛЬ: Научиться создавать и изменять структуру базы данных
⏱️ ПРОДОЛЖИТЕЛЬНОСТЬ: 2-3 недели
📊 СЛОЖНОСТЬ: Начинающий → Средний
```

---

## 📋 СОДЕРЖАНИЕ БЛОКА

```
┌─────────────────────────────────────────────────────────────┐
│  2.1 Создание и изменение таблиц           📅 4-5 дней     │
│  2.2 Ограничения целостности               📅 3-4 дня      │
│  2.3 Индексы                               📅 3-4 дня      │
│  2.4 Модификация данных                    📅 4-5 дней     │
│  2.5 Основы нормализации                   📅 3-4 дня      │
└─────────────────────────────────────────────────────────────┘
```

---

# 🗂️ ГЛАВА 2.1: СОЗДАНИЕ И ИЗМЕНЕНИЕ ТАБЛИЦ

## 🎯 Что изучим:
- Синтаксис CREATE TABLE
- Изменение структуры с ALTER TABLE
- Удаление таблиц DROP TABLE
- Временные таблицы
- Схемы (SCHEMA) в PostgreSQL

---

## 📝 CREATE TABLE - Создание таблиц

### Базовый синтаксис:
```sql
CREATE TABLE имя_таблицы (
    столбец1 тип_данных [ограничения],
    столбец2 тип_данных [ограничения],
    ...
);
```

### 🔧 Практический пример:
```sql
-- Создаем таблицу "Сотрудники"
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE DEFAULT CURRENT_DATE,
    salary DECIMAL(10,2) CHECK (salary > 0),
    department_id INTEGER
);
```

### 📊 Схема таблицы:
```
┌─────────────────────────────────────────────────────────────┐
│                    ТАБЛИЦА: employees                       │
├─────────────────┬───────────────┬─────────────────────────────┤
│ Столбец         │ Тип           │ Ограничения                 │
├─────────────────┼───────────────┼─────────────────────────────┤
│ id              │ SERIAL        │ PRIMARY KEY                 │
│ first_name      │ VARCHAR(50)   │ NOT NULL                    │
│ last_name       │ VARCHAR(50)   │ NOT NULL                    │
│ email           │ VARCHAR(100)  │ UNIQUE                      │
│ hire_date       │ DATE          │ DEFAULT CURRENT_DATE        │
│ salary          │ DECIMAL(10,2) │ CHECK (salary > 0)          │
│ department_id   │ INTEGER       │                             │
└─────────────────┴───────────────┴─────────────────────────────┘
```

---

## 🔄 ALTER TABLE - Изменение структуры

### Добавление столбца:
```sql
-- Добавляем столбец для номера телефона
ALTER TABLE employees 
ADD COLUMN phone VARCHAR(20);
```

### Изменение типа данных:
```sql
-- Увеличиваем размер поля email
ALTER TABLE employees 
ALTER COLUMN email TYPE VARCHAR(150);
```

### Переименование столбца:
```sql
-- Переименовываем столбец
ALTER TABLE employees 
RENAME COLUMN phone TO phone_number;
```

### Удаление столбца:
```sql
-- Удаляем столбец
ALTER TABLE employees 
DROP COLUMN phone_number;
```

---

## 🗑️ DROP TABLE - Удаление таблиц

```sql
-- Простое удаление
DROP TABLE имя_таблицы;

-- Удаление с проверкой существования
DROP TABLE IF EXISTS имя_таблицы;

-- Каскадное удаление (удаляет связанные объекты)
DROP TABLE имя_таблицы CASCADE;
```

---

## ⏰ Временные таблицы

### Локальные временные таблицы:
```sql
-- Создается в текущей сессии, автоматически удаляется
CREATE TEMP TABLE temp_sales (
    sale_id SERIAL,
    product_name VARCHAR(100),
    amount DECIMAL(10,2)
);
```

### Глобальные временные таблицы:
```sql
-- Создается для всех сессий, но данные видны только создателю
CREATE TEMPORARY TABLE session_data (
    session_id VARCHAR(50),
    user_id INTEGER,
    login_time TIMESTAMP
);
```

---

## 🏢 СХЕМЫ (SCHEMA)

### Что такое схема?
```
┌─────────────────────────────────────────────────────────────┐
│                      БАЗА ДАННЫХ                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   СХЕМА: hr     │  │ СХЕМА: sales    │  │ СХЕМА: public│ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌──────────┐ │ │
│  │ │ employees   │ │  │ │ orders      │ │  │ │ users    │ │ │
│  │ │ departments │ │  │ │ products    │ │  │ │ logs     │ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └──────────┘ │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Создание схемы:
```sql
-- Создаем схему для HR отдела
CREATE SCHEMA hr;

-- Создаем таблицу в конкретной схеме
CREATE TABLE hr.employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(50)
);
```

### Работа со схемами:
```sql
-- Установка пути поиска схем
SET search_path TO hr, public;

-- Переключение между схемами
\dn  -- показать все схемы (в psql)
```

---

## 💡 ПРАКТИЧЕСКОЕ ЗАДАНИЕ 2.1

### Задача: Создать структуру интернет-магазина

```sql
-- 1. Создайте схему для интернет-магазина
CREATE SCHEMA shop;

-- 2. Создайте таблицу категорий
CREATE TABLE shop.categories (
    -- Ваш код здесь
);

-- 3. Создайте таблицу товаров
CREATE TABLE shop.products (
    -- Ваш код здесь
);

-- 4. Добавьте столбец "описание" в таблицу товаров
-- Ваш код здесь

-- 5. Переименуйте столбец в более подходящий
-- Ваш код здесь
```

### ✅ Проверочный список:
- [ ] Схема создана
- [ ] Таблицы имеют правильную структуру
- [ ] Использованы подходящие типы данных
- [ ] Добавлены базовые ограничения

---

# 🔒 ГЛАВА 2.2: ОГРАНИЧЕНИЯ ЦЕЛОСТНОСТИ

## 🎯 Что изучим:
- PRIMARY KEY и UNIQUE
- FOREIGN KEY и ссылочная целостность
- CHECK ограничения
- NOT NULL ограничения
- DEFAULT значения

---

## 🗝️ PRIMARY KEY - Первичный ключ

### Определение при создании таблицы:
```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Составной первичный ключ:
```sql
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

### Добавление после создания:
```sql
ALTER TABLE existing_table 
ADD CONSTRAINT pk_existing_table PRIMARY KEY (id);
```

---

## 🔗 FOREIGN KEY - Внешний ключ

### Схема связей:
```
┌─────────────────┐        ┌─────────────────┐
│   CUSTOMERS     │        │     ORDERS      │
├─────────────────┤        ├─────────────────┤
│ customer_id (PK)│◄──────┤│ customer_id (FK)│
│ name            │        │ order_id (PK)   │
│ email           │        │ order_date      │
└─────────────────┘        └─────────────────┘
```

### Создание внешнего ключа:
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE DEFAULT CURRENT_DATE,
    
    -- Определяем внешний ключ
    FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

### Опции для внешних ключей:
```sql
-- При удалении родительской записи:
ON DELETE CASCADE     -- удалить все связанные записи
ON DELETE SET NULL    -- установить NULL в дочерних записях
ON DELETE RESTRICT    -- запретить удаление (по умолчанию)
ON DELETE SET DEFAULT -- установить значение по умолчанию

-- При изменении родительского ключа:
ON UPDATE CASCADE     -- изменить значения в дочерних записях
ON UPDATE SET NULL    -- установить NULL
ON UPDATE RESTRICT    -- запретить изменение
```

---

## ✅ UNIQUE - Уникальность

### Простое ограничение:
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE
);
```

### Составное уникальное ограничение:
```sql
CREATE TABLE user_roles (
    user_id INTEGER,
    role_id INTEGER,
    assigned_date DATE,
    
    UNIQUE (user_id, role_id)  -- пользователь может иметь роль только один раз
);
```

---

## ✔️ CHECK - Проверочные ограничения

### Простые проверки:
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) CHECK (price > 0),
    discount_percent INTEGER CHECK (discount_percent BETWEEN 0 AND 100),
    category VARCHAR(50) CHECK (category IN ('electronics', 'clothing', 'books'))
);
```

### Сложные проверки:
```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    birth_date DATE,
    hire_date DATE,
    salary DECIMAL(10,2),
    
    -- Проверяем, что дата найма позже даты рождения
    CHECK (hire_date > birth_date),
    
    -- Проверяем возраст при найме (должен быть >= 18 лет)
    CHECK (hire_date - birth_date >= INTERVAL '18 years')
);
```

---

## 🚫 NOT NULL - Обязательные поля

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),  -- может быть NULL
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## 🔧 DEFAULT - Значения по умолчанию

### Различные типы значений по умолчанию:
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    is_paid BOOLEAN DEFAULT FALSE,
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    
    -- Вычисляемое значение по умолчанию
    order_number VARCHAR(20) DEFAULT 'ORD-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || LPAD(NEXTVAL('order_seq')::TEXT, 4, '0')
);
```

---

## 📊 Управление ограничениями

### Просмотр ограничений:
```sql
-- Просмотр всех ограничений таблицы
SELECT 
    constraint_name,
    constraint_type,
    table_name
FROM information_schema.table_constraints 
WHERE table_name = 'your_table_name';
```

### Добавление ограничений:
```sql
-- Добавляем именованное ограничение
ALTER TABLE products 
ADD CONSTRAINT chk_positive_price 
CHECK (price > 0);

-- Добавляем внешний ключ
ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
```

### Удаление ограничений:
```sql
-- Удаляем ограничение по имени
ALTER TABLE products 
DROP CONSTRAINT chk_positive_price;

-- Удаляем NOT NULL ограничение
ALTER TABLE customers 
ALTER COLUMN phone DROP NOT NULL;
```

---

## 💡 ПРАКТИЧЕСКОЕ ЗАДАНИЕ 2.2

### Задача: Добавить ограничения целостности

```sql
-- Дана структура таблиц интернет-магазина
-- Добавьте необходимые ограничения

-- 1. Убедитесь, что email клиента уникален
-- Ваш код здесь

-- 2. Добавьте проверку на положительную цену товара
-- Ваш код здесь

-- 3. Создайте связь между заказами и клиентами
-- Ваш код здесь

-- 4. Добавьте ограничение на статус заказа (только определенные значения)
-- Ваш код здесь
```

### ✅ Проверочный список:
- [ ] Все важные поля имеют NOT NULL
- [ ] Уникальные поля помечены как UNIQUE
- [ ] Добавлены CHECK ограничения для валидации
- [ ] Настроены внешние ключи
- [ ] Установлены значения по умолчанию

---

# 🚀 ГЛАВА 2.3: ИНДЕКСЫ

## 🎯 Что изучим:
- Что такое индексы и зачем они нужны
- Создание индексов (CREATE INDEX)
- Типы индексов в PostgreSQL
- Составные индексы
- Когда НЕ нужно создавать индексы

---

## 🤔 Что такое индексы?

### Аналогия с книжным указателем:
```
┌─────────────────────────────────────────────────────────────┐
│                    БЕЗ ИНДЕКСА                             │
│  Поиск "PostgreSQL" в книге на 1000 страниц:               │
│  📖 Страница 1... не найдено                               │
│  📖 Страница 2... не найдено                               │
│  📖 Страница 3... не найдено                               │
│  📖 ...                                                     │
│  📖 Страница 547... НАЙДЕНО! 😅                            │
│                                                             │
│                    С ИНДЕКСОМ                              │
│  📑 Алфавитный указатель:                                  │
│      P... PostgreSQL → страницы 34, 156, 547               │
│  🎯 Сразу переходим на нужные страницы!                    │
└─────────────────────────────────────────────────────────────┘
```

### Как работает индекс в БД:
```
┌─────────────────────────────────────────────────────────────┐
│                   ТАБЛИЦА EMPLOYEES                         │
│  ┌─────┬──────────────┬─────────────┬───────────────────┐    │
│  │ ID  │ FIRST_NAME   │ LAST_NAME   │ EMAIL             │    │
│  ├─────┼──────────────┼─────────────┼───────────────────┤    │
│  │ 1   │ John         │ Smith       │ john@email.com    │    │
│  │ 2   │ Jane         │ Doe         │ jane@email.com    │    │
│  │ 3   │ Bob          │ Johnson     │ bob@email.com     │    │
│  │ ... │ ...          │ ...         │ ...               │    │
│  └─────┴──────────────┴─────────────┴───────────────────┘    │
│                                                             │
│                  ИНДЕКС ПО EMAIL                           │
│  ┌───────────────────┬─────────────────────────────────┐    │
│  │ EMAIL (sorted)    │ POINTER TO ROW                  │    │
│  ├───────────────────┼─────────────────────────────────┤    │
│  │ bob@email.com     │ → Row 3                         │    │
│  │ jane@email.com    │ → Row 2                         │    │
│  │ john@email.com    │ → Row 1                         │    │
│  └───────────────────┴─────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔨 Создание индексов

### Простой индекс:
```sql
-- Создаем индекс для быстрого поиска по email
CREATE INDEX idx_employees_email 
ON employees (email);
```

### Индекс с опциями:
```sql
-- Уникальный индекс
CREATE UNIQUE INDEX idx_employees_email_unique 
ON employees (email);

-- Частичный индекс (только для активных сотрудников)
CREATE INDEX idx_active_employees 
ON employees (last_name) 
WHERE is_active = true;

-- Индекс с сортировкой
CREATE INDEX idx_employees_salary_desc 
ON employees (salary DESC);
```

---

## 📊 Типы индексов в PostgreSQL

### 1. B-tree (по умолчанию)
```sql
-- Подходит для: =, <, <=, >, >=, BETWEEN, IN, ORDER BY
CREATE INDEX idx_btree ON products (price);

-- Хорошо работает с запросами:
SELECT * FROM products WHERE price BETWEEN 100 AND 500;
SELECT * FROM products ORDER BY price;
```

### 2. Hash
```sql
-- Подходит только для проверки равенства (=)
CREATE INDEX idx_hash ON products USING HASH (category);

-- Оптимизирует:
SELECT * FROM products WHERE category = 'electronics';
```

### 3. GIN (Generalized Inverted Index)
```sql
-- Для массивов, JSON, полнотекстового поиска
CREATE INDEX idx_gin ON products USING GIN (tags);

-- Оптимизирует:
SELECT * FROM products WHERE tags @> ARRAY['smartphone'];
```

### 4. GiST (Generalized Search Tree)
```sql
-- Для геометрических данных, полнотекстового поиска
CREATE INDEX idx_gist ON locations USING GIST (coordinates);
```

---

## 🔗 Составные индексы

### Создание составного индекса:
```sql
-- Индекс по нескольким столбцам
CREATE INDEX idx_employee_dept_salary 
ON employees (department_id, salary);
```

### Порядок столбцов важен!
```
┌─────────────────────────────────────────────────────────────┐
│              ПРАВИЛЬНЫЙ ПОРЯДОК                             │
│  CREATE INDEX idx_dept_salary ON employees (dept_id, salary) │
│                                                             │
│  ✅ Быстро:   WHERE dept_id = 5                            │
│  ✅ Быстро:   WHERE dept_id = 5 AND salary > 50000         │
│  ❌ Медленно: WHERE salary > 50000                         │
│                                                             │
│              ПРАВИЛО:                                       │
│  📊 Самые селективные столбцы (меньше дубликатов) - первыми │
│  🔍 Столбцы, часто используемые в WHERE - первыми          │
└─────────────────────────────────────────────────────────────┘
```

---

## ❌ Когда НЕ нужны индексы

### Избегайте индексов если:
```sql
-- ❌ Маленькие таблицы (< 1000 строк)
-- Полное сканирование может быть быстрее

-- ❌ Столбцы с частыми изменениями
-- Каждый UPDATE будет обновлять индекс

-- ❌ Столбцы с низкой селективностью
CREATE TABLE users (
    gender CHAR(1)  -- только 'M'/'F' - плохой кандидат для индекса
);

-- ❌ Слишком много индексов на одной таблице
-- Замедляет INSERT/UPDATE/DELETE операции
```

### 📈 Мониторинг использования индексов:
```sql
-- Проверяем, используются ли индексы
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,      -- количество использований
    idx_tup_read,  -- прочитано строк через индекс
    idx_tup_fetch  -- извлечено строк
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Находим неиспользуемые индексы
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

---

## 💡 ПРАКТИЧЕСКОЕ ЗАДАНИЕ 2.3

### Задача: Оптимизировать запросы индексами

```sql
-- У нас есть таблица заказов:
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    status VARCHAR(20),
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP
);

-- Частые запросы:
-- 1. Поиск заказов клиента
SELECT * FROM orders WHERE customer_id = 123;

-- 2. Поиск заказов по статусу
SELECT * FROM orders WHERE status = 'completed';

-- 3. Заказы за период
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- 4. Активные заказы клиента
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';

-- ЗАДАНИЕ: Создайте оптимальные индексы
-- Ваш код здесь
```

### ✅ Проверочный список:
- [ ] Созданы индексы для часто используемых WHERE условий
- [ ] Учтен порядок столбцов в составных индексах
- [ ] Избегаем избыточных индексов
- [ ] Проверили план выполнения запросов

---

# 📝 ГЛАВА 2.4: МОДИФИКАЦИЯ ДАННЫХ

## 🎯 Что изучим:
- Вставка данных (INSERT)
- Обновление данных (UPDATE)
- Удаление данных (DELETE)
- UPSERT (INSERT ... ON CONFLICT)
- Массовые операции

---

## ➕ INSERT - Вставка данных

### Простая вставка:
```sql
-- Вставка с указанием всех столбцов
INSERT INTO employees (first_name, last_name, email, salary)
VALUES ('John', 'Smith', 'john.smith@company.com', 75000);

-- Вставка с автоинкрементом
INSERT INTO employees (first_name, last_name, email)
VALUES ('Jane', 'Doe', 'jane.doe@company.com');
-- id создастся автоматически (SERIAL)
```

### Множественная вставка:
```sql
INSERT INTO employees (first_name, last_name, email, salary)
VALUES 
    ('Alice', 'Johnson', 'alice.j@company.com', 80000),
    ('Bob', 'Wilson', 'bob.w@company.com', 72000),
    ('Carol', 'Brown', 'carol.b@company.com', 78000);
```

### Вставка из SELECT:
```sql
-- Копируем данные из другой таблицы
INSERT INTO active_employees (first_name, last_name, email)
SELECT first_name, last_name, email
FROM employees
WHERE is_active = true;
```

### Вставка с возвратом данных:
```sql
-- RETURNING позволяет получить вставленные данные
INSERT INTO employees (first_name, last_name, email)
VALUES ('David', 'Miller', 'david.m@company.com')
RETURNING id, first_name, created_at;
```

---

## 🔄 UPDATE - Обновление данных

### Простое обновление:
```sql
-- Обновляем зарплату конкретного сотрудника
UPDATE employees 
SET salary = 85000
WHERE id = 1;
```

### Обновление нескольких столбцов:
```sql
-- Обновляем несколько полей одновременно
UPDATE employees 
SET 
    salary = salary * 1.1,  -- увеличиваем на 10%
    last_updated = NOW()
WHERE department_id = 2;
```

### Условное обновление:
```sql
-- Используем CASE для условной логики
UPDATE employees 
SET salary = CASE 
    WHEN performance_rating = 'excellent' THEN salary * 1.15
    WHEN performance_rating = 'good' THEN salary * 1.10
    WHEN performance_rating = 'average' THEN salary * 1.05
    ELSE salary
END
WHERE hire_date < '2023-01-01';
```

### Обновление с JOIN:
```sql
-- Обновляем данные на основе связанной таблицы
UPDATE employees 
SET salary = salary * d.salary_multiplier
FROM departments d
WHERE employees.department_id = d.id
  AND d.budget_approved = true;
```

---

## ❌ DELETE - Удаление данных

### Простое удаление:
```sql
-- Удаляем конкретного сотрудника
DELETE FROM employees 
WHERE id = 100;
```

### Условное удаление:
```sql
-- Удаляем неактивных сотрудников старше 5 лет
DELETE FROM employees 
WHERE is_active = false 
  AND hire_date < CURRENT_DATE - INTERVAL '5 years';
```

### Удаление с подзапросом:
```sql
-- Удаляем сотрудников из закрытых отделов
DELETE FROM employees 
WHERE department_id IN (
    SELECT id FROM departments 
    WHERE status = 'closed'
);
```

### Безопасное удаление с RETURNING:
```sql
-- Удаляем и сохраняем информацию об удаленных записях
DELETE FROM employees 
WHERE is_active = false
RETURNING id, first_name, last_name, 'deleted at ' || NOW() as deletion_info;
```

---

## 🔄 UPSERT - INSERT ... ON CONFLICT

### Концепция UPSERT:
```
┌─────────────────────────────────────────────────────────────┐
│                        UPSERT                               │
│                                                             │
│  IF запись существует → UPDATE                              │
│  IF запись НЕ существует → INSERT                           │
│                                                             │
│  🎯 Решает проблему: "вставить или обновить"              │
└─────────────────────────────────────────────────────────────┘
```

### Синтаксис ON CONFLICT:
```sql
-- Если email уже существует - обновляем данные
INSERT INTO employees (email, first_name, last_name, salary)
VALUES ('john.smith@company.com', 'John', 'Smith', 80000)
ON CONFLICT (email) 
DO UPDATE SET 
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    salary = EXCLUDED.salary,
    updated_at = NOW();
```

### Условный UPSERT:
```sql
-- Обновляем только если новая зарплата больше
INSERT INTO employees (email, first_name, last_name, salary)
VALUES ('jane.doe@company.com', 'Jane', 'Doe', 90000)
ON CONFLICT (email)
DO UPDATE SET 
    salary = EXCLUDED.salary,
    updated_at = NOW()
WHERE EXCLUDED.salary > employees.salary;
```

### UPSERT с DO NOTHING:
```sql
-- Игнорируем конфликты (ничего не делаем)
INSERT INTO employees (email, first_name, last_name)
VALUES ('existing@company.com', 'Test', 'User')
ON CONFLICT (email) DO NOTHING;
```

---

## 🚀 Массовые операции

### Массовая вставка из CSV:
```sql
-- Копируем данные из CSV файла
COPY employees (first_name, last_name, email, salary)
FROM '/path/to/employees.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');
```

### Массовое обновление:
```sql
-- Обновляем с помощью временной таблицы
CREATE TEMP TABLE salary_updates (
    employee_id INTEGER,
    new_salary DECIMAL(10,2)
);

-- Загружаем данные обновлений
INSERT INTO salary_updates VALUES 
    (1, 85000),
    (2, 90000),
    (3, 78000);

-- Применяем массовое обновление
UPDATE employees 
SET salary = su.new_salary
FROM salary_updates su
WHERE employees.id = su.employee_id;
```

### Транзакционные операции:
```sql
-- Группируем операции в транзакцию
BEGIN;

    INSERT INTO departments (name) VALUES ('New Department');
    
    UPDATE employees 
    SET department_id = (SELECT id FROM departments WHERE name = 'New Department')
    WHERE department_id IS NULL;
    
    DELETE FROM old_employees WHERE hire_date < '2010-01-01';

COMMIT;  -- или ROLLBACK; в случае ошибки
```

---

## 💡 ПРАКТИЧЕСКОЕ ЗАДАНИЕ 2.4

### Задача: Управление данными интернет-магазина

```sql
-- 1. Добавьте 5 новых товаров одним запросом
INSERT INTO products (name, price, category_id, stock_quantity)
VALUES 
    -- Ваш код здесь
;

-- 2. Обновите цены всех товаров в категории "Electronics" на +10%
-- Ваш код здесь

-- 3. Создайте UPSERT для обновления остатков товаров
-- Если товар существует - обновляем количество
-- Если не существует - добавляем новый товар
-- Ваш код здесь

-- 4. Удалите товары с нулевым остатком и ценой менее 10
-- Ваш код здесь

-- 5. Создайте отчет об изменениях (используйте RETURNING)
-- Ваш код здесь
```

### ✅ Проверочный список:
- [ ] Использованы транзакции для критических операций
- [ ] Добавлены проверки безопасности (WHERE условия)
- [ ] Применен UPSERT где это уместно
- [ ] Использован RETURNING для отслеживания изменений

---

# 📐 ГЛАВА 2.5: ОСНОВЫ НОРМАЛИЗАЦИИ

## 🎯 Что изучим:
- Первая нормальная форма (1NF)
- Вторая нормальная форма (2NF)  
- Третья нормальная форма (3NF)
- Практические примеры нормализации
- Когда денормализация оправдана

---

## 🤔 Что такое нормализация?

### Определение:
```
┌─────────────────────────────────────────────────────────────┐
│                    НОРМАЛИЗАЦИЯ                             │
│                                                             │
│  🎯 Цель: Устранить избыточность и аномалии данных         │
│                                                             │
│  ✅ Преимущества:                                          │
│     • Нет дублирования данных                              │
│     • Легче поддерживать целостность                      │
│     • Меньше места на диске                                │
│     • Проще обновлять данные                               │
│                                                             │
│  ❌ Недостатки:                                            │
│     • Больше таблиц                                        │
│     • Сложнее запросы (больше JOIN)                       │
│     • Может быть медленнее для чтения                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ ПЕРВАЯ НОРМАЛЬНАЯ ФОРМА (1NF)

### Правила 1NF:
- Каждая ячейка содержит только одно значение (атомарность)
- Нет повторяющихся групп столбцов
- Каждая строка уникальна

### ❌ НЕ соответствует 1NF:
```sql
-- Проблема: множественные значения в одной ячейке
CREATE TABLE orders_bad (
    order_id INTEGER,
    customer_name VARCHAR(100),
    products VARCHAR(500),  -- "Laptop, Mouse, Keyboard"
    quantities VARCHAR(100) -- "1, 2, 1"
);
```

### ✅ Соответствует 1NF:
```sql
-- Решение: разделяем на отдельные строки
CREATE TABLE orders (
    order_id INTEGER,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    quantity INTEGER,
    PRIMARY KEY (order_id, product_name)
);

-- Теперь каждый товар в отдельной строке
INSERT INTO orders VALUES 
    (1, 'John Smith', 'Laptop', 1),
    (1, 'John Smith', 'Mouse', 2),
    (1, 'John Smith', 'Keyboard', 1);
```

---

## 2️⃣ ВТОРАЯ НОРМАЛЬНАЯ ФОРМА (2NF)

### Правила 2NF:
- Соответствует 1NF
- Нет частичной зависимости от первичного ключа
- Все неключевые атрибуты полностью зависят от всего первичного ключа

### ❌ НЕ соответствует 2NF:
```sql
-- Проблема: customer_name зависит только от части ключа (order_id)
CREATE TABLE order_items_bad (
    order_id INTEGER,
    product_id INTEGER,
    customer_name VARCHAR(100),  -- зависит только от order_id!
    product_name VARCHAR(100),   -- зависит только от product_id!
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

### ✅ Соответствует 2NF:
```sql
-- Решение: выносим частично зависимые атрибуты в отдельные таблицы
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

### 📊 Схема 2NF:
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     ORDERS      │    │   ORDER_ITEMS   │    │    PRODUCTS     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ order_id (PK)   │◄──┤│ order_id (FK)   │    │ product_id (PK) │
│ customer_name   │    │ product_id (FK) │──► │ product_name    │
│ order_date      │    │ quantity        │    │ price           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 3️⃣ ТРЕТЬЯ НОРМАЛЬНАЯ ФОРМА (3NF)

### Правила 3NF:
- Соответствует 2NF
- Нет транзитивной зависимости
- Неключевые атрибуты не зависят от других неключевых атрибутов

### ❌ НЕ соответствует 3NF:
```sql
-- Проблема: department_name зависит от department_id (транзитивная зависимость)
CREATE TABLE employees_bad (
    employee_id INTEGER PRIMARY KEY,
    employee_name VARCHAR(100),
    department_id INTEGER,
    department_name VARCHAR(100),  -- зависит от department_id!
    department_location VARCHAR(100) -- тоже зависит от department_id!
);
```

### ✅ Соответствует 3NF:
```sql
-- Решение: выносим транзитивно зависимые атрибуты
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR(100),
    department_location VARCHAR(100)
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name VARCHAR(100),
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);
```

### 📊 Схема 3NF:
```
┌─────────────────────┐    ┌─────────────────────┐
│     EMPLOYEES       │    │    DEPARTMENTS      │
├─────────────────────┤    ├─────────────────────┤
│ employee_id (PK)    │    │ department_id (PK)  │
│ employee_name       │    │ department_name     │
│ department_id (FK)  │──► │ department_location │
│ hire_date           │    │ budget              │
└─────────────────────┘    └─────────────────────┘
```

---

## 📝 Пример полной нормализации

### Исходная денормализованная таблица:
```sql
-- ❌ Много проблем с избыточностью
CREATE TABLE sales_denormalized (
    sale_id INTEGER,
    customer_name VARCHAR(100),
    customer_city VARCHAR(50),
    customer_country VARCHAR(50),
    product_name VARCHAR(100),
    product_category VARCHAR(50),
    category_description TEXT,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2),  -- вычисляемое поле!
    sale_date DATE
);
```

### После нормализации:
```sql
-- ✅ Нормализованная структура
CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(50) UNIQUE
);

CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(50),
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50),
    category_description TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INTEGER,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    sale_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Вычисляемое поле как представление
CREATE VIEW sales_with_totals AS
SELECT 
    s.sale_id,
    c.customer_name,
    p.product_name,
    s.quantity,
    p.unit_price,
    s.quantity * p.unit_price AS total_price,
    s.sale_date
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
JOIN products p ON s.product_id = p.product_id;
```

---

## ⚖️ Когда денормализация оправдана

### Случаи для денормализации:
```
┌─────────────────────────────────────────────────────────────┐
│              ДЕНОРМАЛИЗАЦИЯ ОПРАВДАНА                       │
│                                                             │
│  📊 OLAP системы (аналитика)                               │
│     • Много чтения, мало записи                            │
│     • Сложные агрегации                                    │
│                                                             │
│  ⚡ Критичная производительность                           │
│     • Избегаем сложных JOIN                                │
│     • Кэшируем вычисления                                  │
│                                                             │
│  📈 Отчеты и дашборды                                      │
│     • Денормализованные витрины данных                     │
│     • Предварительно агрегированные данные                 │
│                                                             │
│  🔄 Исторические данные                                    │
│     • Снимки состояния на определенный момент              │
│     • Аудит и логирование                                  │
└─────────────────────────────────────────────────────────────┘
```

### Пример контролируемой денормализации:
```sql
-- Добавляем денормализованное поле для производительности
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    
    -- Денормализация: дублируем имя клиента для быстрого доступа
    customer_name VARCHAR(100), -- это дубликат из таблицы customers!
    
    total_amount DECIMAL(10,2), -- вычисляемое поле
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Поддерживаем целостность триггером
CREATE OR REPLACE FUNCTION sync_customer_name()
RETURNS TRIGGER AS $$
BEGIN
    NEW.customer_name := (
        SELECT customer_name 
        FROM customers 
        WHERE customer_id = NEW.customer_id
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_customer_name
    BEFORE INSERT OR UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION sync_customer_name();
```

---

## 💡 ПРАКТИЧЕСКОЕ ЗАДАНИЕ 2.5

### Задача: Нормализация базы данных блога

```sql
-- Дана денормализованная таблица
CREATE TABLE blog_posts_bad (
    post_id INTEGER,
    title VARCHAR(200),
    content TEXT,
    author_name VARCHAR(100),
    author_email VARCHAR(100),
    author_bio TEXT,
    category_name VARCHAR(50),
    category_description TEXT,
    tag_names VARCHAR(500), -- "programming,sql,database"
    publish_date DATE,
    view_count INTEGER
);

-- ЗАДАНИЕ: Создайте нормализованную структуру (3NF)
-- Подсказка: выделите сущности - авторы, категории, теги, посты

-- 1. Создайте таблицу авторов
-- Ваш код здесь

-- 2. Создайте таблицу категорий  
-- Ваш код здесь

-- 3. Создайте таблицу тегов
-- Ваш код здесь

-- 4. Создайте таблицу постов
-- Ваш код здесь

-- 5. Создайте связующую таблицу для тегов (many-to-many)
-- Ваш код здесь

-- 6. Создайте представление для удобного чтения
-- Ваш код здесь
```

### ✅ Проверочный список:
- [ ] Соблюдены правила 1NF (атомарность)
- [ ] Соблюдены правила 2NF (нет частичной зависимости)
- [ ] Соблюдены правила 3NF (нет транзитивной зависимости)
- [ ] Созданы подходящие связи между таблицами
- [ ] Добавлены необходимые ограничения целостности

---

# 🎯 ИТОГОВОЕ ЗАДАНИЕ БЛОКА 2

## 🏪 Проект: База данных интернет-магазина

### Техническое задание:
```
┌─────────────────────────────────────────────────────────────┐
│                 ИНТЕРНЕТ-МАГАЗИН "TechStore"                │
│                                                             │
│  📦 Требования:                                            │
│     • Каталог товаров с категориями                       │
│     • Система клиентов и заказов                           │
│     • Управление остатками                                 │
│     • История изменений цен                                │
│     • Система скидок                                       │
│                                                             │
│  🎯 Задачи:                                                │
│     ✅ Спроектировать нормализованную структуру           │
│     ✅ Добавить все ограничения целостности               │
│     ✅ Создать необходимые индексы                        │
│     ✅ Заполнить тестовыми данными                        │
│     ✅ Реализовать основные операции                      │
└─────────────────────────────────────────────────────────────┘
```

### Сущности для реализации:
```sql
-- 1. КАТЕГОРИИ ТОВАРОВ
-- Поля: id, название, описание, родительская_категория

-- 2. ТОВАРЫ  
-- Поля: id, название, описание, категория, цена, остаток

-- 3. КЛИЕНТЫ
-- Поля: id, имя, email, телефон, адрес, дата_регистрации

-- 4. ЗАКАЗЫ
-- Поля: id, клиент, дата, статус, общая_сумма

-- 5. ПОЗИЦИИ ЗАКАЗА
-- Поля: заказ, товар, количество, цена_на_момент_заказа

-- 6. ИСТОРИЯ ЦЕН
-- Поля: товар, цена, дата_начала, дата_окончания

-- ЗАДАНИЕ: Реализуйте полную структуру с учетом всех изученных принципов
```

### ✅ Критерии успешного выполнения:
- [ ] **Нормализация**: Структура соответствует 3NF
- [ ] **Целостность**: Все необходимые ограничения созданы
- [ ] **Производительность**: Добавлены оптимальные индексы
- [ ] **Функциональность**: Реализованы CRUD операции
- [ ] **Тестирование**: База заполнена реалистичными данными

---

# 🎊 ПОЗДРАВЛЯЕМ!

```
┌─────────────────────────────────────────────────────────────┐
│           🎉 ВЫ ЗАВЕРШИЛИ БЛОК 2! 🎉                       │
│                                                             │
│  🚀 Что вы теперь умеете:                                  │
│     ✅ Создавать и изменять структуру БД                   │
│     ✅ Использовать ограничения целостности                │
│     ✅ Оптимизировать запросы с помощью индексов           │
│     ✅ Эффективно модифицировать данные                    │
│     ✅ Проектировать нормализованные структуры             │
│                                                             │
│  ➡️ Следующий блок: "Сложные запросы и объединения"        │
│                                                             │
│  💪 Продолжайте практиковаться!                            │
└─────────────────────────────────────────────────────────────┘
```

---

**📚 Дополнительные материалы:**
- [Официальная документация PostgreSQL - DDL](https://www.postgresql.org/docs/current/ddl.html)
- [PostgreSQL Tutorial - Data Types](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-data-types/)
- [Database Normalization Explained](https://www.guru99.com/database-normalization.html)

**🔗 Полезные команды psql:**
```sql
\d table_name          -- описание таблицы
\di                    -- список индексов  
\dt                    -- список таблиц
\dn                    -- список схем
```