# System Design - Блок 6: Проектирование конкретных систем

**Продолжительность:** 5-6 недель  
**Цель:** Применить знания на практике через разбор реальных кейсов  
**Временные затраты:** 8-12 часов в неделю

---

## 🎯 Обзор блока

```
┌─────────────────────────────────────────────────────────────┐
│                    БЛОК 6: ПРАКТИЧЕСКИЕ КЕЙСЫ              │
├─────────────────────────────────────────────────────────────┤
│ Неделя 23: Социальные системы (Twitter/Facebook)           │
│ Неделя 24: Мессенджеры и чаты                              │
│ Неделя 25: Видеостриминг (YouTube/Netflix)                 │
│ Неделя 26: E-commerce платформы                            │
│ Неделя 27: Поисковые системы                               │
│ Неделя 28: Transportation и финансы                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📅 Неделя 23: Социальные системы

### Глава 6.1: Проектирование социальной сети (Twitter/Facebook)

#### 🎯 Функциональные требования
```
┌─── CORE FEATURES ───┐    ┌─── SCALE REQUIREMENTS ───┐
│ • User Registration │    │ • 1B+ пользователей      │
│ • Create Posts      │    │ • 100M DAU               │
│ • Follow/Unfollow   │    │ • 1M новых постов/день    │
│ • News Feed         │    │ • 100:1 read/write ratio  │
│ • Likes & Comments  │    │ • < 200ms feed latency    │
│ • Search Users      │    │ • 99.9% availability      │
└─────────────────────┘    └───────────────────────────┘
```

#### 🏗️ Высокоуровневая архитектура

```
    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
    │   Mobile    │    │     Web      │    │  3rd Party  │
    │     App     │    │   Browser    │    │    APIs     │
    └──────┬──────┘    └──────┬───────┘    └──────┬──────┘
           │                  │                   │
           └──────────────────┼───────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Load Balancer   │
                    │   (Layer 7)       │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───▼────┐        ┌───────▼────┐        ┌───────▼────┐
    │  User  │        │    Feed    │        │   Media    │
    │Service │        │  Service   │        │  Service   │
    └───┬────┘        └───────┬────┘        └───────┬────┘
        │                     │                     │
    ┌───▼────┐        ┌───────▼────┐        ┌───────▼────┐
    │ User   │        │   Feed     │        │   CDN +    │
    │  DB    │        │   Cache    │        │ S3 Storage │
    └────────┘        └────────────┘        └────────────┘
```

#### 📊 Дизайн базы данных

**User Service:**
```sql
-- Users Table
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(255) UNIQUE,
    display_name VARCHAR(100),
    bio TEXT,
    avatar_url VARCHAR(500),
    created_at TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE
);

-- Followers Relationship (шардируется по follower_id)
CREATE TABLE follows (
    follower_id BIGINT,
    following_id BIGINT,
    created_at TIMESTAMP,
    PRIMARY KEY (follower_id, following_id)
);
```

**Post Service:**
```sql
-- Posts Table (шардируется по user_id)
CREATE TABLE posts (
    post_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    content TEXT,
    media_urls JSON,
    like_count INT DEFAULT 0,
    repost_count INT DEFAULT 0,
    reply_count INT DEFAULT 0,
    created_at TIMESTAMP,
    INDEX idx_user_created (user_id, created_at)
);
```

#### ⚡ Feed Generation Алгоритм

```
PUSH MODEL (для пользователей с < 1M подписчиков):
┌─────────────────────────────────────────────────────────┐
│ 1. User создает пост                                    │
│ 2. Fanout Service забирает список followers             │
│ 3. Асинхронно добавляет пост в cache всех followers     │
│ 4. Feed читается прямо из cache                         │
└─────────────────────────────────────────────────────────┘

PULL MODEL (для celebrity пользователей):
┌─────────────────────────────────────────────────────────┐
│ 1. User запрашивает feed                                │
│ 2. Система получает список following                    │
│ 3. Fetches recent posts от каждого following            │
│ 4. Merge и sort по timestamp                            │
│ 5. Cache результат на 5-10 минут                        │
└─────────────────────────────────────────────────────────┘
```

#### 🔄 Timeline Architecture

```
          ┌─── HOME TIMELINE ───┐           ┌─── USER TIMELINE ───┐
          │                     │           │                     │
    ┌─────▼─────┐         ┌─────▼─────┐     │  ┌─────────────┐   │
    │Redis Cache│         │Redis Cache│     │  │    MySQL    │   │
    │(Hot Data) │         │(Celebrity │     │  │ (User Posts)│   │
    │Timeline   │◄────────┤Timelines) │     │  └─────────────┘   │
    └───────────┘         └───────────┘     │                     │
          │                     │           │  ┌─────────────┐   │
          │               ┌─────▼─────┐     │  │   S3/CDN    │   │
          │               │  MySQL    │     │  │(Media Files)│   │
          │               │(Posts DB) │     │  └─────────────┘   │
          │               └───────────┘     └─────────────────────┘
          │
    ┌─────▼─────┐
    │  Fanout   │
    │  Worker   │
    └───────────┘
```

#### 📈 Масштабирование стратегии

**Database Sharding:**
```
User Sharding Strategy:
┌─────────────────────────────────────┐
│ Shard = hash(user_id) % num_shards  │
│                                     │
│ Shard 1: user_id % 1000 = 0-99     │
│ Shard 2: user_id % 1000 = 100-199  │
│ Shard 3: user_id % 1000 = 200-299  │
│ ...                                 │
└─────────────────────────────────────┘

Following Graph Sharding:
┌─────────────────────────────────────┐
│ Shard по follower_id                │
│ Cross-shard queries для celebrity   │
│ Replica reads для популярных users  │
└─────────────────────────────────────┘
```

**Caching Strategy:**
```
┌── CACHE LAYERS ──┐
│ L1: Browser      │ ← 30s TTL
│ L2: CDN          │ ← 5min TTL  
│ L3: Load Balancer│ ← 1min TTL
│ L4: App Cache    │ ← Real-time
│ L5: DB Cache     │ ← Persistent
└──────────────────┘
```

#### 🚨 Практические задачи

**Задача 1: Celebrity Problem**
```
Проблема: Пользователь с 100M подписчиков постит
Решение:
┌─────────────────────────────────────────┐
│ 1. Hybrid approach (Push + Pull)       │
│ 2. Async fanout в очередях              │
│ 3. Rate limiting на fanout              │
│ 4. Separate celebrity timeline cache    │
└─────────────────────────────────────────┘
```

**Задача 2: Hot Spot Prevention**
```
┌─── TRENDING POSTS ───┐
│ 1. Bloom filter      │ ← Быстрая проверка популярности
│ 2. Separate hot cache│ ← Отдельный cache для viral content
│ 3. Circuit breaker   │ ← Защита от cascade failures
│ 4. Load shedding     │ ← Drop non-critical requests
└──────────────────────┘
```

---

## 📱 Неделя 24: Система чатов и мессенджеров

### Глава 6.2: Real-time Messaging Architecture

#### 🎯 Функциональные требования
```
┌─── MESSAGING FEATURES ───┐    ┌─── SCALE & PERFORMANCE ───┐
│ • 1-on-1 чаты            │    │ • 100M пользователей      │
│ • Group чаты (100 users) │    │ • 1B сообщений/день       │
│ • Media sharing          │    │ • < 100ms message latency │
│ • Message history        │    │ • 99.99% delivery rate    │
│ • Online/Offline status  │    │ • E2E encryption support  │
│ • Push notifications     │    │ • Multi-device sync       │
└──────────────────────────┘    └────────────────────────────┘
```

#### 🏗️ Real-time Communication Architecture

```
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Mobile    │    │     Web     │    │   Desktop   │
    │     App     │    │   Client    │    │     App     │
    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
           │                  │                  │
           └─── WebSocket ────┼─── WebSocket ────┘
                              │
                    ┌─────────▼─────────┐
                    │  WebSocket Load   │
                    │     Balancer      │
                    │ (Sticky Sessions) │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───▼────┐        ┌───────▼────┐        ┌───────▼────┐
    │Gateway │        │  Message   │        │ Presence   │
    │Service │        │  Service   │        │  Service   │
    └───┬────┘        └───────┬────┘        └───────┬────┘
        │                     │                     │
    ┌───▼────┐        ┌───────▼────┐        ┌───────▼────┐
    │Session │        │  Message   │        │ Presence   │
    │  Store │        │   Queue    │        │   Cache    │
    └────────┘        └────────────┘        └────────────┘
