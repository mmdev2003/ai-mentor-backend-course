# ⚡ Блок 3: Конкурентность и параллелизм

**⏱️ Длительность:** 2-3 месяца  
**🎯 Цель:** Освоить горутины и каналы - ключевые особенности Go

---

## 🧠 Философия конкурентности в Go

Go был создан с учетом современных многоядерных процессоров и распределенных систем. Его модель конкурентности основана на принципе:

> **"Не общайтесь разделяя память; вместо этого разделяйте память общаясь"**
> 
> *Don't communicate by sharing memory; share memory by communicating*

```
Традиционный подход          Go подход
──────────────────          ──────────

Потоки + Мьютексы     →     Горутины + Каналы
Разделяемая память    →     Передача сообщений
Сложная синхронизация →     Простая коммуникация

┌─────────────────┐         ┌─────────────────┐
│ Thread 1 ←→ RAM │         │ Goroutine 1     │
│ Thread 2 ←→ RAM │   VS    │       ↓         │
│ Thread 3 ←→ RAM │         │    Channel      │
│     ↑           │         │       ↓         │
│   Mutex         │         │ Goroutine 2     │
└─────────────────┘         └─────────────────┘
```

---

## 3.1 🚀 Основы конкурентности

### Конкурентность vs Параллелизм

Важно понимать разницу между этими концепциями:

```
КОНКУРЕНТНОСТЬ (Concurrency)
═══════════════════════════════════════
Дело о структуре - как организован код

    Задача A ─┐
              ├─→ CPU ─→ Результат
    Задача B ─┘

"Несколько задач МОГУТ выполняться одновременно"

────────────────────────────────────────

ПАРАЛЛЕЛИЗМ (Parallelism)  
═══════════════════════════════════════
Дело о выполнении - как работает железо

    Задача A ──→ CPU 1 ──→ Результат A
    Задача B ──→ CPU 2 ──→ Результат B

"Несколько задач ДЕЙСТВИТЕЛЬНО выполняются одновременно"
```

### Визуализация концепций

```
Последовательное выполнение:
████████████████████████████████████████
A-A-A-A-A-A-B-B-B-B-B-B-C-C-C-C-C-C

Конкурентное выполнение (1 CPU):
████████████████████████████████████████
A-A-B-B-C-A-A-B-C-C-A-B-B-A-C-C

Параллельное выполнение (3 CPU):
████████████████████████████████████████
A-A-A-A-A-A    CPU 1
B-B-B-B-B-B    CPU 2  
C-C-C-C-C-C    CPU 3
```

### Зачем нужна конкурентность?

```
Преимущества конкурентного программирования:
═══════════════════════════════════════════

✅ Отзывчивость UI - пользователь не ждет
✅ Эффективность I/O - пока один запрос ждет, другой обрабатывается
✅ Масштабируемость - больше пользователей одновременно
✅ Производительность - используем все ядра процессора
✅ Модульность - разные части работают независимо

Примеры из реальной жизни:
─────────────────────────

🌐 Web сервер: обслуживает множество клиентов
📁 Загрузчик файлов: скачивает несколько файлов
🎮 Игра: обработка ввода + рендеринг + звук + ИИ
📊 Анализ данных: обработка разных частей датасета
```

### Горутины - легковесные потоки

Горутины - это **функции, выполняющиеся конкурентно** с другим кодом:

```
Сравнение ресурсов:
═══════════════════════════════════════

                OS Thread    Goroutine
                ─────────    ─────────
Размер стека:   1-2 MB      2-8 KB
Время создания: ~1000ns     ~100ns  
Количество:     ~1000       ~100000+
Переключение:   ~1000ns     ~10ns

┌─────────────────────────────────────────┐
│ На одном OS потоке может работать       │
│ тысячи горутин!                         │
└─────────────────────────────────────────┘
```

### Создание горутин

```
Синтаксис:
─────────

go someFunction()     // запуск функции как горутину
go func() {          // анонимная функция как горутина
    // код
}()

Визуализация:
────────────

main()                     main()
  │                          │
  ├─ обычный вызов          ├─ go someFunc() ──→ [Горутина]
  │  someFunc()             │                      │
  │     │                  │                      │
  │  ждет завершения       │  продолжает         │
  │     │                  │  выполнение         │
  └─ продолжение           └─ может завершиться   │
                              раньше горутины!   │
                                                  │
                              ┌───────────────────┘
                              ▼
                           [Горутина работает независимо]
```

### Планировщик Go (Go Scheduler)

Go использует M:N планировщик - M горутин на N OS потоках:

