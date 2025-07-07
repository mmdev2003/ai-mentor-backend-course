# Блок 1: Основы и принципы чистого кода

**Длительность:** 3-4 недели  
**Цель:** Заложить фундамент понимания качественного кода и базовых принципов

---

## 📋 Содержание блока

```
┌─ Глава 1: Введение в архитектуру кода
├─ Глава 2: Принципы чистого кода (Clean Code)
├─ Глава 3: Искусство именования
├─ Глава 4: Структура и организация кода
└─ Глава 5: Комментирование и документация
```

---

## 🎯 Глава 1: Введение в архитектуру кода

### Что такое архитектура и почему она критически важна

```
    ┌─────────────────────────────────────────┐
    │              АРХИТЕКТУРА                │
    ├─────────────────────────────────────────┤
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
    │  │ Модуль  │  │ Модуль  │  │ Модуль  │  │
    │  │   A     │──│   B     │──│   C     │  │
    │  └─────────┘  └─────────┘  └─────────┘  │
    │       │            │            │       │
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
    │  │ Модуль  │  │ Модуль  │  │ Модуль  │  │
    │  │   D     │──│   E     │──│   F     │  │
    │  └─────────┘  └─────────┘  └─────────┘  │
    └─────────────────────────────────────────┘
```

**Архитектура кода** — это структурная организация программного обеспечения, определяющая:
- Как компоненты взаимодействуют друг с другом
- Где размещена бизнес-логика
- Как происходит поток данных
- Какие принципы используются для принятия решений

### Стоимость плохой архитектуры

```
Время разработки   ┌─ Хорошая архитектура
                   │
      ▲            │     ┌─── Плохая архитектура
      │            │    ╱
      │            │   ╱
      │            │  ╱
      │            │ ╱
      │            │╱
      └────────────┴──────────────────► Время
                   
    Начало        6 мес        1 год        2 года
```

**Признаки плохой архитектуры:**
- Любое изменение требует модификации множества файлов
- Код сложно тестировать
- Новые функции добавляются все медленнее
- Багов становится больше с каждым релизом

### Технический долг и его последствия

```
    ┌─────────────────────────────────────────┐
    │           ТЕХНИЧЕСКИЙ ДОЛГ              │
    ├─────────────────────────────────────────┤
    │                                         │
    │  📈 Накопление                          │
    │  ├─ Быстрые решения                     │
    │  ├─ Пропуск рефакторинга                │
    │  ├─ Игнорирование принципов             │
    │  └─ Отсутствие документации             │
    │                                         │
    │  💸 Проценты                            │
    │  ├─ Медленная разработка                │
    │  ├─ Больше багов                        │
    │  ├─ Сложность изменений                 │
    │  └─ Демотивация команды                 │
    │                                         │
    └─────────────────────────────────────────┘
```

---

## 🧹 Глава 2: Принципы чистого кода (Clean Code)

### Читаемость как основа качества

```
    ┌─────────────────────────────────────────┐
    │              ЧИТАЕМЫЙ КОД               │
    ├─────────────────────────────────────────┤
    │                                         │
    │  👁️  Понятность с первого взгляда       │
    │  🎯  Ясность намерений                   │
    │  🔍  Легкость отладки                    │
    │  🤝  Простота сопровождения             │
    │  📚  Возможность обучения               │
    │                                         │
    └─────────────────────────────────────────┘
```

### ❌ Плохой пример (Python):

```python
def calc(a, b, c):
    # вычисляем что-то
    if c == 1:
        return a + b
    elif c == 2:
        return a - b
    elif c == 3:
        return a * b
    elif c == 4:
        if b != 0:
            return a / b
        else:
            return None
    else:
        return None
```

### ✅ Хороший пример (Python):

```python
from enum import Enum
from typing import Optional

class Operation(Enum):
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4

def calculate(first_number: float, second_number: float, operation: Operation) -> Optional[float]:
    """Выполняет арифметическую операцию над двумя числами."""
    
    if operation == Operation.ADD:
        return first_number + second_number
    elif operation == Operation.SUBTRACT:
        return first_number - second_number
    elif operation == Operation.MULTIPLY:
        return first_number * second_number
    elif operation == Operation.DIVIDE:
        return divide_safely(first_number, second_number)
    
    raise ValueError(f"Неподдерживаемая операция: {operation}")

def divide_safely(dividend: float, divisor: float) -> Optional[float]:
    """Безопасное деление с проверкой на ноль."""
    if divisor == 0:
        return None
    return dividend / divisor
```

### ❌ Плохой пример (Go):