```

#### 📊 Message Storage Design

**Message Schema:**
```sql
-- Messages Table (шардируется по chat_id)
CREATE TABLE messages (
    message_id BIGINT PRIMARY KEY,
    chat_id BIGINT,
    sender_id BIGINT,
    content TEXT,
    message_type ENUM('text', 'image', 'video', 'file'),
    media_url VARCHAR(500),
    created_at TIMESTAMP,
    edited_at TIMESTAMP,
    
    INDEX idx_chat_time (chat_id, created_at),
    INDEX idx_sender (sender_id, created_at)
);

-- Chats Metadata
CREATE TABLE chats (
    chat_id BIGINT PRIMARY KEY,
    chat_type ENUM('direct', 'group'),
    name VARCHAR(255),
    created_by BIGINT,
    created_at TIMESTAMP,
    last_activity TIMESTAMP
);

-- Chat Participants
CREATE TABLE chat_participants (
    chat_id BIGINT,
    user_id BIGINT,
    joined_at TIMESTAMP,
    left_at TIMESTAMP,
    role ENUM('admin', 'member'),
    PRIMARY KEY (chat_id, user_id)
);
```

#### ⚡ Message Delivery System

```
MESSAGE FLOW:
┌─────────────────────────────────────────────────────────────────┐
│ 1. Client отправляет сообщение через WebSocket                │
│ 2. Gateway Service валидирует и добавляет в Message Queue     │
│ 3. Message Service обрабатывает и сохраняет в DB              │
│ 4. Fanout к всем участникам чата через Message Queue          │
│ 5. Delivery к online пользователям через WebSocket            │
│ 6. Push notification для offline пользователей                │
│ 7. Acknowledgment обратно отправителю                          │
└─────────────────────────────────────────────────────────────────┘

DELIVERY GUARANTEES:
┌─── AT-LEAST-ONCE DELIVERY ───┐
│ 1. Message ID generation      │
│ 2. Idempotent processing      │
│ 3. Retry mechanism с backoff  │
│ 4. Dead letter queue          │
│ 5. Manual intervention        │
└───────────────────────────────┘
```

#### 🔄 WebSocket Connection Management

```
CONNECTION LIFECYCLE:
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│ 1. CONNECT ──→ Authentication ──→ Session Registration       │
│                       │                      │               │
│ 2. HEARTBEAT ←────────┼──────────────────────┘               │
│                       │                                      │
│ 3. MESSAGE ←──────────┼──────────→ Process & Route           │
│                       │                                      │
│ 4. DISCONNECT ←───────┼──────────→ Cleanup Session           │
│                       │                                      │
└──────────────────────────────────────────────────────────────┘

