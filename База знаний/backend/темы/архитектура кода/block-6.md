# Блок 6: Производительность и масштабируемость

**Длительность:** 5-6 недель  
**Цель:** Освоить принципы создания эффективных и масштабируемых систем

---

## 📊 Введение в производительность и масштабируемость

```
Производительность ≠ Масштабируемость

┌─────────────────┐    ┌─────────────────┐
│ Производительность │    │ Масштабируемость │
│                 │    │                 │
│ • Скорость      │    │ • Рост нагрузки │
│ • Отзывчивость  │    │ • Добавление    │
│ • Пропускная    │    │   ресурсов      │
│   способность   │    │ • Горизонтальное│
│                 │    │   расширение    │
└─────────────────┘    └─────────────────┘
```

**Ключевые метрики:**
- **Latency (задержка)** - время ответа на единичный запрос
- **Throughput (пропускная способность)** - количество запросов в единицу времени
- **Response Time** - время от запроса до получения ответа
- **Scalability** - способность справляться с увеличением нагрузки

---

## 🔍 Глава 1: Профилирование и оптимизация производительности

### 1.1 Методы измерения производительности

```
┌─── ИЗМЕРЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ───┐
│                                    │
│  📈 Синтетическое тестирование     │
│  ├── Load Testing                  │
│  ├── Stress Testing                │
│  └── Spike Testing                 │
│                                    │
│  📊 Профилирование в реальном времени │
│  ├── CPU Profiling                 │
│  ├── Memory Profiling              │
│  └── I/O Profiling                 │
│                                    │
│  🎯 Мониторинг в продакшене        │
│  ├── APM инструменты               │
│  ├── Метрики приложения            │
│  └── Пользовательский опыт         │
└────────────────────────────────────┘
```

#### Инструменты профилирования по языкам:

| Язык | CPU Profiler | Memory Profiler | Комплексные решения |
|------|-------------|----------------|-------------------|
| Java | JProfiler, YourKit | Eclipse MAT | JVisualVM, JConsole |
| C# | PerfView, dotTrace | JetBrains dotMemory | Application Insights |
| Python | cProfile, py-spy | memory_profiler | PyCharm Profiler |
| JavaScript | Chrome DevTools | Heap Snapshot | Node.js Inspector |
| Go | go tool pprof | Built-in profiler | Golang pprof |

### 1.2 Профилирование CPU

**Пример профилирования в Python:**

```python
import cProfile
import pstats
from functools import wraps

def profile_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Топ 10 функций
        
        return result
    return wrapper

@profile_performance
def cpu_intensive_task():
    # Ваш код здесь
    pass
```

**Анализ результатов профилирования:**

```
         ncalls  tottime  percall  cumtime  percall filename:lineno(function)
             1    0.000    0.000    2.500    2.500 <string>:1(<module>)
           100    0.005    0.000    2.500    0.025 algorithm.py:15(process_data)
         10000    1.200    0.000    2.495    0.000 utils.py:42(heavy_computation)
        100000    1.295    0.000    1.295    0.000 {built-in method builtins.sum}
```

**Что анализировать:**
- `tottime` - время выполнения без вложенных вызовов
- `cumtime` - общее время включая вложенные вызовы
- `ncalls` - количество вызовов функции

### 1.3 Профилирование памяти

**Архитектура управления памятью:**

```
┌─── HEAP MEMORY STRUCTURE ───┐
│                             │
│  ┌─────────────────────┐    │
│  │   Young Generation  │    │
│  │  ┌─────┬─────────┐  │    │
│  │  │Eden │Survivor │  │    │
│  │  │Space│  Space  │  │    │
│  │  └─────┴─────────┘  │    │
│  └─────────────────────┘    │
│                             │
│  ┌─────────────────────┐    │
│  │   Old Generation    │    │
│  │  (Tenured Space)    │    │
│  └─────────────────────┘    │
│                             │
│  ┌─────────────────────┐    │
│  │  Permanent/Metaspace │    │
│  │   (Class metadata)   │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

**Пример мониторинга памяти в Java:**

```java
public class MemoryMonitor {
    private static final MemoryMXBean memoryBean = 
        ManagementFactory.getMemoryMXBean();
    
    public static void printMemoryUsage() {
        MemoryUsage heapUsage = memoryBean.getHeapMemoryUsage();
        MemoryUsage nonHeapUsage = memoryBean.getNonHeapMemoryUsage();
        
        System.out.println("--- Memory Usage ---");
        System.out.printf("Heap: %d MB used / %d MB max%n", 
            heapUsage.getUsed() / 1024 / 1024,
            heapUsage.getMax() / 1024 / 1024);
        System.out.printf("Non-Heap: %d MB used%n", 
            nonHeapUsage.getUsed() / 1024 / 1024);
    }
    
