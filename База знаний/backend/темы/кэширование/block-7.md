# Блок 7: Кэширование в современной архитектуре

**⏱️ Продолжительность:** 2-3 недели  
**🎯 Цель:** Применить кэширование в актуальных технологиях и архитектурных паттернах

---

## 🏗️ Глава 1: Кэширование в микросервисах

### 1.1 Введение в микросервисную архитектуру

Микросервисная архитектура представляет уникальные вызовы для кэширования:

```
Монолитная архитектура vs Микросервисная архитектура

МОНОЛИТ                          МИКРОСЕРВИСЫ
┌─────────────────────┐          ┌─────────┐ ┌─────────┐ ┌─────────┐
│                     │          │Service A│ │Service B│ │Service C│
│   Single Cache      │          │   ┌─┐   │ │   ┌─┐   │ │   ┌─┐   │
│   ┌─────────────┐   │          │   │C│   │ │   │C│   │ │   │C│   │
│   │             │   │    vs    │   └─┘   │ │   └─┘   │ │   └─┘   │
│   │    Cache    │   │          └─────────┘ └─────────┘ └─────────┘
│   │             │   │                 │         │         │
│   └─────────────┘   │                 └─────────┼─────────┘
│                     │                           │
└─────────────────────┘                  ┌─────────────┐
                                         │Distributed  │
                                         │   Cache     │
                                         └─────────────┘
```

### 1.2 Проблемы кэширования в микросервисах

#### 🔴 Основные проблемы:

1. **Дублирование данных** - каждый сервис может кэшировать одни и те же данные
2. **Консистентность** - сложность поддержания согласованности между сервисами
3. **Инвалидация** - как уведомить все сервисы об изменении данных?
4. **Сетевые задержки** - дополнительные запросы к распределенному кэшу

#### 🟢 Решения:

```
Паттерн: Cache-per-Service
─────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway                              │
│                   ┌─────────┐                              │
│                   │  Cache  │                              │
│                   └─────────┘                              │
└─────────────────────┬───────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
  ┌──────▼──┐  ┌──────▼──┐  ┌──────▼──┐
  │Service A│  │Service B│  │Service C│
  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │
  │ │Cache│ │  │ │Cache│ │  │ │Cache│ │
  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │
  └─────────┘  └─────────┘  └─────────┘
```

### 1.3 Distributed Caching Patterns для микросервисов

#### Паттерн 1: Shared Nothing Cache

```javascript
// Каждый сервис управляет своим кэшем
class UserService {
  constructor() {
    this.cache = new Map();
  }
  
  async getUser(id) {
    // Проверяем локальный кэш
    if (this.cache.has(id)) {
      return this.cache.get(id);
    }
    
    // Загружаем из базы данных
    const user = await this.db.getUser(id);
    
    // Кэшируем на 10 минут
    this.cache.set(id, user);
    setTimeout(() => this.cache.delete(id), 600000);
    
    return user;
  }
}
```

#### Паттерн 2: Shared Cache Pool

```javascript
// Общий кэш для всех сервисов
class DistributedCacheService {
  constructor(redisCluster) {
    this.redis = redisCluster;
  }
  
  async get(key, serviceName) {
    const namespacedKey = `${serviceName}:${key}`;
    return await this.redis.get(namespacedKey);
  }
  
  async set(key, value, serviceName, ttl = 3600) {
    const namespacedKey = `${serviceName}:${key}`;
    return await this.redis.setex(namespacedKey, ttl, JSON.stringify(value));
  }
}
```

#### Паттерн 3: Cache Aside with Event Sourcing

```
Event-Driven Cache Invalidation
─────────────────────────────────────────────────────────────────

┌─────────────┐    Event     ┌─────────────────┐
│  Service A  │─────────────▶│  Event Bus      │
│             │              │ (Kafka/RabbitMQ)│
└─────────────┘              └─────────────────┘
                                      │
                     ┌────────────────┼────────────────┐
                     │                │                │
              ┌──────▼──┐      ┌──────▼──┐      ┌──────▼──┐
              │Service B│      │Service C│      │Service D│
              │ Cache   │      │ Cache   │      │ Cache   │
              │Invalidate│      │Invalidate│      │Invalidate│
              └─────────┘      └─────────┘      └─────────┘
```