SESSION STORE (Redis):
{
  "user_123": {
    "connections": [
      {
        "device_id": "mobile_456", 
        "server": "ws-server-1",
        "last_seen": "2024-01-15T10:30:00Z"
      },
      {
        "device_id": "web_789",
        "server": "ws-server-3", 
        "last_seen": "2024-01-15T10:29:45Z"
      }
    ],
    "status": "online"
  }
}
```

#### 📱 Push Notifications Architecture

```
    ┌─── MESSAGE CREATED ───┐
              │
              ▼
    ┌─────────────────────┐
    │ Notification Service │
    └─────────┬───────────┘
              │
    ┌─────────▼───────────┐
    │ User Preference     │ ── Check notification settings
    │ Check               │
    └─────────┬───────────┘
              │
    ┌─────────▼───────────┐
    │ Platform Router     │
    └─────┬───────┬───────┘
          │       │
    ┌─────▼──┐ ┌──▼─────┐
    │  FCM   │ │  APNs  │ ── Push to devices
    │(Android│ │ (iOS)  │
    └────────┘ └────────┘
```

#### 🛡️ Security & Encryption

**End-to-End Encryption Flow:**
```
SIGNAL PROTOCOL IMPLEMENTATION:
┌─────────────────────────────────────────────────────────────┐
│ 1. Key Exchange (X3DH Protocol)                            │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐               │
│    │Identity │    │Signed   │    │One-Time │               │
│    │   Key   │    │Pre-Key  │    │Pre-Keys │               │
│    └─────────┘    └─────────┘    └─────────┘               │
│                                                             │
│ 2. Message Encryption (Double Ratchet)                     │
│    ┌─────────────────────────────────────────────────────┐ │
│    │ Message ──→ Encrypt ──→ [Encrypted Payload]        │ │
│    │              ↑                                      │ │
│    │         Ratchet Key                                 │ │
│    └─────────────────────────────────────────────────────┘ │
│                                                             │
│ 3. Forward Secrecy - новый ключ для каждого сообщения     │
└─────────────────────────────────────────────────────────────┘
```

#### 🚨 Практические задачи

**Задача 1: Message Ordering**
```sql
-- Используем Lamport timestamps для ordering
CREATE TABLE messages (
    message_id BIGINT PRIMARY KEY,
    chat_id BIGINT,
    sender_id BIGINT,
    logical_timestamp BIGINT, -- Lamport clock
    vector_clock JSON,        -- Vector clock для conflict resolution
    content TEXT,
    created_at TIMESTAMP
);
```

**Задача 2: Offline Message Sync**
```
SYNCHRONIZATION STRATEGY:
┌─────────────────────────────────────┐
│ 1. Last seen timestamp per device   │
│ 2. Delta sync от last_seen         │
│ 3. Pagination для больших gaps     │
│ 4. Conflict resolution rules       │
│ 5. Merge strategy для duplicates   │
└─────────────────────────────────────┘
```

---

## 🎬 Неделя 25: Видеостриминг платформа

### Глава 6.3: Video Streaming (YouTube/Netflix)

#### 🎯 Функциональные требования
```
┌─── VIDEO FEATURES ───┐       ┌─── SCALE REQUIREMENTS ───┐
│ • Video Upload       │       │ • 2B пользователей       │
│ • Stream Video       │       │ • 100M часов/день         │
│ • Search & Browse    │       │ • 500 часов upload/мин    │
│ • Recommendations   │       │ • Global CDN coverage     │
│ • Comments & Likes   │       │ • 4K/8K video support     │
│ • Subscriptions     │       │ • < 2s startup time       │
└──────────────────────┘       └───────────────────────────┘
```

#### 🏗️ Video Processing Pipeline

```
UPLOAD & PROCESSING FLOW:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ ┌───────────┐    ┌─────────────┐    ┌─────────────────────────┐ │
│ │   Upload  │───→│   Validate  │───→│     Metadata           │ │
│ │  Service  │    │   & Queue   │    │    Extraction          │ │
│ └───────────┘    └─────────────┘    └─────────────────────────┘ │
│                                                  │              │
│ ┌─────────────────────────────────────────────────▼────────────┐ │
│ │               Video Processing Pipeline               │ │
│ │                                                       │ │
│ │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │ │
│ │ │Transcoding│ │Thumbnail │ │  Audio   │ │Subtitles │ │ │
│ │ │Multiple   │ │Generation│ │Processing│ │Generation│ │ │
│ │ │Resolutions│ │          │ │          │ │   (AI)   │ │ │
│ │ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │ │
│ └─────────────────────────┬─────────────────────────────┘ │
│                           │                               │
│ ┌─────────────────────────▼─────────────────────────────┐ │
│ │            CDN Distribution                           │ │
│ │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │ │
│ │ │ Region 1 │ │ Region 2 │ │ Region 3 │ │ Region N │ │ │
│ │ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │ │
│ └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

#### 📊 Video Metadata & Storage

**Video Schema:**
```sql
-- Videos Metadata
CREATE TABLE videos (
    video_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    title VARCHAR(500),
    description TEXT,
    duration_seconds INT,
    file_size_bytes BIGINT,
    upload_date TIMESTAMP,
    processing_status ENUM('uploading', 'processing', 'ready', 'failed'),
    privacy ENUM('public', 'unlisted', 'private'),
    view_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    dislike_count BIGINT DEFAULT 0,
    
    INDEX idx_user_upload (user_id, upload_date),
    INDEX idx_status (processing_status),
    FULLTEXT idx_search (title, description)
);

-- Video Files (разные форматы и качества)
CREATE TABLE video_files (
    file_id BIGINT PRIMARY KEY,
    video_id BIGINT,
    resolution ENUM('240p', '360p', '720p', '1080p', '4K'),
    format ENUM('mp4', 'webm', 'hls'),
    file_url VARCHAR(1000),
    file_size_bytes BIGINT,
    bitrate INT,
    processing_status ENUM('pending', 'ready', 'failed')
);
```

#### ⚡ Adaptive Bitrate Streaming (HLS)

```
HLS STREAMING ARCHITECTURE:
┌─────────────────────────────────────────────────────────────┐
│                     MASTER PLAYLIST                        │
│ #EXTM3U                                                     │
│ #EXT-X-VERSION:3                                           │
│ #EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360      │
│ 360p/playlist.m3u8                                         │
│ #EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=1280x720    │
│ 720p/playlist.m3u8                                         │
│ #EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1920x1080   │
│ 1080p/playlist.m3u8                                        │
└─────────────────────────────────────────────────────────────┘

CLIENT ADAPTIVE LOGIC:
┌─── BANDWIDTH DETECTION ───┐
│ 1. Monitor download speed  │
│ 2. Buffer health check     │
│ 3. Switch quality up/down  │
│ 4. Smooth transitions      │
└────────────────────────────┘
```

#### 🌍 Global CDN Strategy

```
CDN ARCHITECTURE:
                    ┌─── ORIGIN SERVERS ───┐
                    │    (US East/West)    │
                    └──────────┬───────────┘
                               │
    ┌──────────────────────────┼──────────────────────────┐
    │                          │                          │
┌───▼────┐              ┌──────▼──────┐              ┌───▼────┐
│ Europe │              │ Asia Pacific│              │Americas│
│  CDN   │              │     CDN     │              │  CDN   │
└────────┘              └─────────────┘              └────────┘
    │                          │                          │
┌───▼────┐              ┌──────▼──────┐              ┌───▼────┐
│ Edge   │              │    Edge     │              │ Edge   │
│Servers │              │   Servers   │              │Servers │
└────────┘              └─────────────┘              └────────┘

CACHE STRATEGY:
┌─── HOT CONTENT ───┐ ┌─── WARM CONTENT ───┐ ┌─── COLD CONTENT ───┐
│ • Viral videos    │ │ • Popular channels │ │ • Long tail        │
│ • Recent uploads  │ │ • Trending topics  │ │ • Archive content  │
│ • Cache: All edge │ │ • Cache: Regional  │ │ • Cache: Origin    │
└───────────────────┘ └────────────────────┘ └────────────────────┘
```

#### 🤖 Recommendation Engine

```
RECOMMENDATION PIPELINE:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ ┌───────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│ │ User Behavior │  │  Video       │  │   Content Based     │   │
│ │   History     │  │ Metadata     │  │   Filtering         │   │
│ │               │  │              │  │                     │   │
│ │• Views        │  │• Category    │  │• Similar videos     │   │
│ │• Likes        │  │• Tags        │  │• Genre matching     │   │
│ │• Comments     │  │• Duration    │  │• Creator similarity │   │
│ │• Search       │  │• Upload date │  │                     │   │
│ └───────┬───────┘  └──────┬───────┘  └─────────┬───────────┘   │
│         │                 │                    │               │
│         └─────────────────┼────────────────────┘               │
│                           │                                    │
│              ┌────────────▼─────────────┐                      │
│              │  Machine Learning        │                      │
│              │     Models               │                      │
│              │                          │                      │
│              │• Collaborative Filter    │                      │
│              │• Deep Neural Networks    │                      │
│              │• Matrix Factorization    │                      │
│              │• Multi-arm Bandit        │                      │
│              └────────────┬─────────────┘                      │
│                           │                                    │
│              ┌────────────▼─────────────┐                      │
│              │    Ranking & Serving     │                      │
│              │                          │                      │
│              │• A/B Testing             │                      │
│              │• Real-time Scoring       │                      │
│              │• Diversity Injection     │                      │
│              │• Business Rules          │                      │
│              └──────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

#### 📈 Analytics & Metrics

**Viewing Analytics:**
```sql
-- Video Views (Hot table для real-time metrics)
CREATE TABLE video_views_realtime (
    view_id BIGINT PRIMARY KEY,
    video_id BIGINT,
    user_id BIGINT,
    session_id VARCHAR(100),
    watch_duration_seconds INT,
    total_duration_seconds INT,
    quality_changes INT,
    buffering_events INT,
    device_type ENUM('mobile', 'desktop', 'tv', 'tablet'),
    geographic_region VARCHAR(10),
    timestamp TIMESTAMP,
    
    INDEX idx_video_time (video_id, timestamp),
    INDEX idx_user_time (user_id, timestamp)
);

-- Aggregated metrics (для долгосрочной аналитики)
CREATE TABLE video_metrics_daily (
    video_id BIGINT,
    date DATE,
    total_views BIGINT,
    unique_viewers BIGINT,
    total_watch_time_hours DECIMAL(10,2),
    avg_watch_percentage DECIMAL(5,2),
    engagement_rate DECIMAL(5,2),
    PRIMARY KEY (video_id, date)
);
```

#### 🚨 Практические задачи

**Задача 1: Live Streaming**
```
LIVE STREAMING ARCHITECTURE:
┌─────────────────────────────────────────────────────────────┐
│ 1. RTMP Ingestion ──→ Transcoding ──→ HLS/DASH Segments    │
│ 2. Ultra-low latency: WebRTC для < 500ms                   │
│ 3. Chat integration с WebSocket                            │
│ 4. Auto-scaling для viral streams                          │
│ 5. Content moderation в real-time                          │
└─────────────────────────────────────────────────────────────┘
```

**Задача 2: Copyright Detection**
```python
# Content ID система
class CopyrightDetection:
    def generate_fingerprint(self, video_file):
        # Audio fingerprinting (спектральный анализ)
        # Video fingerprinting (ключевые кадры)
        pass
    
    def match_against_database(self, fingerprint):
        # Поиск в базе защищенного контента
        # Fuzzy matching для частичных совпадений
        pass
```

---

## 🛒 Неделя 26: E-commerce платформы

### Глава 6.4: E-commerce Architecture

#### 🎯 Функциональные требования
```
┌─── ECOMMERCE FEATURES ───┐    ┌─── SCALE REQUIREMENTS ───┐
│ • Product Catalog        │    │ • 100M+ продуктов        │
│ • Shopping Cart          │    │ • 10M concurrent users   │
│ • Order Management       │    │ • Black Friday scale     │
│ • Payment Processing     │    │ • 99.99% availability    │
│ • Inventory Management   │    │ • Global operations      │
│ • Recommendations       │    │ • Real-time inventory    │
└──────────────────────────┘    └───────────────────────────┘
```

#### 🏗️ Microservices Architecture

```
E-COMMERCE MICROSERVICES:
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway                             │
│                     (Rate Limiting,                            │
│                   Authentication, Routing)                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼─────┐    ┌──────▼──────┐    ┌─────▼──────┐
│ User    │    │   Product   │    │    Cart    │
│Service  │    │   Service   │    │  Service   │
└─────────┘    └─────────────┘    └────────────┘
    │                 │                 │
┌───▼─────┐    ┌──────▼──────┐    ┌─────▼──────┐
│ User    │    │   Search    │    │    Cart    │
│Database │    │   Service   │    │   Cache    │
└─────────┘    │(Elasticsearch)│   │  (Redis)  │
               └─────────────┘    └────────────┘

┌──────────┐    ┌─────────────┐    ┌─────────────┐
│  Order   │    │  Payment    │    │ Inventory   │
│ Service  │    │  Service    │    │  Service    │
└─────┬────┘    └─────┬───────┘    └─────┬───────┘
      │               │                  │
┌─────▼────┐    ┌─────▼───────┐    ┌─────▼───────┐
│  Order   │    │  Payment    │    │ Inventory   │
│Database  │    │ Gateway     │    │  Database   │
└──────────┘    │(Stripe/etc) │    └─────────────┘
                └─────────────┘
```

#### 📊 Product Catalog Design

**Product Schema:**
```sql
-- Products (шардируется по category)
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    seller_id BIGINT,
    category_id INT,
    name VARCHAR(500),
    description TEXT,
    brand VARCHAR(100),
    price DECIMAL(10,2),
    currency CHAR(3),
    weight_grams INT,
    dimensions JSON, -- {"length": 10, "width": 5, "height": 3}
    attributes JSON, -- Flexible product attributes
    image_urls JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    status ENUM('active', 'inactive', 'deleted'),
    
    INDEX idx_category (category_id),
    INDEX idx_seller (seller_id),
    INDEX idx_price (price),
    FULLTEXT idx_search (name, description, brand)
);