```
Go Runtime Scheduler (M:N модель)
═══════════════════════════════════════════

        Горутины (G)
    G1  G2  G3  G4  G5  G6  G7  G8
     │   │   │   │   │   │   │   │
     └─┬─┘   └─┬─┘   └─┬─┘   └─┬─┘
       │       │       │       │
    ┌──▼──┐ ┌──▼──┐ ┌──▼──┐ ┌──▼──┐
    │ P1  │ │ P2  │ │ P3  │ │ P4  │  ← Процессоры (P)
    └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘    (логические)
       │       │       │       │
    ┌──▼──┐ ┌──▼──┐ ┌──▼──┐ ┌──▼──┐
    │ M1  │ │ M2  │ │ M3  │ │ M4  │  ← OS потоки (M)
    └─────┘ └─────┘ └─────┘ └─────┘

G = Goroutine (горутина)
P = Processor (логический процессор) 
M = Machine (OS поток)

GOMAXPROCS = количество P (по умолчанию = количество CPU ядер)
```

### Work Stealing

Go использует алгоритм "кражи работы":

```
Планировщик с Work Stealing:
═══════════════════════════════════

Процессор P1 (занят)     Процессор P2 (свободен)
┌─────────────────┐      ┌─────────────────┐
│ G1 (выполняется)│      │ (простаивает)   │
│ G2 (в очереди)  │      │                 │
│ G3 (в очереди)  │      │                 │
│ G4 (в очереди)  │      │                 │
└─────────────────┘      └─────────────────┘
        │                        ▲
        │ "кража работы"          │
        └─ G3, G4 ─────────────────┘

Результат:
─────────

P1: G1, G2                P2: G3, G4
┌─────────────────┐      ┌─────────────────┐
│ G1 (выполняется)│      │ G3 (выполняется)│
│ G2 (в очереди)  │      │ G4 (в очереди)  │
└─────────────────┘      └─────────────────┘

✅ Равномерная загрузка всех процессоров
✅ Максимальная производительность
```

---

## 3.2 📡 Каналы

### Концепция каналов

Каналы - это **трубы для передачи данных** между горутинами. Они обеспечивают синхронизацию и коммуникацию.

```
Канал как труба:
═══════════════════════════════════════

Горутина 1          Канал           Горутина 2
┌─────────┐    ┌─────────────┐    ┌─────────┐
│Отправка │───→│ [1][2][3][] │───→│Получение│
│ данных  │    │             │    │ данных  │
└─────────┘    └─────────────┘    └─────────┘

ch <- value    // отправка в канал
value := <-ch  // получение из канала
```

### Типы каналов

```
1. НЕБУФЕРИЗОВАННЫЕ каналы (синхронные)
═══════════════════════════════════════════

ch := make(chan int)

Горутина 1              Горутина 2
┌─────────┐            ┌─────────┐
│ch <- 42 │ ─ ждет ──→ │v := <-ch│
│ блок!   │            │         │
└─────────┘            └─────────┘

⚠️  Отправка блокирует до получения
⚠️  Получение блокирует до отправки
✅  Гарантированная синхронизация

────────────────────────────────────────────

2. БУФЕРИЗОВАННЫЕ каналы (асинхронные)
═══════════════════════════════════════════

ch := make(chan int, 3)  // буфер на 3 элемента

    Отправляем           Канал           Получаем
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ ch <- 1     │───→│ [1][ ][ ]   │    │             │
│ ch <- 2     │───→│ [1][2][ ]   │    │             │
│ ch <- 3     │───→│ [1][2][3]   │    │             │
│ ch <- 4     │ X  │ ПОЛНЫЙ!     │    │ v := <-ch   │←───[1]
│ блокировка! │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘

✅ Отправка НЕ блокирует пока есть место
✅ Получение НЕ блокирует пока есть данные
⚠️ Блокировка только при переполнении/опустошении
```

### Направленные каналы

Каналы могут быть ограничены направлением передачи:

```
Типы каналов по направлению:
═══════════════════════════════════════

chan int        // двунаправленный (чтение и запись)
chan<- int      // только запись (send-only)
<-chan int      // только чтение (receive-only)

Применение:
──────────

func sender(ch chan<- int) {    // может только отправлять
    ch <- 42
    // value := <-ch  // ОШИБКА компиляции!
}

func receiver(ch <-chan int) {  // может только получать
    value := <-ch
    // ch <- 42       // ОШИБКА компиляции!
}

func main() {
    ch := make(chan int)        // двунаправленный
    go sender(ch)              // автоматическое преобразование
    go receiver(ch)            // автоматическое преобразование
}

┌─────────────────────────────────────────────────────┐
│ Направленные каналы помогают предотвратить ошибки   │
│ на этапе компиляции                                 │
└─────────────────────────────────────────────────────┘
```

### Закрытие каналов

```
Жизненный цикл канала:
═════════════════════════════════════════

1. Создание:    ch := make(chan int)
2. Использование: ch <- value, value := <-ch  
3. Закрытие:    close(ch)
4. После закрытия: отправка запрещена, получение возможно

close(ch)  // закрыть канал

// Проверка закрытия
value, ok := <-ch
if !ok {
    // канал закрыт и пуст
}

// Или через range
for value := range ch {
    // автоматически останавливается при закрытии
}

Визуализация закрытого канала:
─────────────────────────────

Открытый канал:          Закрытый канал:
┌─────────────┐         ┌─────────────┐
│ [1][2][3][] │  ───→   │ [1][2][3][X]│
└─────────────┘         └─────────────┘
   ↑                       ↑
отправка OK             отправка ПАНИКА!
получение OK            получение данных + zero value
```