### 1.4 API Gateway кэширование

API Gateway может служить централизованной точкой кэширования:

```yaml
# Kong Gateway конфигурация
services:
  - name: user-service
    url: http://user-service:8080
    plugins:
      - name: proxy-cache
        config:
          response_code: [200, 301, 404]
          request_method: [GET, HEAD]
          content_type: [application/json]
          cache_ttl: 300
          strategy: memory
```

```javascript
// Кастомный middleware для Express Gateway
module.exports = {
  name: 'smart-cache',
  policy: (req, res, next) => {
    const cacheKey = `${req.method}:${req.path}:${JSON.stringify(req.query)}`;
    
    // Проверяем кэш
    cache.get(cacheKey, (err, result) => {
      if (result) {
        return res.json(JSON.parse(result));
      }
      
      // Перехватываем ответ
      const originalSend = res.send;
      res.send = function(data) {
        // Кэшируем только успешные ответы
        if (res.statusCode === 200) {
          cache.setex(cacheKey, 300, data);
        }
        originalSend.call(this, data);
      };
      
      next();
    });
  }
};
```

### 1.5 Service Mesh и кэширование

Service Mesh (Istio, Linkerd) предоставляет возможности кэширования на уровне сети:

```yaml
# Istio VirtualService с кэшированием
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
  - user-service
  http:
  - match:
    - uri:
        prefix: /api/users
    route:
    - destination:
        host: user-service
    headers:
      response:
        set:
          Cache-Control: "max-age=300"
```

```
Service Mesh Caching Architecture
─────────────────────────────────────────────────────────────────

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │    │   Client    │    │   Client    │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                  ┌───────▼───────┐
                  │  Istio Proxy  │
                  │  (with cache) │
                  └───────┬───────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
        ┌─────▼─────┐┌─────▼─────┐┌─────▼─────┐
        │Service A  ││Service B  ││Service C  │
        │           ││           ││           │
        └───────────┘└───────────┘└───────────┘
```

---

## ☁️ Глава 2: Облачное кэширование

### 2.1 AWS ElastiCache

#### Конфигурация Redis Cluster:

```yaml
# CloudFormation template
Resources:
  CacheCluster:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      ReplicationGroupId: !Sub "${AWS::StackName}-redis"
      Description: "Redis cluster for caching"
      NumCacheClusters: 3
      Engine: redis
      CacheNodeType: cache.r6g.large
      CacheParameterGroupName: !Ref CacheParameterGroup
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      SecurityGroupIds:
        - !Ref CacheSecurityGroup
      AutomaticFailoverEnabled: true
      MultiAZEnabled: true
      
  CacheParameterGroup:
    Type: AWS::ElastiCache::ParameterGroup
    Properties:
      CacheParameterGroupFamily: redis7.x
      Description: "Custom Redis parameters"
      Properties:
        maxmemory-policy: allkeys-lru
        timeout: 300
```

#### Использование в приложении:

```javascript
const redis = require('redis');
const cluster = require('cluster');

class AWSCacheService {
  constructor() {
    this.client = redis.createClient({
      host: process.env.REDIS_ENDPOINT,
      port: 6379,
      retry_strategy: (options) => {
        if (options.error && options.error.code === 'ECONNREFUSED') {
          return new Error('Redis server refused connection');
        }
        if (options.total_retry_time > 1000 * 60 * 60) {
          return new Error('Retry time exhausted');
        }
        return Math.min(options.attempt * 100, 3000);
      }
    });
  }
  
  async get(key) {
    try {
      const value = await this.client.get(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    }
  }
  
  async set(key, value, ttl = 3600) {
    try {
      await this.client.setex(key, ttl, JSON.stringify(value));
    } catch (error) {
      console.error('Cache set error:', error);
    }
  }
}
```

### 2.2 Azure Cache for Redis

```csharp
// C# implementation
using Microsoft.Extensions.Caching.StackExchangeRedis;

public class AzureCacheService
{
    private readonly IDatabase _database;
    
    public AzureCacheService(IConnectionMultiplexer redis)
    {
        _database = redis.GetDatabase();
    }
    
    public async Task<T> GetAsync<T>(string key)
    {
        var value = await _database.StringGetAsync(key);
        return value.HasValue ? JsonSerializer.Deserialize<T>(value) : default(T);
    }
    
    public async Task SetAsync<T>(string key, T value, TimeSpan? expiry = null)
    {
        var serialized = JsonSerializer.Serialize(value);
        await _database.StringSetAsync(key, serialized, expiry);
    }
}
```

