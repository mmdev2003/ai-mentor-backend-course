# 🗄️ Блок 4: Кэширование баз данных

```
⏱️ Продолжительность: 2-3 недели
🎯 Цель: Оптимизировать работу с данными через эффективное кэширование
📊 Уровень: Средний → Продвинутый
```

---

## 📋 Содержание блока

```
┌─ Глава 1: Кэширование запросов ──────────────────┐
├─ Глава 2: In-memory базы данных ─────────────────┤  
├─ Глава 3: Стратегии работы с кэшем ──────────────┤
├─ Глава 4: Инвалидация и консистентность ─────────┤
└─ Практические задания + Проект ──────────────────┘
```

---

## 🎯 Введение в кэширование баз данных

### Зачем нужно кэширование БД?

```
Без кэша:                    С кэшем:
                            
App ──────┐                 App ──┐
          ├─ 500ms             ├─ 2ms (cache hit)
Database ─┘                      ├─ 500ms (cache miss)
                            Cache ┴─ Database
```

**Типичные проблемы без кэширования:**
- Высокая нагрузка на БД
- Медленные сложные запросы
- Повторные вычисления
- Неэффективное использование ресурсов

---

## 📚 Глава 1: Кэширование запросов

### 1.1 Query Result Кэширование

**Принцип работы:**
```
SELECT * FROM users WHERE age > 25
         ↓
┌─────────────────────┐
│    Query Cache      │
│ Key: hash(query)    │
│ Value: result_set   │
└─────────────────────┘
```

**Пример реализации на Python:**

```python
import hashlib
import json
from typing import Any, Optional

class QueryCache:
    def __init__(self):
        self.cache = {}
    
    def _generate_key(self, query: str, params: tuple = ()) -> str:
        """Генерируем уникальный ключ для запроса"""
        query_data = f"{query}:{params}"
        return hashlib.md5(query_data.encode()).hexdigest()
    
    def get(self, query: str, params: tuple = ()) -> Optional[Any]:
        """Получаем результат из кэша"""
        key = self._generate_key(query, params)
        return self.cache.get(key)
    
    def set(self, query: str, params: tuple, result: Any, ttl: int = 3600):
        """Сохраняем результат в кэш"""
        key = self._generate_key(query, params)
        self.cache[key] = {
            'result': result,
            'expires': time.time() + ttl
        }

# Использование
cache = QueryCache()
query = "SELECT * FROM products WHERE category = %s"
params = ('electronics',)

# Проверяем кэш
result = cache.get(query, params)
if result is None:
    # Выполняем запрос к БД
    result = database.execute(query, params)
    cache.set(query, params, result)
```

### 1.2 Prepared Statements Кэширование

**Схема кэширования подготовленных запросов:**

```
┌─────────────────────────────────────────────────┐
│                 Application                     │
├─────────────────────────────────────────────────┤
│  Prepared Statement Cache                       │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │ Query Plan  │  │ Query Plan  │  │ Query    │ │
│  │ Hash: abc   │  │ Hash: def   │  │ Plan...  │ │
│  └─────────────┘  └─────────────┘  └──────────┘ │
├─────────────────────────────────────────────────┤
│                  Database                       │
└─────────────────────────────────────────────────┘
```

### 1.3 ORM-уровень кэширование

**Пример с Django ORM:**

```python
from django.core.cache import cache
from django.db import models

class ProductManager(models.Manager):
    def get_by_category_cached(self, category):
        cache_key = f"products_category_{category}"
        products = cache.get(cache_key)
        
        if products is None:
            products = list(self.filter(category=category))
            cache.set(cache_key, products, timeout=3600)
        
        return products

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    objects = ProductManager()
```

---

## 🏪 Глава 2: In-memory базы данных

### 2.1 Redis: Мощный кэш с богатыми структурами данных

**Архитектура Redis:**

