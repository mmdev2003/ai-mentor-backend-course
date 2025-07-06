# PostgreSQL Блок 3: Сложные запросы и объединения

```
🎯 ЦЕЛЬ БЛОКА: Освоить продвинутые техники работы с несколькими таблицами
⏱️ ПРОДОЛЖИТЕЛЬНОСТЬ: 3-4 недели
📊 СЛОЖНОСТЬ: Средний уровень
```

---

## 📋 Содержание блока

```
┌─────────────────────────────────────────────────────────────┐
│  БЛОК 3: СЛОЖНЫЕ ЗАПРОСЫ И ОБЪЕДИНЕНИЯ                     │
├─────────────────────────────────────────────────────────────┤
│  3.1 → Объединения таблиц (JOIN)           │ 5-6 дней      │
│  3.2 → Подзапросы                           │ 5-6 дней      │
│  3.3 → CTE (Common Table Expressions)      │ 4-5 дней      │
│  3.4 → Агрегатные функции и группировка    │ 4-5 дней      │
│  3.5 → Оконные функции                     │ 6-7 дней      │
│  3.6 → Операции с множествами               │ 2-3 дня       │
└─────────────────────────────────────────────────────────────┘
```

---

## 3.1 Объединения таблиц (JOIN) 🔗

### Теоретическая база

JOIN операции позволяют объединять данные из нескольких таблиц на основе связей между ними.

```
┌──────────────────┐    JOIN    ┌──────────────────┐
│    Таблица A     │◄──────────►│    Таблица B     │
│                  │            │                  │
│ id │ name        │            │ id │ category    │
├────┼─────────────┤            ├────┼─────────────┤
│ 1  │ iPhone      │            │ 1  │ Electronics │
│ 2  │ Book        │            │ 2  │ Literature  │
│ 3  │ Chair       │            │ 3  │ Furniture   │
└────┴─────────────┘            └────┴─────────────┘
```

### Типы JOIN операций

#### 🔵 INNER JOIN (Внутреннее соединение)

```sql
-- Возвращает только совпадающие записи из обеих таблиц
SELECT p.name, c.category
FROM products p
INNER JOIN categories c ON p.category_id = c.id;
```

**Визуализация INNER JOIN:**
```
Таблица A          Таблица B          Результат
┌─────────┐        ┌─────────┐        ┌─────────┐
│    1    │────────│    1    │───────►│    1    │
│    2    │────────│    2    │───────►│    2    │
│    3    │   ╱    │    4    │        │         │
│    5    │ ╱      └─────────┘        └─────────┘
└─────────┘
```

#### 🟢 LEFT JOIN (Левое соединение)

```sql
-- Возвращает ВСЕ записи из левой таблицы + совпадающие из правой
SELECT p.name, c.category
FROM products p
LEFT JOIN categories c ON p.category_id = c.id;
```

**Визуализация LEFT JOIN:**
```
Таблица A          Таблица B          Результат
┌─────────┐        ┌─────────┐        ┌─────────┐
│    1    │────────│    1    │───────►│    1    │
│    2    │────────│    2    │───────►│    2    │
│    3    │   ╱    │    4    │───────►│    3    │ (NULL)
│    5    │ ╱      └─────────┘───────►│    5    │ (NULL)
└─────────┘                           └─────────┘
```

#### 🟡 RIGHT JOIN (Правое соединение)

```sql
-- Возвращает ВСЕ записи из правой таблицы + совпадающие из левой
SELECT p.name, c.category
FROM products p
RIGHT JOIN categories c ON p.category_id = c.id;
```

#### 🔴 FULL OUTER JOIN (Полное внешнее соединение)

```sql
-- Возвращает ВСЕ записи из обеих таблиц
SELECT p.name, c.category
FROM products p
FULL OUTER JOIN categories c ON p.category_id = c.id;
```

**Визуализация FULL OUTER JOIN:**
```
Таблица A          Таблица B          Результат
┌─────────┐        ┌─────────┐        ┌─────────┐
│    1    │────────│    1    │───────►│    1    │
│    2    │────────│    2    │───────►│    2    │
│    3    │   ╱    │    4    │───────►│    3    │ (NULL)
│    5    │ ╱      │    6    │───────►│    5    │ (NULL)
└─────────┘        └─────────┘───────►│ (NULL)  │ 4
                                  ───────►│ (NULL)  │ 6
                                      └─────────┘
```