    public static void forceGC() {
        System.gc();
        System.runFinalization();
    }
}
```

### 1.4 Оптимизация узких мест

**Стратегии оптимизации:**

```
┌─── OPTIMIZATION STRATEGIES ───┐
│                               │
│  🎯 Алгоритмическая           │
│  ├── Выбор лучших алгоритмов  │
│  ├── Структуры данных         │
│  └── Сложность O(n)           │
│                               │
│  ⚡ Микрооптимизации          │
│  ├── Избегание создания       │
│  │   объектов                │
│  ├── Пулы объектов            │
│  └── Примитивные типы         │
│                               │
│  🏗️ Архитектурная             │
│  ├── Кэширование              │
│  ├── Асинхронность            │
│  └── Распараллеливание        │
└───────────────────────────────┘
```

**Пример оптимизации алгоритма:**

```python
# ❌ Неэффективно - O(n²)
def find_duplicates_slow(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

# ✅ Эффективно - O(n)
def find_duplicates_fast(items):
    seen = set()
    duplicates = set()
    
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return list(duplicates)
```

---

## 💾 Глава 2: Стратегии кэширования

### 2.1 Уровни кэширования

```
┌─── CACHING LAYERS ───┐
│                      │
│  🌐 Browser Cache    │
│  │                  │
│  ↓                  │
│  🔄 CDN Cache        │
│  │                  │
│  ↓                  │
│  🚀 Reverse Proxy    │
│  │   (Nginx/Varnish)│
│  ↓                  │
│  💻 Application Cache│
│  │   (In-Memory)    │
│  ↓                  │
│  🗄️ Database Cache   │
│  │   (Query Cache)  │
│  ↓                  │
│  💿 Persistent Cache │
│     (Redis/Memcached)│
└──────────────────────┘
```

### 2.2 Cache Patterns (Паттерны кэширования)

#### Cache-Aside (Lazy Loading)

```
┌─── CACHE-ASIDE PATTERN ───┐
│                           │
│  Application              │
│       │                  │
│       ├─1. Check Cache   │
│       │                  │
│   ┌───▼───┐              │
│   │ Cache │              │
│   └───┬───┘              │
│       │                  │
│       ├─2. Cache Miss    │
│       │                  │
│       ├─3. Read from DB  │
│       │                  │
│   ┌───▼───┐              │
│   │  DB   │              │
│   └───┬───┘              │
│       │                  │
│       └─4. Store in Cache│
└───────────────────────────┘
```

**Реализация Cache-Aside:**

```python
import redis
import json
from typing import Optional

class CacheAside:
    def __init__(self, redis_client):
        self.cache = redis_client
        self.ttl = 3600  # 1 час
    
    def get_user(self, user_id: int) -> Optional[dict]:
        # 1. Проверяем кэш
        cache_key = f"user:{user_id}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data:
            # Cache Hit
            return json.loads(cached_data)
        
        # 2. Cache Miss - идем в БД
        user = self.fetch_user_from_db(user_id)
        
        if user:
            # 3. Сохраняем в кэш
            self.cache.setex(
                cache_key, 
                self.ttl, 
                json.dumps(user)
            )
        
        return user
    
    def update_user(self, user_id: int, user_data: dict):
        # Обновляем БД
        self.update_user_in_db(user_id, user_data)
        
        # Инвалидируем кэш
        cache_key = f"user:{user_id}"
        self.cache.delete(cache_key)
```

#### Write-Through Pattern

```
┌─── WRITE-THROUGH PATTERN ───┐
│                             │
│  Application                │
│       │                    │
│       ├─1. Write to Cache  │
│       │                    │
│   ┌───▼───┐                │
│   │ Cache │                │
│   └───┬───┘                │
│       │                    │
│       ├─2. Write to DB     │
│       │    (Synchronous)   │
│   ┌───▼───┐                │
│   │  DB   │                │
│   └───────┘                │
│                             │
│  + Consistency              │
│  - Higher latency           │
└─────────────────────────────┘
```

#### Write-Behind (Write-Back) Pattern

```
┌─── WRITE-BEHIND PATTERN ───┐
│                            │
│  Application               │
│       │                   │
│       ├─1. Write to Cache │
│       │    (Fast response)│
│   ┌───▼───┐               │
│   │ Cache │               │
│   └───┬───┘               │
│       │                   │
│       ├─2. Async write    │
│       │    to DB later    │
│   ┌───▼───┐               │
│   │  DB   │               │
│   └───────┘               │
│                           │
│  + Low latency            │
│  - Risk of data loss      │
└───────────────────────────┘
```

### 2.3 Распределенное кэширование

**Архитектура распределенного кэша:**

```
┌─── DISTRIBUTED CACHE TOPOLOGY ───┐
│                                  │
│     App1    App2    App3         │
│       │       │       │          │
│       └───────┼───────┘          │
│               │                  │
│        ┌──────▼──────┐           │
│        │ Load Balancer│           │
│        └──────┬──────┘           │
│               │                  │
│     ┌─────────┼─────────┐        │
│     │         │         │        │
│ ┌───▼───┐ ┌───▼───┐ ┌───▼───┐    │
│ │Redis-1│ │Redis-2│ │Redis-3│    │
│ │Master │ │Master │ │Master │    │
│ └───┬───┘ └───┬───┘ └───┬───┘    │
│     │         │         │        │
│ ┌───▼───┐ ┌───▼───┐ ┌───▼───┐    │
│ │Redis-1│ │Redis-2│ │Redis-3│    │
│ │Replica│ │Replica│ │Replica│    │
│ └───────┘ └───────┘ └───────┘    │
└──────────────────────────────────┘
```

**Стратегии распределения данных:**

```
┌─── DATA DISTRIBUTION STRATEGIES ───┐
│                                    │
│  🔄 Consistent Hashing             │
│  ├── Равномерное распределение     │
│  ├── Минимальное перемещение       │
│  └── Добавление/удаление узлов     │
│                                    │
│  📊 Hash Partitioning              │
│  ├── key % number_of_nodes         │
│  ├── Простота реализации           │
│  └── Проблемы при изменении узлов  │
│                                    │
│  🎯 Range Partitioning             │
│  ├── Разделение по диапазонам     │
│  ├── Хорошо для последовательных  │
│  └── Риск неравномерного распред.  │
└────────────────────────────────────┘
```

### 2.4 Инвалидация кэша

**Стратегии инвалидации:**

```python
class CacheInvalidation:
    def __init__(self, cache_client):
        self.cache = cache_client
    
    # 1. TTL-based (Time To Live)
    def set_with_ttl(self, key: str, value: str, ttl: int):
        """Автоматическое истечение через TTL"""
        self.cache.setex(key, ttl, value)
    
    # 2. Tag-based invalidation
    def set_with_tags(self, key: str, value: str, tags: list):
        """Инвалидация по тегам"""
        # Сохраняем основные данные
        self.cache.set(key, value)
        
        # Связываем с тегами
        for tag in tags:
            tag_key = f"tag:{tag}"
            self.cache.sadd(tag_key, key)
    
    def invalidate_by_tag(self, tag: str):
        """Инвалидируем все ключи с тегом"""
        tag_key = f"tag:{tag}"
        keys = self.cache.smembers(tag_key)
        
        if keys:
            # Удаляем данные
            self.cache.delete(*keys)
            # Удаляем тег
            self.cache.delete(tag_key)
    
    # 3. Event-driven invalidation
    def on_user_updated(self, user_id: int):
        """Обработчик события обновления пользователя"""
        patterns = [
            f"user:{user_id}",
            f"user:{user_id}:*",
            f"friends:{user_id}",
            f"timeline:{user_id}"
        ]
        
        for pattern in patterns:
            keys = self.cache.keys(pattern)
            if keys:
                self.cache.delete(*keys)
```

---

## ⚡ Глава 3: Асинхронное программирование

### 3.1 Модели конкурентности

```
┌─── CONCURRENCY MODELS ───┐
│                          │
│  🧵 Threading            │
│  ├── Preemptive         │
│  ├── Shared memory      │
│  └── Context switching  │
│                          │
│  🔄 Event Loop           │
│  ├── Single-threaded    │
│  ├── Non-blocking I/O   │
│  └── Callback queue     │
│                          │
│  🎭 Actor Model          │
│  ├── Message passing    │
│  ├── Isolated state     │
│  └── Fault tolerance    │
│                          │
│  ⚙️ Coroutines           │
│  ├── Cooperative        │
│  ├── Lightweight        │
│  └── No stack switching │
└──────────────────────────┘
```

### 3.2 Event Loop Architecture

```
┌─── EVENT LOOP CYCLE ───┐
│                        │
│  ┌─────────────────┐   │
│  │  Call Stack     │   │
│  │  ┌───────────┐  │   │
│  │  │ function()│  │   │
│  │  └───────────┘  │   │
│  └─────────────────┘   │
│           │             │
│  ┌─────────▼─────────┐ │
│  │   Event Loop      │ │
│  │                   │ │
│  │  1. Timer Phase   │ │
│  │  2. Pending I/O   │ │
│  │  3. Poll Phase    │ │
│  │  4. Check Phase   │ │
│  │  5. Close Phase   │ │
│  └─────────┬─────────┘ │
│           │             │
│  ┌─────────▼─────────┐ │
│  │  Callback Queue   │ │
│  │  ┌─────┬─────┬──┐ │ │
│  │  │cb1  │cb2  │..│ │ │
│  │  └─────┴─────┴──┘ │ │
│  └───────────────────┘ │
└────────────────────────┘
```

### 3.3 Async/Await Patterns

**Python asyncio пример:**

```python
import asyncio
import aiohttp
import time
from typing import List

class AsyncHttpClient:
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def fetch_url(self, url: str) -> dict:
        """Асинхронный HTTP запрос"""
        try:
            async with self.session.get(url) as response:
                return {
                    'url': url,
                    'status': response.status,
                    'data': await response.text()
                }
        except Exception as e:
            return {
                'url': url,
                'error': str(e)
            }
    
    async def fetch_multiple(self, urls: List[str]) -> List[dict]:
        """Параллельные запросы"""
        tasks = [self.fetch_url(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Использование
async def main():
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/3',
    ]
    
    async with AsyncHttpClient() as client:
        start_time = time.time()
        results = await client.fetch_multiple(urls)
        end_time = time.time()
        
        print(f"Выполнено за {end_time - start_time:.2f} секунд")
        # Результат: ~3 секунды вместо 6 (1+2+3)

# Запуск
asyncio.run(main())
```

### 3.4 Неблокирующий I/O

**Сравнение блокирующего и неблокирующего I/O:**

```
┌─── BLOCKING I/O ───┐     ┌─── NON-BLOCKING I/O ───┐
│                    │     │                        │
│  Thread 1          │     │  Event Loop            │
│  ├── Request A     │     │  ├── Start Request A   │
│  │   (wait...)    │     │  ├── Start Request B   │
│  │   (wait...)    │     │  ├── Start Request C   │
│  │   Response A   │     │  │                      │
│  │                │     │  ├── Response A ready  │
│  Thread 2          │     │  ├── Response C ready  │
│  ├── Request B     │     │  ├── Response B ready  │
│  │   (wait...)    │     │  │                      │
│  │   Response B   │     │  └── All completed     │
│  │                │     │                        │
│  Thread 3          │     │  Single Thread!       │
│  ├── Request C     │     │                        │
│  │   (wait...)    │     │                        │
│  │   Response C   │     │                        │
└────────────────────┘     └────────────────────────┘
```

### 3.5 Управление Concurrency

**Паттерны управления потоками:**

```python
import asyncio
from asyncio import Semaphore, Queue
from typing import Callable, Any

class ConcurrencyManager:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = Semaphore(max_concurrent)
        self.results_queue = Queue()
    
    async def limited_task(self, coro: Callable, *args, **kwargs):
        """Выполнение задачи с ограничением конкурентности"""
        async with self.semaphore:
            return await coro(*args, **kwargs)
    
    async def producer_consumer_pattern(self):
        """Паттерн Производитель-Потребитель"""
        
        async def producer(queue: Queue):
            """Производитель задач"""
            for i in range(100):
                await queue.put(f"task_{i}")
                await asyncio.sleep(0.1)
            
            # Сигнал завершения
            await queue.put(None)
        
        async def consumer(queue: Queue, consumer_id: int):
            """Потребитель задач"""
            while True:
                task = await queue.get()
                if task is None:
                    # Передаем сигнал другим потребителям
                    await queue.put(None)
                    break
                
                # Обрабатываем задачу
                print(f"Consumer {consumer_id} processing {task}")
                await asyncio.sleep(0.5)
                queue.task_done()
        
        # Очередь задач
        task_queue = Queue(maxsize=20)
        
        # Запускаем производителя и потребителей
        await asyncio.gather(
            producer(task_queue),
            *[consumer(task_queue, i) for i in range(3)]
        )

# Использование
async def example_usage():
    manager = ConcurrencyManager(max_concurrent=5)
    
    # Создаем множество задач
    async def heavy_task(task_id: int):
        print(f"Starting task {task_id}")
        await asyncio.sleep(1)
        return f"Result {task_id}"
    
    # Ограниченное выполнение
    tasks = [
        manager.limited_task(heavy_task, i) 
        for i in range(20)
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"Completed {len(results)} tasks")
```

---

## 📈 Глава 4: Масштабирование систем

### 4.1 Типы масштабирования

```
┌─── SCALING STRATEGIES ───┐
│                          │
│  ⬆️ Vertical Scaling     │
│  (Scale Up)              │
│  ┌─────────────────┐    │
│  │ Single Server   │    │
│  │                 │    │
│  │ CPU: 2→8 cores  │    │
│  │ RAM: 8→32 GB    │    │
│  │ SSD: 256→1TB    │    │
│  └─────────────────┘    │
│                          │
│  ➡️ Horizontal Scaling   │
│  (Scale Out)             │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐│
│  │S1 │ │S2 │ │S3 │ │S4 ││
│  └───┘ └───┘ └───┘ └───┘│
│    Load Balanced         │
└──────────────────────────┘
```

**Сравнение подходов:**

| Аспект | Vertical Scaling | Horizontal Scaling |
|--------|------------------|-------------------|
| **Сложность** | Низкая | Высокая |
| **Стоимость** | Высокая (экспоненциальный рост) | Линейная |
| **Отказоустойчивость** | Single Point of Failure | Распределенная |
| **Лимиты** | Физические ограничения | Теоретически безграничное |
| **Время простоя** | Требуется для апгрейда | Rolling updates |

### 4.2 Load Balancing стратегии

```
┌─── LOAD BALANCING ALGORITHMS ───┐
│                                 │
│  🔄 Round Robin                 │
│  Request 1 → Server 1           │
│  Request 2 → Server 2           │
│  Request 3 → Server 3           │
│  Request 4 → Server 1 (cycle)   │
│                                 │
│  ⚖️ Weighted Round Robin        │
│  S1 (weight=3): 60% requests    │
│  S2 (weight=2): 40% requests    │
│                                 │
│  📊 Least Connections           │
│  Route to server with fewest    │
│  active connections             │
│                                 │
│  🎯 IP Hash                     │
│  hash(client_ip) % server_count │
│  Sticky sessions                │
└─────────────────────────────────┘
```

**Архитектура Load Balancer:**

```
┌─── MULTI-LAYER LOAD BALANCING ───┐
│                                  │
│          🌐 Internet             │
│               │                  │
│    ┌──────────▼──────────┐       │
│    │   DNS Load Balancer │       │
│    │   (Geographic)      │       │
│    └──────────┬──────────┘       │
│               │                  │
│    ┌──────────▼──────────┐       │
│    │  L4 Load Balancer   │       │
│    │  (TCP/IP Layer)     │       │
│    └─────────┬─┬─────────┘       │
│              │ │                 │
│    ┌─────────▼─▼─────────┐       │
│    │  L7 Load Balancer   │       │
│    │  (Application Layer)│       │
│    └─┬─────────────────┬─┘       │
│      │                 │         │
│  ┌───▼───┐         ┌───▼───┐     │
│  │App    │   ...   │App    │     │
│  │Server │         │Server │     │
│  │  1    │         │  N    │     │
│  └───────┘         └───────┘     │
└──────────────────────────────────┘
```

**Реализация простого Load Balancer:**

```python
import asyncio
import random
from typing import List, Dict
from dataclasses import dataclass
from enum import Enum

class LBAlgorithm(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"

@dataclass
class Server:
    host: str
    port: int
    weight: int = 1
    active_connections: int = 0
    is_healthy: bool = True

class LoadBalancer:
    def __init__(self, algorithm: LBAlgorithm = LBAlgorithm.ROUND_ROBIN):
        self.servers: List[Server] = []
        self.algorithm = algorithm
        self.current_index = 0
        self.weighted_index = 0
    
    def add_server(self, server: Server):
        self.servers.append(server)
    
    def get_next_server(self) -> Server:
        healthy_servers = [s for s in self.servers if s.is_healthy]
        
        if not healthy_servers:
            raise Exception("No healthy servers available")
        
        if self.algorithm == LBAlgorithm.ROUND_ROBIN:
            return self._round_robin(healthy_servers)
        elif self.algorithm == LBAlgorithm.LEAST_CONNECTIONS:
            return self._least_connections(healthy_servers)
        elif self.algorithm == LBAlgorithm.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin(healthy_servers)
    
    def _round_robin(self, servers: List[Server]) -> Server:
        server = servers[self.current_index % len(servers)]
        self.current_index += 1
        return server
    
    def _least_connections(self, servers: List[Server]) -> Server:
        return min(servers, key=lambda s: s.active_connections)
    
    def _weighted_round_robin(self, servers: List[Server]) -> Server:
        # Простая реализация weighted round robin
        weighted_servers = []
        for server in servers:
            weighted_servers.extend([server] * server.weight)
        
        server = weighted_servers[self.weighted_index % len(weighted_servers)]
        self.weighted_index += 1
        return server
    
    async def health_check(self):
        """Периодическая проверка здоровья серверов"""
        while True:
            for server in self.servers:
                try:
                    # Простая проверка доступности
                    reader, writer = await asyncio.wait_for(
                        asyncio.open_connection(server.host, server.port),
                        timeout=5.0
                    )
                    writer.close()
                    await writer.wait_closed()
                    server.is_healthy = True
                except:
                    server.is_healthy = False
            
            await asyncio.sleep(30)  # Проверка каждые 30 секунд
```

### 4.3 Database Sharding и Partitioning

**Стратегии шардинга:**

```
┌─── SHARDING STRATEGIES ───┐
│                           │
│  🔢 Range-based Sharding  │
│  Shard 1: user_id 1-1000  │
│  Shard 2: user_id 1001-2000│
│  Shard 3: user_id 2001-3000│
│                           │
│  #️⃣ Hash-based Sharding   │
│  hash(user_id) % 3        │
│  Равномерное распределение │
│                           │
│  📊 Directory-based       │
│  Lookup service знает     │
│  где находится каждый key │
│                           │
│  🌍 Geographic Sharding   │
│  US East, US West, Europe │
│  Близость к пользователю  │
└───────────────────────────┘
```

**Архитектура шардированной БД:**

```
┌─── SHARDED DATABASE ARCHITECTURE ───┐
│                                     │
│           Application               │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │    Shard Router     │          │
│    │  (Query Coordinator)│          │
│    └─┬─────────┬─────────┬─┘        │
│      │         │         │          │
│  ┌───▼───┐ ┌───▼───┐ ┌───▼───┐      │
│  │Shard 1│ │Shard 2│ │Shard 3│      │
│  │       │ │       │ │       │      │
│  │Users  │ │Users  │ │Users  │      │
│  │1-1000 │ │1001-  │ │2001-  │      │
│  │       │ │2000   │ │3000   │      │
│  └───────┘ └───────┘ └───────┘      │
│                                     │
│  ┌─────────────────────────────┐    │
│  │        Challenges           │    │
│  │ • Cross-shard queries       │    │
│  │ • Rebalancing shards        │    │
│  │ • Distributed transactions  │    │
│  │ • Hotspot avoidance         │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

**Реализация Shard Router:**

```python
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ShardConfig:
    shard_id: str
    connection_string: str
    weight: float = 1.0
    is_active: bool = True

class ShardRouter:
    def __init__(self):
        self.shards: Dict[str, ShardConfig] = {}
        self.hash_ring: List[tuple] = []  # (hash_value, shard_id)
        self.virtual_nodes = 150  # Виртуальные узлы для лучшего распределения
    
    def add_shard(self, shard: ShardConfig):
        """Добавление нового шарда"""
        self.shards[shard.shard_id] = shard
        self._rebuild_hash_ring()
    
    def remove_shard(self, shard_id: str):
        """Удаление шарда"""
        if shard_id in self.shards:
            del self.shards[shard_id]
            self._rebuild_hash_ring()
    
    def _rebuild_hash_ring(self):
        """Перестроение кольца хэшей (Consistent Hashing)"""
        self.hash_ring = []
        
        for shard_id in self.shards:
            # Создаем виртуальные узлы для каждого шарда
            for i in range(self.virtual_nodes):
                virtual_key = f"{shard_id}:{i}"
                hash_value = int(hashlib.md5(virtual_key.encode()).hexdigest(), 16)
                self.hash_ring.append((hash_value, shard_id))
        
        # Сортируем по хэш-значению
        self.hash_ring.sort()
    
    def get_shard_for_key(self, key: str) -> Optional[ShardConfig]:
        """Определение шарда для ключа"""
        if not self.hash_ring:
            return None
        
        # Хэшируем ключ
        key_hash = int(hashlib.md5(str(key).encode()).hexdigest(), 16)
        
        # Находим ближайший узел в кольце
        for hash_value, shard_id in self.hash_ring:
            if key_hash <= hash_value:
                return self.shards.get(shard_id)
        
        # Если не нашли, берем первый (кольцо замыкается)
        return self.shards.get(self.hash_ring[0][1])
    
    def route_query(self, user_id: int, query: str) -> Dict[str, Any]:
        """Маршрутизация запроса к нужному шарду"""
        shard = self.get_shard_for_key(user_id)
        
        if not shard or not shard.is_active:
            raise Exception(f"No active shard found for user_id: {user_id}")
        
        return {
            'shard_id': shard.shard_id,
            'connection': shard.connection_string,
            'query': query
        }
    
    def get_shards_for_broadcast(self) -> List[ShardConfig]:
        """Получение всех активных шардов для broadcast запросов"""
        return [shard for shard in self.shards.values() if shard.is_active]

# Использование
router = ShardRouter()

# Добавляем шарды
router.add_shard(ShardConfig("shard_1", "postgresql://db1:5432/users"))
router.add_shard(ShardConfig("shard_2", "postgresql://db2:5432/users"))
router.add_shard(ShardConfig("shard_3", "postgresql://db3:5432/users"))

# Маршрутизация запросов
user_id = 12345
route_info = router.route_query(user_id, "SELECT * FROM users WHERE id = ?")
print(f"Query for user {user_id} goes to {route_info['shard_id']}")
```

### 4.4 CAP теорема и Eventual Consistency

```
┌─── CAP THEOREM ───┐
│                   │
│  C - Consistency  │
│  │               │
│  │    ┌─────┐    │
│  └────┤ CAP ├────┘
│       └─┬───┘     
│         │         
│  A - Availability │
│         │         
│         │         
│  P - Partition    │
│      Tolerance    │
│                   │
│  Choose any 2!    │
└───────────────────┘
```

**Стратегии консистентности:**

| Тип | Описание | Примеры | Плюсы | Минусы |
|-----|----------|---------|-------|--------|
| **Strong Consistency** | Все узлы видят одни данные | RDBMS, Zookeeper | Простота | Высокая задержка |
| **Eventual Consistency** | Узлы сойдутся во времени | DNS, Amazon S3 | Высокая доступность | Сложность логики |
| **Weak Consistency** | Никаких гарантий | Memcached | Максимальная скорость | Потеря данных |
| **Causal Consistency** | Причинно-связанные операции | Social Media | Интуитивность | Сложная реализация |

---

## 📊 Глава 5: Обработка больших данных

### 5.1 Batch vs Stream Processing

```
┌─── DATA PROCESSING PARADIGMS ───┐
│                                 │
│  📦 Batch Processing            │
│  ┌─────────────────────────┐    │
│  │ Input Data              │    │
│  │ ┌───┬───┬───┬───┬───┐   │    │
│  │ │ 1 │ 2 │ 3 │ 4 │ 5 │   │    │
│  │ └───┴───┴───┴───┴───┘   │    │
│  │           │             │    │
│  │    ┌──────▼──────┐      │    │
│  │    │  Process    │      │    │
│  │    │  All Data   │      │    │
│  │    └──────┬──────┘      │    │
│  │           │             │    │
│  │    ┌──────▼──────┐      │    │
│  │    │   Output    │      │    │
│  │    └─────────────┘      │    │
│  └─────────────────────────┘    │
│                                 │
│  🌊 Stream Processing           │
│  ┌─────────────────────────┐    │
│  │ Input Stream            │    │
│  │ ──→1──→2──→3──→4──→5──→ │    │
│  │     │   │   │   │   │   │    │
│  │     ▼   ▼   ▼   ▼   ▼   │    │
│  │  [Process each event]   │    │
│  │     │   │   │   │   │   │    │
│  │     ▼   ▼   ▼   ▼   ▼   │    │
│  │ ──→1'─→2'─→3'─→4'─→5'─→│    │
│  │ Output Stream           │    │
│  └─────────────────────────┘    │
└─────────────────────────────────┘
```

### 5.2 MapReduce парадигма

**Концептуальная модель MapReduce:**

```
┌─── MAPREDUCE WORKFLOW ───┐
│                          │
│  📄 Input Data           │
│  ┌─────────────────┐     │
│  │ File 1: [a,b,c] │     │
│  │ File 2: [d,e,f] │     │
│  │ File 3: [g,h,i] │     │
│  └─────────────────┘     │
│            │             │
│  ┌─────────▼─────────┐   │
│  │   MAP PHASE       │   │
│  │                   │   │
│  │ Mapper1→[(a,1)]   │   │
│  │ Mapper2→[(d,1)]   │   │
│  │ Mapper3→[(g,1)]   │   │
│  └─────────┬─────────┘   │
│            │             │
│  ┌─────────▼─────────┐   │
│  │  SHUFFLE & SORT   │   │
│  │                   │   │
│  │ Group by key      │   │
│  │ [(a,[1,1,1])]     │   │
│  └─────────┬─────────┘   │
│            │             │
│  ┌─────────▼─────────┐   │
│  │  REDUCE PHASE     │   │
│  │                   │   │
│  │ Reducer→[(a,3)]   │   │
│  │ Output: counts    │   │
│  └───────────────────┘   │
└──────────────────────────┘
```

**Реализация простого MapReduce:**

```python
from collections import defaultdict
from typing import List, Tuple, Callable, Any
import multiprocessing as mp
from functools import reduce

class MapReduceFramework:
    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or mp.cpu_count()
    
    def map_reduce(self, 
                   data: List[Any],
                   map_func: Callable,
                   reduce_func: Callable,
                   partition_func: Callable = None) -> dict:
        """
        Выполнение MapReduce операции
        """
        # MAP PHASE
        with mp.Pool(self.num_workers) as pool:
            map_results = pool.map(map_func, data)
        
        # Flatten результатов маппинга
        flattened = []
        for result in map_results:
            if isinstance(result, list):
                flattened.extend(result)
            else:
                flattened.append(result)
        
        # SHUFFLE & SORT PHASE
        grouped = defaultdict(list)
        for key, value in flattened:
            grouped[key].append(value)
        
        # REDUCE PHASE
        final_results = {}
        for key, values in grouped.items():
            final_results[key] = reduce_func(values)
        
        return final_results

# Пример: подсчет слов в документах
def word_count_mapper(document: str) -> List[Tuple[str, int]]:
    """Map функция для подсчета слов"""
    words = document.lower().split()
    return [(word, 1) for word in words]

def word_count_reducer(counts: List[int]) -> int:
    """Reduce функция для суммирования"""
    return sum(counts)

# Использование
documents = [
    "hello world hello",
    "world of data processing",
    "hello data world"
]

framework = MapReduceFramework()
word_counts = framework.map_reduce(
    documents,
    word_count_mapper,
    word_count_reducer
)

print(word_counts)
# {'hello': 3, 'world': 3, 'of': 1, 'data': 2, 'processing': 1}
```

### 5.3 Data Pipeline архитектуры

**Lambda Architecture:**

```
┌─── LAMBDA ARCHITECTURE ───┐
│                           │
│     📥 Data Sources       │
│     ┌─────┬─────┬─────┐   │
│     │API  │Logs │IoT  │   │
│     └──┬──┴──┬──┴──┬──┘   │
│        │     │     │      │
│        └─────┼─────┘      │
│              │            │
│    ┌─────────▼─────────┐  │
│    │   Message Queue   │  │
│    │   (Kafka/Kinesis) │  │
│    └─────┬─────────┬───┘  │
│          │         │      │
│  ┌───────▼─┐   ┌───▼───┐  │
│  │ Batch   │   │Stream │  │
│  │ Layer   │   │Layer  │  │
│  │         │   │       │  │
│  │ HDFS/S3 │   │Storm/ │  │
│  │ +Spark  │   │Kafka  │  │
│  │         │   │Streams│  │
│  └───┬─────┘   └───┬───┘  │
│      │             │      │
│      └─────┬───────┘      │
│            │              │
│    ┌───────▼───────┐      │
│    │ Serving Layer │      │
│    │   (NoSQL DB)  │      │
│    └───────────────┘      │
└───────────────────────────┘
```

**Kappa Architecture (упрощенная):**

```
┌─── KAPPA ARCHITECTURE ───┐
│                          │
│     📥 Data Sources      │
│     ┌─────┬─────┬─────┐  │
│     │API  │Logs │IoT  │  │
│     └──┬──┴──┬──┴──┬──┘  │
│        │     │     │     │
│        └─────┼─────┘     │
│              │           │
│    ┌─────────▼─────────┐ │
│    │   Stream Processor│ │
│    │   (Kafka Streams/ │ │
│    │    Apache Flink)  │ │
│    └─────────┬─────────┘ │
│              │           │
│    ┌─────────▼─────────┐ │
│    │ Serving Layer     │ │
│    │ • Real-time views │ │
│    │ • Historical data │ │
│    └───────────────────┘ │
│                          │
│  + Простота              │
│  + Единый код            │
│  - Reprocessing сложнее  │
└──────────────────────────┘
```

### 5.4 Реализация простого Stream Processor

```python
import asyncio
import json
from typing import Dict, List, Callable, Any
from collections import deque, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class StreamEvent:
    key: str
    value: Any
    timestamp: datetime
    partition: int = 0

class WindowedAggregator:
    """Агрегатор с временными окнами"""
    
    def __init__(self, window_size: timedelta, slide_interval: timedelta):
        self.window_size = window_size
        self.slide_interval = slide_interval
        self.windows: Dict[str, deque] = defaultdict(deque)
        self.aggregates: Dict[str, Any] = {}
    
    def add_event(self, event: StreamEvent):
        """Добавление события в окна"""
        key = event.key
        self.windows[key].append(event)
        
        # Удаление старых событий
        cutoff_time = event.timestamp - self.window_size
        while (self.windows[key] and 
               self.windows[key][0].timestamp < cutoff_time):
            self.windows[key].popleft()
    
    def get_window_aggregate(self, key: str, agg_func: Callable) -> Any:
        """Получение агрегата для окна"""
        if key not in self.windows:
            return None
        
        values = [event.value for event in self.windows[key]]
        return agg_func(values) if values else None

class StreamProcessor:
    """Простой процессор потоков данных"""
    
    def __init__(self):
        self.processors: List[Callable] = []
        self.aggregators: Dict[str, WindowedAggregator] = {}
        self.state: Dict[str, Any] = {}
    
    def add_processor(self, func: Callable):
        """Добавление функции обработки"""
        self.processors.append(func)
    
    def add_aggregator(self, name: str, aggregator: WindowedAggregator):
        """Добавление агрегатора"""
        self.aggregators[name] = aggregator
    
    async def process_stream(self, events: List[StreamEvent]):
        """Обработка потока событий"""
        for event in events:
            # Применяем все процессоры
            processed_event = event
            for processor in self.processors:
                processed_event = await self._apply_processor(
                    processor, processed_event
                )
            
            # Обновляем агрегаторы
            for agg in self.aggregators.values():
                agg.add_event(processed_event)
            
            # Выводим результат
            await self._emit_results(processed_event)
    
    async def _apply_processor(self, processor: Callable, event: StreamEvent) -> StreamEvent:
        """Применение процессора к событию"""
        if asyncio.iscoroutinefunction(processor):
            return await processor(event)
        else:
            return processor(event)
    
    async def _emit_results(self, event: StreamEvent):
        """Вывод результатов обработки"""
        # Можно отправлять в другие системы, логировать и т.д.
        print(f"Processed: {event.key} = {event.value} at {event.timestamp}")

# Пример использования
async def main():
    # Создаем процессор
    processor = StreamProcessor()
    
    # Добавляем обработчик для фильтрации
    def filter_processor(event: StreamEvent) -> StreamEvent:
        if isinstance(event.value, (int, float)) and event.value > 0:
            return event
        return None
    
    # Добавляем обработчик для трансформации
    async def transform_processor(event: StreamEvent) -> StreamEvent:
        if event and isinstance(event.value, (int, float)):
            event.value = event.value * 2  # Умножаем на 2
        return event
    
    processor.add_processor(filter_processor)
    processor.add_processor(transform_processor)
    
    # Создаем агрегатор для скользящего окна
    window_agg = WindowedAggregator(
        window_size=timedelta(minutes=5),
        slide_interval=timedelta(minutes=1)
    )
    processor.add_aggregator("sliding_window", window_agg)
    
    # Генерируем тестовые события
    events = []
    base_time = datetime.now()
    
    for i in range(10):
        event = StreamEvent(
            key=f"sensor_{i % 3}",
            value=i * 10,
            timestamp=base_time + timedelta(seconds=i * 30)
        )
        events.append(event)
    
    # Обрабатываем поток
    await processor.process_stream(events)
    
    # Выводим агрегаты
    for sensor_id in ["sensor_0", "sensor_1", "sensor_2"]:
        avg_value = window_agg.get_window_aggregate(
            sensor_id, 
            lambda values: sum(values) / len(values)
        )
        print(f"Average for {sensor_id}: {avg_value}")

# Запуск
asyncio.run(main())
```

---

## 📈 Глава 6: Мониторинг и наблюдаемость

### 6.1 Три столпа наблюдаемости

```
┌─── THREE PILLARS OF OBSERVABILITY ───┐
│                                      │
│  📊 METRICS                          │
│  ┌─────────────────────────────┐     │
│  │ • Численные показатели      │     │
│  │ • Временные ряды            │     │
│  │ • Агрегированные данные     │     │
│  │                             │     │
│  │ Examples:                   │     │
│  │ - Response time: 200ms      │     │
│  │ - Error rate: 0.1%          │     │
│  │ - CPU usage: 75%            │     │
│  └─────────────────────────────┘     │
│                                      │
│  📝 LOGS                             │
│  ┌─────────────────────────────┐     │
│  │ • Структурированные записи  │     │
│  │ • События приложения        │     │
│  │ • Контекстная информация    │     │
│  │                             │     │
│  │ Examples:                   │     │
│  │ - Error messages            │     │
│  │ - User actions              │     │
│  │ - System events             │     │
│  └─────────────────────────────┘     │
│                                      │
│  🔍 TRACES                           │
│  ┌─────────────────────────────┐     │
│  │ • Путь запроса через систему│     │
│  │ • Распределенные вызовы     │     │
│  │ • Причинно-следственные связи│     │
│  │                             │     │
│  │ Examples:                   │     │
│  │ - Request flow              │     │
│  │ - Service dependencies      │     │
│  │ - Performance bottlenecks   │     │
│  └─────────────────────────────┘     │
└──────────────────────────────────────┘
```

### 6.2 Метрики и их типы

**Классификация метрик:**

| Тип метрики | Описание | Примеры | Когда использовать |
|-------------|----------|---------|-------------------|
| **Counter** | Всегда увеличивается | HTTP requests, errors | Подсчет событий |
| **Gauge** | Может расти/падать | CPU usage, memory | Текущее состояние |
| **Histogram** | Распределение значений | Response times | Анализ распределения |
| **Summary** | Квантили за период | 95th percentile latency | Производительность |

**Реализация системы метрик:**

```python
import time
import threading
from typing import Dict, List, Optional
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
import statistics

@dataclass
class MetricSample:
    value: float
    timestamp: float
    labels: Dict[str, str] = None

class MetricRegistry:
    """Реестр метрик приложения"""
    
    def __init__(self):
        self._metrics: Dict[str, 'BaseMetric'] = {}
        self._lock = threading.Lock()
    
    def counter(self, name: str, help_text: str = "") -> 'Counter':
        """Создание/получение счетчика"""
        return self._get_or_create(name, Counter, help_text)
    
    def gauge(self, name: str, help_text: str = "") -> 'Gauge':
        """Создание/получение индикатора"""
        return self._get_or_create(name, Gauge, help_text)
    
    def histogram(self, name: str, buckets: List[float] = None, help_text: str = "") -> 'Histogram':
        """Создание/получение гистограммы"""
        buckets = buckets or [0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
        return self._get_or_create(name, Histogram, help_text, buckets=buckets)
    
    def _get_or_create(self, name: str, metric_class, help_text: str, **kwargs):
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = metric_class(name, help_text, **kwargs)
            return self._metrics[name]
    
    def collect_all(self) -> Dict[str, List[MetricSample]]:
        """Сбор всех метрик"""
        result = {}
        with self._lock:
            for name, metric in self._metrics.items():
                result[name] = metric.collect()
        return result

class BaseMetric:
    def __init__(self, name: str, help_text: str):
        self.name = name
        self.help_text = help_text
        self._lock = threading.Lock()
    
    def collect(self) -> List[MetricSample]:
        raise NotImplementedError

class Counter(BaseMetric):
    """Счетчик - всегда увеличивается"""
    
    def __init__(self, name: str, help_text: str):
        super().__init__(name, help_text)
        self._value = 0.0
    
    def inc(self, amount: float = 1.0, labels: Dict[str, str] = None):
        """Увеличение счетчика"""
        if amount < 0:
            raise ValueError("Counter can only increase")
        
        with self._lock:
            self._value += amount
    
    def collect(self) -> List[MetricSample]:
        with self._lock:
            return [MetricSample(self._value, time.time())]

class Gauge(BaseMetric):
    """Индикатор - может увеличиваться и уменьшаться"""
    
    def __init__(self, name: str, help_text: str):
        super().__init__(name, help_text)
        self._value = 0.0
    
    def set(self, value: float, labels: Dict[str, str] = None):
        """Установка значения"""
        with self._lock:
            self._value = value
    
    def inc(self, amount: float = 1.0):
        """Увеличение значения"""
        with self._lock:
            self._value += amount
    
    def dec(self, amount: float = 1.0):
        """Уменьшение значения"""
        with self._lock:
            self._value -= amount
    
    def collect(self) -> List[MetricSample]:
        with self._lock:
            return [MetricSample(self._value, time.time())]

class Histogram(BaseMetric):
    """Гистограмма для измерения распределения значений"""
    
    def __init__(self, name: str, help_text: str, buckets: List[float]):
        super().__init__(name, help_text)
        self.buckets = sorted(buckets)
        self._bucket_counts = [0] * len(buckets)
        self._count = 0
        self._sum = 0.0
        self._samples = deque(maxlen=1000)  # Последние 1000 образцов
    
    def observe(self, value: float, labels: Dict[str, str] = None):
        """Добавление наблюдения"""
        with self._lock:
            self._count += 1
            self._sum += value
            self._samples.append(value)
            
            # Обновляем bucket'ы
            for i, bucket_limit in enumerate(self.buckets):
                if value <= bucket_limit:
                    self._bucket_counts[i] += 1
    
    def collect(self) -> List[MetricSample]:
        with self._lock:
            samples = []
            timestamp = time.time()
            
            # Bucket counts
            for i, (bucket_limit, count) in enumerate(zip(self.buckets, self._bucket_counts)):
                samples.append(MetricSample(
                    count, 
                    timestamp, 
                    {"le": str(bucket_limit)}
                ))
            
            # Total count and sum
            samples.append(MetricSample(self._count, timestamp, {"type": "count"}))
            samples.append(MetricSample(self._sum, timestamp, {"type": "sum"}))
            
            # Percentiles
            if self._samples:
                sorted_samples = sorted(self._samples)
                p50 = statistics.median(sorted_samples)
                p95 = sorted_samples[int(0.95 * len(sorted_samples))]
                p99 = sorted_samples[int(0.99 * len(sorted_samples))]
                
                samples.extend([
                    MetricSample(p50, timestamp, {"quantile": "0.5"}),
                    MetricSample(p95, timestamp, {"quantile": "0.95"}),
                    MetricSample(p99, timestamp, {"quantile": "0.99"})
                ])
            
            return samples

# Глобальный реестр метрик
METRICS = MetricRegistry()

# Пример использования метрик
class MetricsExample:
    def __init__(self):
        # Создаем метрики
        self.request_count = METRICS.counter(
            "http_requests_total", 
            "Total HTTP requests"
        )
        self.active_users = METRICS.gauge(
            "active_users_current",
            "Currently active users"
        )
        self.response_time = METRICS.histogram(
            "http_request_duration_seconds",
            "HTTP request duration in seconds",
            buckets=[0.1, 0.5, 1.0, 2.5, 5.0]
        )
    
    def handle_request(self, path: str):
        """Обработка HTTP запроса с метриками"""
        start_time = time.time()
        
        try:
            # Увеличиваем счетчик запросов
            self.request_count.inc()
            
            # Имитируем обработку
            time.sleep(0.1)
            
            # Записываем время ответа
            duration = time.time() - start_time
            self.response_time.observe(duration)
            
        except Exception as e:
            # Можно добавить метрику ошибок
            error_counter = METRICS.counter("http_errors_total")
            error_counter.inc()
            raise
    
    def user_login(self):
        """Пользователь залогинился"""
        self.active_users.inc()
    
    def user_logout(self):
        """Пользователь разлогинился"""
        self.active_users.dec()
```

### 6.3 Structured Logging

**Архитектура логирования:**

```
┌─── LOGGING ARCHITECTURE ───┐
│                            │
│  Application               │
│       │                   │
│  ┌────▼────┐              │
│  │ Logger  │              │
│  │ (JSON)  │              │
│  └────┬────┘              │
│       │                   │
│  ┌────▼────┐              │
│  │ Agent   │              │
│  │(Fluentd/│              │
│  │Filebeat)│              │
│  └────┬────┘              │
│       │                   │
│  ┌────▼────┐              │
│  │ Message │              │
│  │ Queue   │              │
│  │(Kafka)  │              │
│  └────┬────┘              │
│       │                   │
│  ┌────▼────┐              │
│  │Log Store│              │
│  │(ELK/    │              │
│  │ Loki)   │              │
│  └─────────┘              │
└────────────────────────────┘
```

**Реализация структурированного логгера:**

```python
import json
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
import traceback
import uuid
from contextvars import ContextVar

# Контекстная переменная для trace ID
trace_id_var: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)

class StructuredLogger:
    """Структурированный логгер с поддержкой JSON"""
    
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Создаем JSON formatter
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        self.logger.addHandler(handler)
        
        self.base_context = {
            "service": "myapp",
            "version": "1.0.0"
        }
    
    def _create_log_entry(self, level: str, message: str, **kwargs) -> Dict[str, Any]:
        """Создание структурированной записи лога"""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": message,
            "trace_id": trace_id_var.get(),
            **self.base_context,
            **kwargs
        }
        
        # Удаляем None значения
        return {k: v for k, v in entry.items() if v is not None}
    
    def info(self, message: str, **kwargs):
        entry = self._create_log_entry("INFO", message, **kwargs)
        self.logger.info(json.dumps(entry))
    
    def warning(self, message: str, **kwargs):
        entry = self._create_log_entry("WARNING", message, **kwargs)
        self.logger.warning(json.dumps(entry))
    
    def error(self, message: str, error: Exception = None, **kwargs):
        entry = self._create_log_entry("ERROR", message, **kwargs)
        
        if error:
            entry.update({
                "error_type": type(error).__name__,
                "error_message": str(error),
                "stack_trace": traceback.format_exc()
            })
        
        self.logger.error(json.dumps(entry))
    
    def debug(self, message: str, **kwargs):
        entry = self._create_log_entry("DEBUG", message, **kwargs)
        self.logger.debug(json.dumps(entry))

class JsonFormatter(logging.Formatter):
    """JSON форматтер для стандартного logging"""
    
    def format(self, record):
        # Если сообщение уже JSON, возвращаем как есть
        try:
            json.loads(record.getMessage())
            return record.getMessage()
        except:
            # Если не JSON, создаем структуру
            log_entry = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }
            
            if record.exc_info:
                log_entry["stack_trace"] = self.formatException(record.exc_info)
            
            return json.dumps(log_entry)

class RequestTracker:
    """Трекер запросов с автоматическим логированием"""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
    
    def __enter__(self):
        # Генерируем уникальный trace ID
        self.trace_id = str(uuid.uuid4())
        trace_id_var.set(self.trace_id)
        
        self.start_time = time.time()
        self.logger.info("Request started", trace_id=self.trace_id)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        
        if exc_type:
            self.logger.error(
                "Request failed",
                duration_ms=duration * 1000,
                error_type=exc_type.__name__,
                trace_id=self.trace_id
            )
        else:
            self.logger.info(
                "Request completed",
                duration_ms=duration * 1000,
                trace_id=self.trace_id
            )
        
        trace_id_var.set(None)

# Использование
logger = StructuredLogger("web_service")

def handle_user_request(user_id: int, action: str):
    """Пример обработки запроса с логированием"""
    with RequestTracker(logger):
        try:
            logger.info(
                "Processing user action",
                user_id=user_id,
                action=action,
                ip_address="192.168.1.100"
            )
            
            # Имитация работы
            if action == "error":
                raise ValueError("Something went wrong")
            
            logger.info(
                "Action completed successfully",
                user_id=user_id,
                action=action
            )
            
        except Exception as e:
            logger.error("Failed to process action", error=e, user_id=user_id)
            raise

# Пример использования
handle_user_request(12345, "login")
```

### 6.4 Distributed Tracing

**Концепция распределенного трейсинга:**

```
┌─── DISTRIBUTED TRACE ───┐
│                         │
│  Frontend               │
│      │ GET /api/user    │
│      │ Span A           │
│      └─────┬───────────►│
│            │            │
│  API Gateway            │
│      │ Span B           │
│      ├──────────────────┤
│      │ /auth/validate   │
│      └─────┬───────────►│
│            │            │
│  Auth Service           │
│      │ Span C           │
│      ├──────────────────┤
│      │ /users/profile   │
│      └─────┬───────────►│
│            │            │
│  User Service           │
│      │ Span D           │
│      ├─────┬────────────┤
│      │ DB Query         │
│      │ Span E           │
│      └─────┴────────────┤
│                         │
│  Trace = A→B→C→D→E      │
│  Parent-Child relations │
└─────────────────────────┘
```

**Реализация простого трейсера:**

```python
import time
import uuid
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from contextvars import ContextVar
from datetime import datetime

@dataclass
class Span:
    """Span представляет одну операцию в trace"""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    operation_name: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    tags: Dict[str, str] = field(default_factory=dict)
    logs: List[Dict] = field(default_factory=list)
    
    @property
    def duration_ms(self) -> Optional[float]:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return None
    
    def set_tag(self, key: str, value: str):
        """Добавление тега к span'у"""
        self.tags[key] = value
    
    def log(self, message: str, **kwargs):
        """Добавление лог-записи к span'у"""
        log_entry = {
            "timestamp": time.time(),
            "message": message,
            **kwargs
        }
        self.logs.append(log_entry)
    
    def finish(self):
        """Завершение span'а"""
        self.end_time = time.time()

# Контекстные переменные для текущего trace/span
current_trace_id: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
current_span: ContextVar[Optional[Span]] = ContextVar('span', default=None)

class Tracer:
    """Простой distributed tracer"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.spans: List[Span] = []
    
    def start_trace(self, operation_name: str) -> Span:
        """Начало нового trace"""
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=None,
            operation_name=operation_name
        )
        
        span.set_tag("service.name", self.service_name)
        
        current_trace_id.set(trace_id)
        current_span.set(span)
        
        self.spans.append(span)
        return span
    
    def start_span(self, operation_name: str, parent_span: Optional[Span] = None) -> Span:
        """Начало нового span в рамках существующего trace"""
        trace_id = current_trace_id.get()
        parent = parent_span or current_span.get()
        
        if not trace_id:
            return self.start_trace(operation_name)
        
        span_id = str(uuid.uuid4())
        parent_span_id = parent.span_id if parent else None
        
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            operation_name=operation_name
        )
        
        span.set_tag("service.name", self.service_name)
        
        current_span.set(span)
        self.spans.append(span)
        return span
    
    def get_trace_context(self) -> Dict[str, str]:
        """Получение контекста для передачи между сервисами"""
        span = current_span.get()
        if span:
            return {
                "trace-id": span.trace_id,
                "span-id": span.span_id
            }
        return {}
    
    def inject_context(self, trace_id: str, parent_span_id: str):
        """Внедрение контекста из внешнего запроса"""
        current_trace_id.set(trace_id)
        # Можно создать dummy span для контекста
    
    def finish_span(self, span: Optional[Span] = None):
        """Завершение span'а"""
        target_span = span or current_span.get()
        if target_span:
            target_span.finish()
    
    def export_traces(self) -> List[Dict]:
        """Экспорт всех traces в JSON формате"""
        traces = {}
        
        # Группируем spans по trace_id
        for span in self.spans:
            if span.trace_id not in traces:
                traces[span.trace_id] = []
            
            traces[span.trace_id].append({
                "span_id": span.span_id,
                "parent_span_id": span.parent_span_id,
                "operation_name": span.operation_name,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "duration_ms": span.duration_ms,
                "tags": span.tags,
                "logs": span.logs
            })
        
        return [{"trace_id": tid, "spans": spans} for tid, spans in traces.items()]

class TracedOperation:
    """Контекстный менеджер для автоматического трейсинга"""
    
    def __init__(self, tracer: Tracer, operation_name: str, **tags):
        self.tracer = tracer
        self.operation_name = operation_name
        self.tags = tags
        self.span = None
    
    def __enter__(self):
        self.span = self.tracer.start_span(self.operation_name)
        
        # Добавляем теги
        for key, value in self.tags.items():
            self.span.set_tag(key, str(value))
        
        return self.span
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.span.set_tag("error", "true")
            self.span.set_tag("error.type", exc_type.__name__)
            self.span.log("error", message=str(exc_val))
        
        self.tracer.finish_span(self.span)

# Пример использования
tracer = Tracer("user-service")

def get_user_profile(user_id: int):
    """Получение профиля пользователя с трейсингом"""
    
    # Начинаем основной span
    with TracedOperation(tracer, "get_user_profile", user_id=user_id) as span:
        span.log("Starting user profile retrieval")
        
        # Span для проверки кэша
        with TracedOperation(tracer, "cache_lookup") as cache_span:
            cache_span.set_tag("cache.key", f"user:{user_id}")
            # Имитация проверки кэша
            time.sleep(0.01)
            cache_hit = False
            cache_span.set_tag("cache.hit", str(cache_hit).lower())
        
        if not cache_hit:
            # Span для запроса к БД
            with TracedOperation(tracer, "database_query") as db_span:
                db_span.set_tag("db.type", "postgresql")
                db_span.set_tag("db.statement", "SELECT * FROM users WHERE id = ?")
                
                # Имитация запроса к БД
                time.sleep(0.05)
                db_span.log("Query executed successfully")
        
        span.log("User profile retrieved successfully")
        return {"user_id": user_id, "name": "John Doe"}

# Использование
def simulate_request():
    """Имитация обработки запроса"""
    
    # Начинаем новый trace
    with TracedOperation(tracer, "handle_user_request") as root_span:
        root_span.set_tag("http.method", "GET")
        root_span.set_tag("http.url", "/api/users/123")
        
        # Вызываем бизнес-логику
        user = get_user_profile(123)
        
        root_span.set_tag("http.status_code", "200")
        root_span.log("Request completed successfully")

# Выполняем запрос
simulate_request()

# Экспортируем traces
traces = tracer.export_traces()
print(json.dumps(traces, indent=2))
```

### 6.5 SLI/SLO/SLA Framework

**Концепции надежности:**

```
┌─── RELIABILITY PYRAMID ───┐
│                           │
│        📋 SLA             │
│   Service Level Agreement │
│   (External commitment)   │
│  ┌─────────────────────┐  │
│  │ "99.9% uptime"      │  │
│  │ "< 200ms response"  │  │
│  └─────────────────────┘  │
│            ▲              │
│        📊 SLO             │
│  Service Level Objective  │
│   (Internal target)       │
│  ┌─────────────────────┐  │
│  │ "99.95% success"    │  │
│  │ "95th % < 150ms"    │  │
│  └─────────────────────┘  │
│            ▲              │
│        📈 SLI             │
│  Service Level Indicator  │
│    (Measurement)          │
│  ┌─────────────────────┐  │
│  │ Success rate        │  │
│  │ Response time       │  │
│  │ Error budget        │  │
│  └─────────────────────┘  │
└───────────────────────────┘
```

**Реализация SLI/SLO мониторинга:**

```python
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import deque, defaultdict
from datetime import datetime, timedelta
import statistics

@dataclass
class SLIConfig:
    """Конфигурация Service Level Indicator"""
    name: str
    metric_name: str
    good_threshold: Optional[float] = None
    bad_threshold: Optional[float] = None
    is_latency_metric: bool = False

@dataclass
class SLOConfig:
    """Конфигурация Service Level Objective"""
    name: str
    sli_name: str
    target_percentage: float  # 99.9
    window_days: int = 30

class SLITracker:
    """Трекер для Service Level Indicators"""
    
    def __init__(self):
        self.measurements: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.configs: Dict[str, SLIConfig] = {}
    
    def register_sli(self, config: SLIConfig):
        """Регистрация нового SLI"""
        self.configs[config.name] = config
    
    def record_measurement(self, sli_name: str, value: float, timestamp: Optional[float] = None):
        """Запись измерения"""
        if timestamp is None:
            timestamp = time.time()
        
        self.measurements[sli_name].append({
            'value': value,
            'timestamp': timestamp
        })
    
    def calculate_sli(self, sli_name: str, window_minutes: int = 60) -> Optional[float]:
        """Вычисление SLI за указанный период"""
        if sli_name not in self.configs:
            return None
        
        config = self.configs[sli_name]
        measurements = self.measurements[sli_name]
        
        if not measurements:
            return None
        
        # Фильтруем измерения по времени
        cutoff_time = time.time() - (window_minutes * 60)
        recent_measurements = [
            m for m in measurements 
            if m['timestamp'] >= cutoff_time
        ]
        
        if not recent_measurements:
            return None
        
        values = [m['value'] for m in recent_measurements]
        
        if config.is_latency_metric:
            # Для латенси считаем процентиль
            return statistics.quantile(values, 0.95) if values else None
        else:
            # Для availability считаем процент успешных запросов
            if config.good_threshold is not None:
                good_count = sum(1 for v in values if v >= config.good_threshold)
            elif config.bad_threshold is not None:
                good_count = sum(1 for v in values if v < config.bad_threshold)
            else:
                good_count = sum(1 for v in values if v > 0)
            
            return (good_count / len(values)) * 100 if values else 0

class SLOMonitor:
    """Монитор Service Level Objectives"""
    
    def __init__(self, sli_tracker: SLITracker):
        self.sli_tracker = sli_tracker
        self.slos: Dict[str, SLOConfig] = {}
        self.error_budgets: Dict[str, float] = {}
    
    def register_slo(self, config: SLOConfig):
        """Регистрация нового SLO"""
        self.slos[config.name] = config
        # Инициализируем error budget (100% - target%)
        self.error_budgets[config.name] = 100.0 - config.target_percentage
    
    def check_slo_compliance(self, slo_name: str) -> Dict[str, float]:
        """Проверка соблюдения SLO"""
        if slo_name not in self.slos:
            return {}
        
        slo = self.slos[slo_name]
        
        # Получаем текущий SLI
        current_sli = self.sli_tracker.calculate_sli(slo.sli_name)
        
        if current_sli is None:
            return {"status": "no_data"}
        
        # Вычисляем остаток error budget
        if current_sli >= slo.target_percentage:
            compliance_status = "compliant"
            error_budget_used = 0.0
        else:
            compliance_status = "breach"
            error_budget_used = slo.target_percentage - current_sli
        
        error_budget_remaining = self.error_budgets[slo_name] - error_budget_used
        
        return {
            "status": compliance_status,
            "current_sli": current_sli,
            "target_slo": slo.target_percentage,
            "error_budget_used": error_budget_used,
            "error_budget_remaining": error_budget_remaining,
            "error_budget_usage_percent": (error_budget_used / self.error_budgets[slo_name]) * 100
        }
    
    def get_error_budget_burn_rate(self, slo_name: str, window_hours: int = 1) -> float:
        """Скорость сжигания error budget"""
        if slo_name not in self.slos:
            return 0.0
        
        # Упрощенная версия - в реальности нужно учитывать historical data
        compliance = self.check_slo_compliance(slo_name)
        if compliance.get("status") == "breach":
            # Если SLO нарушен, считаем текущую скорость сжигания
            return compliance.get("error_budget_used", 0.0) / window_hours
        
        return 0.0

class ReliabilityDashboard:
    """Dashboard для мониторинга надежности"""
    
    def __init__(self, sli_tracker: SLITracker, slo_monitor: SLOMonitor):
        self.sli_tracker = sli_tracker
        self.slo_monitor = slo_monitor
    
    def generate_report(self) -> Dict:
        """Генерация отчета о надежности"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "slis": {},
            "slos": {},
            "alerts": []
        }
        
        # SLI данные
        for sli_name in self.sli_tracker.configs:
            report["slis"][sli_name] = {
                "current_value": self.sli_tracker.calculate_sli(sli_name),
                "1h_value": self.sli_tracker.calculate_sli(sli_name, 60),
                "24h_value": self.sli_tracker.calculate_sli(sli_name, 1440)
            }
        
        # SLO данные
        for slo_name in self.slo_monitor.slos:
            compliance = self.slo_monitor.check_slo_compliance(slo_name)
            burn_rate = self.slo_monitor.get_error_budget_burn_rate(slo_name)
            
            report["slos"][slo_name] = {
                **compliance,
                "error_budget_burn_rate": burn_rate
            }
            
            # Проверка алертов
            if compliance.get("status") == "breach":
                report["alerts"].append({
                    "type": "slo_breach",
                    "slo": slo_name,
                    "severity": "high",
                    "message": f"SLO {slo_name} breached: {compliance.get('current_sli', 0):.2f}% < {compliance.get('target_slo', 0):.2f}%"
                })
            
            # Алерт о быстром сжигании error budget
            error_budget_usage = compliance.get("error_budget_usage_percent", 0)
            if error_budget_usage > 50:
                report["alerts"].append({
                    "type": "error_budget_burn",
                    "slo": slo_name,
                    "severity": "medium",
                    "message": f"High error budget usage: {error_budget_usage:.1f}%"
                })
        
        return report

# Пример использования
def main():
    # Создаем трекер и монитор
    sli_tracker = SLITracker()
    slo_monitor = SLOMonitor(sli_tracker)
    dashboard = ReliabilityDashboard(sli_tracker, slo_monitor)
    
    # Регистрируем SLI
    sli_tracker.register_sli(SLIConfig(
        name="api_availability",
        metric_name="http_success_rate",
        good_threshold=200,  # HTTP status < 400
        bad_threshold=400
    ))
    
    sli_tracker.register_sli(SLIConfig(
        name="api_latency",
        metric_name="response_time_95p",
        is_latency_metric=True
    ))
    
    # Регистрируем SLO
    slo_monitor.register_slo(SLOConfig(
        name="api_availability_slo",
        sli_name="api_availability",
        target_percentage=99.9,
        window_days=30
    ))
    
    slo_monitor.register_slo(SLOConfig(
        name="api_latency_slo",
        sli_name="api_latency",
        target_percentage=95.0,  # 95% запросов < threshold
        window_days=30
    ))
    
    # Имитируем измерения
    import random
    for i in range(1000):
        # Availability measurements (HTTP status codes)
        status_code = 200 if random.random() > 0.005 else 500  # 99.5% success rate
        sli_tracker.record_measurement("api_availability", status_code)
        
        # Latency measurements (response time in ms)
        latency = random.lognormvariate(4.0, 0.5)  # ~55ms median, some outliers
        sli_tracker.record_measurement("api_latency", latency)
        
        time.sleep(0.001)  # Небольшая задержка
    
    # Генерируем отчет
    report = dashboard.generate_report()
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
```

---

## 🎯 Практические задания

### Задание 1: Профилирование и оптимизация

```python
# Задача: оптимизировать данную функцию
def slow_function(data_list):
    result = []
    for i in range(len(data_list)):
        for j in range(len(data_list)):
            if i != j and data_list[i] == data_list[j]:
                result.append(data_list[i])
    return list(set(result))

# Требования:
# 1. Провести профилирование
# 2. Определить узкие места
# 3. Реализовать оптимизированную версию
# 4. Сравнить производительность
```

### Задание 2: Кэширование

```python
# Задача: реализовать многоуровневое кэширование
class UserService:
    def get_user_by_id(self, user_id: int):
        # Медленный запрос к БД
        time.sleep(0.1)  
        return {"id": user_id, "name": f"User{user_id}"}
    
    def get_user_friends(self, user_id: int):
        # Очень медленный запрос
        time.sleep(0.5)  
        return [f"friend_{i}" for i in range(5)]

# Требования:
# 1. Добавить L1 кэш (in-memory)
# 2. Добавить L2 кэш (Redis)
# 3. Реализовать cache-aside pattern
# 4. Добавить TTL и инвалидацию
```

### Задание 3: Масштабирование

```python
# Задача: спроектировать архитектуру для масштабирования
class ChatService:
    def send_message(self, from_user: int, to_user: int, message: str):
        pass
    
    def get_chat_history(self, user1: int, user2: int):
        pass
    
    def get_user_chats(self, user_id: int):
        pass

# Требования:
# 1. Поддержка 1M+ пользователей
# 2. Горизонтальное масштабирование
# 3. Шардинг по пользователям
# 4. Load balancing стратегия
# 5. Кэширование популярных чатов
```

---

## 📚 Дополнительные ресурсы

### Книги
- **"Designing Data-Intensive Applications"** - Martin Kleppmann
- **"High Performance MySQL"** - Baron Schwartz
- **"Building Microservices"** - Sam Newman
- **"Site Reliability Engineering"** - Google SRE Team

### Инструменты
- **Профилирование:** JProfiler, py-spy, perf, Chrome DevTools
- **Мониторинг:** Prometheus, Grafana, ELK Stack, Jaeger
- **Кэширование:** Redis, Memcached, Hazelcast, Apache Ignite
- **Load Testing:** JMeter, Artillery, k6, Gatling

### Онлайн ресурсы
- High Scalability (highscalability.com)
- Engineering blogs: Netflix, Uber, Airbnb, GitHub
- SRE Resources (sre.google)
- Performance testing guides

---

## ✅ Чек-лист итогового результата

После изучения блока вы должны уметь:

**📊 Производительность:**
- [ ] Профилировать приложения и находить bottlenecks
- [ ] Выбирать правильные алгоритмы и структуры данных
- [ ] Оптимизировать memory usage и CPU utilization
- [ ] Измерять и анализировать метрики производительности

**💾 Кэширование:**
- [ ] Проектировать многоуровневые системы кэширования
- [ ] Выбирать подходящие cache patterns
- [ ] Реализовывать распределенное кэширование
- [ ] Управлять инвалидацией кэша

**⚡ Асинхронность:**
- [ ] Проектировать неблокирующие системы
- [ ] Использовать async/await patterns
- [ ] Управлять concurrency и parallelism
- [ ] Избегать race conditions и deadlocks

**📈 Масштабирование:**
- [ ] Выбирать между вертикальным и горизонтальным масштабированием
- [ ] Проектировать load balancing стратегии
- [ ] Реализовывать database sharding
- [ ] Понимать CAP теорему и consistency models

**📊 Большие данные:**
- [ ] Различать batch и stream processing
- [ ] Применять MapReduce парадигму
- [ ] Проектировать data pipelines
- [ ] Выбирать между Lambda и Kappa архитектурами

**🔍 Мониторинг:**
- [ ] Реализовывать метрики, логи и трейсы
- [ ] Проектировать observability систем
- [ ] Настраивать distributed tracing
- [ ] Определять и мониторить SLI/SLO/SLA

**Время изучения:** 5-6 недель при 15-20 часах в неделю  
**Итоговый проект:** Высокопроизводительное и масштабируемое приложение с полным мониторингом