-- Inventory (separate service для real-time updates)
CREATE TABLE inventory (
    product_id BIGINT PRIMARY KEY,
    quantity_available INT,
    reserved_quantity INT, -- Корзины пользователей
    warehouse_id INT,
    last_updated TIMESTAMP,
    
    INDEX idx_warehouse (warehouse_id),
    INDEX idx_updated (last_updated)
);
```

#### 🛒 Shopping Cart Implementation

```
CART SERVICE ARCHITECTURE:
┌─────────────────────────────────────────────────────────────┐
│                    CART STATES                              │
│                                                             │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│ │   ACTIVE    │───→│  ABANDONED  │───→│  EXPIRED    │      │
│ │   (Redis)   │    │  (30 days)  │    │ (Cleanup)   │      │
│ └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                             │
│ Cart Data Structure (Redis):                               │
│ {                                                           │
│   "user_123": {                                            │
│     "items": [                                             │
│       {                                                    │
│         "product_id": 456,                                 │
│         "quantity": 2,                                     │
│         "price": 29.99,                                    │
│         "added_at": "2024-01-15T10:30:00Z"                │
│       }                                                    │
│     ],                                                     │
│     "total": 59.98,                                        │
│     "currency": "USD",                                     │
│     "last_updated": "2024-01-15T10:35:00Z"                │
│   }                                                        │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
```

#### 💳 Order Processing Workflow

```
ORDER PROCESSING SAGA:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ 1. CREATE ORDER                                                 │
│    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│    │   Validate  │───→│   Reserve   │───→│    Create   │       │
│    │    Cart     │    │  Inventory  │    │    Order    │       │
│    └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                  │              │
│ 2. PAYMENT PROCESSING                            │              │
│    ┌─────────────┐    ┌─────────────┐    ┌──────▼──────┐       │
│    │   Process   │───→│   Confirm   │───→│   Update    │       │
│    │   Payment   │    │   Payment   │    │   Order     │       │
│    └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                  │              │
│ 3. FULFILLMENT                                   │              │
│    ┌─────────────┐    ┌─────────────┐    ┌──────▼──────┐       │
│    │   Create    │───→│   Notify    │───→│   Track     │       │
│    │  Shipment   │    │   Customer  │    │   Delivery  │       │
│    └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                                 │
│ COMPENSATING ACTIONS (если что-то fails):                      │
│ • Inventory Release                                             │
│ • Payment Refund                                                │
│ • Order Cancellation                                            │
│ • Customer Notification                                         │
└─────────────────────────────────────────────────────────────────┘
```

#### 🔍 Search & Recommendations

**Elasticsearch Product Index:**
```json
{
  "mappings": {
    "properties": {
      "product_id": {"type": "keyword"},
      "name": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": {"type": "keyword"},
          "suggest": {"type": "completion"}
        }
      },
      "category": {"type": "keyword"},
      "brand": {"type": "keyword"},
      "price": {"type": "double"},
      "rating": {"type": "double"},
      "review_count": {"type": "integer"},
      "tags": {"type": "keyword"},
      "availability": {"type": "boolean"},
      "location": {"type": "geo_point"}
    }
  }
}
```

**Recommendation Strategies:**
```
RECOMMENDATION ENGINE:
┌─── COLLABORATIVE FILTERING ───┐
│ • User-based CF               │ ← "Пользователи как вы также купили"
│ • Item-based CF               │ ← "Часто покупают вместе"
│ • Matrix Factorization        │ ← Скрытые факторы
└───────────────────────────────┘

┌─── CONTENT-BASED ───┐
│ • Product similarity          │ ← Похожие товары
│ • Category preferences        │ ← Интересы пользователя
│ • Brand affinity              │ ← Предпочтения брендов
└───────────────────────────────┘

┌─── BUSINESS RULES ───┐
│ • Seasonal promotions         │ ← Акции и скидки
│ • Inventory optimization      │ ← Продвижение остатков
│ • Profit margin optimization  │ ← Высокомаржинальные товары
└───────────────────────────────┘
```

#### 📊 Inventory Management

```sql
-- Inventory Events (Event sourcing для audit trail)
CREATE TABLE inventory_events (
    event_id BIGINT PRIMARY KEY,
    product_id BIGINT,
    event_type ENUM('restock', 'sale', 'reservation', 'release', 'adjustment'),
    quantity_change INT, -- может быть отрицательным
    reason VARCHAR(500),
    user_id BIGINT, -- кто изменил
    order_id BIGINT, -- если связано с заказом
    timestamp TIMESTAMP,
    
    INDEX idx_product_time (product_id, timestamp),
    INDEX idx_event_type (event_type, timestamp)
);

-- Real-time inventory view (materialized от events)
CREATE TABLE current_inventory (
    product_id BIGINT PRIMARY KEY,
    available_quantity INT,
    reserved_quantity INT,
    total_quantity INT GENERATED ALWAYS AS (available_quantity + reserved_quantity),
    last_updated TIMESTAMP,
    
    CHECK (available_quantity >= 0),
    CHECK (reserved_quantity >= 0)
);
```

#### 🚨 Практические задачи

**Задача 1: Inventory Race Conditions**
```sql
-- Optimistic locking для предотвращения overselling
BEGIN TRANSACTION;
SELECT available_quantity, version 
FROM inventory 
WHERE product_id = ? FOR UPDATE;