### 🔄 SELF JOIN (Само-соединение)

```sql
-- Соединение таблицы с самой собой
-- Пример: найти сотрудников и их менеджеров
SELECT 
    emp.name AS employee,
    mgr.name AS manager
FROM employees emp
LEFT JOIN employees mgr ON emp.manager_id = mgr.id;
```

### ⚡ Практические примеры

#### Пример 1: Интернет-магазин

```sql
-- Получить все заказы с информацией о клиентах и товарах
SELECT 
    o.order_id,
    c.customer_name,
    p.product_name,
    oi.quantity,
    oi.price
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_date DESC;
```

#### Пример 2: Многоуровневые категории

```sql
-- Получить все категории с их родительскими категориями
SELECT 
    child.name AS category,
    parent.name AS parent_category
FROM categories child
LEFT JOIN categories parent ON child.parent_id = parent.id;
```

---

## 3.2 Подзапросы 🎯

### Типы подзапросов

```
ПОДЗАПРОСЫ
├── Скалярные (возвращают одно значение)
├── Столбцовые (возвращают один столбец)
├── Табличные (возвращают таблицу)
└── Коррелированные (зависят от внешнего запроса)
```

#### 🎯 Скалярные подзапросы

```sql
-- Найти товары дороже средней цены
SELECT name, price
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
);
```

#### 📊 Подзапросы с IN

```sql
-- Найти клиентов, которые делали заказы в 2024 году
SELECT customer_name
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE EXTRACT(YEAR FROM order_date) = 2024
);
```

#### ✅ Подзапросы с EXISTS

```sql
-- Найти категории, в которых есть товары
SELECT category_name
FROM categories c
WHERE EXISTS (
    SELECT 1
    FROM products p
    WHERE p.category_id = c.category_id
);
```

**Визуализация EXISTS:**
```
Основной запрос    →    Подзапрос для каждой строки
┌─────────────┐         ┌────────────────────────┐
│ Category 1  │────────►│ EXISTS товары? ✅ ДА   │
├─────────────┤         ├────────────────────────┤
│ Category 2  │────────►│ EXISTS товары? ❌ НЕТ  │
├─────────────┤         ├────────────────────────┤
│ Category 3  │────────►│ EXISTS товары? ✅ ДА   │
└─────────────┘         └────────────────────────┘
```

#### 🔄 Коррелированные подзапросы

```sql
-- Найти самый дорогой товар в каждой категории
SELECT p1.name, p1.price, p1.category_id
FROM products p1
WHERE p1.price = (
    SELECT MAX(p2.price)
    FROM products p2
    WHERE p2.category_id = p1.category_id
);
```

### ⚖️ Подзапросы vs JOIN: Когда что использовать?

```
┌─────────────────────┬─────────────────────────────────────┐
│     ПОДЗАПРОСЫ      │              JOIN                   │
├─────────────────────┼─────────────────────────────────────┤
│ ✅ Проще читать      │ ✅ Обычно быстрее                   │
│ ✅ Логичная структу- │ ✅ Меньше дублирования данных       │
│    ра для фильтрации│ ✅ Возможность получать данные      │
│ ❌ Могут быть медлен-│    из нескольких таблиц             │
│    нее              │ ❌ Сложнее при сложной логике       │
│ ❌ Ограниченный до-  │    фильтрации                       │
│    ступ к данным    │                                     │
└─────────────────────┴─────────────────────────────────────┘
```

---

## 3.3 CTE (Common Table Expressions) 📝

### Что такое CTE?

CTE - это именованный временный результирующий набор, который существует только в рамках одного SQL-запроса.

```sql
WITH cte_name AS (
    -- Подзапрос
    SELECT column1, column2
    FROM table_name
    WHERE condition
)
-- Основной запрос использует CTE
SELECT *
FROM cte_name;
```

### 🔗 Простые CTE