```
┌─────────────────────────────────────────────────┐
│                   Redis                         │
├─────────────────────────────────────────────────┤
│  Data Types:                                    │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ │
│  │ Strings │ │  Lists  │ │  Sets   │ │ Hashes │ │
│  └─────────┘ └─────────┘ └─────────┘ └────────┘ │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ │
│  │ Sorted  │ │ Bitmaps │ │ HyperLL │ │ Streams│ │
│  │  Sets   │ │         │ │   ogs   │ │        │ │
│  └─────────┘ └─────────┘ └─────────┘ └────────┘ │
├─────────────────────────────────────────────────┤
│  Persistence: RDB + AOF                         │
│  Replication: Master-Slave                      │
│  Clustering: Redis Cluster                      │
└─────────────────────────────────────────────────┘
```

**Практические примеры Redis:**

```python
import redis
import json
from datetime import datetime, timedelta

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 1. Кэширование пользовательских сессий
def cache_user_session(user_id: int, session_data: dict):
    key = f"user_session:{user_id}"
    r.hset(key, mapping=session_data)
    r.expire(key, 3600)  # TTL 1 час

# 2. Счетчики и статистика
def increment_page_views(page_id: str):
    key = f"page_views:{page_id}"
    r.incr(key)
    
    # Счетчик за день
    today = datetime.now().strftime("%Y-%m-%d")
    daily_key = f"page_views:{page_id}:{today}"
    r.incr(daily_key)
    r.expire(daily_key, 86400)  # TTL 24 часа

# 3. Leaderboard с Sorted Sets
def add_to_leaderboard(user_id: int, score: int):
    r.zadd("game_leaderboard", {f"user:{user_id}": score})

def get_top_players(limit: int = 10):
    return r.zrevrange("game_leaderboard", 0, limit-1, withscores=True)

# 4. Кэширование результатов API
def cache_api_response(endpoint: str, params: dict, response: dict):
    key = f"api_cache:{endpoint}:{hash(str(params))}"
    r.setex(key, 300, json.dumps(response))  # TTL 5 минут

def get_cached_api_response(endpoint: str, params: dict):
    key = f"api_cache:{endpoint}:{hash(str(params))}"
    cached = r.get(key)
    return json.loads(cached) if cached else None
```

### 2.2 Memcached: Простота и скорость

**Архитектура Memcached:**

```
┌─────────────────────────────────────────────────┐
│               Memcached Cluster                 │
├─────────────────────────────────────────────────┤
│  Node 1        Node 2        Node 3             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│  │  Slab   │   │  Slab   │   │  Slab   │        │
│  │ Class 1 │   │ Class 1 │   │ Class 1 │        │
│  └─────────┘   └─────────┘   └─────────┘        │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│  │  Slab   │   │  Slab   │   │  Slab   │        │
│  │ Class 2 │   │ Class 2 │   │ Class 2 │        │
│  └─────────┘   └─────────┘   └─────────┘        │
├─────────────────────────────────────────────────┤
│          Consistent Hashing                     │
└─────────────────────────────────────────────────┘
```

**Пример использования Memcached:**

```python
import memcache
import pickle

# Подключение к Memcached
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

class MemcachedCache:
    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:11211'])
    
    def get(self, key: str):
        return self.mc.get(key)
    
    def set(self, key: str, value, time: int = 3600):
        return self.mc.set(key, value, time)
    
    def delete(self, key: str):
        return self.mc.delete(key)
    
    def get_multi(self, keys: list):
        return self.mc.get_multi(keys)

# Использование для кэширования объектов
def get_user_profile(user_id: int):
    cache_key = f"user_profile:{user_id}"
    profile = mc.get(cache_key)
    
    if profile is None:
        # Загружаем из БД
        profile = database.get_user_profile(user_id)
        mc.set(cache_key, profile, time=3600)
    
    return profile
```

### 2.3 Сравнение Redis vs Memcached

