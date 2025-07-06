# Блок 3: Кэширование в веб-разработке

**⏱️ Продолжительность:** 2-3 недели  
**🎯 Цель:** Освоить все аспекты кэширования в веб-приложениях

---

## 🌐 Глава 1: Браузерное кэширование

### Что такое браузерное кэширование?

Браузерное кэширование — это механизм временного хранения веб-ресурсов (HTML, CSS, JS, изображения) в локальном хранилище браузера пользователя для ускорения последующих загрузок.

```
┌─────────────────────────────────────────────────────────────┐
│                    БРАУЗЕРНОЕ КЭШИРОВАНИЕ                   │
└─────────────────────────────────────────────────────────────┘

Первый запрос:
Browser ────request────→ Server
       ←───response────  (200 OK + Cache headers)
       
Повторный запрос:
Browser ────request────→ Server  
       ←───304 Not Modified────  (если ресурс не изменился)
       
или

Browser (использует кэш) ──×──→ Server (запрос не отправляется)
```

### HTTP заголовки для кэширования

#### 1. Cache-Control

Основной заголовок для управления кэшированием:

```http
Cache-Control: max-age=3600          // Кэшировать на 1 час
Cache-Control: no-cache              // Всегда проверять с сервером
Cache-Control: no-store              // Никогда не кэшировать
Cache-Control: private               // Только браузер, не CDN
Cache-Control: public                // Можно кэшировать везде
Cache-Control: must-revalidate       // Проверить после истечения
```

#### 2. ETag (Entity Tag)

Уникальный идентификатор версии ресурса:

```
┌─────────────────────────────────────────────────────────────┐
│                        ETAG WORKFLOW                        │
└─────────────────────────────────────────────────────────────┘

1. Первый запрос:
   GET /style.css
   Response: ETag: "abc123"
   
2. Повторный запрос:
   GET /style.css
   If-None-Match: "abc123"
   
3. Ответ сервера:
   - Если файл не изменился: 304 Not Modified
   - Если изменился: 200 OK + новый ETag
```

#### 3. Last-Modified

Дата последнего изменения ресурса:

```http
Last-Modified: Wed, 21 Oct 2023 07:28:00 GMT

// При повторном запросе:
If-Modified-Since: Wed, 21 Oct 2023 07:28:00 GMT
```

### Практический пример настройки кэширования

```html
<!-- HTML с оптимальным кэшированием -->
<!DOCTYPE html>
<html>
<head>
    <!-- CSS с версионированием для cache busting -->
    <link rel="stylesheet" href="/css/styles.css?v=1.2.3">
    
    <!-- Предзагрузка критических ресурсов -->
    <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
</head>
<body>
    <!-- JavaScript с хешем для кэш-инвалидации -->
    <script src="/js/app.abc123.min.js"></script>
</body>
</html>
```

```javascript
// Настройка сервера (Node.js/Express)
app.use('/static', express.static('public', {
    maxAge: '1y',           // Статические ресурсы на год
    etag: true,             // Включить ETag
    lastModified: true      // Включить Last-Modified
}));

// HTML страницы не кэшируем
app.get('/', (req, res) => {
    res.set('Cache-Control', 'no-cache');
    res.render('index');
});
```

### Service Workers — продвинутое кэширование

Service Workers предоставляют программный контроль над кэшированием:

```javascript
// sw.js - Service Worker
const CACHE_NAME = 'my-app-v1.0.0';
const urlsToCache = [
    '/',
    '/css/styles.css',
    '/js/app.js',
    '/images/logo.png'
];

// Установка и кэширование ресурсов
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

// Стратегия "Cache First"
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Возвращаем из кэша или делаем сетевой запрос
                return response || fetch(event.request);
            })
    );
});
```

### Стратегии кэширования в Service Workers

```
┌─────────────────────────────────────────────────────────────┐
│                 СТРАТЕГИИ КЭШИРОВАНИЯ                       │
└─────────────────────────────────────────────────────────────┘

1. CACHE FIRST (статические ресурсы)
   Cache ──✓──→ Response
     │
   ──×── Network ──→ Response

2. NETWORK FIRST (динамический контент)
   Network ──✓──→ Response
      │               │
   ──×── Cache ──✓──→ Response

3. STALE WHILE REVALIDATE (баланс)
   Cache ──→ Response (сразу)
   Network ──→ Update Cache (в фоне)
```

