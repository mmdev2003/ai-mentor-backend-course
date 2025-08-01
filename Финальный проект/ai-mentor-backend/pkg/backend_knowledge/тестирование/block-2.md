# 🎯 Блок 2: Практические навыки тестирования
**Продолжительность:** 3-4 месяца  
**Цель:** Освоить практические навыки создания тестов, поиска багов и документирования результатов

---

## 📋 Обзор блока

```
Глава 2.1: Техники тест-дизайна           [4 недели]
Глава 2.2: Тестовая документация          [3 недели]  
Глава 2.3: Работа с багами                [3 недели]
Глава 2.4: Тестирование веб-приложений    [4 недели]
Глава 2.5: Работа с базами данных         [2 недели]
```

------

## 🧠 Глава 2.1: Техники тест-дизайна (4 недели)

### Неделя 1: Классы эквивалентности и граничные значения

**Теория:**
- **Классы эквивалентности** - группировка входных данных, которые должны обрабатываться одинаково
- **Граничные значения** - тестирование на границах допустимых значений

**Практическое задание:**
```
Пример: Поле "Возраст" (диапазон 18-65)
┌─────────────────────────────────────────────────────────┐
│ Недопустимые │ Граничные │ Допустимые │ Граничные │ Недопустимые │
│   значения   │ значения  │  значения  │ значения  │   значения   │
├─────────────────────────────────────────────────────────┤
│    < 18      │  17, 18   │   19-64    │  65, 66   │    > 65      │
└─────────────────────────────────────────────────────────┘
```

**Упражнение:**
Создайте тест-кейсы для поля "Количество товаров в корзине" (1-99)

------

### Неделя 2: Таблицы решений и причинно-следственные диаграммы

**Таблица решений для логики скидок:**
```
┌─────────────────────────────────────────────────────────┐
│               УСЛОВИЯ                 │ T1│ T2│ T3│ T4│
├─────────────────────────────────────────────────────────┤
│ Сумма заказа > 1000₽                 │ Y │ Y │ N │ N │
│ Клиент - VIP                         │ Y │ N │ Y │ N │
├─────────────────────────────────────────────────────────┤
│               ДЕЙСТВИЯ                │   │   │   │   │
├─────────────────────────────────────────────────────────┤
│ Скидка 15%                           │ X │   │   │   │
│ Скидка 10%                           │   │ X │   │   │
│ Скидка 5%                            │   │   │ X │   │
│ Без скидки                           │   │   │   │ X │
└─────────────────────────────────────────────────────────┘
```

**Причинно-следственная диаграмма:**
```
    Причины                 Следствия
┌─────────────┐            ┌─────────────┐
│ Неверный    │────────────│ Сообщение   │
│ логин       │            │ об ошибке   │
└─────────────┘            └─────────────┘
       │                          │
       └──────────────────────────┘
┌─────────────┐            ┌─────────────┐
│ Неверный    │────────────│ Блокировка  │
│ пароль      │            │ аккаунта    │
└─────────────┘            └─────────────┘
```

------

### Неделя 3: Тестирование состояний и переходов

**Диаграмма состояний заказа:**
```
     [Создан]
        │
        ▼
   [Подтвержден] ←──────────── [Отменен]
        │                        ▲
        ▼                        │
   [Оплачен] ───────────────────┤
        │                        │
        ▼                        │
   [Отправлен] ─────────────────┤
        │                        │
        ▼                        │
   [Доставлен] ─────────────────┘
```

**Матрица переходов:**
```
┌─────────────┬───────┬───────┬───────┬───────┬───────┐
│ Из\В        │Создан │Подтвер│Оплачен│Отправ │Доставл│
├─────────────┼───────┼───────┼───────┼───────┼───────┤
│ Создан      │   -   │   ✓   │   ✗   │   ✗   │   ✗   │
│ Подтвержден │   ✗   │   -   │   ✓   │   ✗   │   ✗   │
│ Оплачен     │   ✗   │   ✗   │   -   │   ✓   │   ✗   │
│ Отправлен   │   ✗   │   ✗   │   ✗   │   -   │   ✓   │
│ Доставлен   │   ✗   │   ✗   │   ✗   │   ✗   │   -   │
└─────────────┴───────┴───────┴───────┴───────┴───────┘
```

------

### Неделя 4: Попарное тестирование и исследовательское тестирование