```sql
-- Найти клиентов с высокими тратами
WITH high_spenders AS (
    SELECT 
        customer_id,
        SUM(total_amount) as total_spent
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total_amount) > 1000
)
SELECT 
    c.customer_name,
    hs.total_spent
FROM customers c
INNER JOIN high_spenders hs ON c.customer_id = hs.customer_id;
```

### 🔄 Рекурсивные CTE

```sql
-- Построить иерархию сотрудников
WITH RECURSIVE employee_hierarchy AS (
    -- Базовый случай: топ-менеджеры
    SELECT 
        employee_id,
        employee_name,
        manager_id,
        0 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Рекурсивный случай: подчиненные
    SELECT 
        e.employee_id,
        e.employee_name,
        e.manager_id,
        eh.level + 1
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM employee_hierarchy ORDER BY level, employee_name;
```

**Визуализация рекурсивного CTE:**
```
Итерация 0:     Итерация 1:     Итерация 2:
┌─────────┐     ┌─────────┐     ┌─────────┐
│ CEO     │     │ CEO     │     │ CEO     │
│ (level 0)│     │ Manager1│     │ Manager1│
└─────────┘     │ Manager2│     │ Manager2│
                │ (level 1)│     │ Employee1│
                └─────────┘     │ Employee2│
                                │ (level 2)│
                                └─────────┘
```

### 🎭 Множественные CTE

```sql
WITH 
monthly_sales AS (
    SELECT 
        EXTRACT(MONTH FROM order_date) as month,
        SUM(total_amount) as monthly_total
    FROM orders
    WHERE EXTRACT(YEAR FROM order_date) = 2024
    GROUP BY EXTRACT(MONTH FROM order_date)
),
avg_monthly_sale AS (
    SELECT AVG(monthly_total) as avg_sale
    FROM monthly_sales
)
SELECT 
    ms.month,
    ms.monthly_total,
    CASE 
        WHEN ms.monthly_total > ams.avg_sale THEN 'Above Average'
        ELSE 'Below Average'
    END as performance
FROM monthly_sales ms
CROSS JOIN avg_monthly_sale ams
ORDER BY ms.month;
```

---

## 3.4 Агрегатные функции и группировка 📊

### Основные агрегатные функции

```
┌─────────────────────────────────────────────────────────┐
│                АГРЕГАТНЫЕ ФУНКЦИИ                       │
├─────────────┬───────────────────────────────────────────┤
│ COUNT()     │ Подсчет количества строк                  │
│ SUM()       │ Сумма значений                            │
│ AVG()       │ Среднее арифметическое                    │
│ MIN()       │ Минимальное значение                      │
│ MAX()       │ Максимальное значение                     │
│ STRING_AGG()│ Объединение строк                         │
└─────────────┴───────────────────────────────────────────┘
```

### 📈 GROUP BY - основы

```sql
-- Продажи по категориям
SELECT 
    category_name,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM products p
JOIN categories c ON p.category_id = c.category_id
GROUP BY category_name
ORDER BY avg_price DESC;
```

**Визуализация GROUP BY:**
```
Исходные данные:        Группировка:           Агрегация:
┌─────────────────┐     ┌─────────────────┐    ┌─────────────────┐
│Product│Category │     │  Electronics    │    │Electronics│AVG│
│Phone  │Electron.│────►│  ├─Phone        │───►│    $500   │   │
│Laptop │Electron.│     │  └─Laptop       │    │Books     │$25│
│Book   │Books    │     │  Books          │    │Furniture │$200│
│Table  │Furniture│     │  ├─Book         │    └─────────────────┘
│Chair  │Furniture│     │  Furniture      │
└─────────────────┘     │  ├─Table        │
                        │  └─Chair        │
                        └─────────────────┘
```

### 🎯 HAVING - фильтрация групп

```sql
-- Категории с более чем 5 товарами и средней ценой > $100
SELECT 
    category_name,
    COUNT(*) as product_count,
    AVG(price) as avg_price
FROM products p
JOIN categories c ON p.category_id = c.category_id
GROUP BY category_name
HAVING COUNT(*) > 5 AND AVG(price) > 100
ORDER BY avg_price DESC;
```