-- Проверяем availability
IF available_quantity >= requested_quantity THEN
    UPDATE inventory 
    SET available_quantity = available_quantity - ?,
        reserved_quantity = reserved_quantity + ?,
        version = version + 1
    WHERE product_id = ? AND version = ?;
    
    IF ROW_COUNT() = 0 THEN
        ROLLBACK; -- Кто-то другой обновил раньше
        RETURN 'conflict';
    END IF;
ELSE
    ROLLBACK;
    RETURN 'insufficient_stock';
END IF;

COMMIT;
```

**Задача 2: Payment Processing Resilience**
```
PAYMENT RESILIENCE PATTERNS:
┌─────────────────────────────────────┐
│ 1. Circuit Breaker для payment API │
│ 2. Retry с exponential backoff     │
│ 3. Multiple payment providers      │
│ 4. Idempotency keys               │
│ 5. Payment status reconciliation  │
│ 6. Fraud detection integration    │
└─────────────────────────────────────┘
```

---

## 🔍 Неделя 27: Поисковые системы

### Глава 6.5: Search Engine Architecture

#### 🎯 Функциональные требования
```
┌─── SEARCH FEATURES ───┐         ┌─── SCALE REQUIREMENTS ───┐
│ • Web Crawling        │         │ • 100B+ web pages        │
│ • Full-text Search    │         │ • 100K queries/second    │
│ • Auto-suggestions    │         │ • < 200ms response time  │
│ • Image/Video Search  │         │ • 99.9% availability     │
│ • Real-time Indexing  │         │ • Global coverage        │
│ • Personalized Results│         │ • Multi-language support │
└───────────────────────┘         └───────────────────────────┘
```

#### 🏗️ Search Engine Architecture

```
SEARCH ENGINE PIPELINE:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ 1. WEB CRAWLING                                                 │
│    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│    │ Seed URLs   │───→│   Crawler   │───→│   Content   │       │
│    │  Manager    │    │   Fleet     │    │  Extractor  │       │
│    └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                  │              │
│ 2. CONTENT PROCESSING                            │              │
│    ┌─────────────┐    ┌─────────────┐    ┌──────▼──────┐       │
│    │ Duplicate   │───→│ Text        │───→│   Link      │       │
│    │ Detection   │    │ Processing  │    │ Extraction  │       │
│    └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                  │              │
│ 3. INDEXING                                      │              │
│    ┌─────────────┐    ┌─────────────┐    ┌──────▼──────┐       │
│    │ Inverted    │───→│ Forward     │───→│   Index     │       │
│    │   Index     │    │   Index     │    │ Distribution│       │
│    └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                  │              │
│ 4. QUERY PROCESSING                              │              │
│    ┌─────────────┐    ┌─────────────┐    ┌──────▼──────┐       │
│    │  Query      │───→│  Ranking    │───→│  Results    │       │
│    │ Processing  │    │  Algorithm  │    │  Serving    │       │
│    └─────────────┘    └─────────────┘    └─────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

#### 🕷️ Web Crawler Architecture

```
DISTRIBUTED CRAWLER:
┌─────────────────────────────────────────────────────────────┐
│                     URL FRONTIER                           │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│ │  Priority   │  │  Politeness │  │     Freshness       │ │
│ │   Queue     │  │   Control   │  │     Manager         │ │
│ │             │  │ (robots.txt)│  │  (Re-crawl freq)    │ │
│ └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼────┐     ┌──────▼──────┐     ┌────▼───┐
│Crawler │     │   Crawler   │     │Crawler │
│Node 1  │     │   Node 2    │     │Node N  │
└───┬────┘     └──────┬──────┘     └────┬───┘
    │                 │                 │
┌───▼────┐     ┌──────▼──────┐     ┌────▼───┐
│Content │     │   Content   │     │Content │
│Storage │     │   Storage   │     │Storage │
└────────┘     └─────────────┘     └────────┘

POLITENESS CONSTRAINTS:
┌─────────────────────────────────────┐
│ • robots.txt соблюдение             │
│ • Delay между запросами к домену    │
│ • Concurrent connections limit      │
│ • User-Agent rotation               │
│ • IP address rotation               │
└─────────────────────────────────────┘
```

#### 📊 Inverted Index Structure

```
INVERTED INDEX DESIGN:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│ Term: "machine"                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Document Postings List:                                 │ │
│ │                                                         │ │
│ │ Doc1: {tf: 3, positions: [12, 45, 78]}                 │ │
│ │ Doc2: {tf: 1, positions: [23]}                         │ │
│ │ Doc5: {tf: 2, positions: [5, 67]}                      │ │
│ │ Doc7: {tf: 1, positions: [89]}                         │ │
│ │ ...                                                     │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Index Sharding Strategy:                                    │
│ ┌─── TERM PARTITIONING ───┐  ┌─── DOCUMENT PARTITIONING ─┐ │
│ │ Shard 1: a-f            │  │ Shard 1: docs 1-1M        │ │
│ │ Shard 2: g-m            │  │ Shard 2: docs 1M-2M       │ │
│ │ Shard 3: n-s            │  │ Shard 3: docs 2M-3M       │ │
│ │ Shard 4: t-z            │  │ ...                       │ │
│ └─────────────────────────┘  └───────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Index Storage Schema:**
```sql
-- Inverted Index (NoSQL - Cassandra/HBase)
CREATE TABLE inverted_index (
    term VARCHAR(100),
    shard_id INT,
    posting_list BLOB, -- Compressed list of document IDs
    term_frequency BIGINT,
    document_frequency BIGINT,
    PRIMARY KEY (term, shard_id)
);

-- Document Metadata
CREATE TABLE documents (
    doc_id BIGINT PRIMARY KEY,
    url VARCHAR(2000),
    title VARCHAR(1000),
    content_hash VARCHAR(64),
    page_rank DECIMAL(10,8),
    crawl_timestamp TIMESTAMP,
    last_modified TIMESTAMP,
    content_length INT,
    language CHAR(2),
    
    INDEX idx_url_hash (url(100)),
    INDEX idx_crawl_time (crawl_timestamp),
    INDEX idx_page_rank (page_rank DESC)
);
```

#### 🎯 Ranking Algorithm

```
RANKING FACTORS:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│ 1. RELEVANCE SCORE                                          │
│    ┌─── TF-IDF ───┐    ┌─── BM25 ───┐    ┌─── Semantic ─┐ │
│    │ Term Freq *  │    │ Improved   │    │ Word2Vec,    │ │
│    │ Inverse Doc  │    │ TF-IDF     │    │ BERT-based   │ │
│    │ Frequency    │    │ Algorithm  │    │ Similarity   │ │
│    └──────────────┘    └────────────┘    └──────────────┘ │
│                                                             │
│ 2. AUTHORITY SCORE                                          │
│    ┌─── PageRank ───┐  ┌─── HITS ────┐   ┌─── Trust ────┐ │
│    │ Link-based     │  │ Hub/Authority│   │ Domain       │ │
│    │ Authority      │  │ Algorithm    │   │ Reputation   │ │
│    └────────────────┘  └──────────────┘   └──────────────┘ │
│                                                             │
│ 3. USER SIGNALS                                             │
│    ┌─── Click Rate ─┐  ┌─── Dwell Time─┐  ┌─── Bounce ──┐ │
│    │ CTR for query  │  │ Time on page  │  │ Quick back   │ │
│    │ result pairs   │  │ after click   │  │ to results   │ │
│    └────────────────┘  └───────────────┘  └──────────────┘ │
│                                                             │
│ FINAL SCORE = α*Relevance + β*Authority + γ*UserSignals    │
└─────────────────────────────────────────────────────────────┘
```

#### ⚡ Query Processing Pipeline

```
QUERY EXECUTION:
┌─────────────────────────────────────────────────────────────┐
│ 1. QUERY PARSING                                            │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│    │ Tokenization│─→│ Spell Check │─→│ Query Expansion │   │
│    │ & Stemming  │  │ & Suggest   │  │ (Synonyms)      │   │
│    └─────────────┘  └─────────────┘  └─────────────────┘   │
│                                                             │
│ 2. INDEX LOOKUP                                             │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│    │ Term Lookup │─→│ Intersection│─→│ Initial Ranking │   │
│    │ (Parallel)  │  │ of Postings │  │ (TF-IDF/BM25)   │   │
│    └─────────────┘  └─────────────┘  └─────────────────┘   │
│                                                             │
│ 3. RESULT PROCESSING                                        │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│    │ Re-ranking  │─→│ Snippet     │─→│ Result Serving  │   │
│    │ (ML Models) │  │ Generation  │  │ & Caching       │   │
│    └─────────────┘  └─────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### 🔤 Auto-suggestion System