**Попарное тестирование (Pairwise):**
```
Параметры:
- Браузер: Chrome, Firefox, Safari
- ОС: Windows, MacOS, Linux  
- Разрешение: 1920x1080, 1366x768, 1024x768

Минимальный набор тестов:
┌─────────┬─────────┬─────────────┐
│ Браузер │    ОС   │ Разрешение  │
├─────────┼─────────┼─────────────┤
│ Chrome  │ Windows │ 1920x1080   │
│ Chrome  │ MacOS   │ 1366x768    │
│ Firefox │ Windows │ 1024x768    │
│ Firefox │ Linux   │ 1920x1080   │
│ Safari  │ MacOS   │ 1024x768    │
│ Safari  │ Linux   │ 1366x768    │
└─────────┴─────────┴─────────────┘
```

**Исследовательское тестирование:**
```
🔍 Чартер: Исследовать функцию поиска товаров
📋 Время: 60 минут
📝 Заметки:
  - Протестировать различные типы запросов
  - Проверить сортировку результатов
  - Изучить поведение при пустых результатах
  - Найти неочевидные баги
```

------

## 📄 Глава 2.2: Тестовая документация (3 недели)

### Неделя 1: Тест-план

**Структура тест-плана:**
```
1. ВВЕДЕНИЕ
   ├── 1.1 Цель документа
   ├── 1.2 Область применения
   └── 1.3 Аудитория

2. ОБЪЕКТ ТЕСТИРОВАНИЯ
   ├── 2.1 Описание системы
   ├── 2.2 Функциональность
   └── 2.3 Ограничения

3. СТРАТЕГИЯ ТЕСТИРОВАНИЯ
   ├── 3.1 Подходы к тестированию
   ├── 3.2 Уровни тестирования
   └── 3.3 Типы тестирования

4. КРИТЕРИИ ВХОДА/ВЫХОДА
   ├── 4.1 Критерии начала
   ├── 4.2 Критерии завершения
   └── 4.3 Критерии приостановки

5. РЕСУРСЫ
   ├── 5.1 Человеческие ресурсы
   ├── 5.2 Технические ресурсы
   └── 5.3 Тестовые данные

6. РИСКИ И МИТИГАЦИЯ
```

------

### Неделя 2: Тест-кейсы

**Шаблон тест-кейса:**
```
┌─────────────────────────────────────────────────────────┐
│ ID: TC001                                               │
│ Название: Авторизация с корректными данными             │
│ Приоритет: Высокий                                      │
│ Предусловия: Пользователь зарегистрирован               │
├─────────────────────────────────────────────────────────┤
│ ШАГИ ВЫПОЛНЕНИЯ:                                        │
│ 1. Открыть страницу авторизации                         │
│ 2. Ввести корректный email                              │
│ 3. Ввести корректный пароль                             │
│ 4. Нажать кнопку "Войти"                                │
├─────────────────────────────────────────────────────────┤
│ ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:                                    │
│ Пользователь успешно авторизован и перенаправлен       │
│ на главную страницу                                     │
└─────────────────────────────────────────────────────────┘
```

**Правила хорошего тест-кейса:**
- ✅ Один тест-кейс = одна проверка
- ✅ Четкие и понятные шаги
- ✅ Проверяемый результат
- ✅ Воспроизводимость
- ✅ Независимость от других тестов

------

### Неделя 3: Чек-листы и матрица трассировки

**Чек-лист vs Тест-кейс:**
```
┌─────────────────┬─────────────────┬─────────────────┐
│   Критерий      │   Чек-лист      │   Тест-кейс     │
├─────────────────┼─────────────────┼─────────────────┤
│ Детализация     │ Минимальная     │ Максимальная    │
│ Время создания  │ Быстро          │ Долго           │
│ Повторное исп.  │ Ограниченное    │ Полное          │
│ Отчетность      │ Базовая         │ Подробная       │
│ Новички         │ Сложно          │ Легко           │
└─────────────────┴─────────────────┴─────────────────┘
```

**Матрица трассировки:**
```
┌─────────────────┬──────────────────────────────────────┐
│   Требование    │           Тест-кейсы                 │
├─────────────────┼──────────────────────────────────────┤
│ REQ-001: Вход   │ TC001, TC002, TC003, TC004           │
│ REQ-002: Поиск  │ TC005, TC006, TC007                  │
│ REQ-003: Корзина│ TC008, TC009, TC010, TC011, TC012    │
│ REQ-004: Заказ  │ TC013, TC014, TC015, TC016           │
└─────────────────┴──────────────────────────────────────┘
```

------

## 🐛 Глава 2.3: Работа с багами (3 недели)

### Неделя 1: Жизненный цикл дефекта