### Local Storage и Session Storage как кэш

```javascript
// Кэширование данных в Local Storage
class LocalStorageCache {
    constructor(prefix = 'cache_') {
        this.prefix = prefix;
    }
    
    set(key, data, ttl = 3600000) { // TTL в миллисекундах
        const item = {
            data: data,
            timestamp: Date.now(),
            ttl: ttl
        };
        localStorage.setItem(this.prefix + key, JSON.stringify(item));
    }
    
    get(key) {
        const item = localStorage.getItem(this.prefix + key);
        if (!item) return null;
        
        const parsed = JSON.parse(item);
        const now = Date.now();
        
        // Проверяем TTL
        if (now - parsed.timestamp > parsed.ttl) {
            localStorage.removeItem(this.prefix + key);
            return null;
        }
        
        return parsed.data;
    }
    
    clear() {
        Object.keys(localStorage)
            .filter(key => key.startsWith(this.prefix))
            .forEach(key => localStorage.removeItem(key));
    }
}

// Использование
const cache = new LocalStorageCache();
cache.set('user_data', userData, 1800000); // 30 минут
const cachedData = cache.get('user_data');
```

---

## 🌍 Глава 2: CDN и edge кэширование

### Что такое CDN?

CDN (Content Delivery Network) — это географически распределенная сеть серверов, которая доставляет контент пользователям с ближайшего к ним сервера.

```
┌─────────────────────────────────────────────────────────────┐
│                    АРХИТЕКТУРА CDN                          │
└─────────────────────────────────────────────────────────────┘

        Origin Server (Москва)
               │
    ┌──────────┼──────────┐
    │          │          │
Edge Server Edge Server Edge Server
 (Москва)   (СПб)    (Екатеринбург)
    │          │          │
 Users      Users      Users
(Центр)   (Север)    (Урал)

Время отклика: 10ms vs 150ms без CDN
```

### Стратегии кэширования в CDN

#### 1. Push CDN
```
Developer ──push──→ CDN ──serve──→ Users
```
- Разработчик сам загружает контент на CDN
- Полный контроль над тем, что кэшируется
- Подходит для статического контента

#### 2. Pull CDN
```
Users ──request──→ CDN ──miss──→ Origin
                    │  ←─────────┘
                 cache ──serve──→ Users
```
- CDN автоматически кэширует при первом запросе
- Проще в настройке
- Подходит для динамического контента

### Настройка CloudFlare CDN

```javascript
// cloudflare-worker.js
addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
    const url = new URL(request.url);
    
    // Настройки кэширования для разных типов контента
    if (url.pathname.match(/\.(jpg|jpeg|png|gif|webp)$/)) {
        // Изображения кэшируем на месяц
        return fetch(request, {
            cf: {
                cacheTtl: 2592000,
                cacheEverything: true
            }
        });
    }
    
    if (url.pathname.match(/\.(css|js)$/)) {
        // CSS/JS кэшируем на неделю
        return fetch(request, {
            cf: {
                cacheTtl: 604800,
                cacheEverything: true
            }
        });
    }
    
    // API запросы кэшируем на 5 минут
    if (url.pathname.startsWith('/api/')) {
        return fetch(request, {
            cf: {
                cacheTtl: 300
            }
        });
    }
    
    // Остальное не кэшируем
    return fetch(request);
}
```

### Edge Computing и кэширование

```
┌─────────────────────────────────────────────────────────────┐
│                    EDGE COMPUTING                           │
└─────────────────────────────────────────────────────────────┘

Traditional:
User ──→ CDN ──→ Origin Server ──→ Database
     150ms    200ms           50ms
     Total: 400ms

Edge Computing:
User ──→ Edge Server (with cache) ──→ Response
     10ms              15ms
     Total: 25ms
```