### 2.3 Google Cloud Memorystore

```python
# Python implementation
import redis
from google.cloud import logging
import json

class GCPCacheService:
    def __init__(self, host, port=6379):
        self.client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
            health_check_interval=30
        )
        self.logger = logging.Client().logger('cache-service')
    
    def get(self, key):
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            self.logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key, value, ttl=3600):
        try:
            serialized = json.dumps(value)
            self.client.setex(key, ttl, serialized)
        except Exception as e:
            self.logger.error(f"Cache set error: {e}")
```

### 2.4 Serverless кэширование стратегии

#### AWS Lambda с ElastiCache:

```javascript
// Lambda function с подключением к ElastiCache
const redis = require('redis');

let client;

exports.handler = async (event) => {
  // Переиспользуем соединение между вызовами
  if (!client) {
    client = redis.createClient({
      host: process.env.REDIS_ENDPOINT,
      port: 6379
    });
  }
  
  const cacheKey = `user:${event.userId}`;
  
  // Проверяем кэш
  const cached = await client.get(cacheKey);
  if (cached) {
    return {
      statusCode: 200,
      body: JSON.stringify({
        data: JSON.parse(cached),
        source: 'cache'
      })
    };
  }
  
  // Загружаем данные
  const userData = await fetchUserData(event.userId);
  
  // Кэшируем на 5 минут
  await client.setex(cacheKey, 300, JSON.stringify(userData));
  
  return {
    statusCode: 200,
    body: JSON.stringify({
      data: userData,
      source: 'database'
    })
  };
};
```

#### Edge кэширование с CloudFlare Workers:

```javascript
// CloudFlare Worker для edge кэширования
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const cacheKey = new Request(request.url, request);
  const cache = caches.default;
  
  // Проверяем edge кэш
  let response = await cache.match(cacheKey);
  
  if (!response) {
    // Делаем запрос к origin
    response = await fetch(request);
    
    // Кэшируем на edge на 1 час
    if (response.status === 200) {
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'public, max-age=3600');
      
      response = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: headers
      });
      
      event.waitUntil(cache.put(cacheKey, response.clone()));
    }
  }
  
  return response;
}
```

### 2.5 Auto-scaling для кэширующих систем

#### AWS Auto Scaling Group для Redis:

```yaml
# Auto Scaling конфигурация
Resources:
  CacheAutoScalingGroup:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 10
      MinCapacity: 2
      ResourceId: !Sub "replication-group/${CacheReplicationGroup}"
      RoleARN: !GetAtt ApplicationAutoScalingRole.Arn
      ScalableDimension: elasticache:replication-group:NodeGroups
      ServiceNamespace: elasticache
      
  CacheScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: CPUScalingPolicy
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref CacheAutoScalingGroup
      TargetTrackingScalingPolicyConfiguration:
        TargetValue: 70.0
        PredefinedMetricSpecification:
          PredefinedMetricType: ElastiCachePrimaryCPUUtilization
```

---

## 🤖 Глава 3: AI/ML кэширование

### 3.1 Кэширование предобученных моделей

#### Model Caching Pipeline:

```
ML Model Caching Architecture
─────────────────────────────────────────────────────────────────

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Model Store   │    │   Model Cache   │    │   Inference     │
│   (S3/GCS)      │    │   (Redis/Mem)   │    │   Service       │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │        Load Model    │         Get Model    │
          │◄─────────────────────┼──────────────────────┤
          │                      │                      │
          │                      │◄─────────────────────┤
          │                      │      Cache Miss      │
          │                      │                      │
          │                      │      Load Model      │
          │──────────────────────┼─────────────────────▶│
          │                      │                      │
          │                      │      Cache Hit       │
          │                      │─────────────────────▶│
```

#### Реализация:

```python
import pickle
import redis
import hashlib
from typing import Optional, Any
import numpy as np
from sklearn.base import BaseEstimator

class MLModelCache:
    def __init__(self, redis_client: redis.Redis, ttl: int = 3600):
        self.redis = redis_client
        self.ttl = ttl
    
    def _get_model_key(self, model_id: str, version: str) -> str:
        return f"model:{model_id}:{version}"
    
    def _get_prediction_key(self, model_key: str, input_hash: str) -> str:
        return f"prediction:{model_key}:{input_hash}"
    
    def _hash_input(self, input_data: np.ndarray) -> str:
        return hashlib.sha256(input_data.tobytes()).hexdigest()
    
    def cache_model(self, model_id: str, version: str, model: BaseEstimator):
        """Кэширование модели"""
        key = self._get_model_key(model_id, version)
        serialized_model = pickle.dumps(model)
        self.redis.setex(key, self.ttl, serialized_model)
    
    def get_model(self, model_id: str, version: str) -> Optional[BaseEstimator]:
        """Получение модели из кэша"""
        key = self._get_model_key(model_id, version)
        serialized_model = self.redis.get(key)
        
        if serialized_model:
            return pickle.loads(serialized_model)
        return None
    
    def cache_prediction(self, model_id: str, version: str, 
                        input_data: np.ndarray, prediction: Any):
        """Кэширование результата предсказания"""
        model_key = self._get_model_key(model_id, version)
        input_hash = self._hash_input(input_data)
        prediction_key = self._get_prediction_key(model_key, input_hash)
        
        self.redis.setex(prediction_key, self.ttl, pickle.dumps(prediction))
    
    def get_prediction(self, model_id: str, version: str, 
                      input_data: np.ndarray) -> Optional[Any]:
        """Получение кэшированного предсказания"""
        model_key = self._get_model_key(model_id, version)
        input_hash = self._hash_input(input_data)
        prediction_key = self._get_prediction_key(model_key, input_hash)
        
        cached_prediction = self.redis.get(prediction_key)
        if cached_prediction:
            return pickle.loads(cached_prediction)
        return None

# Использование
cache = MLModelCache(redis.Redis(host='localhost', port=6379))

# Кэшируем модель
model = load_trained_model()
cache.cache_model('sentiment_analysis', 'v1.0', model)

# Используем кэшированную модель
cached_model = cache.get_model('sentiment_analysis', 'v1.0')
if cached_model:
    prediction = cached_model.predict(input_data)
    cache.cache_prediction('sentiment_analysis', 'v1.0', input_data, prediction)
```

### 3.2 Feature Store как кэш

```python
class FeatureStore:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def get_features(self, entity_id: str, feature_groups: list) -> dict:
        """Получение фичей для сущности"""
        pipeline = self.redis.pipeline()
        
        for group in feature_groups:
            key = f"features:{group}:{entity_id}"
            pipeline.hgetall(key)
        
        results = pipeline.execute()
        
        features = {}
        for i, group in enumerate(feature_groups):
            if results[i]:
                features[group] = {
                    k.decode(): float(v.decode()) 
                    for k, v in results[i].items()
                }
        
        return features
    
    def set_features(self, entity_id: str, feature_group: str, 
                    features: dict, ttl: int = 3600):
        """Кэширование фичей"""
        key = f"features:{feature_group}:{entity_id}"
        
        # Конвертируем все значения в строки
        string_features = {k: str(v) for k, v in features.items()}
        
        self.redis.hmset(key, string_features)
        self.redis.expire(key, ttl)
    
    def compute_and_cache_features(self, entity_id: str, 
                                  feature_group: str) -> dict:
        """Вычисление и кэширование фичей"""
        # Проверяем кэш
        cached_features = self.get_features(entity_id, [feature_group])
        if cached_features.get(feature_group):
            return cached_features[feature_group]
        
        # Вычисляем фичи
        features = self._compute_features(entity_id, feature_group)
        
        # Кэшируем
        self.set_features(entity_id, feature_group, features)
        
        return features
    
    def _compute_features(self, entity_id: str, feature_group: str) -> dict:
        """Вычисление фичей (заглушка)"""
        # Здесь была бы логика вычисления фичей
        return {
            'feature_1': 0.5,
            'feature_2': 1.2,
            'feature_3': -0.8
        }
```

### 3.3 Кэширование результатов inference