**Диаграмма жизненного цикла:**
```
    [Новый]
       │
       ▼
   [Назначен] ──────────────► [Отклонен]
       │                          │
       ▼                          │
   [В работе] ──────────────► [Дубликат]
       │                          │
       ▼                          │
   [Исправлен] ──────────────► [Не воспроизводится]
       │                          │
       ▼                          │
   [Тестируется] ────────────────►│
       │                          │
   ┌───▼───┐                      │
   │Прошел?│                      │
   └─┬─────┘                      │
     │ Да                         │
     ▼                            │
   [Закрыт] ◄─────────────────────┘
     │ Нет
     ▼
   [Переоткрыт]
```

------

### Неделя 2: Классификация багов

**Критичность:**
```
🔴 BLOCKER   - Полная блокировка системы
🟠 CRITICAL  - Критическая функциональность не работает
🟡 MAJOR     - Важная функциональность работает некорректно
🟢 MINOR     - Незначительные проблемы
🔵 TRIVIAL   - Косметические дефекты
```

**Приоритет:**
```
P1 - Исправить немедленно
P2 - Исправить в текущей версии
P3 - Исправить в следующей версии
P4 - Исправить когда будет время
```

**Типы багов:**
```
┌─────────────────────────────────────────────────────────┐
│ 🔧 Функциональные                                        │
│ ├── Неправильная логика                                 │
│ ├── Неверные расчеты                                    │
│ └── Нарушение бизнес-правил                             │
├─────────────────────────────────────────────────────────┤
│ 🎨 Интерфейсные                                         │
│ ├── Неправильное отображение                            │
│ ├── Проблемы с версткой                                 │
│ └── Юзабилити                                           │
├─────────────────────────────────────────────────────────┤
│ ⚡ Производительности                                    │
│ ├── Медленная загрузка                                  │
│ ├── Высокое потребление ресурсов                        │
│ └── Таймауты                                            │
└─────────────────────────────────────────────────────────┘
```

------

### Неделя 3: Составление баг-репортов

**Шаблон баг-репорта:**
```
┌─────────────────────────────────────────────────────────┐
│ ID: BUG-001                                             │
│ Заголовок: Кнопка "Купить" не работает на iOS Safari   │
│ Критичность: Major        Приоритет: P1                │
│ Статус: Новый             Назначен: Developer_1        │
├─────────────────────────────────────────────────────────┤
│ ОКРУЖЕНИЕ:                                              │
│ • ОС: iOS 15.6                                          │
│ • Браузер: Safari 15.6                                  │
│ • Устройство: iPhone 13                                 │
│ • URL: https://shop.example.com/product/123             │
├─────────────────────────────────────────────────────────┤
│ ПРЕДУСЛОВИЯ:                                            │
│ • Пользователь авторизован                              │
│ • Товар добавлен в корзину                              │
│ • Корзина содержит 1 товар                              │
├─────────────────────────────────────────────────────────┤
│ ШАГИ ВОСПРОИЗВЕДЕНИЯ:                                   │
│ 1. Открыть страницу товара                              │
│ 2. Нажать кнопку "Купить"                               │
│ 3. Наблюдать результат                                  │
├─────────────────────────────────────────────────────────┤
│ ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:                                    │
│ Открывается страница оформления заказа                  │
├─────────────────────────────────────────────────────────┤
│ ФАКТИЧЕСКИЙ РЕЗУЛЬТАТ:                                  │
│ Кнопка не реагирует на нажатие, никаких действий       │
│ не происходит                                           │
├─────────────────────────────────────────────────────────┤
│ ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:                              │
│ • Скриншот: screenshot_001.png                          │
│ • Логи: console_log.txt                                 │
│ • На Android Chrome работает корректно                  │
└─────────────────────────────────────────────────────────┘
```

**Правила хорошего баг-репорта:**
- ✅ Информативный заголовок
- ✅ Четкие шаги воспроизведения
- ✅ Точное описание проблемы
- ✅ Приложения (скриншоты, логи)
- ✅ Информация об окружении

------

## 🌐 Глава 2.4: Тестирование веб-приложений (4 недели)

### Неделя 1: Особенности тестирования веб-интерфейсов