```javascript
// Пример Edge функции (Cloudflare Workers)
export default {
    async fetch(request) {
        const cache = caches.default;
        const cacheKey = new Request(request.url, request);
        
        // Проверяем кэш
        let response = await cache.match(cacheKey);
        
        if (!response) {
            // Генерируем ответ на Edge
            const data = await generateDataAtEdge(request);
            response = new Response(JSON.stringify(data), {
                headers: {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'public, max-age=300'
                }
            });
            
            // Сохраняем в кэш
            await cache.put(cacheKey, response.clone());
        }
        
        return response;
    }
};
```

---

## 🖥️ Глава 3: Серверное кэширование

### Reverse Proxy кэширование

```
┌─────────────────────────────────────────────────────────────┐
│                  REVERSE PROXY CACHE                        │
└─────────────────────────────────────────────────────────────┘

Internet ──→ Nginx/Varnish ──→ App Server ──→ Database
             (Reverse Proxy)
                   │
               [Cache Layer]
                   │
           ┌───────┴───────┐
           │   Cached      │
           │   Responses   │
           └───────────────┘
```

### Конфигурация Nginx для кэширования

```nginx
# nginx.conf
http {
    # Настройка кэш-зоны
    proxy_cache_path /var/cache/nginx 
                     levels=1:2 
                     keys_zone=my_cache:10m 
                     max_size=10g 
                     inactive=60m;
    
    server {
        listen 80;
        server_name example.com;
        
        location / {
            proxy_pass http://backend;
            
            # Включаем кэширование
            proxy_cache my_cache;
            proxy_cache_valid 200 302 10m;
            proxy_cache_valid 404 1m;
            
            # Заголовки для кэширования
            proxy_cache_use_stale error timeout invalid_header updating;
            proxy_cache_background_update on;
            proxy_cache_revalidate on;
            
            # Добавляем информацию о статусе кэша
            add_header X-Cache-Status $upstream_cache_status;
        }
        
        # Статические файлы
        location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # API с коротким кэшем
        location /api/ {
            proxy_pass http://backend;
            proxy_cache my_cache;
            proxy_cache_valid 200 5m;
        }
    }
}
```

### Varnish Cache конфигурация

```vcl
# default.vcl
vcl 4.1;

backend default {
    .host = "127.0.0.1";
    .port = "8080";
    .connect_timeout = 60s;
    .first_byte_timeout = 60s;
    .between_bytes_timeout = 60s;
}

sub vcl_recv {
    # Убираем cookies для статических ресурсов
    if (req.url ~ "^[^?]*\.(7z|avi|bmp|bz2|css|csv|doc|docx|eot|flac|flv|gif|gz|ico|jpeg|jpg|js|less|mka|mkv|mov|mp3|mp4|mpeg|mpg|odt|otf|ogg|ogm|opus|pdf|png|ppt|pptx|rar|rtf|svg|svgz|swf|tar|tbz|tgz|ttf|txt|txz|wav|webm|webp|woff|woff2|xls|xlsx|xml|xz|zip)(\?.*)?$") {
        unset req.http.Cookie;
    }
    
    # Обходим кэш для админки
    if (req.url ~ "^/admin") {
        return (pass);
    }
}

sub vcl_backend_response {
    # Кэшируем ответы с определенными статусами
    if (beresp.status == 200 || beresp.status == 301 || beresp.status == 302) {
        if (bereq.url ~ "\.(css|js|png|gif|jp(e)?g|swf|ico|woff|woff2)$") {
            set beresp.ttl = 1w;
            set beresp.http.Cache-Control = "public, max-age=604800";
        } else {
            set beresp.ttl = 5m;
        }
    }
}

sub vcl_deliver {
    # Добавляем заголовок с информацией о попадании в кэш
    if (obj.hits > 0) {
        set resp.http.X-Cache = "HIT";
        set resp.http.X-Cache-Hits = obj.hits;
    } else {
        set resp.http.X-Cache = "MISS";
    }
}
```

### Application-level кэширование