```
SUGGESTION ARCHITECTURE:
┌─────────────────────────────────────────────────────────────┐
│                    SUGGESTION SOURCES                       │
│                                                             │
│ ┌─── QUERY LOGS ────┐ ┌─── TRENDING ───┐ ┌─── PERSONAL ──┐ │
│ │ • Popular queries │ │ • Real-time    │ │ • User history│ │
│ │ • Prefix matching │ │ • Trending     │ │ • Personalized│ │
│ │ • Frequency based │ │ • News topics  │ │ • Context     │ │
│ └───────────────────┘ └────────────────┘ └───────────────┘ │
│                                                             │
│                          │                                  │
│               ┌──────────▼──────────┐                       │
│               │   TRIE STRUCTURE    │                       │
│               │   (Prefix Tree)     │                       │
│               │                     │                       │
│               │ Root                │                       │
│               │  ├─ c               │                       │
│               │  │  ├─ ca           │                       │
│               │  │  │  ├─ cat (50k) │                       │
│               │  │  │  └─ car (30k) │                       │
│               │  │  └─ co           │                       │
│               │  │     └─ code(20k) │                       │
│               │  └─ ...             │                       │
│               └─────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘

SUGGESTION API:
GET /suggest?q=mach&limit=10
Response:
{
  "suggestions": [
    {"text": "machine learning", "score": 95000},
    {"text": "machine gun", "score": 87000},
    {"text": "machine learning algorithms", "score": 45000}
  ]
}
```

#### 🚨 Практические задачи

**Задача 1: Duplicate Detection**
```python
# Simhash для near-duplicate detection
class DocumentDeduplication:
    def __init__(self):
        self.shingle_size = 3
        self.hash_size = 64
    
    def generate_simhash(self, text):
        # Создаем shingles (n-граммы)
        shingles = self.generate_shingles(text)
        # Вычисляем hash для каждого shingle
        # Комбинируем в simhash
        pass
    
    def is_duplicate(self, hash1, hash2, threshold=3):
        # Hamming distance между simhash
        return bin(hash1 ^ hash2).count('1') <= threshold
```

**Задача 2: Real-time Indexing**
```
INCREMENTAL INDEXING:
┌─────────────────────────────────────┐
│ 1. Hot Index (Recent documents)     │
│ 2. Warm Index (Last week)           │
│ 3. Cold Index (Archived)            │
│                                     │
│ Query execution:                    │
│ • Search all indexes in parallel   │
│ • Merge results by relevance       │
│ • Periodic index consolidation     │
└─────────────────────────────────────┘
```

---

## 🚗 Неделя 28: Transportation и финансовые системы

### Глава 6.6: Ride-sharing сервис (Uber/Lyft)

#### 🎯 Функциональные требования
```
┌─── RIDE-SHARING FEATURES ───┐    ┌─── SCALE REQUIREMENTS ───┐
│ • Real-time Matching        │    │ • 100M пользователей     │
│ • Dynamic Pricing           │    │ • 10M trips/день          │
│ • Route Optimization        │    │ • < 5s matching time     │
│ • Payment Processing        │    │ • 99.99% availability    │
│ • Real-time Tracking        │    │ • Global coverage        │
│ • Driver Management         │    │ • Multi-modal transport  │
└──────────────────────────────┘    └───────────────────────────┘
```

#### 🏗️ Geospatial Architecture

```
LOCATION-BASED SERVICES:
┌─────────────────────────────────────────────────────────────┐
│                    GEOSPATIAL INDEXING                     │
│                                                             │
│ ┌─── QUAD TREE ────┐  ┌─── GEOHASH ────┐  ┌─── S2 CELLS ─┐ │
│ │ Recursive        │  │ Base32 encoding│  │ Google S2     │ │
│ │ subdivision      │  │ of lat/lng     │  │ Geometry      │ │
│ │ ┌─────┬─────┐   │  │ "9q5c8"        │  │ Library       │ │
│ │ │ NW  │ NE  │   │  │ Proximity      │  │ Hierarchical  │ │
│ │ ├─────┼─────┤   │  │ search         │  │ spatial cells │ │
│ │ │ SW  │ SE  │   │  └────────────────┘  └───────────────┘ │
│ │ └─────┴─────┘   │                                        │
│ └─────────────────┘                                        │
│                                                             │
│ DRIVER LOCATION UPDATES:                                    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 1. Driver app отправляет GPS координаты каждые 4 сек   │ │
│ │ 2. Location Service обновляет geospatial index         │ │
│ │ 3. Matching Service использует proximity search        │ │
│ │ 4. Real-time updates через WebSocket                   │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### 🎯 Matching Algorithm

```
DRIVER-RIDER MATCHING:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│ 1. PROXIMITY SEARCH                                         │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│    │ Get nearby  │─→│ Filter by   │─→│ Rank by score   │   │
│    │ drivers     │  │ availability│  │ (ETA + rating)  │   │
│    │ (radius 5km)│  │ & capacity  │  │                 │   │
│    └─────────────┘  └─────────────┘  └─────────────────┘   │
│                                                             │
│ 2. MATCHING SCORE CALCULATION                               │
│    Score = w1*Distance + w2*ETA + w3*DriverRating +        │
│           w4*AcceptanceRate + w5*CancellationRate           │
│                                                             │
│ 3. DISPATCH OPTIMIZATION                                    │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│    │ Hungarian   │  │ Greedy      │  │ Machine Learning│   │
│    │ Algorithm   │  │ Assignment  │  │ Based Matching  │   │
│    │ (Optimal)   │  │ (Fast)      │  │ (Predictive)    │   │
│    └─────────────┘  └─────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### 💰 Dynamic Pricing Engine

```
SURGE PRICING ALGORITHM:
┌─────────────────────────────────────────────────────────────┐
│                    SUPPLY & DEMAND                          │
│                                                             │
│ ┌─── DEMAND FACTORS ────┐  ┌─── SUPPLY FACTORS ──────────┐  │
│ │ • Active riders       │  │ • Available drivers        │  │
│ │ • Ride requests       │  │ • Driver utilization       │  │
│ │ │ • Wait times         │  │ • Historical patterns      │  │
│ │ • Events & weather    │  │ • Driver incentives        │  │
│ └───────────────────────┘  └────────────────────────────┘  │
│                                                             │
│ SURGE MULTIPLIER CALCULATION:                               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ base_price = base_fare + (distance * rate_per_km)      │ │
│ │                                                         │ │
│ │ surge_multiplier = max(1.0, min(5.0,                   │ │
│ │   demand_factor / supply_factor * locality_adjustment)) │ │
│ │                                                         │ │
│ │ final_price = base_price * surge_multiplier            │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ REAL-TIME PRICE UPDATES:                                    │
│ • Recalculate every 30 seconds                             │
│ • Smooth price transitions (max 20% change)                │
│ • Notify users of price changes                            │
│ • Historical price tracking                                │
└─────────────────────────────────────────────────────────────┘
```