```
┌─────────────────────┬──────────────────┬─────────────────┐
│     Характеристика  │      Redis       │   Memcached     │
├─────────────────────┼──────────────────┼─────────────────┤
│  Структуры данных   │   Богатые типы   │  Только K-V     │
│  Персистентность    │   RDB + AOF      │      Нет        │
│  Репликация         │      Есть        │      Нет        │
│  Кластеризация      │  Redis Cluster   │ Клиентская      │
│  Многопоточность    │ Однопоточная     │ Многопоточная   │
│  Производительность │    Высокая       │   Очень высокая │
│  Сложность          │    Средняя       │     Низкая      │
│  Функциональность   │    Богатая       │    Базовая      │
└─────────────────────┴──────────────────┴─────────────────┘
```

---

## 🔄 Глава 3: Стратегии работы с кэшем

### 3.1 Cache-aside (Lazy Loading)

**Схема работы:**

```
Application Request
        │
        ▼
┌───────────────┐    Cache Hit     ┌─────────────┐
│  Check Cache  │ ───────────────▶ │   Return    │
│               │                  │    Data     │
└───────────────┘                  └─────────────┘
        │
        │ Cache Miss
        ▼
┌───────────────┐                  ┌─────────────┐
│ Query Database│ ───────────────▶ │  Store in   │
│               │                  │    Cache    │
└───────────────┘                  └─────────────┘
        │
        ▼
┌───────────────┐
│  Return Data  │
└───────────────┘
```

**Реализация Cache-aside:**

```python
class CacheAsidePattern:
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database
    
    def get_user(self, user_id: int):
        # 1. Проверяем кэш
        cache_key = f"user:{user_id}"
        user = self.cache.get(cache_key)
        
        if user is not None:
            print("Cache HIT")
            return user
        
        # 2. Cache miss - идем в базу
        print("Cache MISS")
        user = self.database.get_user(user_id)
        
        if user is not None:
            # 3. Сохраняем в кэш
            self.cache.set(cache_key, user, ttl=3600)
        
        return user
    
    def update_user(self, user_id: int, user_data: dict):
        # 1. Обновляем в базе
        self.database.update_user(user_id, user_data)
        
        # 2. Инвалидируем кэш
        cache_key = f"user:{user_id}"
        self.cache.delete(cache_key)
```

### 3.2 Write-through кэширование

**Схема работы:**

```
Write Request
        │
        ▼
┌───────────────┐                  ┌─────────────┐
│  Update Cache │ ───────────────▶ │   Update    │
│               │                  │  Database   │
└───────────────┘                  └─────────────┘
        │                                  │
        └──────────── Both Success ────────┘
        │
        ▼
┌───────────────┐
│    Success    │
└───────────────┘
```

**Реализация Write-through:**

```python
class WriteThroughCache:
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database
    
    def get_product(self, product_id: int):
        cache_key = f"product:{product_id}"
        product = self.cache.get(cache_key)
        
        if product is None:
            product = self.database.get_product(product_id)
            if product:
                self.cache.set(cache_key, product)
        
        return product
    
    def update_product(self, product_id: int, product_data: dict):
        cache_key = f"product:{product_id}"
        
        try:
            # 1. Обновляем кэш
            self.cache.set(cache_key, product_data)
            
            # 2. Обновляем базу данных
            self.database.update_product(product_id, product_data)
            
            return True
        except Exception as e:
            # Откатываем изменения в кэше
            self.cache.delete(cache_key)
            raise e
```

### 3.3 Write-behind (Write-back)

**Схема работы:**

```
Write Request
        │
        ▼
┌───────────────┐                  ┌─────────────┐
│  Update Cache │                  │   Queue     │
│               │ ───────────────▶ │  Write Job  │
└───────────────┘                  └─────────────┘
        │                                  │
        ▼                                  │
┌───────────────┐              Async      │
│ Return Success│              Update     │
└───────────────┘                  │      │
                                   ▼      ▼
                           ┌─────────────────┐
                           │  Update Database│
                           └─────────────────┘
```

**Реализация Write-behind:**