### Range по каналам

```
Элегантный способ обработки всех данных из канала:

// Отправка данных
go func() {
    for i := 1; i <= 5; i++ {
        ch <- i
    }
    close(ch)  // ВАЖНО: закрыть канал
}()

// Получение данных
for value := range ch {
    fmt.Println(value)  // 1, 2, 3, 4, 5
}
// цикл автоматически завершается при закрытии канала

Что происходит внутри:
─────────────────────

for value := range ch {     ≡     for {
    // обработка                      value, ok := <-ch
}                                     if !ok {
                                          break
                                      }
                                      // обработка value
                                  }
```

---

## 3.3 🔀 Select и мультиплексирование

### Оператор Select

Select позволяет **ждать операции с несколькими каналами одновременно**:

```
Синтаксис select:
═══════════════════════════════════════

select {
case value := <-ch1:
    // получили из ch1
case ch2 <- data:
    // отправили в ch2  
case <-timeout:
    // таймаут
default:
    // если никто не готов
}

Визуализация:
────────────

      ch1 ──┐
      ch2 ──┤ SELECT ──→ выполнится первый готовый case
   timeout ──┤
   default ──┘
```

### Неблокирующие операции

```
Блокирующая операция:              Неблокирующая операция:
────────────────────              ─────────────────────────

value := <-ch                     select {
// ждет данных                    case value := <-ch:
                                      // получили данные
                                  default:
                                      // канал пуст, продолжаем
                                  }

ch <- value                       select {
// ждет свободного места          case ch <- value:
                                      // отправили данные
                                  default:
                                      // канал полон, продолжаем
                                  }
```

### Таймауты

```
Реализация таймаутов с помощью select:
═════════════════════════════════════════

import "time"

select {
case result := <-slowOperation():
    // операция завершилась вовремя
case <-time.After(5 * time.Second):
    // операция заняла больше 5 секунд
    fmt.Println("Таймаут!")
}

Визуализация таймаута:
─────────────────────

t=0s    slowOperation() ────────────────────?
t=0s    time.After(5s) ──────┬── timeout
                             │
t=5s ────────────────────────┘
        ↑
    SELECT выберет timeout, если операция не завершена
```

### Тикеры (Tickers)

```
Тикеры для периодических операций:
═════════════════════════════════════════

ticker := time.NewTicker(1 * time.Second)
defer ticker.Stop()

for {
    select {
    case <-ticker.C:
        fmt.Println("Тик каждую секунду")
    case <-done:
        return  // выход из цикла
    }
}

Временная диаграмма тикера:
──────────────────────────

t=0s ────┬────┬────┬────┬────┬────→
         │    │    │    │    │
       tick  tick tick tick tick
         │    │    │    │    │
      action action action action action
```

### Паттерн Fan-in

Объединение нескольких каналов в один:

```
Fan-in паттерн:
═══════════════════════════════════════

    input1 ──┐
             ├─→ fanIn() ──→ output
    input2 ──┘

func fanIn(input1, input2 <-chan string) <-chan string {
    output := make(chan string)
    
    go func() {
        for {
            select {
            case msg := <-input1:
                output <- msg
            case msg := <-input2:
                output <- msg
            }
        }
    }()
    
    return output
}

Применение:
──────────

ch1 := make(chan string)  // источник 1
ch2 := make(chan string)  // источник 2
merged := fanIn(ch1, ch2) // объединенный канал

// Теперь можем читать из одного канала
for msg := range merged {
    fmt.Println(msg)  // сообщения из обоих источников
}
```

### Паттерн Fan-out

Распределение данных по нескольким обработчикам:

```
Fan-out паттерн:
═══════════════════════════════════════

                    ┌─→ worker1
    input ──→ split ┼─→ worker2  
                    └─→ worker3

func fanOut(input <-chan int, workers int) []<-chan int {
    outputs := make([]<-chan int, workers)
    
    for i := 0; i < workers; i++ {
        output := make(chan int)
        outputs[i] = output
        
        go func(out chan<- int) {
            for data := range input {
                out <- process(data)  // обработка данных
            }
            close(out)
        }(output)
    }
    
    return outputs
}

Польза Fan-out:
──────────────

✅ Параллельная обработка данных
✅ Масштабирование под нагрузку  
✅ Эффективное использование CPU
```

---

## 3.4 🔒 Синхронизация

### Пакет sync

Иногда каналы избыточны - нужны простые примитивы синхронизации:

```
Когда использовать каналы vs sync:
═══════════════════════════════════════════

КАНАЛЫ хороши для:                SYNC хорош для:
─────────────────                ──────────────

✅ Передачи данных                ✅ Простой синхронизации  
✅ Координации горутин            ✅ Защиты разделяемого состояния
✅ Сигнализации                   ✅ Счетчиков, флагов
✅ Пайплайнов обработки           ✅ Кэшей, пулов соединений

Пример выбора:
─────────────

Плохо:                           Хорошо:
var counter int                  var counter int
counterChan := make(chan int)    var mu sync.Mutex

go func() {                      func increment() {
    for {                            mu.Lock()
        select {                     counter++
        case <-increment:            mu.Unlock()
            counter++             }
        }
    }
}()
```

### Mutex - взаимное исключение

```
Mutex (Mutual Exclusion):
═══════════════════════════════════════

var mu sync.Mutex
var counter int

func increment() {
    mu.Lock()      // захватить блокировку
    counter++      // критическая секция
    mu.Unlock()    // освободить блокировку
}

Визуализация работы Mutex:
─────────────────────────

Горутина 1:           Горутина 2:           Горутина 3:
mu.Lock() ✅         mu.Lock() ⏳ ждет     mu.Lock() ⏳ ждет
counter++ ✅         blocked               blocked  
mu.Unlock() ✅       ↓                     ↓
                     mu.Lock() ✅          blocked
                     counter++ ✅          ↓
                     mu.Unlock() ✅        mu.Lock() ✅
                                           counter++ ✅
                                           mu.Unlock() ✅

Результат: безопасное изменение counter без гонки данных
```

### RWMutex - читатели-писатели

```
RWMutex позволяет множественное чтение:
═════════════════════════════════════════════

var rwmu sync.RWMutex
var data map[string]string

func read(key string) string {
    rwmu.RLock()         // блокировка для чтения
    value := data[key]   // множественные читатели OK
    rwmu.RUnlock()
    return value
}

func write(key, value string) {
    rwmu.Lock()          // эксклюзивная блокировка
    data[key] = value    // только один писатель
    rwmu.Unlock()
}

Схема блокировок:
────────────────

Операция    Читатели    Писатели    Разрешено?
────────    ────────    ────────    ─────────
Чтение      Есть        Нет         ✅ ДА
Чтение      Есть        Есть        ❌ НЕТ  
Запись      Нет         Нет         ✅ ДА
Запись      Есть        Нет         ❌ НЕТ
Запись      Нет         Есть        ❌ НЕТ

┌─────────────────────────────────────────────────────┐
│ RWMutex оптимален когда чтения гораздо чаще записей │
└─────────────────────────────────────────────────────┘
```

### WaitGroup - ожидание группы горутин

```
WaitGroup для синхронизации завершения:
═════════════════════════════════════════════

var wg sync.WaitGroup

func worker(id int) {
    defer wg.Done()        // уменьшить счетчик при выходе
    // выполнить работу
    fmt.Printf("Worker %d finished\n", id)
}

func main() {
    for i := 1; i <= 3; i++ {
        wg.Add(1)          // увеличить счетчик
        go worker(i)
    }
    wg.Wait()              // ждать пока счетчик не станет 0
    fmt.Println("All done!")
}

Диаграмма WaitGroup:
───────────────────

main()                    WaitGroup счетчик
  │                       ─────────────────
  ├─ wg.Add(1) ──────────→ 0 → 1
  ├─ go worker(1)
  ├─ wg.Add(1) ──────────→ 1 → 2  
  ├─ go worker(2)
  ├─ wg.Add(1) ──────────→ 2 → 3
  ├─ go worker(3)
  ├─ wg.Wait() ⏳ ждет
  │                       worker(1): wg.Done() → 3 → 2
  │                       worker(2): wg.Done() → 2 → 1  
  │                       worker(3): wg.Done() → 1 → 0
  └─ продолжение ✅        счетчик = 0, main() продолжается
```

### Once - однократное выполнение

```
sync.Once гарантирует выполнение функции только один раз:
════════════════════════════════════════════════════════

var once sync.Once
var instance *Database

func GetDatabase() *Database {
    once.Do(func() {
        instance = &Database{} // выполнится только один раз
        instance.Connect()
    })
    return instance
}

Применение (Singleton паттерн):
─────────────────────────────

go GetDatabase()  // первый вызов - создает instance
go GetDatabase()  // второй вызов - возвращает существующий
go GetDatabase()  // третий вызов - возвращает существующий

Внутренняя схема:
────────────────

Вызов 1:  once.Do() → выполняет функцию → устанавливает флаг
Вызов 2:  once.Do() → видит флаг → НЕ выполняет функцию  
Вызов 3:  once.Do() → видит флаг → НЕ выполняет функцию

✅ Потокобезопасно
✅ Без гонки данных
✅ Ленивая инициализация
```

### Atomic операции