### 🔢 GROUPING SETS, ROLLUP, CUBE

#### GROUPING SETS
```sql
-- Продажи по разным измерениям
SELECT 
    category_name,
    brand_name,
    SUM(sales_amount) as total_sales
FROM sales_view
GROUP BY GROUPING SETS (
    (category_name),           -- По категориям
    (brand_name),             -- По брендам
    (category_name, brand_name), -- По категориям и брендам
    ()                        -- Общий итог
);
```

#### ROLLUP
```sql
-- Иерархические итоги: год → месяц → день
SELECT 
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month,
    EXTRACT(DAY FROM order_date) as day,
    SUM(total_amount) as daily_sales
FROM orders
GROUP BY ROLLUP (
    EXTRACT(YEAR FROM order_date),
    EXTRACT(MONTH FROM order_date),
    EXTRACT(DAY FROM order_date)
);
```

**Визуализация ROLLUP:**
```
┌─────────────────────────────────────────┐
│ ROLLUP результат:                       │
├─────────┬───────┬─────┬─────────────────┤
│ Year    │ Month │ Day │ Sales           │
├─────────┼───────┼─────┼─────────────────┤
│ 2024    │   1   │  1  │ $1000 (детализ.)│
│ 2024    │   1   │  2  │ $1500 (детализ.)│
│ 2024    │   1   │NULL │ $2500 (итог мес.)│
│ 2024    │   2   │  1  │ $2000 (детализ.)│
│ 2024    │   2   │NULL │ $2000 (итог мес.)│
│ 2024    │ NULL  │NULL │ $4500 (итог год)│
│ NULL    │ NULL  │NULL │ $4500 (общий)   │
└─────────┴───────┴─────┴─────────────────┘
```

---

## 3.5 Оконные функции (Window Functions) 🪟

### Что такое оконные функции?

Оконные функции выполняют вычисления над набором строк, связанных с текущей строкой, **НЕ сворачивая** результат в одну строку.

```sql
SELECT 
    column1,
    column2,
    WINDOW_FUNCTION() OVER (
        PARTITION BY column1 
        ORDER BY column2
        ROWS/RANGE frame_specification
    )
FROM table_name;
```

### 🔢 Функции ранжирования

```sql
-- Ранжирование товаров по цене в каждой категории
SELECT 
    product_name,
    category_name,
    price,
    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as row_num,
    RANK() OVER (PARTITION BY category_id ORDER BY price DESC) as rank_val,
    DENSE_RANK() OVER (PARTITION BY category_id ORDER BY price DESC) as dense_rank_val
FROM products p
JOIN categories c ON p.category_id = c.category_id;
```

**Визуализация функций ранжирования:**
```
Цена: $100, $90, $90, $80

ROW_NUMBER():  1, 2, 3, 4    (уникальные номера)
RANK():        1, 2, 2, 4    (пропускает номера при равенстве)
DENSE_RANK():  1, 2, 2, 3    (не пропускает номера)
```

### 📊 Агрегатные функции как оконные

```sql
-- Накопительная сумма продаж
SELECT 
    order_date,
    daily_sales,
    SUM(daily_sales) OVER (ORDER BY order_date) as running_total,
    AVG(daily_sales) OVER (ORDER BY order_date ROWS 6 PRECEDING) as avg_7_days
FROM daily_sales_view
ORDER BY order_date;
```

### ↔️ Функции смещения

```sql
-- Сравнение с предыдущими/следующими значениями
SELECT 
    month,
    sales,
    LAG(sales) OVER (ORDER BY month) as prev_month_sales,
    LEAD(sales) OVER (ORDER BY month) as next_month_sales,
    sales - LAG(sales) OVER (ORDER BY month) as month_growth
FROM monthly_sales;
```

**Визуализация LAG/LEAD:**
```
        LAG(1)     Текущая строка    LEAD(1)
          ←              ↓              →
┌─────────────────────────────────────────────┐
│ Jan │ Feb │ Mar │ Apr │ May │ Jun │ Jul │   │
└─────────────────────────────────────────────┘
  100   120   110   150   140   160   180

Для строки "Apr" (150):
LAG(sales) = 110 (значение Mar)
LEAD(sales) = 140 (значение May)
```