```python
import asyncio
import aioredis
from typing import List, Dict, Any

class InferenceCache:
    def __init__(self, redis_url: str):
        self.redis = None
    
    async def init_redis(self):
        self.redis = await aioredis.from_url(redis_url)
    
    async def batch_inference(self, model_name: str, inputs: List[np.ndarray]) -> List[Any]:
        """Батчевый inference с кэшированием"""
        if not self.redis:
            await self.init_redis()
        
        # Создаем ключи для всех входов
        cache_keys = [
            f"inference:{model_name}:{self._hash_input(inp)}" 
            for inp in inputs
        ]
        
        # Проверяем кэш батчем
        cached_results = await self.redis.mget(*cache_keys)
        
        # Определяем, какие результаты нужно вычислить
        to_compute = []
        results = [None] * len(inputs)
        
        for i, cached in enumerate(cached_results):
            if cached:
                results[i] = pickle.loads(cached)
            else:
                to_compute.append((i, inputs[i]))
        
        # Вычисляем недостающие результаты
        if to_compute:
            indices, inputs_to_compute = zip(*to_compute)
            computed_results = await self._run_inference(model_name, inputs_to_compute)
            
            # Кэшируем новые результаты
            cache_pipeline = self.redis.pipeline()
            for idx, result in zip(indices, computed_results):
                results[idx] = result
                cache_key = cache_keys[idx]
                cache_pipeline.setex(cache_key, 3600, pickle.dumps(result))
            
            await cache_pipeline.execute()
        
        return results
    
    async def _run_inference(self, model_name: str, inputs: List[np.ndarray]) -> List[Any]:
        """Запуск inference (заглушка)"""
        # Здесь была бы логика запуска модели
        await asyncio.sleep(0.1)  # Симулируем время inference
        return [f"result_for_{i}" for i in range(len(inputs))]
    
    def _hash_input(self, input_data: np.ndarray) -> str:
        return hashlib.sha256(input_data.tobytes()).hexdigest()[:16]
```

---

## 🔄 Глава 4: Real-time и streaming системы

### 4.1 Кэширование в Apache Kafka

#### Kafka Streams с кэшированием:

```java
// Java implementation для Kafka Streams
public class CachedStreamProcessor {
    private final ReadOnlyKeyValueStore<String, String> store;
    private final Duration cacheTtl = Duration.ofMinutes(5);
    
    public void processStream(KStream<String, String> input) {
        input
            .transformValues(() -> new ValueTransformerWithKey<String, String, String>() {
                private KeyValueStore<String, CachedValue> cache;
                
                @Override
                public void init(ProcessorContext context) {
                    this.cache = context.getStateStore("cache-store");
                }
                
                @Override
                public String transform(String key, String value) {
                    // Проверяем кэш
                    CachedValue cached = cache.get(key);
                    if (cached != null && !cached.isExpired()) {
                        return cached.getValue();
                    }
                    
                    // Обрабатываем значение
                    String processed = processValue(value);
                    
                    // Кэшируем результат
                    cache.put(key, new CachedValue(processed, System.currentTimeMillis()));
                    
                    return processed;
                }
            }, "cache-store")
            .to("output-topic");
    }
    
    private String processValue(String value) {
        // Логика обработки
        return value.toUpperCase();
    }
    
    private static class CachedValue {
        private final String value;
        private final long timestamp;
        
        public CachedValue(String value, long timestamp) {
            this.value = value;
            this.timestamp = timestamp;
        }
        
        public boolean isExpired() {
            return System.currentTimeMillis() - timestamp > 300000; // 5 минут
        }
        
        public String getValue() {
            return value;
        }
    }
}
```

#### Kafka Connect с кэшированием:

```json
{
  "name": "cached-jdbc-source",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:postgresql://localhost:5432/mydb",
    "mode": "incrementing",
    "incrementing.column.name": "id",
    "topic.prefix": "cached-",
    "transforms": "Cache",
    "transforms.Cache.type": "org.apache.kafka.connect.transforms.Cache",
    "transforms.Cache.cache.size": "10000",
    "transforms.Cache.ttl.ms": "300000"
  }
}
```

### 4.2 Stream Processing кэширование

#### Apache Flink с кэшированием:

```scala
// Scala implementation для Flink
import org.apache.flink.streaming.api.scala._
import org.apache.flink.util.Collector

class CachedProcessFunction extends ProcessFunction[String, String] {
  private var cache: ValueState[CachedResult] = _
  
  override def open(parameters: Configuration): Unit = {
    val cacheDescriptor = new ValueStateDescriptor[CachedResult](
      "cache", 
      createTypeInformation[CachedResult]
    )
    cache = getRuntimeContext.getState(cacheDescriptor)
  }
  
  override def processElement(
    value: String,
    ctx: ProcessFunction[String, String]#Context,
    out: Collector[String]
  ): Unit = {
    val currentTime = ctx.timestamp()
    val cached = cache.value()
    
    // Проверяем кэш
    if (cached != null && !cached.isExpired(currentTime)) {
      out.collect(cached.result)
      return
    }
    
    // Обрабатываем значение
    val processed = expensiveOperation(value)
    
    // Кэшируем результат
    cache.update(CachedResult(processed, currentTime))
    
    // Регистрируем таймер для очистки кэша
    ctx.timerService().registerProcessingTimeTimer(currentTime + 300000) // 5 минут
    
    out.collect(processed)
  }
  
  override def onTimer(
    timestamp: Long,
    ctx: ProcessFunction[String, String]#OnTimerContext,
    out: Collector[String]
  ): Unit = {
    // Очищаем кэш по таймеру
    cache.clear()
  }
  
  private def expensiveOperation(value: String): String = {
    // Дорогая операция
    Thread.sleep(100)
    value.reverse
  }
}

case class CachedResult(result: String, timestamp: Long) {
  def isExpired(currentTime: Long): Boolean = {
    currentTime - timestamp > 300000 // 5 минут
  }
}
```

### 4.3 Event Sourcing и кэширование

```python
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio

@dataclass
class Event:
    id: str
    type: str
    data: Dict[str, Any]
    timestamp: datetime
    version: int

class EventStore:
    def __init__(self):
        self.events: List[Event] = []
        self.snapshots: Dict[str, Any] = {}
    
    async def append_event(self, event: Event):
        self.events.append(event)
        await self._invalidate_cache(event)
    
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[Event]:
        return [e for e in self.events 
                if e.id == aggregate_id and e.version > from_version]
    
    async def _invalidate_cache(self, event: Event):
        # Инвалидируем кэш для агрегата
        if event.id in self.snapshots:
            del self.snapshots[event.id]

class CachedAggregateRepository:
    def __init__(self, event_store: EventStore, cache_ttl: int = 300):
        self.event_store = event_store
        self.cache: Dict[str, tuple] = {}  # (aggregate, timestamp)
        self.cache_ttl = cache_ttl
    
    async def get_aggregate(self, aggregate_id: str) -> Any:
        # Проверяем кэш
        if aggregate_id in self.cache:
            aggregate, timestamp = self.cache[aggregate_id]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                return aggregate
        
        # Загружаем из event store
        events = await self.event_store.get_events(aggregate_id)
        aggregate = self._build_aggregate_from_events(events)
        
        # Кэшируем
        self.cache[aggregate_id] = (aggregate, datetime.now())
        
        return aggregate
    
    def _build_aggregate_from_events(self, events: List[Event]) -> Any:
        # Восстанавливаем состояние агрегата из событий
        aggregate = {}
        for event in events:
            aggregate = self._apply_event(aggregate, event)
        return aggregate
    
    def _apply_event(self, aggregate: Dict, event: Event) -> Dict:
        # Применяем событие к агрегату
        if event.type == "UserCreated":
            aggregate.update(event.data)
        elif event.type == "UserUpdated":
            aggregate.update(event.data)
        return aggregate
```

---

## 🛠️ Практические задания

### Задание 1: Кэширующий слой для микросервисов

Создайте кэширующий слой для микросервисной архитектуры:

```javascript
// Стартовый код для задания
class MicroserviceCacheLayer {
  constructor(redisClient, eventBus) {
    this.redis = redisClient;
    this.eventBus = eventBus;
    this.setupEventHandlers();
  }
  
  setupEventHandlers() {
    // TODO: Настройте обработчики событий для инвалидации кэша
  }
  
  async cacheWithTags(key, value, tags = [], ttl = 3600) {
    // TODO: Реализуйте кэширование с тегами
  }
  
  async invalidateByTag(tag) {
    // TODO: Реализуйте инвалидацию по тегу
  }
  
  async distributedLock(key, ttl = 30) {
    // TODO: Реализуйте распределенную блокировку
  }
}

// Требования:
// 1. Поддержка тегированного кэширования
// 2. Event-driven инвалидация
// 3. Распределенные блокировки
// 4. Метрики и мониторинг
```

### Задание 2: Serverless кэширование

Реализуйте кэширование для serverless функций:

```python
# Стартовый код для задания
import json
import boto3
from datetime import datetime, timedelta

class ServerlessCacheService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.cache_table = self.dynamodb.Table('cache-table')
    
    async def get_with_fallback(self, key, fallback_func, ttl=300):
        # TODO: Реализуйте получение из кэша с fallback
        pass
    
    async def warm_cache(self, keys_and_functions):
        # TODO: Реализуйте предварительный прогрев кэша
        pass
    
    async def batch_invalidate(self, pattern):
        # TODO: Реализуйте батчевую инвалидацию
        pass

# Требования:
# 1. Использование DynamoDB как кэш
# 2. Автоматический прогрев кэша
# 3. Batch операции
# 4. Поддержка различных TTL стратегий
```

### Задание 3: ML Pipeline кэширование

Создайте систему кэширования для ML pipeline:

```python
# Стартовый код для задания
class MLPipelineCache:
    def __init__(self, redis_client, model_store):
        self.redis = redis_client
        self.model_store = model_store
    
    async def cached_inference(self, model_id, version, input_data):
        # TODO: Реализуйте кэшированный inference
        pass
    
    async def cache_model_artifacts(self, model_id, version, artifacts):
        # TODO: Реализуйте кэширование артефактов модели
        pass
    
    async def feature_cache_pipeline(self, entity_ids, feature_groups):
        # TODO: Реализуйте пайплайн кэширования фичей
        pass

# Требования:
# 1. Кэширование результатов inference
# 2. Кэширование артефактов моделей
# 3. Feature store integration
# 4. Batch processing поддержка
```

---

## 📊 Контрольные вопросы

1. **Архитектурные решения:**
   - Какие паттерны кэширования лучше подходят для микросервисов?
   - Как обеспечить консистентность кэша в распределенной системе?

2. **Облачное кэширование:**
   - В чем преимущества и недостатки различных облачных решений?
   - Как настроить автоматическое масштабирование кэша?

3. **AI/ML кэширование:**
   - Какие специфические проблемы решает кэширование в ML?
   - Как кэшировать результаты для батчевого inference?

4. **Streaming системы:**
   - Как кэширование интегрируется с обработкой потоков?
   - Какие метрики важны для stream processing кэшей?

---

## 🎯 Результаты обучения

После изучения этого блока вы будете уметь:
- ✅ Проектировать кэширование для микросервисных архитектур
- ✅ Использовать облачные решения для кэширования
- ✅ Настраивать автоматическое масштабирование кэшей
- ✅ Реализовывать кэширование для AI/ML систем
- ✅ Интегрировать кэширование с streaming обработкой
- ✅ Выбирать оптимальные решения для современных архитектур

---

## 📚 Дополнительные материалы

### Полезные ссылки:
- [AWS ElastiCache Best Practices](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/BestPractices.html)
- [Google Cloud Memorystore](https://cloud.google.com/memorystore)
- [Azure Cache for Redis](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/)
- [Istio Traffic Management](https://istio.io/latest/docs/concepts/traffic-management/)

### Инструменты:
- **Облачные кэши:** AWS ElastiCache, Azure Cache, GCP Memorystore
- **Service Mesh:** Istio, Linkerd, Consul Connect
- **Streaming:** Apache Kafka, Apache Flink, Apache Pulsar
- **Мониторинг:** Prometheus, Grafana, DataDog

### Проекты для изучения:
- [Netflix Zuul](https://github.com/Netflix/zuul) - API Gateway с кэшированием
- [Envoy Proxy](https://github.com/envoyproxy/envoy) - Proxy с возможностями кэширования
- [Apache Kafka Streams](https://github.com/apache/kafka) - Stream processing с кэшированием