```
Атомарные операции для простых типов:
══════════════════════════════════════════

import "sync/atomic"

var counter int64

func increment() {
    atomic.AddInt64(&counter, 1)    // атомарное добавление
}

func load() int64 {
    return atomic.LoadInt64(&counter)  // атомарное чтение
}

func store(value int64) {
    atomic.StoreInt64(&counter, value)  // атомарная запись
}

Сравнение подходов:
──────────────────

Mutex подход:                    Atomic подход:
─────────────                   ──────────────

var mu sync.Mutex               var counter int64
var counter int64

func increment() {              func increment() {
    mu.Lock()                       atomic.AddInt64(&counter, 1)
    counter++                   }
    mu.Unlock()
}                               ✅ Быстрее
                                ✅ Проще
✅ Универсально                 ❌ Только для простых типов
❌ Медленнее для простых операций
```

---

## 3.5 🏭 Паттерны конкурентности

### Worker Pool

Ограниченное количество воркеров для обработки задач:

```
Worker Pool архитектура:
═══════════════════════════════════════════════

    Задачи          Канал задач        Воркеры
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Task 1    │───→│             │───→│  Worker 1   │
│   Task 2    │───→│ [T][T][T][] │───→│  Worker 2   │
│   Task 3    │───→│             │───→│  Worker 3   │
│   Task N    │───→│             │    └─────────────┘
└─────────────┘    └─────────────┘           │
                                             ▼
                                    ┌─────────────┐
                                    │  Результаты │
                                    └─────────────┘

Преимущества Worker Pool:
────────────────────────

✅ Контроль количества горутин
✅ Эффективное использование ресурсов  
✅ Защита от перегрузки системы
✅ Простое масштабирование

type Job struct {
    ID   int
    Data string
}

func workerPool(jobs <-chan Job, results chan<- string, workerCount int) {
    var wg sync.WaitGroup
    
    // Создаем воркеры
    for i := 0; i < workerCount; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for job := range jobs {
                result := processJob(job)  // обработка задачи
                results <- result
            }
        }(i)
    }
    
    go func() {
        wg.Wait()      // ждем завершения всех воркеров
        close(results) // закрываем канал результатов
    }()
}
```

### Pipeline Pattern

Последовательная обработка данных через стадии:

```
Pipeline - конвейер обработки:
═══════════════════════════════════════════════

Input → Stage1 → Stage2 → Stage3 → Output

┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Числа   │───→│Фильтр   │───→│ Квадрат │───→│Формат   │
│1,2,3,4,5│    │четные   │    │ числа   │    │строки   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
  [1,2,3,4,5]   [2,4]         [4,16]       ["4","16"]

Реализация:
──────────

func pipeline() {
    // Стадия 1: генерация чисел
    numbers := generate(1, 2, 3, 4, 5)
    
    // Стадия 2: фильтр четных  
    evens := filter(numbers)
    
    // Стадия 3: возведение в квадрат
    squares := square(evens)
    
    // Стадия 4: форматирование
    strings := format(squares)
    
    // Получение результатов
    for result := range strings {
        fmt.Println(result)
    }
}

func filter(input <-chan int) <-chan int {
    output := make(chan int)
    go func() {
        defer close(output)
        for num := range input {
            if num%2 == 0 {  // только четные
                output <- num
            }
        }
    }()
    return output
}

Преимущества Pipeline:
─────────────────────

✅ Модульность - каждая стадия независима
✅ Параллелизм - стадии работают одновременно
✅ Переиспользование - стадии можно комбинировать
✅ Тестируемость - легко тестировать отдельные стадии
```

### Producer-Consumer

Классический паттерн асинхронной обработки:

```
Producer-Consumer модель:
═══════════════════════════════════════════════

Producer                Buffer               Consumer
┌─────────┐         ┌─────────────┐         ┌─────────┐
│Создает  │────────→│ [][][][][] │────────→│Обрабатывает│
│данные   │         │   Канал    │         │  данные │
└─────────┘         └─────────────┘         └─────────┘

Множественные производители и потребители:
─────────────────────────────────────────

Producer1 ──┐                              ┌── Consumer1
            ├─→ Буферизованный канал ──┤
Producer2 ──┘                              └── Consumer2

func producer(ch chan<- string, id int) {
    for i := 0; i < 5; i++ {
        data := fmt.Sprintf("Producer %d: item %d", id, i)
        ch <- data
        time.Sleep(time.Millisecond * 100)  // имитация работы
    }
}

func consumer(ch <-chan string, id int) {
    for data := range ch {
        fmt.Printf("Consumer %d received: %s\n", id, data)
        time.Sleep(time.Millisecond * 200)  // имитация обработки
    }
}

func main() {
    ch := make(chan string, 10)  // буферизованный канал
    
    // Запускаем производителей
    go producer(ch, 1)
    go producer(ch, 2)
    
    // Запускаем потребителей  
    go consumer(ch, 1)
    go consumer(ch, 2)
    
    time.Sleep(2 * time.Second)
    close(ch)
}

Применения:
──────────

🌐 Web сервер: запросы → обработка
📁 Загрузчик: URLs → скачивание файлов
📊 Аналитика: события → агрегация данных
📧 Email: сообщения → отправка
```