#### 🗺️ Route Optimization

```sql
-- Trip Route Storage
CREATE TABLE trip_routes (
    trip_id BIGINT PRIMARY KEY,
    pickup_location GEOMETRY(POINT),
    dropoff_location GEOMETRY(POINT),
    optimized_route GEOMETRY(LINESTRING),
    estimated_duration_seconds INT,
    estimated_distance_meters INT,
    traffic_conditions JSON,
    route_alternatives JSON,
    created_at TIMESTAMP,
    
    SPATIAL INDEX idx_pickup (pickup_location),
    SPATIAL INDEX idx_dropoff (dropoff_location)
);

-- Driver Location Tracking (Hot data)
CREATE TABLE driver_locations (
    driver_id BIGINT,
    current_location GEOMETRY(POINT),
    heading INT, -- Compass direction 0-360
    speed_kmh DECIMAL(5,2),
    accuracy_meters INT,
    timestamp TIMESTAMP,
    
    PRIMARY KEY (driver_id, timestamp),
    SPATIAL INDEX idx_location_time (current_location, timestamp)
);
```

#### 📱 Real-time Tracking System

```
TRACKING ARCHITECTURE:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│ ┌─── DRIVER APP ───┐    ┌─── LOCATION ────┐    ┌─── RIDER ─┐ │
│ │ GPS Updates      │───→│    SERVICE      │───→│    APP    │ │
│ │ Every 4 seconds  │    │                 │    │           │ │
│ │                  │    │ • Geofencing    │    │ Live ETA  │ │
│ │ Battery-aware    │    │ • Route match   │    │ Map view  │ │
│ │ frequency adj.   │    │ • Anomaly det.  │    │ Progress  │ │
│ └──────────────────┘    └─────────────────┘    └───────────┘ │
│                                   │                         │
│ ┌─── STREAM PROCESSING ───────────▼─────────────────────────┐ │
│ │ Apache Kafka + Apache Flink                              │ │
│ │                                                           │ │
│ │ • Real-time location aggregation                         │ │
│ │ • ETA calculation updates                                │ │
│ │ • Geofence event detection                               │ │
│ │ • Route deviation alerts                                 │ │
│ │ • Driver behavior analysis                               │ │
│ └───────────────────────────────────────────────────────────┘ │
│                                   │                         │
│ ┌─── NOTIFICATIONS ───────────────▼─────────────────────────┐ │
│ │ • Push notifications (arrival, delays)                   │ │
│ │ • SMS updates for critical events                        │ │
│ │ • In-app real-time updates                               │ │
│ │ • Emergency contact notifications                        │ │
│ └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Глава 6.7: Финансовая система и платежи

#### 🎯 Функциональные требования
```
┌─── PAYMENT FEATURES ───┐        ┌─── COMPLIANCE & SECURITY ───┐
│ • Account Management   │        │ • PCI DSS compliance         │
│ • P2P Transfers        │        │ • AML/KYC verification       │
│ • Merchant Payments    │        │ • Fraud detection            │
│ • Multi-currency       │        │ • Audit trails              │
│ • International Wire   │        │ • Data encryption            │
│ • Credit/Debit Cards   │        │ • Regulatory reporting       │
└────────────────────────┘        └──────────────────────────────┘
```

#### 🏗️ Payment Processing Architecture

```
PAYMENT SYSTEM OVERVIEW:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ ┌─── CLIENT LAYER ───┐                                          │
│ │ Mobile Apps        │ ← SSL/TLS encryption                     │
│ │ Web Interface      │ ← API rate limiting                      │
│ │ Merchant APIs      │ ← Authentication/Authorization           │
│ └────────────────────┘                                          │
│                │                                                │
│ ┌──────────────▼──────────────┐                                 │
│ │        API GATEWAY          │ ← Request routing & validation  │
│ │    (Authentication &        │                                 │
│ │    Rate Limiting)           │                                 │
│ └──────────────┬──────────────┘                                 │
│                │                                                │
│ ┌─── PAYMENT SERVICES ────────▼─────────────────────────────────┐ │
│ │                                                               │ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │ │
│ │ │   Account   │ │  Payment    │ │      Fraud              │ │ │
│ │ │  Service    │ │ Processing  │ │    Detection            │ │ │
│ │ └─────────────┘ └─────────────┘ └─────────────────────────┘ │ │
│ │                                                               │ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │ │
│ │ │ Compliance  │ │   Ledger    │ │     Notification        │ │ │
│ │ │  Service    │ │  Service    │ │      Service            │ │ │
│ │ └─────────────┘ └─────────────┘ └─────────────────────────┘ │ │
│ └───────────────────────────────────────────────────────────────┘ │
│                │                                                │
│ ┌──────────────▼──────────────┐                                 │
│ │    EXTERNAL INTEGRATIONS    │                                 │
│ │                             │                                 │
│ │ • Card Networks (Visa/MC)   │ ← Payment processing            │
│ │ • Banks (ACH/Wire)          │ ← Account funding               │
│ │ • Crypto Exchanges          │ ← Digital currency             │
│ │ • Regulatory APIs           │ ← Compliance reporting          │
│ └─────────────────────────────┘                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 💾 Account & Ledger Design

**Double-Entry Bookkeeping:**
```sql
-- Accounts
CREATE TABLE accounts (
    account_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    account_type ENUM('checking', 'savings', 'credit', 'merchant'),
    currency CHAR(3),
    balance DECIMAL(20,8), -- Высокая точность для финансов
    available_balance DECIMAL(20,8), -- После pending transactions
    frozen_amount DECIMAL(20,8), -- Заблокированные средства
    status ENUM('active', 'frozen', 'closed'),
    created_at TIMESTAMP,
    
    INDEX idx_user (user_id),
    INDEX idx_currency (currency),
    CHECK (balance >= 0 OR account_type = 'credit')
);

-- Ledger Entries (Immutable transaction log)
CREATE TABLE ledger_entries (
    entry_id BIGINT PRIMARY KEY,
    transaction_id BIGINT,
    account_id BIGINT,
    amount DECIMAL(20,8), -- Положительное = дебет, отрицательное = кредит
    balance_after DECIMAL(20,8),
    entry_type ENUM('debit', 'credit'),
    description VARCHAR(500),
    reference_id VARCHAR(100), -- External transaction reference
    created_at TIMESTAMP,
    
    INDEX idx_account_time (account_id, created_at),
    INDEX idx_transaction (transaction_id),
    INDEX idx_reference (reference_id)
);

-- Transactions (Business logic layer)
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    from_account_id BIGINT,
    to_account_id BIGINT,
    amount DECIMAL(20,8),
    currency CHAR(3),
    transaction_type ENUM('transfer', 'payment', 'refund', 'fee'),
    status ENUM('pending', 'completed', 'failed', 'cancelled'),
    description VARCHAR(500),
    metadata JSON, -- Additional transaction details
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    INDEX idx_accounts (from_account_id, to_account_id),
    INDEX idx_status_time (status, created_at),
    INDEX idx_amount_currency (amount, currency)
);
```

#### 🔒 Security & Fraud Detection