```python
import queue
import threading
import time

class WriteBehindCache:
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database
        self.write_queue = queue.Queue()
        self.dirty_keys = set()
        
        # Запускаем фоновый процесс записи
        self.writer_thread = threading.Thread(target=self._background_writer)
        self.writer_thread.daemon = True
        self.writer_thread.start()
    
    def get(self, key: str):
        return self.cache.get(key)
    
    def set(self, key: str, value, write_to_db: bool = True):
        # 1. Записываем в кэш
        self.cache.set(key, value)
        
        if write_to_db:
            # 2. Добавляем в очередь на запись в БД
            self.write_queue.put((key, value))
            self.dirty_keys.add(key)
    
    def _background_writer(self):
        """Фоновый процесс записи в БД"""
        while True:
            try:
                # Забираем из очереди с таймаутом
                key, value = self.write_queue.get(timeout=1)
                
                # Записываем в БД
                self.database.set(key, value)
                
                # Убираем из dirty keys
                self.dirty_keys.discard(key)
                
                self.write_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error writing to database: {e}")
                # Можно добавить retry логику
```

### 3.4 Refresh-ahead

**Схема работы:**

```
Cache Entry Timeline:
│
├─ TTL: 60s ────┐
│               │
├─ Refresh: 50s │ ◄── Refresh-ahead trigger
│               │
├─ Expire: 60s ─┘
│
▼
Background refresh starts before expiration
```

**Реализация Refresh-ahead:**

```python
import time
import threading
from typing import Callable, Any

class RefreshAheadCache:
    def __init__(self, cache, refresh_function: Callable, 
                 ttl: int = 3600, refresh_ahead_factor: float = 0.8):
        self.cache = cache
        self.refresh_function = refresh_function
        self.ttl = ttl
        self.refresh_ahead_time = ttl * refresh_ahead_factor
        self.refresh_in_progress = set()
    
    def get(self, key: str):
        # Получаем данные с метаинформацией
        cached_data = self.cache.get(f"data:{key}")
        cached_time = self.cache.get(f"time:{key}")
        
        if cached_data is None:
            # Cache miss - загружаем синхронно
            return self._load_and_cache(key)
        
        # Проверяем, нужно ли обновить заранее
        if (cached_time and 
            time.time() - cached_time > self.refresh_ahead_time and
            key not in self.refresh_in_progress):
            
            # Запускаем асинхронное обновление
            threading.Thread(
                target=self._async_refresh, 
                args=(key,)
            ).start()
        
        return cached_data
    
    def _load_and_cache(self, key: str):
        """Загружает данные и кэширует их"""
        data = self.refresh_function(key)
        current_time = time.time()
        
        self.cache.set(f"data:{key}", data, ttl=self.ttl)
        self.cache.set(f"time:{key}", current_time, ttl=self.ttl)
        
        return data
    
    def _async_refresh(self, key: str):
        """Асинхронное обновление кэша"""
        if key in self.refresh_in_progress:
            return
        
        self.refresh_in_progress.add(key)
        try:
            self._load_and_cache(key)
        finally:
            self.refresh_in_progress.discard(key)
```

---

## ⚡ Глава 4: Инвалидация и консистентность

### 4.1 TTL (Time To Live) стратегии

**Типы TTL:**

```
Fixed TTL:
│────────────────│ 3600s
0               3600

Sliding TTL:
│──────│──────│──────│ Access extends TTL
0    Access  Access  New expiry

Hierarchical TTL:
Hot data:   │──│ 60s
Warm data:  │────────│ 300s  
Cold data:  │──────────────────│ 3600s
```

**Реализация умного TTL:**