**Чек-лист тестирования веб-формы:**
```
┌─────────────────────────────────────────────────────────┐
│ 📋 ФУНКЦИОНАЛЬНОСТЬ                                      │
│ □ Все поля работают корректно                           │
│ □ Валидация полей                                       │
│ □ Обязательные поля помечены                            │
│ □ Сообщения об ошибках понятны                          │
│ □ Успешная отправка формы                               │
├─────────────────────────────────────────────────────────┤
│ 🎨 ИНТЕРФЕЙС                                            │
│ □ Корректное отображение во всех браузерах              │
│ □ Адаптивность под разные экраны                        │
│ □ Читаемость текста                                     │
│ □ Логичное расположение элементов                       │
│ □ Состояния элементов (hover, focus, active)           │
├─────────────────────────────────────────────────────────┤
│ 🔒 БЕЗОПАСНОСТЬ                                         │
│ □ Защита от XSS                                         │
│ □ Валидация на стороне сервера                          │
│ □ Защита от CSRF                                        │
│ □ Безопасная передача данных                            │
└─────────────────────────────────────────────────────────┘
```

------

### Неделя 2: Кроссбраузерное тестирование

**Матрица совместимости:**
```
┌─────────────────┬───────┬───────┬───────┬───────┬───────┐
│ Браузер\Версия  │ Win10 │ MacOS │ Linux │ iOS   │Android│
├─────────────────┼───────┼───────┼───────┼───────┼───────┤
│ Chrome Latest   │   ✅   │   ✅   │   ✅   │   ✅   │   ✅   │
│ Chrome -1       │   ✅   │   ✅   │   ✅   │   ✅   │   ✅   │
│ Firefox Latest  │   ✅   │   ✅   │   ✅   │   -   │   ✅   │
│ Safari Latest   │   -   │   ✅   │   -   │   ✅   │   -   │
│ Edge Latest     │   ✅   │   ✅   │   ✅   │   -   │   ✅   │
│ IE 11           │   ⚠️   │   -   │   -   │   -   │   -   │
└─────────────────┴───────┴───────┴───────┴───────┴───────┘
```

**Основные различия браузеров:**
```
🔍 CSS поддержка:
├── Grid Layout: IE11 - частичная поддержка
├── Flexbox: IE11 - баги с flex-basis
└── Custom Properties: IE11 - не поддерживается

🔍 JavaScript:
├── ES6+: IE11 - требует транспиляции
├── Fetch API: IE11 - нужен полифилл
└── Promise: IE11 - нужен полифилл

🔍 Rendering:
├── Webkit: Safari, Chrome (до v27)
├── Blink: Chrome (v28+), Edge (v79+)
└── Gecko: Firefox
```

------

### Неделя 3: Responsive design и DevTools

**Контрольные точки (breakpoints):**
```
📱 Mobile:     320px - 768px
📱 Tablet:     768px - 1024px  
💻 Desktop:    1024px - 1440px
🖥️  Large:     1440px+

Тестирование:
├── 320px  (iPhone 5)
├── 375px  (iPhone X)
├── 768px  (iPad Portrait)
├── 1024px (iPad Landscape)
├── 1366px (Laptop)
└── 1920px (Desktop)
```

**DevTools для тестирования:**
```
┌─────────────────────────────────────────────────────────┐
│ 🔧 ОСНОВНЫЕ ИНСТРУМЕНТЫ                                  │
│ ├── Elements - DOM/CSS инспектор                        │
│ ├── Console - JavaScript консоль                        │
│ ├── Network - Мониторинг сетевых запросов               │
│ ├── Performance - Анализ производительности             │
│ └── Application - Локальные данные, кеши                │
├─────────────────────────────────────────────────────────┤
│ 🎯 ПОЛЕЗНЫЕ ФУНКЦИИ                                     │
│ ├── Device Mode - Эмуляция мобильных устройств          │
│ ├── Lighthouse - Аудит качества                         │
│ ├── Coverage - Анализ используемого кода                │
│ └── Security - Проверка безопасности                    │
└─────────────────────────────────────────────────────────┘
```

------

### Неделя 4: HTML/CSS для тестировщиков

**Основные HTML элементы:**
```html
<!-- Структура документа -->
<html>
<head>
  <title>Заголовок страницы</title>
  <meta charset="UTF-8">
</head>
<body>
  <!-- Заголовки -->
  <h1>Главный заголовок</h1>
  <h2>Подзаголовок</h2>
  
  <!-- Формы -->
  <form>
    <input type="text" required>
    <input type="email" required>
    <button type="submit">Отправить</button>
  </form>
  
  <!-- Списки -->
  <ul>
    <li>Элемент списка</li>
  </ul>
</body>
</html>
```

**Важные CSS селекторы:**
```css
/* Класс */
.button { color: blue; }

/* ID */
#main-header { font-size: 24px; }

/* Атрибут */
input[type="email"] { border: 1px solid red; }

/* Состояние */
.button:hover { background: gray; }
.input:focus { border: 2px solid blue; }

/* Медиа запросы */
@media (max-width: 768px) {
  .container { width: 100%; }
}
```

------