```javascript
// Express.js middleware для кэширования
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 }); // 10 минут по умолчанию

function cacheMiddleware(duration = 300) {
    return (req, res, next) => {
        // Создаем ключ кэша на основе URL и query параметров
        const key = `cache_${req.originalUrl || req.url}`;
        const cachedResponse = cache.get(key);
        
        if (cachedResponse) {
            console.log('Cache HIT:', key);
            return res.json(cachedResponse);
        }
        
        console.log('Cache MISS:', key);
        
        // Перехватываем метод json
        const originalJson = res.json.bind(res);
        res.json = (data) => {
            // Сохраняем в кэш только успешные ответы
            if (res.statusCode === 200) {
                cache.set(key, data, duration);
            }
            return originalJson(data);
        };
        
        next();
    };
}

// Использование
app.get('/api/users', cacheMiddleware(600), async (req, res) => {
    const users = await User.findAll();
    res.json(users);
});
```

---

## 🔄 Глава 4: API и динамический контент

### Кэширование REST API ответов

```
┌─────────────────────────────────────────────────────────────┐
│                   API CACHING STRATEGY                      │
└─────────────────────────────────────────────────────────────┘

GET /api/users           → Cache for 5 minutes
GET /api/users/123       → Cache for 10 minutes  
POST/PUT/DELETE          → Invalidate related cache
GET /api/real-time-data  → No cache (TTL=0)
```

```javascript
// Интеллектуальное кэширование API
class APICache {
    constructor() {
        this.cache = new Map();
        this.dependencies = new Map(); // Зависимости между эндпоинтами
    }
    
    // Настройка зависимостей кэша
    setupDependencies() {
        this.dependencies.set('/api/users', ['/api/users/*']);
        this.dependencies.set('/api/posts', ['/api/posts/*', '/api/users/*']);
    }
    
    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;
        
        if (Date.now() > item.expiry) {
            this.cache.delete(key);
            return null;
        }
        
        return item.data;
    }
    
    set(key, data, ttl = 300000) {
        this.cache.set(key, {
            data,
            expiry: Date.now() + ttl,
            tags: this.extractTags(key)
        });
    }
    
    // Инвалидация по тегам
    invalidateByTag(tag) {
        for (const [key, item] of this.cache.entries()) {
            if (item.tags.includes(tag)) {
                this.cache.delete(key);
            }
        }
    }
    
    extractTags(key) {
        const tags = [];
        if (key.includes('/users')) tags.push('users');
        if (key.includes('/posts')) tags.push('posts');
        return tags;
    }
}

// Middleware для автоматической инвалидации
app.use('/api', (req, res, next) => {
    if (['POST', 'PUT', 'DELETE'].includes(req.method)) {
        // Инвалидируем связанные кэши после изменения данных
        res.on('finish', () => {
            if (res.statusCode < 400) {
                const tags = extractTagsFromURL(req.url);
                tags.forEach(tag => apiCache.invalidateByTag(tag));
            }
        });
    }
    next();
});
```

### GraphQL кэширование

```javascript
// Apollo Server с кэшированием
const { ApolloServer } = require('apollo-server-express');
const { RedisCache } = require('apollo-server-cache-redis');

const server = new ApolloServer({
    typeDefs,
    resolvers,
    cache: new RedisCache({
        host: 'localhost',
        port: 6379,
    }),
    cacheControl: {
        defaultMaxAge: 300, // 5 минут по умолчанию
    },
});

// Схема с настройками кэширования
const typeDefs = `
    type User {
        id: ID!
        name: String!
        posts: [Post!]! @cacheControl(maxAge: 60)
    }
    
    type Post {
        id: ID!
        title: String!
        content: String!
        author: User! @cacheControl(maxAge: 300)
    }
    
    type Query {
        user(id: ID!): User @cacheControl(maxAge: 600)
        posts: [Post!]! @cacheControl(maxAge: 120)
        realtimeData: RealtimeData @cacheControl(maxAge: 0)
    }
`;

// Резолверы с гранулярным кэшированием
const resolvers = {
    Query: {
        user: async (_, { id }, { dataSources, cache }) => {
            const cacheKey = `user:${id}`;
            let user = await cache.get(cacheKey);
            
            if (!user) {
                user = await dataSources.userAPI.getUserById(id);
                await cache.set(cacheKey, user, { ttl: 600 });
            }
            
            return user;
        },
    },
};
```

### Стратегии инвалидации для динамического контента