```python
class SmartTTLCache:
    def __init__(self):
        self.cache = {}
        self.access_count = {}
        self.last_access = {}
    
    def get(self, key: str):
        if key in self.cache:
            # Обновляем статистику доступа
            self.access_count[key] = self.access_count.get(key, 0) + 1
            self.last_access[key] = time.time()
            
            return self.cache[key]['data']
        return None
    
    def set(self, key: str, value, base_ttl: int = 3600):
        # Вычисляем TTL на основе популярности
        access_frequency = self.access_count.get(key, 0)
        
        if access_frequency > 100:
            ttl = base_ttl * 2  # Горячие данные живут дольше
        elif access_frequency > 10:
            ttl = base_ttl
        else:
            ttl = base_ttl // 2  # Холодные данные - короче
        
        self.cache[key] = {
            'data': value,
            'expires': time.time() + ttl,
            'ttl': ttl
        }
    
    def cleanup_expired(self):
        """Удаляет просроченные записи"""
        current_time = time.time()
        expired_keys = [
            key for key, item in self.cache.items()
            if item['expires'] < current_time
        ]
        
        for key in expired_keys:
            del self.cache[key]
            self.access_count.pop(key, None)
            self.last_access.pop(key, None)
```

### 4.2 Event-driven инвалидация

**Архитектура событийной инвалидации:**

```
┌─────────────┐    Event    ┌──────────────┐    Invalidate    ┌─────────┐
│  Database   │ ─────────▶ │  Event Bus   │ ──────────────▶ │  Cache  │
│   Changes   │            │  (Redis Pub/ │                 │ Cluster │
└─────────────┘            │  Sub, Kafka) │                 └─────────┘
                           └──────────────┘
                                   │
                                   ▼
                           ┌──────────────┐
                           │  Cache Tags  │
                           │  Resolution  │
                           └──────────────┘
```

**Реализация событийной инвалидации:**

```python
import redis
import json
from typing import Set, List

class EventDrivenCache:
    def __init__(self, cache, redis_client):
        self.cache = cache
        self.redis = redis_client
        self.tag_mapping = {}  # key -> set of tags
        
        # Подписываемся на события инвалидации
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe('cache_invalidation')
        
        # Запускаем слушатель событий
        threading.Thread(target=self._listen_events, daemon=True).start()
    
    def set_with_tags(self, key: str, value, tags: Set[str], ttl: int = 3600):
        """Сохраняет значение с тегами"""
        self.cache.set(key, value, ttl)
        self.tag_mapping[key] = tags
        
        # Сохраняем обратное отображение тег -> ключи
        for tag in tags:
            tag_key = f"tag:{tag}"
            self.redis.sadd(tag_key, key)
            self.redis.expire(tag_key, ttl + 300)  # Чуть больше TTL кэша
    
    def invalidate_by_tag(self, tag: str):
        """Инвалидирует все ключи с данным тегом"""
        tag_key = f"tag:{tag}"
        keys_to_invalidate = self.redis.smembers(tag_key)
        
        for key in keys_to_invalidate:
            self.cache.delete(key.decode())
            # Удаляем из tag mapping
            if key.decode() in self.tag_mapping:
                del self.tag_mapping[key.decode()]
        
        # Удаляем сам тег
        self.redis.delete(tag_key)
    
    def publish_invalidation_event(self, tags: List[str]):
        """Публикует событие инвалидации"""
        event = {
            'type': 'invalidate',
            'tags': tags,
            'timestamp': time.time()
        }
        self.redis.publish('cache_invalidation', json.dumps(event))
    
    def _listen_events(self):
        """Слушает события инвалидации"""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                try:
                    event = json.loads(message['data'].decode())
                    if event['type'] == 'invalidate':
                        for tag in event['tags']:
                            self.invalidate_by_tag(tag)
                except Exception as e:
                    print(f"Error processing invalidation event: {e}")

# Пример использования
cache_system = EventDrivenCache(cache, redis_client)

# Кэшируем данные с тегами
cache_system.set_with_tags(
    "user:123", 
    {"id": 123, "name": "Alice"}, 
    tags={"user", "user:123", "profile"}
)

# При обновлении пользователя инвалидируем связанные кэши
def update_user(user_id: int, data: dict):
    database.update_user(user_id, data)
    cache_system.publish_invalidation_event([f"user:{user_id}", "user", "profile"])
```

### 4.3 Cache Warming

**Стратегии предзагрузки:**