```
FRAUD DETECTION PIPELINE:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ ┌─── REAL-TIME RULES ───┐   ┌─── ML MODELS ───┐                │
│ │                       │   │                 │                │
│ │ • Velocity checks     │   │ • Behavioral    │                │
│ │ • Geo-location       │   │   analysis      │                │
│ │ • Device fingerprint │   │ • Anomaly       │                │
│ │ • Amount thresholds  │   │   detection     │                │
│ │ • Blacklist check    │   │ • Risk scoring  │                │
│ │                       │   │                 │                │
│ └───────┬───────────────┘   └────────┬────────┘                │
│         │                            │                         │
│         └─────────┬────────────────────┘                         │
│                   │                                            │
│      ┌────────────▼─────────────┐                              │
│      │    DECISION ENGINE       │                              │
│      │                          │                              │
│      │ Risk Score: 0-100        │                              │
│      │ • 0-30: Auto approve     │                              │
│      │ • 31-70: Additional auth │                              │
│      │ • 71-100: Block/Review   │                              │
│      └────────────┬─────────────┘                              │
│                   │                                            │
│ ┌─── ACTIONS ─────▼─────────────────────────────────────────┐  │
│ │                                                           │  │
│ │ • Approve transaction                                     │  │
│ │ • Request additional authentication (2FA, SMS)           │  │
│ │ • Temporarily hold transaction for manual review         │  │
│ │ • Block transaction and freeze account                   │  │
│ │ • Generate compliance alert                              │  │
│ │                                                           │  │
│ └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

#### 🌍 International Transfers

```
CROSS-BORDER PAYMENT FLOW:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ 1. INITIATION                                                   │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│    │ Customer    │─→│ FX Rate     │─→│ Compliance Check    │   │
│    │ Request     │  │ Calculation │  │ (AML/Sanctions)     │   │
│    └─────────────┘  └─────────────┘  └─────────────────────┘   │
│                                                                 │
│ 2. ROUTING DECISION                                             │
│    ┌─────────────────────────────────────────────────────────┐ │
│    │ Route Selection Based On:                               │ │
│    │ • Destination country                                   │ │
│    │ • Amount & currency                                     │ │
│    │ • Speed requirements                                    │ │
│    │ • Cost optimization                                     │ │
│    │                                                         │ │
│    │ Options:                                                │ │
│    │ • SWIFT network (1-5 days)                             │ │
│    │ • Correspondent banking (2-3 days)                     │ │
│    │ • Digital corridors (minutes-hours)                    │ │
│    │ • Cryptocurrency rails (experimental)                  │ │
│    └─────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 3. EXECUTION & TRACKING                                         │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│    │ Fund        │─→│ Transfer    │─→│ Settlement &        │   │
│    │ Conversion  │  │ Execution   │  │ Confirmation        │   │
│    └─────────────┘  └─────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

#### 📊 Compliance & Reporting

```sql
-- AML Transaction Monitoring
CREATE TABLE aml_alerts (
    alert_id BIGINT PRIMARY KEY,
    transaction_id BIGINT,
    customer_id BIGINT,
    alert_type ENUM('velocity', 'amount', 'pattern', 'geography'),
    risk_score INT, -- 0-100
    alert_status ENUM('open', 'investigating', 'closed', 'escalated'),
    created_at TIMESTAMP,
    resolved_at TIMESTAMP,
    analyst_notes TEXT,
    
    INDEX idx_customer_time (customer_id, created_at),
    INDEX idx_status (alert_status),
    INDEX idx_risk_score (risk_score DESC)
);

-- Regulatory Reporting
CREATE TABLE regulatory_reports (
    report_id BIGINT PRIMARY KEY,
    report_type ENUM('SAR', 'CTR', 'FBAR', 'OFAC'),
    reporting_period DATE,
    jurisdiction CHAR(2), -- Country code
    file_path VARCHAR(500),
    submission_status ENUM('pending', 'submitted', 'acknowledged'),
    generated_at TIMESTAMP,
    submitted_at TIMESTAMP
);
```

#### 🚨 Практические задачи

**Задача 1: Idempotency для платежей**
```sql
-- Idempotency table для предотвращения duplicate payments
CREATE TABLE payment_idempotency (
    idempotency_key VARCHAR(100) PRIMARY KEY,
    transaction_id BIGINT,
    response_data JSON,
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    
    INDEX idx_expires (expires_at)
);

-- Example implementation
BEGIN TRANSACTION;
SELECT transaction_id FROM payment_idempotency 
WHERE idempotency_key = ? AND expires_at > NOW();

IF FOUND THEN
    RETURN cached_response;
ELSE
    -- Process payment
    INSERT INTO payment_idempotency VALUES (...);
    RETURN new_response;
END IF;
COMMIT;
```

**Задача 2: Eventual Consistency в распределенной системе**
```
SAGA PATTERN for PAYMENT PROCESSING:
┌─────────────────────────────────────────────────────────────┐
│ 1. Reserve funds       ──→ Success ──→ Continue            │
│    ↓ Failure                           ↓                   │
│    Compensate: Release reserve         │                   │
│                                        │                   │
│ 2. Process payment     ──→ Success ──→ Continue            │
│    ↓ Failure                           ↓                   │
│    Compensate: Refund & Release        │                   │
│                                        │                   │
│ 3. Update balances     ──→ Success ──→ Complete            │
│    ↓ Failure                                               │
│    Compensate: Reverse payment & Release                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Итоговые задания блока 6

### Финальные проекты (выберите 2 из 6)

**1. Социальная сеть с 1B пользователей**
- Полная архитектура с масштабированием
- Feed generation для celebrity пользователей
- Content moderation система
- Analytics и recommendation engine

**2. Глобальная видеоплатформа**
- Multi-region CDN стратегия
- Live streaming architecture
- Copyright detection система
- Monetization и ad serving

**3. E-commerce marketplace**
- Multi-vendor platform
- Real-time inventory с миллионами SKU
- Fraud detection для платежей
- International expansion strategy

**4. Enterprise search engine**
- Документооборот для корпораций
- Security и access control
- Multi-language support
- Advanced analytics

**5. Финтех платформа**
- Multi-currency wallet
- Cryptocurrency integration
- Regulatory compliance (global)
- Advanced fraud detection

**6. Smart city transportation**
- Multi-modal transport integration
- Real-time optimization
- Predictive demand forecasting
- Environmental impact tracking

### Критерии оценки

```
┌─── TECHNICAL EXCELLENCE (40%) ───┐
│ • Правильность архитектурных     │
│   решений                        │
│ • Handling edge cases            │
│ • Performance оптимизация        │
│ • Security considerations        │
└──────────────────────────────────┘

┌─── SCALABILITY (30%) ───┐
│ • Horizontal scaling     │
│ • Database partitioning  │
│ • Caching strategies     │
│ • Global distribution    │
└──────────────────────────┘

┌─── BUSINESS UNDERSTANDING (20%) ───┐
│ • Trade-off analysis              │
│ • Cost considerations              │
│ • Business requirements mapping   │
│ • Risk assessment                 │
└────────────────────────────────────┘

┌─── COMMUNICATION (10%) ───┐
│ • Clear diagrams          │
│ • Logical explanation     │
│ • Q&A handling            │
│ • Presentation skills     │
└───────────────────────────┘
```

### 📚 Рекомендуемые материалы

**Книги:**
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Building Microservices" - Sam Newman  
- "System Design Interview" - Alex Xu
- "High Performance MySQL" - Baron Schwartz

**Практические ресурсы:**
- AWS Architecture Center
- Google Cloud Architecture Framework
- Microservices.io patterns
- High Scalability blog

**Инструменты:**
- Draw.io для диаграмм
- Apache JMeter для load testing
- Docker для containerization
- Kubernetes для orchestration

---

## 🏆 Результаты блока

По завершении этого блока вы сможете:

✅ **Проектировать системы любой сложности** - от социальных сетей до финансовых платформ

✅ **Принимать обоснованные архитектурные решения** с учетом бизнес-требований и технических ограничений

✅ **Масштабировать системы** для обслуживания миллиардов пользователей

✅ **Оптимизировать производительность** с использованием современных паттернов и технологий

✅ **Обеспечивать безопасность** и соответствие регулятивным требованиям

✅ **Коммуницировать архитектурные решения** техническим и бизнес-аудиториям

**Следующий шаг:** Блок 7 - Экспертный уровень и архитектурное лидерство