```go
func proc(d []int) int {
    s := 0
    for i := 0; i < len(d); i++ {
        if d[i] > 0 {
            s += d[i]
        }
    }
    return s
}
```

### ✅ Хороший пример (Go):

```go
// CalculatePositiveSum возвращает сумму всех положительных чисел в слайсе
func CalculatePositiveSum(numbers []int) int {
    positiveSum := 0
    
    for _, number := range numbers {
        if isPositive(number) {
            positiveSum += number
        }
    }
    
    return positiveSum
}

func isPositive(number int) bool {
    return number > 0
}
```

### Принцип наименьшего удивления

```
    ┌─────────────────────────────────────────┐
    │     ПРИНЦИП НАИМЕНЬШЕГО УДИВЛЕНИЯ       │
    ├─────────────────────────────────────────┤
    │                                         │
    │  Код должен работать так,               │
    │  как ожидает разработчик                │
    │                                         │
    │  ✅ Предсказуемое поведение             │
    │  ✅ Согласованность в именовании        │
    │  ✅ Соответствие конвенциям             │
    │  ✅ Интуитивные интерфейсы              │
    │                                         │
    └─────────────────────────────────────────┘
```

---

## 🏷️ Глава 3: Искусство именования

### Выбор значимых имен

```
    ┌─────────────────────────────────────────┐
    │             ХОРОШИЕ ИМЕНА               │
    ├─────────────────────────────────────────┤
    │                                         │
    │  📝 Выражают намерения                  │
    │  🎯 Указывают на назначение             │
    │  🔍 Облегчают поиск                     │
    │  📖 Произносимы                         │
    │  🚫 Избегают дезинформации              │
    │                                         │
    └─────────────────────────────────────────┘
```

### Примеры плохого и хорошего именования

#### ❌ Плохо:
```python
# Python
d = 30  # дней
users = []  # список пользователей
def proc_usr(u):  # обработать пользователя
    pass

def get_usr_by_id(id):  # получить пользователя по ID
    pass
```

```go
// Go
var d int = 30
var users []string
func procUsr(u User) error { return nil }
func getUsrById(id int) (*User, error) { return nil, nil }
```

#### ✅ Хорошо:
```python
# Python
TRIAL_PERIOD_DAYS = 30
active_users = []

def validate_user_credentials(user: User) -> bool:
    """Проверяет корректность учетных данных пользователя."""
    pass

def find_user_by_id(user_id: int) -> Optional[User]:
    """Находит пользователя по его уникальному идентификатору."""
    pass
```

```go
// Go
const TrialPeriodDays = 30
var activeUsers []User

func ValidateUserCredentials(user User) error {
    // Проверяет корректность учетных данных пользователя
    return nil
}

func FindUserByID(userID int) (*User, error) {
    // Находит пользователя по его уникальному идентификатору
    return nil, nil
}
```

### Контекст и область видимости

```
    Область видимости     │ Длина имени
    ─────────────────────┼─────────────────
    Локальная переменная │ Короткое (i, j, err)
    Поле класса          │ Среднее (userID, firstName)
    Глобальная функция   │ Длинное (CalculateMonthlyRevenue)
    Константа            │ Очень описательное (MAX_RETRY_ATTEMPTS)
```

---

## 🏗️ Глава 4: Структура и организация кода

### Принципы разбиения на функции

```
    ┌─────────────────────────────────────────┐
    │            ХОРОШАЯ ФУНКЦИЯ              │
    ├─────────────────────────────────────────┤
    │                                         │
    │  🎯 Делает одну вещь                    │
    │  📏 Короткая (< 20 строк)               │
    │  📝 Выразительное имя                   │
    │  📋 Мало параметров (< 4)               │
    │  🚫 Без побочных эффектов               │
    │                                         │
    └─────────────────────────────────────────┘
```

### ❌ Плохой пример (Python):

```python
def process_order(order_data):
    # валидация
    if not order_data.get('customer_id'):
        return {'error': 'No customer ID'}
    if not order_data.get('items'):
        return {'error': 'No items'}
    
    # расчет цены
    total = 0
    for item in order_data['items']:
        total += item['price'] * item['quantity']
    
    # применение скидки
    if order_data.get('discount_code'):
        if order_data['discount_code'] == 'SAVE10':
            total *= 0.9
        elif order_data['discount_code'] == 'SAVE20':
            total *= 0.8
    
    # сохранение в БД
    db.save_order({
        'customer_id': order_data['customer_id'],
        'total': total,
        'items': order_data['items']
    })
    
    # отправка email
    send_email(order_data['customer_id'], f'Order total: ${total}')
    
    return {'success': True, 'total': total}
```