```
Cold Start Problem:
Time │
     │     ┌─ High latency spikes
     │    ╱│
     │   ╱ │
     │  ╱  │
     └─╱───┴────────────────────────
       Cache deployment

With Cache Warming:
Time │
     │ ┌─ Smooth performance
     │ │
     │ │
     │ │
     └─┴────────────────────────────
       Pre-warmed cache
```

**Реализация Cache Warming:**

```python
import asyncio
import concurrent.futures
from typing import List, Callable

class CacheWarmer:
    def __init__(self, cache, data_loader: Callable):
        self.cache = cache
        self.data_loader = data_loader
    
    async def warm_cache_batch(self, keys: List[str], batch_size: int = 10):
        """Предзагружает кэш пакетами"""
        semaphore = asyncio.Semaphore(batch_size)
        
        async def warm_single_key(key: str):
            async with semaphore:
                try:
                    # Проверяем, нет ли уже в кэше
                    if self.cache.get(key) is None:
                        data = await self.data_loader(key)
                        if data is not None:
                            self.cache.set(key, data)
                            print(f"Warmed cache for key: {key}")
                except Exception as e:
                    print(f"Failed to warm cache for {key}: {e}")
        
        # Запускаем все задачи параллельно
        tasks = [warm_single_key(key) for key in keys]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def warm_popular_data(self):
        """Предзагружает популярные данные"""
        popular_keys = [
            "trending_products",
            "featured_categories", 
            "homepage_content",
            "popular_articles"
        ]
        
        asyncio.run(self.warm_cache_batch(popular_keys))
    
    def warm_user_specific_data(self, user_ids: List[int]):
        """Предзагружает пользовательские данные"""
        keys = [
            f"user_profile:{user_id}" for user_id in user_ids
        ] + [
            f"user_preferences:{user_id}" for user_id in user_ids
        ]
        
        asyncio.run(self.warm_cache_batch(keys))

# Scheduler для периодического warming
class CacheWarmingScheduler:
    def __init__(self, warmer: CacheWarmer):
        self.warmer = warmer
        self.running = False
    
    def start_periodic_warming(self, interval: int = 3600):
        """Запускает периодическое обновление кэша"""
        self.running = True
        
        def warming_loop():
            while self.running:
                try:
                    print("Starting cache warming...")
                    self.warmer.warm_popular_data()
                    print("Cache warming completed")
                except Exception as e:
                    print(f"Cache warming failed: {e}")
                
                time.sleep(interval)
        
        threading.Thread(target=warming_loop, daemon=True).start()
    
    def stop(self):
        self.running = False
```

### 4.4 Cache Stampede Protection

**Проблема Cache Stampede:**

```
Cache expires at T=0
│
├─ T=0: Request 1 ──┐
├─ T=1: Request 2 ──┤
├─ T=2: Request 3 ──┤ ◄── All hit database
├─ T=3: Request 4 ──┤      simultaneously
├─ T=4: Request 5 ──┘
│
▼ Database overload
```

**Решение с блокировками:**