```javascript
// Event-driven cache invalidation
const EventEmitter = require('events');
const cacheInvalidator = new EventEmitter();

// Подписка на события инвалидации
cacheInvalidator.on('user:updated', (userId) => {
    cache.invalidate(`user:${userId}`);
    cache.invalidatePattern(`user:${userId}:*`);
    cache.invalidateByTag('users');
});

cacheInvalidator.on('post:created', (postData) => {
    cache.invalidateByTag('posts');
    cache.invalidate(`user:${postData.authorId}:posts`);
});

// В контроллерах
app.put('/api/users/:id', async (req, res) => {
    const user = await User.update(req.params.id, req.body);
    
    // Эмитим событие для инвалидации
    cacheInvalidator.emit('user:updated', req.params.id);
    
    res.json(user);
});
```

### Cache warming стратегии

```javascript
// Автоматический прогрев кэша
class CacheWarmer {
    constructor(cache, scheduler) {
        this.cache = cache;
        this.scheduler = scheduler;
        this.warmingRules = new Map();
    }
    
    // Добавляем правило прогрева
    addWarmingRule(pattern, generator, schedule) {
        this.warmingRules.set(pattern, { generator, schedule });
        this.scheduler.scheduleJob(schedule, () => this.warmCache(pattern));
    }
    
    async warmCache(pattern) {
        const rule = this.warmingRules.get(pattern);
        if (!rule) return;
        
        try {
            const data = await rule.generator();
            const keys = this.generateKeysFromPattern(pattern);
            
            for (const key of keys) {
                await this.cache.set(key, data[key], 3600);
            }
            
            console.log(`Cache warmed for pattern: ${pattern}`);
        } catch (error) {
            console.error(`Cache warming failed for ${pattern}:`, error);
        }
    }
    
    generateKeysFromPattern(pattern) {
        // Генерируем ключи на основе паттерна
        // Например, для "popular:posts" возвращаем ключи популярных постов
        return ['popular:posts:today', 'popular:posts:week'];
    }
}

// Настройка прогрева
const warmer = new CacheWarmer(cache, scheduler);

// Прогреваем популярный контент каждый час
warmer.addWarmingRule(
    'popular:*',
    async () => {
        const popularPosts = await Post.findPopular();
        const popularUsers = await User.findPopular();
        return {
            'popular:posts': popularPosts,
            'popular:users': popularUsers
        };
    },
    '0 * * * *' // каждый час
);
```

---

## 🛠️ Практические задания

### Задание 1: Настройка оптимального браузерного кэширования

Создайте SPA приложение с правильно настроенным кэшированием:

1. Настройте HTTP заголовки для разных типов ресурсов
2. Реализуйте версионирование статических файлов
3. Добавьте Service Worker с стратегией "Cache First" для статики и "Network First" для API

### Задание 2: CDN интеграция

Настройте CDN для своего проекта:

1. Подключите CloudFlare или другой CDN
2. Настройте правила кэширования для разных типов контента
3. Создайте Edge функцию для кэширования API ответов

### Задание 3: Middleware для кэширования API

Разработайте универсальное middleware для кэширования API:

1. Поддержка TTL для разных эндпоинтов
2. Автоматическая инвалидация при изменении данных
3. Система тегов для группового удаления кэша

### Задание 4: Мониторинг кэш-производительности

Создайте dashboard для мониторинга эффективности кэша:

1. Метрики hit rate для разных типов контента
2. Графики производительности до/после кэширования
3. Автоматические алерты при снижении эффективности

---

## 📊 Контрольные вопросы

1. Объясните разницу между `Cache-Control: no-cache` и `Cache-Control: no-store`
2. Когда следует использовать ETag, а когда Last-Modified?
3. Какие стратегии кэширования лучше всего подходят для Service Workers?
4. Как настроить правильную инвалидацию кэша в микросервисной архитектуре?
5. Объясните принцип работы Edge Computing и его преимущества для кэширования

---

## ✅ Результат блока

После изучения этого блока вы будете способны:

- Настраивать эффективное кэширование для веб-проектов любого масштаба
- Понимать всю цепочку кэширования от браузера до сервера
- Оптимизировать загрузку страниц через правильное использование CDN
- Создавать интеллектуальные системы инвалидации кэша
- Мониторить и улучшать производительность кэширующих систем