### ✅ Хороший пример (Python):

```python
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class OrderItem:
    price: float
    quantity: int

@dataclass
class Order:
    customer_id: str
    items: List[OrderItem]
    discount_code: Optional[str] = None

class OrderProcessor:
    def process_order(self, order: Order) -> Dict[str, any]:
        """Обрабатывает заказ: валидирует, рассчитывает стоимость, сохраняет."""
        
        validation_error = self._validate_order(order)
        if validation_error:
            return {'error': validation_error}
        
        total_cost = self._calculate_total_cost(order)
        
        self._save_order_to_database(order, total_cost)
        self._send_confirmation_email(order.customer_id, total_cost)
        
        return {'success': True, 'total': total_cost}
    
    def _validate_order(self, order: Order) -> Optional[str]:
        """Валидирует данные заказа."""
        if not order.customer_id:
            return 'Customer ID is required'
        if not order.items:
            return 'Order must contain at least one item'
        return None
    
    def _calculate_total_cost(self, order: Order) -> float:
        """Рассчитывает общую стоимость заказа с учетом скидок."""
        subtotal = sum(item.price * item.quantity for item in order.items)
        return self._apply_discount(subtotal, order.discount_code)
    
    def _apply_discount(self, amount: float, discount_code: Optional[str]) -> float:
        """Применяет скидку к сумме."""
        discount_rates = {
            'SAVE10': 0.9,
            'SAVE20': 0.8
        }
        
        if discount_code in discount_rates:
            return amount * discount_rates[discount_code]
        return amount
    
    def _save_order_to_database(self, order: Order, total: float):
        """Сохраняет заказ в базу данных."""
        # Логика сохранения
        pass
    
    def _send_confirmation_email(self, customer_id: str, total: float):
        """Отправляет email с подтверждением заказа."""
        # Логика отправки email
        pass
```

### Размер функций и классов

```
    ┌─────────────────────────────────────────┐
    │           РАЗМЕРЫ КОМПОНЕНТОВ           │
    ├─────────────────────────────────────────┤
    │                                         │
    │  Функция:     5-20 строк               │
    │  Метод:       5-15 строк               │
    │  Класс:       < 200 строк              │
    │  Файл:        < 500 строк              │
    │  Параметры:   ≤ 3-4                     │
    │                                         │
    └─────────────────────────────────────────┘
```

### Вертикальное форматирование (Go пример):

```go
package user

import (
    "errors"
    "fmt"
    "time"
)

// User представляет пользователя системы
type User struct {
    ID        int       `json:"id"`
    Email     string    `json:"email"`
    CreatedAt time.Time `json:"created_at"`
}

// UserService предоставляет операции для работы с пользователями
type UserService struct {
    repository UserRepository
    validator  UserValidator
}

// NewUserService создает новый экземпляр UserService
func NewUserService(repo UserRepository, validator UserValidator) *UserService {
    return &UserService{
        repository: repo,
        validator:  validator,
    }
}

// CreateUser создает нового пользователя после валидации
func (s *UserService) CreateUser(email string) (*User, error) {
    if err := s.validator.ValidateEmail(email); err != nil {
        return nil, fmt.Errorf("invalid email: %w", err)
    }

    user := &User{
        Email:     email,
        CreatedAt: time.Now(),
    }

    if err := s.repository.Save(user); err != nil {
        return nil, fmt.Errorf("failed to save user: %w", err)
    }

    return user, nil
}

// FindUserByEmail находит пользователя по email
func (s *UserService) FindUserByEmail(email string) (*User, error) {
    if email == "" {
        return nil, errors.New("email cannot be empty")
    }

    return s.repository.FindByEmail(email)
}
```

---

## 📝 Глава 5: Комментирование и документация

### Когда комментарии нужны, а когда вредны

```
    ┌─────────────────────────────────────────┐
    │              КОММЕНТАРИИ                │
    ├─────────────────────────────────────────┤
    │                                         │
    │  ✅ ХОРОШИЕ КОММЕНТАРИИ:                │
    │    • Объяснение "почему", не "что"      │
    │    • Предупреждения                     │
    │    • TODO и FIXME                       │
    │    • Документация API                   │
    │    • Сложные алгоритмы                  │
    │                                         │
    │  ❌ ПЛОХИЕ КОММЕНТАРИИ:                 │
    │    • Очевидные вещи                     │
    │    • Устаревшая информация              │
    │    • Компенсация плохого кода           │
    │    • Журнал изменений                   │
    │                                         │
    └─────────────────────────────────────────┘
```

### ❌ Плохие комментарии:

```python
# Плохо: объясняет очевидное
counter = 0  # устанавливаем счетчик в ноль

# Плохо: устаревший комментарий
def calculate_tax(amount):
    # Старая ставка налога была 18%
    return amount * 0.20  # Сейчас 20%

# Плохо: компенсирует плохой код
def proc(d):  # обрабатывает данные пользователя
    pass
```

### ✅ Хорошие комментарии:

```python
# Хорошо: объясняет "почему"
# Используем экспоненциальную задержку для предотвращения DDoS атак
time.sleep(2 ** retry_count)

# Хорошо: предупреждение
def delete_all_users():
    """
    ВНИМАНИЕ: Эта функция удаляет ВСЕХ пользователей из базы данных!
    Используйте только для очистки тестовых данных.
    """
    pass

# Хорошо: объяснение сложного алгоритма
def quick_sort(arr):
    """
    Реализация быстрой сортировки с оптимизацией для небольших массивов.
    
    Алгоритм использует рандомизированный выбор опорного элемента
    для предотвращения худшего случая O(n²) на отсортированных данных.
    """
    pass

# Хорошо: TODO с объяснением
# TODO: Реализовать кэширование результатов для улучшения производительности
# Приоритет: средний, планируется в версии 2.1
def expensive_calculation():
    pass
```

### Go документация:

```go
// Package calculator предоставляет функции для математических вычислений
package calculator

// Errors возвращаемые пакетом calculator
var (
    ErrDivisionByZero = errors.New("division by zero")
    ErrInvalidInput   = errors.New("invalid input")
)

// Calculator выполняет арифметические операции
type Calculator struct {
    precision int
}

// NewCalculator создает новый Calculator с заданной точностью
//
// Параметр precision определяет количество знаков после запятой
// для операций с плавающей точкой. Если precision < 0, используется
// значение по умолчанию (2).
func NewCalculator(precision int) *Calculator {
    if precision < 0 {
        precision = 2
    }
    return &Calculator{precision: precision}
}

// Divide выполняет деление двух чисел
//
// Возвращает результат деления dividend на divisor.
// Если divisor равен нулю, возвращает ErrDivisionByZero.
//
// Пример использования:
//   calc := NewCalculator(2)
//   result, err := calc.Divide(10, 3)
//   if err != nil {
//       log.Fatal(err)
//   }
//   fmt.Printf("Результат: %.2f", result) // Результат: 3.33
func (c *Calculator) Divide(dividend, divisor float64) (float64, error) {
    if divisor == 0 {
        return 0, ErrDivisionByZero
    }
    
    result := dividend / divisor
    
    // Округляем результат до заданной точности
    multiplier := math.Pow(10, float64(c.precision))
    return math.Round(result*multiplier) / multiplier, nil
}
```

---

## 🎯 Практические задания

### 📋 Задание 1: Рефакторинг "грязного" кода

Дан код на Python:
```python
def f(l):
    r = []
    for i in range(len(l)):
        if l[i] % 2 == 0:
            r.append(l[i] * 2)
    return r

def g(d, k):
    if k in d:
        return d[k]
    else:
        return None
```

**Задача:** Отрефакторить код согласно принципам чистого кода.

### 📋 Задание 2: Создание style guide

Создайте краткий style guide для вашей команды, включающий:
- Правила именования
- Структуру функций
- Комментирование
- Форматирование

### 📋 Задание 3: Код-ревью с фокусом на читаемость

Проведите ревью кода коллеги, сосредоточившись на:
- Понятности имен
- Размере функций
- Наличии магических чисел
- Качестве комментариев

---

## 📊 Критерии оценки блока

```
    ┌─────────────────────────────────────────┐
    │          ИТОГОВАЯ ОЦЕНКА БЛОКА          │
    ├─────────────────────────────────────────┤
    │                                         │
    │  ✅ Понимание принципов чистого кода    │
    │  ✅ Умение выбирать хорошие имена       │
    │  ✅ Навык организации кода              │
    │  ✅ Правильное использование комментариев│
    │  ✅ Способность оценивать качество кода │
    │                                         │
    │  🎯 Результат: Умение писать читаемый,  │
    │     понятный код и оценивать качество   │
    │     существующего кода                  │
    │                                         │
    └─────────────────────────────────────────┘
```

---

## 🚀 Переход к следующему блоку

После успешного освоения принципов чистого кода вы готовы перейти к изучению **SOLID принципов и основ ООП**, где научитесь создавать гибкие и расширяемые архитектуры.

```
Блок 1: Основы ────► Блок 2: SOLID ────► Блок 3: Паттерны
   ✅                     🎯                    ⏳
```