```python
import threading
import time
from typing import Optional, Callable

class StampedeProtectedCache:
    def __init__(self, cache, data_loader: Callable):
        self.cache = cache
        self.data_loader = data_loader
        self.loading_locks = {}
        self.lock = threading.Lock()
    
    def get_with_stampede_protection(self, key: str, ttl: int = 3600) -> Optional[any]:
        """Получает данные с защитой от stampede"""
        
        # 1. Пытаемся получить из кэша
        value = self.cache.get(key)
        if value is not None:
            return value
        
        # 2. Cache miss - нужно загрузить данные
        # Проверяем, не загружает ли уже кто-то эти данные
        with self.lock:
            if key in self.loading_locks:
                loading_lock = self.loading_locks[key]
            else:
                loading_lock = threading.Lock()
                self.loading_locks[key] = loading_lock
        
        # 3. Пытаемся захватить блокировку загрузки
        if loading_lock.acquire(blocking=False):
            try:
                # Мы первые - загружаем данные
                print(f"Loading data for key: {key}")
                value = self.data_loader(key)
                
                if value is not None:
                    self.cache.set(key, value, ttl)
                
                return value
            finally:
                loading_lock.release()
                # Удаляем блокировку
                with self.lock:
                    if key in self.loading_locks:
                        del self.loading_locks[key]
        else:
            # Кто-то уже загружает - ждем
            print(f"Waiting for data loading: {key}")
            with loading_lock:
                # После получения блокировки данные должны быть в кэше
                return self.cache.get(key)

# Альтернативное решение с вероятностным обновлением
class ProbabilisticCache:
    def __init__(self, cache, data_loader: Callable):
        self.cache = cache
        self.data_loader = data_loader
    
    def get_with_probabilistic_refresh(self, key: str, ttl: int = 3600, 
                                     refresh_probability: float = 0.1):
        """Вероятностное обновление для предотвращения stampede"""
        
        cached_item = self.cache.get_with_metadata(key)
        
        if cached_item is None:
            # Cache miss - загружаем
            return self._load_and_cache(key, ttl)
        
        value, cache_time = cached_item['value'], cached_item['time']
        age = time.time() - cache_time
        
        # Вероятность обновления растет с возрастом записи
        if age > ttl * 0.8:  # После 80% TTL
            remaining_ttl = ttl - age
            probability = refresh_probability * (age / ttl)
            
            if random.random() < probability:
                # Обновляем асинхронно
                threading.Thread(
                    target=self._async_refresh,
                    args=(key, ttl)
                ).start()
        
        return value
    
    def _load_and_cache(self, key: str, ttl: int):
        value = self.data_loader(key)
        if value is not None:
            self.cache.set_with_metadata(key, value, ttl)
        return value
    
    def _async_refresh(self, key: str, ttl: int):
        try:
            self._load_and_cache(key, ttl)
        except Exception as e:
            print(f"Async refresh failed for {key}: {e}")
```

---

## 🛠️ Практические задания

### Задание 1: Создание системы кэширования для ORM

**Цель:** Реализовать middleware для автоматического кэширования ORM запросов

```python
# Ваша задача - дополнить этот класс
class ORMCacheMiddleware:
    def __init__(self, orm_session, cache_backend):
        self.orm = orm_session
        self.cache = cache_backend
    
    def execute_query(self, query_obj):
        """
        Задачи:
        1. Генерировать уникальный ключ кэша для запроса
        2. Проверять кэш перед выполнением запроса
        3. Кэшировать результаты с умным TTL
        4. Обрабатывать разные типы запросов (SELECT, COUNT, etc.)
        """
        pass
    
    def invalidate_model_cache(self, model_class, instance_id=None):
        """
        Задачи:
        1. Инвалидировать связанные кэши при изменении модели
        2. Поддерживать тегированную инвалидацию
        3. Обрабатывать связанные модели
        """
        pass

# Пример использования:
# cache_middleware = ORMCacheMiddleware(db_session, redis_cache)
# users = cache_middleware.execute_query(User.query.filter(User.active == True))
```

### Задание 2: Distributed Cache с Redis Cluster

**Цель:** Построить распределенный кэш с автоматическим шардированием

```python
class DistributedRedisCache:
    def __init__(self, redis_nodes):
        """
        Задачи:
        1. Реализовать консистентное хеширование
        2. Обеспечить отказоустойчивость
        3. Автоматическое переключение между узлами
        4. Мониторинг состояния кластера
        """
        self.nodes = redis_nodes
        
    def get(self, key: str):
        """Должен автоматически выбирать правильный узел"""
        pass
    
    def set(self, key: str, value, ttl: int = 3600):
        """Должен поддерживать репликацию"""
        pass
    
    def get_cluster_stats(self):
        """Статистика по всему кластеру"""
        pass
```

### Задание 3: Система автоматической инвалидации

**Цель:** Создать систему, которая автоматически инвалидирует кэш при изменении данных