### 🎯 Практические применения

#### Топ-N запросы
```sql
-- Топ-3 товара по продажам в каждой категории
WITH ranked_products AS (
    SELECT 
        product_name,
        category_name,
        total_sales,
        ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY total_sales DESC) as rn
    FROM product_sales_view
)
SELECT *
FROM ranked_products
WHERE rn <= 3;
```

#### Перцентили
```sql
-- Найти товары в топ-10% по цене
SELECT 
    product_name,
    price,
    PERCENT_RANK() OVER (ORDER BY price) as price_percentile
FROM products
WHERE PERCENT_RANK() OVER (ORDER BY price) >= 0.9;
```

---

## 3.6 Операции с множествами 🔄

### Типы операций

```
ОПЕРАЦИИ С МНОЖЕСТВАМИ:
├── UNION     (Объединение без дубликатов)
├── UNION ALL (Объединение с дубликатами)
├── INTERSECT (Пересечение)
└── EXCEPT    (Разность)
```

### 🔗 UNION и UNION ALL

```sql
-- Все контакты: клиенты и поставщики
SELECT 'Customer' as type, customer_name as name, email
FROM customers
UNION ALL
SELECT 'Supplier' as type, supplier_name as name, email
FROM suppliers
ORDER BY type, name;
```

**Визуализация UNION:**
```
Таблица A        Таблица B        UNION           UNION ALL
┌─────────┐     ┌─────────┐      ┌─────────┐     ┌─────────┐
│    1    │     │    3    │      │    1    │     │    1    │
│    2    │     │    4    │      │    2    │     │    2    │
│    3    │     │    5    │  ───►│    3    │     │    3    │
└─────────┘     └─────────┘      │    4    │     │    3    │
                                 │    5    │     │    4    │
                                 └─────────┘     │    5    │
                                                 └─────────┘
                Убирает дубли      Оставляет все
```

### ⚡ INTERSECT (Пересечение)

```sql
-- Клиенты, которые также являются поставщиками
SELECT email
FROM customers
INTERSECT
SELECT email
FROM suppliers;
```

### ➖ EXCEPT (Разность)

```sql
-- Товары, которые никогда не заказывались
SELECT product_id
FROM products
EXCEPT
SELECT DISTINCT product_id
FROM order_items;
```

---

## 🎯 Практические задания

### Задание 1: Интернет-магазин - Сложная аналитика

Создайте запрос, который покажет:
- ТОП-5 клиентов по сумме заказов
- Их любимую категорию товаров
- Процент от общих продаж магазина

```sql
-- Ваше решение здесь
```

### Задание 2: Иерархия категорий

Используя рекурсивный CTE, постройте полное дерево категорий с уровнями вложенности.

### Задание 3: Анализ продаж

Создайте отчет с использованием оконных функций:
- Ранжирование товаров по продажам
- Рост продаж относительно предыдущего месяца
- Накопительная сумма продаж

---

## ✅ Чек-лист освоения блока

```
□ Понимаю различия между типами JOIN
□ Умею использовать подзапросы эффективно
□ Знаю когда использовать CTE вместо подзапросов
□ Владею рекурсивными CTE для иерархий
□ Понимаю разницу между GROUP BY и оконными функциями
□ Умею создавать сложные аналитические запросы
□ Знаю операции с множествами и их применение
□ Могу оптимизировать сложные запросы
```

---

## 🔍 Дополнительные ресурсы

- **PostgreSQL Documentation**: JOIN типы и оптимизация
- **Практика**: Решение задач на HackerRank SQL
- **Книга**: "Window Functions Explained" для углубленного изучения

---

## ➡️ Следующий блок

**Блок 4: Производительность и оптимизация**
- Планы выполнения запросов
- Индексы: углубленное изучение  
- Оптимизация сложных запросов

```
🎓 РЕЗУЛЬТАТ БЛОКА 3:
Умение писать сложные аналитические запросы,
глубокое понимание JOIN и группировок
```