### Rate Limiting

Ограничение скорости обработки:

```
Rate Limiter с токенами:
═══════════════════════════════════════════════

    Токены (разрешения)
┌─────────────────────────┐
│ [T][T][T][ ][ ][ ][ ]   │ ← Bucket (ведро токенов)  
└─────────────────────────┘
           ▲                   
           │ добавляется каждые 100ms
           │
    ┌─────────────┐
    │ Время: tick │
    └─────────────┘

Запрос ──→ Есть токен? ──┬── ДА ──→ Обработать
                         │
                         └── НЕТ ──→ Отклонить/Ждать

func rateLimiter(rate time.Duration, burst int) <-chan time.Time {
    ticker := time.NewTicker(rate)
    tokens := make(chan time.Time, burst)
    
    // Заполняем начальные токены
    for i := 0; i < burst; i++ {
        select {
        case tokens <- time.Now():
        default:
        }
    }
    
    // Добавляем токены с заданной скоростью
    go func() {
        for tick := range ticker.C {
            select {
            case tokens <- tick:
            default:  // ведро полное, пропускаем токен
            }
        }
    }()
    
    return tokens
}

Использование:
─────────────

limiter := rateLimiter(100*time.Millisecond, 5)  // 10 req/sec, burst 5

for request := range requests {
    <-limiter  // ждем токен
    go handleRequest(request)  // обрабатываем запрос
}

Типы Rate Limiting:
──────────────────

1. Token Bucket - токены пополняются с постоянной скоростью
2. Leaky Bucket - запросы обрабатываются с постоянной скоростью  
3. Fixed Window - N запросов в фиксированный период
4. Sliding Window - N запросов в скользящий период
```

### Circuit Breaker

Защита от каскадных отказов:

```
Circuit Breaker - автоматический выключатель:
═══════════════════════════════════════════════════

Состояния Circuit Breaker:
─────────────────────────

    CLOSED                 OPEN                 HALF-OPEN
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│ Запросы     │  ────→│ Запросы     │  ────→│ Ограниченные│
│ проходят    │   │   │ отклоняются │   │   │ запросы     │
│             │   │   │             │   │   │             │
│ ✅ Норма    │   │   │ ❌ Сбой      │   │   │ 🔍 Проверка │
└─────────────┘   │   └─────────────┘   │   └─────────────┘
       ▲          │          │          │          │
       │          │          │          │          │
       │    много ошибок    таймаут   успех       ошибка
       │          │          │          │          │
       └──────────┘          ▼          └──────────┘

Временная диаграмма:
───────────────────

t=0    [CLOSED] ────── запросы OK ──────
t=30   [CLOSED] ────── начались ошибки ──  
t=35   [OPEN] ──────── все запросы отклоняются ──
t=95   [HALF-OPEN] ─── пробуем один запрос ──
t=96   [CLOSED] ────── если OK, то открываемся ──

type CircuitBreaker struct {
    maxFailures  int
    resetTimeout time.Duration
    failures     int
    lastFailTime time.Time
    state        State  // CLOSED, OPEN, HALF_OPEN
    mutex        sync.Mutex
}

func (cb *CircuitBreaker) Call(operation func() error) error {
    cb.mutex.Lock()
    defer cb.mutex.Unlock()
    
    switch cb.state {
    case OPEN:
        if time.Since(cb.lastFailTime) > cb.resetTimeout {
            cb.state = HALF_OPEN
            cb.failures = 0
        } else {
            return ErrCircuitBreakerOpen
        }
        
    case HALF_OPEN:
        // Пропускаем ограниченное количество запросов
    }
    
    err := operation()
    
    if err != nil {
        cb.failures++
        cb.lastFailTime = time.Now()
        if cb.failures >= cb.maxFailures {
            cb.state = OPEN
        }
        return err
    }
    
    cb.failures = 0
    cb.state = CLOSED
    return nil
}

Применение:
──────────

cb := NewCircuitBreaker(5, 30*time.Second)  // 5 ошибок, 30сек таймаут

err := cb.Call(func() error {
    return callExternalService()  // может падать
})

if err != nil {
    if err == ErrCircuitBreakerOpen {
        return getCachedResult()  // возвращаем кэш
    }
    return err
}
```

### Обработка ошибок в горутинах