## 🗄️ Глава 2.5: Работа с базами данных (2 недели)

### Неделя 1: Основы SQL

**Основные команды SQL:**
```sql
-- Выборка данных
SELECT * FROM users;
SELECT name, email FROM users WHERE age > 18;

-- Группировка и сортировка
SELECT status, COUNT(*) FROM orders 
GROUP BY status 
ORDER BY COUNT(*) DESC;

-- Соединения таблиц
SELECT u.name, o.total 
FROM users u 
JOIN orders o ON u.id = o.user_id;

-- Агрегатные функции
SELECT 
  COUNT(*) as total_orders,
  SUM(total) as total_amount,
  AVG(total) as avg_order
FROM orders;
```

**Типы данных для тестирования:**
```
┌─────────────────┬─────────────────────────────────────┐
│ Тип данных      │ Что тестировать                     │
├─────────────────┼─────────────────────────────────────┤
│ VARCHAR(50)     │ Длина строки, спецсимволы           │
│ INT             │ Диапазон значений, переполнение     │
│ DECIMAL(10,2)   │ Точность, округление                │
│ DATE/DATETIME   │ Форматы дат, временные зоны         │
│ BOOLEAN         │ Логические значения, NULL           │
└─────────────────┴─────────────────────────────────────┘
```

------

### Неделя 2: Тестирование CRUD операций

**Чек-лист тестирования CRUD:**
```
┌─────────────────────────────────────────────────────────┐
│ 🔧 CREATE (Создание)                                     │
│ □ Создание с валидными данными                          │
│ □ Создание с невалидными данными                        │
│ □ Создание дубликатов                                   │
│ □ Создание с пустыми полями                             │
│ □ Создание с максимальными значениями                   │
├─────────────────────────────────────────────────────────┤
│ 📖 READ (Чтение)                                        │
│ □ Поиск по ID                                           │
│ □ Поиск по фильтрам                                     │
│ □ Сортировка результатов                                │
│ □ Пагинация                                             │
│ □ Поиск несуществующих записей                          │
├─────────────────────────────────────────────────────────┤
│ ✏️ UPDATE (Обновление)                                   │
│ □ Обновление существующей записи                        │
│ □ Обновление несуществующей записи                      │
│ □ Частичное обновление                                  │
│ □ Обновление с невалидными данными                      │
│ □ Конкурентное обновление                               │
├─────────────────────────────────────────────────────────┤
│ 🗑️ DELETE (Удаление)                                     │
│ □ Удаление существующей записи                          │
│ □ Удаление несуществующей записи                        │
│ □ Каскадное удаление                                    │
│ □ Мягкое удаление                                       │
│ □ Восстановление удаленных записей                      │
└─────────────────────────────────────────────────────────┘
```

------

## 🏆 Итоговый результат блока 2

### Практические навыки:
```
✅ Создание тест-кейсов с использованием техник тест-дизайна
✅ Написание качественных баг-репортов
✅ Тестирование веб-приложений в разных браузерах
✅ Работа с тестовой документацией
✅ Базовые навыки работы с SQL
```

### Портфолио:
```
📁 Проект "Тестирование интернет-магазина"
├── 📄 Тест-план (15 страниц)
├── 📋 50+ тест-кейсов
├── 🐛 20+ баг-репортов
├── 📊 Матрица трассировки
└── 📱 Отчет по кроссбраузерному тестированию
```

### Инструменты:
```
🔧 Освоенные инструменты:
├── Jira (баг-трекинг)
├── TestRail (управление тестами)
├── Browser DevTools
├── SQL клиент (DBeaver/phpMyAdmin)
└── Инструменты скриншотов
```

------

## 📝 Домашние задания

### Задание 1: Техники тест-дизайна
Создайте тест-кейсы для формы регистрации, используя все изученные техники

### Задание 2: Баг-репорты
Найдите и опишите 10 багов в тестовом приложении

### Задание 3: Кроссбраузерное тестирование
Протестируйте веб-приложение в 5 разных браузерах и составьте отчет

### Задание 4: SQL запросы
Напишите 20 SQL запросов для проверки данных в тестовой БД

------

## 🎯 Подготовка к следующему блоку

Перед переходом к блоку 3 "Автоматизация тестирования" убедитесь, что вы:
- ✅ Уверенно создаете тест-кейсы
- ✅ Находите и описываете баги
- ✅ Работаете с тестовой документацией
- ✅ Знаете основы HTML/CSS/SQL
- ✅ Имеете портфолио с примерами работ

**Следующий блок**: Автоматизация тестирования - изучение программирования и инструментов автоматизации.