```python
class AutoInvalidationSystem:
    def __init__(self, cache, database):
        """
        Задачи:
        1. Отслеживать изменения в БД
        2. Определять зависимости между данными
        3. Инвалидировать связанные кэши
        4. Поддерживать batch инвалидацию
        """
        pass
    
    def track_dependencies(self, cache_key: str, db_tables: List[str]):
        """Регистрирует зависимости кэша от таблиц БД"""
        pass
    
    def on_database_change(self, table: str, operation: str, record_id: int):
        """Обработчик изменений в БД"""
        pass
```

### Задание 4: Cache Performance Benchmark

**Цель:** Создать систему для тестирования производительности кэширования

```python
class CacheBenchmark:
    def __init__(self):
        """
        Задачи:
        1. Тестировать разные алгоритмы вытеснения
        2. Измерять hit rate, latency, throughput
        3. Генерировать разные паттерны доступа
        4. Создавать отчеты с визуализацией
        """
        pass
    
    def run_benchmark_suite(self, cache_implementations: List):
        """Запускает полный набор тестов"""
        pass
    
    def generate_access_patterns(self, pattern_type: str):
        """Генерирует паттерны доступа: random, sequential, hotspot"""
        pass
```

### Задание 5: Cache Warming System

**Цель:** Реализовать систему предзагрузки кэша

```python
class IntelligentCacheWarmer:
    def __init__(self, cache, analytics_db):
        """
        Задачи:
        1. Анализировать паттерны доступа
        2. Предсказывать популярные данные
        3. Планировать warming tasks
        4. Оптимизировать время обновления
        """
        pass
    
    def analyze_access_patterns(self, time_period: timedelta):
        """Анализ паттернов доступа за период"""
        pass
    
    def predict_hot_data(self):
        """Предсказание горячих данных"""
        pass
    
    def schedule_warming(self):
        """Планирование задач предзагрузки"""
        pass
```

---

## 📊 Критерии оценки практических заданий

```
┌─────────────────────┬──────────────────────────────────────────┐
│    Критерий         │              Описание                   │
├─────────────────────┼──────────────────────────────────────────┤
│ Корректность (30%)  │ Правильная реализация алгоритмов        │
│ Производительность  │ Эффективность и оптимизация             │
│ (25%)               │                                          │
│ Надежность (20%)    │ Обработка ошибок, отказоустойчивость    │
│ Архитектура (15%)   │ Качество дизайна, расширяемость         │
│ Документация (10%)  │ Комментарии, README, примеры            │
└─────────────────────┴──────────────────────────────────────────┘
```

---

## 🎯 Ожидаемые результаты блока

После завершения этого блока вы будете уметь:

✅ **Проектировать кэширующие системы для БД** любого уровня сложности  
✅ **Выбирать оптимальные стратегии** кэширования для конкретных задач  
✅ **Реализовывать распределенное кэширование** с Redis/Memcached  
✅ **Решать проблемы консистентности** и инвалидации данных  
✅ **Оптимизировать производительность** приложений через кэширование  
✅ **Мониторить и отлаживать** кэширующие системы  
✅ **Интегрировать кэширование** с современными ORM и фреймворками  

---

## 📚 Дополнительные материалы

### Рекомендуемое чтение:
- **"Redis in Action"** - Josiah Carlson
- **"Designing Data-Intensive Applications"** - Martin Kleppmann  
- **"Database Internals"** - Alex Petrov

### Полезные ресурсы:
- [Redis Documentation](https://redis.io/documentation)
- [Memcached Wiki](https://github.com/memcached/memcached/wiki)
- [Database Caching Strategies](https://aws.amazon.com/caching/database-caching/)

### Инструменты для практики:
- **Redis** - для экспериментов с in-memory кэшированием
- **Memcached** - для изучения простого K-V кэширования  
- **Apache JMeter** - для нагрузочного тестирования
- **Grafana + Prometheus** - для мониторинга производительности

---

**Следующий блок:** 🔄 Распределенное кэширование → Переход к масштабируемым решениям

---

*Этот материал создан для глубокого изучения кэширования баз данных. Практикуйтесь с реальными проектами и не бойтесь экспериментировать!*