```
Проблема: горутины "глотают" ошибки
═══════════════════════════════════════════════

❌ Плохо:
go func() {
    result, err := doSomething()
    if err != nil {
        // ошибка потеряна!
        return
    }
    // ...
}()

✅ Хорошо - возвращаем ошибки через каналы:

type Result struct {
    Data  string
    Error error
}

func worker(tasks <-chan Task, results chan<- Result) {
    for task := range tasks {
        data, err := process(task)
        results <- Result{Data: data, Error: err}
    }
}

func main() {
    tasks := make(chan Task)
    results := make(chan Result)
    
    go worker(tasks, results)
    
    // Отправляем задачи
    tasks <- Task{ID: 1}
    close(tasks)
    
    // Получаем результаты и обрабатываем ошибки
    for result := range results {
        if result.Error != nil {
            log.Printf("Ошибка: %v", result.Error)
            continue
        }
        fmt.Printf("Результат: %s", result.Data)
    }
}

Паттерн errgroup:
────────────────

import "golang.org/x/sync/errgroup"

func processFiles(files []string) error {
    g := new(errgroup.Group)
    
    for _, file := range files {
        file := file  // capture loop variable
        g.Go(func() error {
            return processFile(file)  // любая ошибка отменит все
        })
    }
    
    return g.Wait()  // ждем все горутины, возвращаем первую ошибку
}

Преимущества errgroup:
─────────────────────

✅ Автоматическая отмена при первой ошибке
✅ Простая обработка ошибок от множества горутин  
✅ Ограничение количества горутин
✅ Контекст для отмены
```

---

## 3.6 🎛️ Контекст (Context)

### Концепция контекста

Context - это способ **передачи метаданных** через границы API и горутин:

```
Контекст как "рюкзак" для горутин:
═══════════════════════════════════════════════

┌─────────────────────────────────────┐
│              Context                │
│  ┌─────────────────────────────────┐│
│  │ 🕐 Deadline: 2024-01-01 15:00   ││  
│  │ ❌ Cancellation: cancel()       ││
│  │ 📦 Values: userID=123           ││
│  │ 🔗 Parent: parent context       ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
                    │
                    ▼
        Передается во все горутины
        
main() ──→ handler() ──→ service() ──→ database()
  │           │             │            │
context.Background() ──→ ctx ──→ ctx ──→ ctx
```

### Создание контекстов

```
Иерархия контекстов:
═══════════════════════════════════════════════

// Корневой контекст (никогда не отменяется)
ctx := context.Background()

// Контекст с отменой
ctx, cancel := context.WithCancel(ctx)
defer cancel()  // важно вызвать для освобождения ресурсов

// Контекст с таймаутом  
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

// Контекст с дедлайном
deadline := time.Now().Add(10 * time.Second)
ctx, cancel := context.WithDeadline(ctx, deadline)
defer cancel()

// Контекст со значениями
ctx = context.WithValue(ctx, "userID", 123)

Дерево контекстов:
─────────────────

context.Background()
├── WithTimeout(5s)
│   ├── WithValue("userID", 123)
│   │   └── WithCancel()
│   └── WithValue("requestID", "abc")
└── WithCancel()
    └── WithTimeout(10s)

При отмене родителя отменяются все потомки!
```

### Отмена операций

```
Graceful cancellation:
═════════════════════════════════════════════

func longRunningOperation(ctx context.Context) error {
    for i := 0; i < 1000; i++ {
        // Проверяем отмену
        select {
        case <-ctx.Done():
            return ctx.Err()  // context.Canceled или context.DeadlineExceeded
        default:
        }
        
        // Выполняем работу
        if err := doWork(i); err != nil {
            return err
        }
        
        time.Sleep(10 * time.Millisecond)
    }
    return nil
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()
    
    err := longRunningOperation(ctx)
    if err != nil {
        if err == context.DeadlineExceeded {
            fmt.Println("Операция превысила лимит времени")
        } else if err == context.Canceled {
            fmt.Println("Операция была отменена")
        }
    }
}

Схема отмены:
────────────

t=0s    start operation ────────────┐
t=1s    работаем... ────────────────┤
t=2s    TIMEOUT! ───────────────────┤ ← ctx.Done() закрывается
t=2s    select получает сигнал ─────┤
t=2s    return ctx.Err() ───────────┘
```

### Передача значений

```
Context Values - передача метаданных:
═══════════════════════════════════════════════

// Определяем типы ключей (избегаем коллизий)
type key string

const (
    userIDKey     key = "userID"
    requestIDKey  key = "requestID"
    traceIDKey    key = "traceID"
)

func handleRequest(w http.ResponseWriter, r *http.Request) {
    // Извлекаем данные из запроса
    userID := getUserIDFromToken(r.Header.Get("Authorization"))
    requestID := generateRequestID()
    
    // Создаем контекст с метаданными
    ctx := context.WithValue(r.Context(), userIDKey, userID)
    ctx = context.WithValue(ctx, requestIDKey, requestID)
    
    // Передаем контекст дальше
    user, err := getUserService(ctx, userID)
    if err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    
    json.NewEncoder(w).Encode(user)
}

func getUserService(ctx context.Context, id int) (*User, error) {
    // Извлекаем метаданные
    requestID := ctx.Value(requestIDKey).(string)
    logger := log.WithField("requestID", requestID)
    
    logger.Info("Fetching user from database")
    
    // Передаем контекст в слой базы данных
    return db.GetUser(ctx, id)
}

func (db *Database) GetUser(ctx context.Context, id int) (*User, error) {
    // Проверяем отмену перед долгой операцией
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }
    
    // SQL запрос с контекстом (автоматическая отмена)
    row := db.QueryRowContext(ctx, "SELECT * FROM users WHERE id = ?", id)
    
    var user User
    err := row.Scan(&user.ID, &user.Name, &user.Email)
    return &user, err
}

Лучшие практики Context Values:
──────────────────────────────

✅ Используйте для метаданных запроса (userID, traceID)
✅ НЕ используйте для обязательных параметров функции
✅ Определяйте типизированные ключи
✅ Документируйте какие значения ожидаются

❌ НЕ передавайте nil context - используйте context.TODO()
❌ НЕ храните контекст в структурах
❌ НЕ используйте для передачи опциональных параметров
```

### Контекст в HTTP

```
HTTP сервер с контекстом:
═══════════════════════════════════════════════

func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Создаем контекст с таймаутом для каждого запроса
        ctx, cancel := context.WithTimeout(r.Context(), 30*time.Second)
        defer cancel()
        
        // Добавляем метаданные
        requestID := generateRequestID()
        ctx = context.WithValue(ctx, "requestID", requestID)
        
        // Передаем модифицированный контекст дальше
        r = r.WithContext(ctx)
        next.ServeHTTP(w, r)
    })
}

func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    
    // Делаем HTTP запрос к внешнему API
    client := &http.Client{}
    req, _ := http.NewRequestWithContext(ctx, "GET", "https://api.example.com/data", nil)
    
    resp, err := client.Do(req)
    if err != nil {
        if err == context.DeadlineExceeded {
            http.Error(w, "Таймаут внешнего API", 504)
            return
        }
        http.Error(w, err.Error(), 500)
        return
    }
    defer resp.Body.Close()
    
    // Обрабатываем ответ...
}

Цепочка обработки HTTP запроса:
──────────────────────────────

Browser ──→ Server ──→ Middleware ──→ Handler ──→ Service ──→ Database
            │            │             │           │           │
       HTTP Context ──→ +timeout ──→ +metadata ──→ pass ──→ QueryContext

Преимущества:
────────────

✅ Автоматическая отмена при разрыве соединения
✅ Контроль времени выполнения запросов
✅ Трассировка запросов через микросервисы
✅ Graceful shutdown при перезапуске сервера
```

---

## 🏆 Итоговые знания блока 3

После изучения этого блока вы будете знать:

### 📚 Концептуальные знания
- **Философию конкурентности Go**: "Don't communicate by sharing memory; share memory by communicating"
- **Горутины**: легковесные потоки и планировщик Go
- **Каналы**: синхронизация и коммуникация между горутинами
- **Select**: мультиплексирование операций с каналами
- **Sync пакет**: примитивы синхронизации для защиты данных
- **Context**: управление жизненным циклом и отмена операций

### 🛠️ Практические навыки
- Написание высокопроизводительных concurrent приложений
- Эффективное использование горутин и каналов
- Понимание проблем конкурентности (race conditions, deadlocks)
- Применение паттернов конкурентного программирования
- Управление жизненным циклом горутин

### 🎯 Паттерны и техники
- **Worker Pools** - контролируемое количество обработчиков
- **Pipeline** - конвейерная обработка данных
- **Fan-in/Fan-out** - агрегация и распределение данных
- **Rate Limiting** - контроль нагрузки
- **Circuit Breaker** - защита от каскадных отказов
- **Graceful Cancellation** - корректная отмена операций

---

## 🚨 Важные принципы

### Выбор между каналами и sync

```
КАНАЛЫ лучше для:                    SYNC лучше для:
───────────────────                 ──────────────────

✅ Передачи данных между горутинами   ✅ Защиты простого состояния
✅ Координации и сигнализации        ✅ Счетчиков и флагов  
✅ Построения пайплайнов             ✅ Кэшей и пулов
✅ Producer-Consumer паттернов       ✅ Коротких критических секций

"Начинайте с каналов, переходите к sync при необходимости"
```

### Предотвращение утечек горутин

```
❌ Утечка горутин:
go func() {
    for {
        // бесконечный цикл без выхода
        doWork()
    }
}()

✅ Правильно:
go func() {
    for {
        select {
        case <-ctx.Done():
            return  // выход при отмене
        default:
            doWork()
        }
    }
}()

✅ Еще лучше:
go func() {
    ticker := time.NewTicker(time.Second)
    defer ticker.Stop()
    
    for {
        select {
        case <-ticker.C:
            doWork()
        case <-ctx.Done():
            return
        }
    }
}()
```

---

## 📝 Что дальше?

Теперь вы готовы к изучению **Блока 4: Работа с данными и внешними системами** - где применим знания о конкурентности для создания высокопроизводительных веб-приложений и интеграций с базами данных! 🚀

*Помните: конкурентность - это суперсила Go. Используйте её мудро!* ⚡