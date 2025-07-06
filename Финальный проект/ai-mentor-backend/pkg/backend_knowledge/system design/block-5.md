# 🔐 System Design Block 5: Security and Authentication

```
████████╗██╗  ██╗███████╗    ██████╗ ██████╗  ██████╗ ████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗ 
╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
   ██║   ███████║█████╗      ██████╔╝██████╔╝██║   ██║   ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝
   ██║   ██╔══██║██╔══╝      ██╔═══╝ ██╔══██╗██║   ██║   ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
   ██║   ██║  ██║███████╗    ██║     ██║  ██║╚██████╔╝   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```

**📚 Продолжительность:** 2-3 недели  
**🎯 Цель:** Обеспечить безопасность проектируемых систем  
**⏱️ Временные затраты:** 8-12 часов в неделю

---

## 🗺️ Навигация по блоку

```
Week 20-21: Security Fundamentals
├── 5.1 Information Security Basics
└── 5.2 Authentication & Authorization

Week 22: Data & Infrastructure Protection  
├── 5.3 Encryption Strategies
├── 5.4 Rate Limiting & DDoS Protection
└── 5.5 Security by Design
```

---

## 📅 Week 20-21: Security Fundamentals

```
 ░▒▓█  SECURITY FOUNDATIONS  █▓▒░
═══════════════════════════════════════════════════════════════════════════════════
```

### 📖 Chapter 5.1: Information Security Basics in Systems

#### 🔍 **Theory (3 hours)**

##### 🛡️ **CIA Triad: The Foundation of Security**

```
         ┌─────────────────┐
         │   INFORMATION   │
         │    SECURITY     │
         └─────────┬───────┘
                   │
         ┌─────────┴─────────┐
         │                   │
    ┌────▼────┐    ┌────────▼────┐
    │ PEOPLE  │    │ TECHNOLOGY  │
    └─────────┘    └─────────────┘
```

**🔒 Confidentiality (Конфиденциальность)**
- Информация доступна только авторизованным пользователям
- Примеры нарушений: утечки данных, несанкционированный доступ
- Методы защиты: шифрование, контроль доступа

**✅ Integrity (Целостность)**
- Данные остаются неизменными и точными
- Примеры нарушений: модификация данных, corruption
- Методы защиты: хеширование, цифровые подписи

**🌐 Availability (Доступность)**
- Системы и данные доступны при необходимости
- Примеры нарушений: DDoS атаки, системные сбои
- Методы защиты: резервирование, балансировка нагрузки

---

##### 🎯 **Threat Modeling Process**

```
THREAT MODELING WORKFLOW
═══════════════════════════════════════════════════════════════════

Step 1: DEFINE ARCHITECTURE
┌─────────────────────────────────────┐
│  Web App  →  API Gateway  →  DB     │
│     ↓            ↓           ↓      │
│   Users      Auth Service   Cache   │
└─────────────────────────────────────┘

Step 2: IDENTIFY THREATS (STRIDE)
┌─────────────────┬─────────────────────────────────────┐
│ SPOOFING        │ Подмена идентичности пользователя   │
│ TAMPERING       │ Изменение данных в передаче        │
│ REPUDIATION     │ Отказ от совершенных действий       │
│ INFO DISCLOSURE │ Утечка конфиденциальной информации  │
│ DENIAL SERVICE  │ Недоступность сервиса               │
│ ELEVATION       │ Повышение привилегий                │
└─────────────────┴─────────────────────────────────────┘

Step 3: VULNERABILITY ANALYSIS
┌─────────────────────────────────────┐
│ • Слабые пароли                     │
│ • Незашифрованные соединения        │
│ • Отсутствие input validation       │
│ • Устаревшие компоненты             │
│ • Неправильная конфигурация         │
└─────────────────────────────────────┘

Step 4: COUNTERMEASURES
┌─────────────────────────────────────┐
│ • Multi-factor authentication       │
│ • HTTPS/TLS encryption              │
│ • Input sanitization               │
│ • Regular security updates         │
│ • Security hardening               │
└─────────────────────────────────────┘
```

---

##### 🚨 **OWASP Top 10 Security Risks**

```
🥇 OWASP TOP 10 - 2021 🥇
═══════════════════════════════════════════════════════════════════

1️⃣  BROKEN ACCESS CONTROL
    └── Пользователи получают доступ к ресурсам без авторизации

2️⃣  CRYPTOGRAPHIC FAILURES  
    └── Слабое шифрование или его отсутствие

3️⃣  INJECTION
    └── SQL, NoSQL, OS, LDAP injection атаки

4️⃣  INSECURE DESIGN
    └── Отсутствие security controls в дизайне

5️⃣  SECURITY MISCONFIGURATION
    └── Неправильные настройки безопасности

6️⃣  VULNERABLE COMPONENTS
    └── Использование компонентов с уязвимостями

7️⃣  IDENTIFICATION & AUTHENTICATION FAILURES
    └── Слабая аутентификация и управление сессиями

8️⃣  SOFTWARE & DATA INTEGRITY FAILURES
    └── Нарушение целостности ПО и данных

9️⃣  SECURITY LOGGING & MONITORING FAILURES
    └── Недостаточное логирование и мониторинг

🔟 SERVER-SIDE REQUEST FORGERY (SSRF)
    └── Принуждение сервера к выполнению запросов
```

---

##### 🛡️ **Defense in Depth Strategy**

```
MULTI-LAYERED SECURITY APPROACH
═══════════════════════════════════════════════════════════════════

      🌐 PERIMETER SECURITY
    ╔═══════════════════════════╗
    ║   Firewall & WAF          ║
    ╚═══════════════════════════╝
            │
      🏢 NETWORK SECURITY  
    ╔═══════════════════════════╗
    ║   IDS/IPS, VPN, Segm.     ║
    ╚═══════════════════════════╝
            │
      💻 HOST SECURITY
    ╔═══════════════════════════╗
    ║   Antivirus, Updates      ║
    ╚═══════════════════════════╝
            │
      📱 APPLICATION SECURITY
    ╔═══════════════════════════╗
    ║   Input Validation, Auth  ║
    ╚═══════════════════════════╝
            │
      💾 DATA SECURITY
    ╔═══════════════════════════╗
    ║   Encryption, Backup      ║
    ╚═══════════════════════════╝
```

---

#### 🛠️ **Practice (2 hours)**

##### **Exercise 1: Threat Modeling для веб-приложения**

**Сценарий:** Интернет-банкинг приложение

```
BANKING APP ARCHITECTURE
═══════════════════════════════════════════════════════════════════

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Mobile    │────│     Web     │────│   Admin     │
│    App      │    │  Frontend   │    │   Panel     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                  ┌─────────────┐
                  │ API Gateway │
                  └─────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
     │    Auth     │ │  Banking    │ │ Notification│
     │   Service   │ │   Service   │ │   Service   │
     └─────────────┘ └─────────────┘ └─────────────┘
              │            │            │
              └────────────┼────────────┘
                           │
                  ┌─────────────┐
                  │  Database   │
                  │   Cluster   │
                  └─────────────┘
```

**Задача:** Идентифицировать угрозы для каждого компонента используя STRIDE модель

**Template для анализа:**
```
COMPONENT: [Название компонента]
THREATS:
├── Spoofing: [Описание угрозы]
├── Tampering: [Описание угрозы] 
├── Repudiation: [Описание угрозы]
├── Information Disclosure: [Описание угрозы]
├── Denial of Service: [Описание угрозы]
└── Elevation of Privilege: [Описание угрозы]

MITIGATIONS:
└── [Список мер противодействия]
```

---

##### **Exercise 2: Security Checklist Development**

**Создать чеклист безопасности для нового микросервиса:**

```
🔐 MICROSERVICE SECURITY CHECKLIST
═══════════════════════════════════════════════════════════════════

AUTHENTICATION & AUTHORIZATION
□ Реализована многофакторная аутентификация
□ Используется принцип минимальных привилегий  
□ JWT токены имеют короткий срок жизни
□ Refresh токены хранятся безопасно

NETWORK SECURITY  
□ Все соединения используют HTTPS/TLS
□ Межсервисная коммуникация шифрована
□ Настроен корректный CORS
□ Используется service mesh для security

INPUT VALIDATION
□ Валидация всех входящих данных
□ Protection от injection атак
□ Rate limiting настроен
□ File upload безопасно обрабатывается

DATA PROTECTION
□ Чувствительные данные зашифрованы
□ PII данные обфусцированы в логах
□ Резервные копии зашифрованы
□ Secure deletion реализован

MONITORING & LOGGING
□ Security events логируются
□ Anomaly detection настроен
□ Alerts для security incidents
□ Log integrity защищена

INFRASTRUCTURE
□ Container images сканируются
□ Secrets management используется
□ Network segmentation применяется
□ Regular security updates
```

---

### 📖 Chapter 5.2: Authentication & Authorization

#### 🔍 **Theory (3 hours)**

##### 🔑 **Authentication vs Authorization**

```
AUTHENTICATION vs AUTHORIZATION
═══════════════════════════════════════════════════════════════════

🔐 AUTHENTICATION (AuthN)
┌─────────────────────────────────────┐
│ "Who are you?"                      │
│                                     │
│ • Verifies identity                 │
│ • Username/password                 │
│ • Biometrics                        │
│ • Multi-factor auth                 │
│ • Single sign-on                    │
└─────────────────────────────────────┘

🔒 AUTHORIZATION (AuthZ)  
┌─────────────────────────────────────┐
│ "What can you do?"                  │
│                                     │
│ • Verifies permissions              │
│ • Role-based access control         │
│ • Attribute-based access control    │
│ • Resource-based permissions        │
│ • Policy enforcement                │
└─────────────────────────────────────┘

FLOW EXAMPLE:
┌─────┐  AuthN   ┌─────┐  AuthZ   ┌─────┐
│User │ ───────→ │API  │ ───────→ │Data │
└─────┘          │Gate │          └─────┘
                 └─────┘
```

---

##### 🌊 **OAuth 2.0 Flows Deep Dive**

```
OAUTH 2.0 AUTHORIZATION CODE FLOW
═══════════════════════════════════════════════════════════════════

┌──────────┐                               ┌──────────────┐
│          │ 1. Authorization Request      │              │
│  Client  │ ────────────────────────────→ │ Authorization│
│   App    │                               │    Server    │
│          │ ←──────────────────────────── │              │
└──────────┘ 2. Authorization Grant        └──────────────┘
     │                                              │
     │ 3. Authorization Grant                       │
     │ ────────────────────────────────────────────┘
     │
     │ 4. Access Token Request
     │ ──────────────────────────→ ┌──────────────┐
     │                             │              │
     │ ←────────────────────────── │ Token Server │
     │ 5. Access Token Response    │              │
     │                             └──────────────┘
     │
     │ 6. Protected Resource Request
     │ ──────────────────────────→ ┌──────────────┐
     │                             │              │
     │ ←────────────────────────── │   Resource   │
       7. Protected Resource       │    Server    │
                                   └──────────────┘

GRANT TYPES COMPARISON:
┌────────────────┬─────────────┬─────────────┬─────────────┐
│ Grant Type     │ Use Case    │ Security    │ Complexity  │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ Authorization  │ Web Apps    │ High        │ High        │
│ Code           │             │             │             │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ Implicit       │ SPAs        │ Medium      │ Medium      │
│ (deprecated)   │             │             │             │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ Client         │ Server Apps │ High        │ Low         │
│ Credentials    │             │             │             │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ Resource Owner │ Trusted     │ Low         │ Low         │
│ Password       │ Apps        │             │             │
└────────────────┴─────────────┴─────────────┴─────────────┘
```

---

##### 🎫 **JWT Tokens: Structure and Usage**

```
JWT TOKEN STRUCTURE
═══════════════════════════════════════════════════════════════════

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│         HEADER          │         PAYLOAD         │        SIGNATURE        │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ {                       │ {                       │ HMACSHA256(             │
│   "alg": "HS256",       │   "sub": "1234567890",  │   base64UrlEncode(      │
│   "typ": "JWT"          │   "name": "John Doe",   │     header) + "." +     │
│ }                       │   "iat": 1516239022     │   base64UrlEncode(      │
│                         │ }                       │     payload),           │
│                         │                         │   secret)               │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘

JWT BEST PRACTICES:
┌─────────────────────────────────────────────────────────────────┐
│ ✅ DO's                        │ ❌ DON'Ts                      │
├────────────────────────────────┼────────────────────────────────┤
│ • Short expiration times       │ • Store sensitive data         │
│ • Use strong algorithms        │ • Use for session storage      │
│ • Validate all claims          │ • Client-side only validation  │
│ • Implement refresh tokens     │ • Weak signing secrets         │
│ • Rotate signing keys          │ • Long-lived tokens            │
└────────────────────────────────┴────────────────────────────────┘

TOKEN STORAGE COMPARISON:
┌─────────────────┬─────────────┬─────────────┬─────────────┐
│ Storage Type    │ Security    │ XSS Risk    │ CSRF Risk   │
├─────────────────┼─────────────┼─────────────┼─────────────┤
│ localStorage    │ Low         │ High        │ Low         │
│ sessionStorage  │ Medium      │ High        │ Low         │
│ httpOnly Cookie │ High        │ Low         │ High        │
│ Memory Only     │ High        │ Low         │ Low         │
└─────────────────┴─────────────┴─────────────┴─────────────┘
```

---

##### 🔐 **Single Sign-On (SSO) Architectures**

```
SSO ARCHITECTURE PATTERNS
═══════════════════════════════════════════════════════════════════

SAML-BASED SSO:
┌─────────────┐                        ┌─────────────┐
│             │ 1. Access Request      │             │
│   Browser   │ ─────────────────────→ │ Service     │
│             │                        │ Provider    │
│             │ 2. SAML Request        │ (SP)        │
│             │ ←───────────────────── │             │
└─────────────┘                        └─────────────┘
       │                                      │
       │ 3. Redirect to IdP                   │
       ↓                                      │
┌─────────────┐                               │
│             │ 4. Authentication             │
│ Identity    │ ←─────────────────────────────┘
│ Provider    │
│ (IdP)       │ 5. SAML Response
│             │ ─────────────────────────┐
└─────────────┘                          │
       │                                 ↓
       │ 6. Post SAML Response   ┌─────────────┐
       └───────────────────────→ │   Browser   │
                                 │             │
                                 │ 7. Access   │
                                 │ Granted     │
                                 └─────────────┘

OIDC-BASED SSO:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │             │    │             │
│   Client    │────│ OpenID      │────│ Resource    │
│ Application │    │ Provider    │    │ Server      │
│             │    │ (OP)        │    │             │
└─────────────┘    └─────────────┘    └─────────────┘

BENEFITS:
• Enhanced user experience
• Centralized access control  
• Reduced password fatigue
• Improved security posture
• Simplified compliance

CHALLENGES:
• Single point of failure
• Complex implementation
• Identity provider dependency
• Token management complexity
```

---

#### 🛠️ **Practice (3 hours)**

##### **Exercise 1: OAuth2 Flow Design**

**Сценарий:** Дизайн OAuth2 flow для мобильного приложения банка

```
MOBILE BANKING APP OAUTH2 DESIGN
═══════════════════════════════════════════════════════════════════

REQUIREMENTS:
• High security standards
• Offline capability
• Token refresh mechanism
• Biometric authentication
• Device registration

PROPOSED FLOW:
┌─────────────┐                    ┌─────────────┐
│   Mobile    │ 1. PKCE Request    │             │
│    App      │ ─────────────────→ │ Auth Server │
│             │                    │             │
│             │ 2. Auth Code       │             │
│             │ ←───────────────── │             │
└─────────────┘                    └─────────────┘
       │                                  │
       │ 3. Token Exchange                │
       │ + Device Fingerprint             │
       │ ─────────────────────────────────┘
       │
       │ 4. Access + Refresh Tokens
       │ ←─────────────────────────
       │
       │ 5. Biometric Validation
       │ (Local)
       │
       │ 6. API Calls with Access Token
       │ ─────────────────────────→ ┌─────────────┐
       │                            │ Banking API │
       │ ←───────────────────────── │             │
         7. Protected Resources     └─────────────┘

SECURITY ENHANCEMENTS:
• PKCE (Proof Key for Code Exchange)
• Device binding with certificates
• Biometric authentication integration
• Short-lived access tokens (15 min)
• Longer refresh tokens with rotation
• Certificate pinning
```

**Задание:** Спроектировать полный OAuth2 flow с учетом всех security considerations

---

##### **Exercise 2: JWT Implementation Strategy**

```
JWT STRATEGY FOR MICROSERVICES
═══════════════════════════════════════════════════════════════════

TOKEN STRUCTURE:
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "key-id-2024"
  },
  "payload": {
    "iss": "https://auth.company.com",
    "sub": "user-12345",
    "aud": ["api.company.com"],
    "exp": 1640995200,
    "iat": 1640991600,
    "jti": "token-uuid",
    "scope": ["read:profile", "write:orders"],
    "role": "customer",
    "permissions": [
      "orders:read",
      "profile:update"
    ]
  }
}

MICROSERVICE VALIDATION:
┌─────────────────────────────────────────────────────────────────┐
│ SERVICE A (Orders)                                              │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 1. Receive JWT in Authorization header                      │ │
│ │ 2. Validate signature with public key                      │ │
│ │ 3. Check expiration time                                    │ │
│ │ 4. Verify audience contains service URL                    │ │
│ │ 5. Check required permissions: "orders:read"               │ │
│ │ 6. Process request or return 403                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

TOKEN REFRESH STRATEGY:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │    │ Auth Server │    │ Microservice│
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       │ 1. API Call       │                   │
       │ ─────────────────────────────────────→│
       │                   │                   │
       │                   │ 2. 401 Expired   │
       │ ←─────────────────────────────────────│
       │                   │                   │
       │ 3. Refresh Token  │                   │
       │ ─────────────────→│                   │
       │                   │                   │
       │ 4. New Tokens     │                   │
       │ ←─────────────────│                   │
       │                   │                   │
       │ 5. Retry API Call │                   │
       │ ─────────────────────────────────────→│
       │                   │                   │
       │ 6. Success        │                   │
       │ ←─────────────────────────────────────│
```

**Задание:** Создать JWT validation middleware для микросервиса с обработкой всех edge cases

---

## 📅 Week 22: Data & Infrastructure Protection

```
 ░▒▓█  PROTECTION & DEFENSE  █▓▒░
═══════════════════════════════════════════════════════════════════════════════════
```

### 📖 Chapter 5.3: Encryption - Data at Rest and in Transit

#### 🔍 **Theory (2 hours)**

##### 🔐 **Symmetric vs Asymmetric Encryption**

```
ENCRYPTION TYPES COMPARISON
═══════════════════════════════════════════════════════════════════

SYMMETRIC ENCRYPTION
┌─────────────────────────────────────────────────────────────────┐
│                        SHARED SECRET                           │
│               ┌─────────────────────────┐                       │
│      Encrypt  │                         │  Decrypt             │
│ Data ───────→ │    AES-256 Algorithm    │ ←─────── Data        │
│               │                         │                      │
│               └─────────────────────────┘                       │
│                                                                 │
│ ✅ PROS:                          ❌ CONS:                      │
│ • Fast performance                • Key distribution problem    │
│ • Low computational overhead      • Key management complexity   │
│ • Suitable for large data        • Same key for encrypt/decrypt │
│                                                                 │
│ 🔑 ALGORITHMS: AES, DES, 3DES, ChaCha20                        │
└─────────────────────────────────────────────────────────────────┘

ASYMMETRIC ENCRYPTION  
┌─────────────────────────────────────────────────────────────────┐
│                    PUBLIC/PRIVATE KEY PAIR                     │
│                                                                 │
│ ┌─────────────┐              ┌─────────────┐                   │
│ │ Public Key  │    Encrypt   │ Private Key │                   │
│ │             │ ───────────→ │             │                   │
│ │   (Share)   │              │ (Keep Safe) │                   │
│ └─────────────┘              └─────────────┘                   │
│                                                                 │
│ ✅ PROS:                          ❌ CONS:                      │
│ • No key sharing needed           • Slow performance           │
│ • Digital signatures possible     • High computational cost    │
│ • Key distribution solved         • Not suitable for large data│
│                                                                 │
│ 🔑 ALGORITHMS: RSA, ECC, DSA, ElGamal                          │
└─────────────────────────────────────────────────────────────────┘

HYBRID APPROACH (Best Practice):
┌─────────────────────────────────────────────────────────────────┐
│ 1. Generate random symmetric key (AES)                         │
│ 2. Encrypt data with symmetric key (fast)                      │
│ 3. Encrypt symmetric key with public key (secure)              │
│ 4. Send both encrypted data and encrypted key                  │
│ 5. Receiver decrypts key with private key                      │
│ 6. Use decrypted key to decrypt data                           │
└─────────────────────────────────────────────────────────────────┘
```

---

##### 🌐 **TLS/SSL Implementation**

```
TLS HANDSHAKE PROCESS
═══════════════════════════════════════════════════════════════════

┌─────────────┐                               ┌─────────────┐
│   Client    │                               │   Server    │
└─────────────┘                               └─────────────┘
       │                                              │
       │ 1. ClientHello                               │
       │ ────────────────────────────────────────────→│
       │   • TLS version                              │
       │   • Cipher suites                            │
       │   • Random number                            │
       │                                              │
       │                                              │
       │ 2. ServerHello                               │
       │ ←────────────────────────────────────────────│
       │   • Selected cipher suite                    │
       │   • Server random                            │
       │   • Certificate                              │
       │                                              │
       │ 3. Client Key Exchange                       │
       │ ────────────────────────────────────────────→│
       │   • Pre-master secret (encrypted)           │
       │                                              │
       │ 4. Change Cipher Spec + Finished             │
       │ ←──────────────────────────────────────────→ │
       │                                              │
       │ 5. Encrypted Application Data                │
       │ ←──────────────────────────────────────────→ │

TLS CONFIGURATION BEST PRACTICES:
┌─────────────────────────────────────────────────────────────────┐
│ TLS VERSION:                                                    │
│ ✅ TLS 1.3 (preferred)                                          │
│ ✅ TLS 1.2 (acceptable)                                         │
│ ❌ TLS 1.1, 1.0, SSL (deprecated)                              │
│                                                                 │
│ CIPHER SUITES (TLS 1.3):                                       │
│ • TLS_AES_256_GCM_SHA384                                        │
│ • TLS_CHACHA20_POLY1305_SHA256                                  │
│ • TLS_AES_128_GCM_SHA256                                        │
│                                                                 │
│ CERTIFICATE:                                                    │
│ • RSA 2048+ or ECC P-256+                                       │
│ • SHA-256 signature                                             │
│ • Valid certificate chain                                       │
│ • Proper hostname verification                                  │
│                                                                 │
│ ADDITIONAL SECURITY:                                            │
│ • HTTP Strict Transport Security (HSTS)                        │
│ • Certificate pinning                                           │
│ • Perfect Forward Secrecy (PFS)                                 │
│ • OCSP stapling                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

##### 💾 **Database Encryption Strategies**

```
DATABASE ENCRYPTION LAYERS
═══════════════════════════════════════════════════════════════════

APPLICATION LAYER ENCRYPTION:
┌─────────────────────────────────────────────────────────────────┐
│ Application Code                                                │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ encrypt(sensitive_data, app_key) → encrypted_data           │ │
│ │ store(encrypted_data) → database                            │ │
│ │                                                             │ │
│ │ ✅ PROS:                  ❌ CONS:                           │ │
│ │ • Fine-grained control    • Performance overhead            │ │
│ │ • Selective encryption    • Key management complexity       │ │
│ │ • App-level key mgmt      • Vulnerable to memory attacks   │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

DATABASE LAYER ENCRYPTION (TDE):
┌─────────────────────────────────────────────────────────────────┐
│ Database Engine                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Automatic encryption/decryption                             │ │
│ │ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │ │
│ │ │  Raw Data   │ →  │ Encrypted   │ →  │  Storage    │      │ │
│ │ │             │    │   Pages     │    │             │      │ │
│ │ └─────────────┘    └─────────────┘    └─────────────┘      │ │
│ │                                                             │ │
│ │ ✅ PROS:                  ❌ CONS:                           │ │
│ │ • Transparent operation   • All-or-nothing encryption       │ │
│ │ • No app changes needed   • Limited granularity             │ │
│ │ • Good performance        • Key management still complex    │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

FIELD-LEVEL ENCRYPTION:
┌─────────────────────────────────────────────────────────────────┐
│ Table: users                                                    │
│ ┌───────┬──────────────────┬─────────────────────────────────┐  │
│ │ id    │ name             │ ssn                             │  │
│ ├───────┼──────────────────┼─────────────────────────────────┤  │
│ │ 1     │ John Doe         │ AES256_ENCRYPT("123-45-6789")  │  │
│ │ 2     │ Jane Smith       │ AES256_ENCRYPT("987-65-4321")  │  │
│ └───────┴──────────────────┴─────────────────────────────────┘  │
│                                                                 │
│ ✅ PROS:                  ❌ CONS:                               │
│ • Granular encryption     • Complex query operations           │
│ • Selective protection    • Index limitations                  │
│ • Compliance friendly     • Performance impact on queries     │
└─────────────────────────────────────────────────────────────────┘

ENCRYPTION KEY HIERARCHY:
┌─────────────────────────────────────────────────────────────────┐
│                    KEY MANAGEMENT                               │
│                                                                 │
│     ┌─────────────────────────────────────────────────────┐     │
│     │              MASTER KEY                             │     │
│     │         (HSM or Key Management Service)             │     │
│     └─────────────────────┬───────────────────────────────┘     │
│                           │                                     │
│            ┌──────────────┴──────────────┐                      │
│            │                             │                      │
│     ┌──────▼──────┐                ┌────▼─────┐                │
│     │ DEK (Data   │                │ KEK (Key │                │
│     │ Encryption  │                │ Encrypt  │                │
│     │ Key)        │                │ Key)     │                │
│     └─────────────┘                └──────────┘                │
│            │                             │                      │
│     ┌──────▼──────┐                ┌────▼─────┐                │
│     │ Encrypted   │                │ Encrypted│                │
│     │ Data        │                │ DEKs     │                │
│     └─────────────┘                └──────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

---

##### 🔐 **Key Management Systems**

```
ENTERPRISE KEY MANAGEMENT ARCHITECTURE
═══════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│                    KEY MANAGEMENT SERVICE                      │
│                                                                 │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│ │   Key       │  │    Key      │  │    Key      │              │
│ │ Generation  │  │  Storage    │  │ Rotation    │              │
│ │             │  │    (HSM)    │  │             │              │
│ └─────────────┘  └─────────────┘  └─────────────┘              │
│        │                │                │                     │
│        └────────────────┼────────────────┘                     │
│                         │                                      │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│ │   Access    │  │   Audit     │  │  Policy     │              │
│ │  Control    │  │   Logging   │  │ Management  │              │
│ └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌─────▼──────┐ ┌──────▼───────┐
│  Application   │ │ Database   │ │ File System  │
│   Services     │ │ Services   │ │   Services   │
└────────────────┘ └────────────┘ └──────────────┘

KEY LIFECYCLE:
┌─────────────────────────────────────────────────────────────────┐
│ 1. GENERATION                                                   │
│    • Cryptographically secure random generation                │
│    • Appropriate key strength (AES-256, RSA-2048+)            │
│    • Hardware Security Module (HSM) generation                 │
│                                                                 │
│ 2. DISTRIBUTION                                                 │
│    • Secure key exchange protocols                             │
│    • Out-of-band key delivery                                  │
│    • Key splitting for high-value keys                         │
│                                                                 │
│ 3. STORAGE                                                      │
│    • Hardware Security Modules (HSM)                           │
│    • Key encryption keys (KEK)                                 │
│    • Access control and authentication                         │
│                                                                 │
│ 4. USAGE                                                        │
│    • Principle of least privilege                              │
│    • Usage auditing and monitoring                             │
│    • Rate limiting and anomaly detection                       │
│                                                                 │
│ 5. ROTATION                                                     │
│    • Regular automated rotation                                │
│    • Emergency rotation procedures                             │
│    • Backward compatibility during transition                  │
│                                                                 │
│ 6. DESTRUCTION                                                  │
│    • Secure key deletion                                       │
│    • Compliance with retention policies                        │
│    • Cryptographic shredding                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

#### 🛠️ **Practice (2 hours)**

##### **Exercise 1: Encryption Strategy Design**

```
SCENARIO: Healthcare Data Platform
═══════════════════════════════════════════════════════════════════

REQUIREMENTS:
• HIPAA compliance
• Patient data protection  
• Doctor-patient confidentiality
• Audit trail requirements
• Performance considerations

DATA CLASSIFICATION:
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Data Type       │ Sensitivity     │ Encryption      │ Key Management  │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Medical Records │ Critical        │ AES-256-GCM     │ HSM + Per-      │
│                 │                 │ Field-level     │ Patient Keys    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Personal Info   │ High            │ AES-256-CBC     │ Application     │
│ (Name, Address) │                 │ Column-level    │ Master Key      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Medical Images  │ High            │ AES-256-CTR     │ Object Storage  │
│ (X-rays, MRI)   │                 │ File-level      │ Encryption      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Metadata        │ Medium          │ TLS in Transit  │ Standard        │
│ (Timestamps)    │                 │ DB-level at rest│ Database Keys   │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

ARCHITECTURE DESIGN:
┌─────────────────────────────────────────────────────────────────┐
│ Web App → API Gateway → Microservices → Encrypted Database     │
│   ↑           ↑             ↑               ↑                   │
│  TLS       mTLS +        JWT +          TDE + Field           │
│         API Keys      Field Encrypt     Encryption            │
└─────────────────────────────────────────────────────────────────┘
```

**Задание:** Спроектировать полную encryption strategy с учетом compliance требований

---

### 📖 Chapter 5.4: Rate Limiting & DDoS Protection

#### 🔍 **Theory (2 hours)**

##### 🚦 **Rate Limiting Algorithms**

```
RATE LIMITING ALGORITHMS COMPARISON
═══════════════════════════════════════════════════════════════════

1. TOKEN BUCKET
┌─────────────────────────────────────────────────────────────────┐
│         ┌─────────────────────────────────────┐                 │
│         │            TOKEN BUCKET             │                 │
│         │  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐    │                 │
│ Refill  │  │ T │ │ T │ │ T │ │ T │ │ T │    │ Request         │
│ Rate ──→│  └───┘ └───┘ └───┘ └───┘ └───┘    │ ←─── Consumer   │
│         │        Capacity: 5 tokens        │                 │
│         └─────────────────────────────────────┘                 │
│                                                                 │
│ ✅ PROS:                          ❌ CONS:                      │
│ • Allows bursts up to capacity    • Memory overhead per user   │
│ • Smooth traffic distribution     • Complex state management   │
│ • Good for bursty traffic         • Token bucket size tuning   │
│                                                                 │
│ ALGORITHM:                                                      │
│ if (tokens >= request_cost):                                    │
│     tokens -= request_cost                                      │
│     allow_request()                                             │
│ else:                                                           │
│     reject_request()                                            │
└─────────────────────────────────────────────────────────────────┘

2. LEAKY BUCKET
┌─────────────────────────────────────────────────────────────────┐
│                 LEAKY BUCKET                                    │
│         ┌─────────────────────────────────────┐                 │
│         │ ████████████████████████████████    │ ← Incoming      │
│ Output  │ ████████████████████████████████    │   Requests      │
│ Rate ←──│ ████████████████████████████████    │                 │
│ (Fixed) │ ████████████████████████████████    │                 │
│         │ ████████████████████████████████    │                 │
│         └─────────────────┬───────────────────┘                 │
│                           │ Constant Leak Rate                  │
│                           ↓                                     │
│                                                                 │
│ ✅ PROS:                          ❌ CONS:                      │
│ • Smooth, constant output rate    • No burst allowance         │
│ • Simple implementation           • May drop valid requests     │
│ • Protects downstream services    • Less flexible than token   │
│                                                                 │
│ ALGORITHM:                                                      │
│ if (queue.size() < bucket_size):                                │
│     queue.add(request)                                          │
│ else:                                                           │
│     drop_request()                                              │
│                                                                 │
│ // Process queue at fixed rate                                  │
│ process_queue_at_rate(output_rate)                              │
└─────────────────────────────────────────────────────────────────┘

3. SLIDING WINDOW LOG
┌─────────────────────────────────────────────────────────────────┐
│               SLIDING WINDOW LOG                                │
│                                                                 │
│ Window: Last 60 seconds                                         │
│ ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐              │
│ │ R │ R │   │ R │   │ R │ R │   │ R │   │   │NOW│              │
│ └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘              │
│  55  50  45  40  35  30  25  20  15  10   5   0                │
│                                                                 │
│ Count requests in sliding window: 6 requests                    │
│ Limit: 10 requests/minute → ALLOW                               │
│                                                                 │
│ ✅ PROS:                          ❌ CONS:                      │
│ • Precise rate limiting           • High memory usage          │
│ • No boundary effects             • Complex log management     │
│ • Accurate request tracking       • Performance overhead       │
│                                                                 │
│ ALGORITHM:                                                      │
│ current_time = now()                                            │
│ window_start = current_time - window_size                       │
│ count = log.count_requests_since(window_start)                  │
│ if (count < limit):                                             │
│     log.add_request(current_time)                               │
│     allow_request()                                             │
│ else:                                                           │
│     reject_request()                                            │
└─────────────────────────────────────────────────────────────────┘

4. SLIDING WINDOW COUNTER
┌─────────────────────────────────────────────────────────────────┐
│             SLIDING WINDOW COUNTER                              │
│                                                                 │
│ Previous Window    Current Window                               │
│ ┌─────────────────┬─────────────────┐                          │
│ │ 12 requests     │ 8 requests      │                          │
│ │ (minute N-1)    │ (minute N)      │                          │
│ └─────────────────┴─────────────────┘                          │
│                   ↑                                            │
│              30 seconds into                                    │
│              current window                                     │
│                                                                 │
│ Estimated count = (12 * 0.5) + 8 = 14 requests                 │
│ Limit: 20 requests/minute → ALLOW                               │
│                                                                 │
│ ✅ PROS:                          ❌ CONS:                      │
│ • Memory efficient                • Approximation only          │
│ • Good performance                • Edge case inaccuracies      │
│ • Reasonable accuracy             • Burst at window boundaries  │
│                                                                 │
│ ALGORITHM:                                                      │
│ prev_count = get_count(previous_window)                         │
│ curr_count = get_count(current_window)                          │
│ time_in_curr = (now() % window_size) / window_size              │
│ estimated = prev_count * (1 - time_in_curr) + curr_count       │
│ if (estimated < limit):                                         │
│     increment_count(current_window)                             │
│     allow_request()                                             │
│ else:                                                           │
│     reject_request()                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

##### 🛡️ **DDoS Attack Types and Protection**

```
DDOS ATTACK CLASSIFICATION
═══════════════════════════════════════════════════════════════════

LAYER 3/4 ATTACKS (Network/Transport):
┌─────────────────────────────────────────────────────────────────┐
│ SYN FLOOD ATTACK                                                │
│ ┌─────────────┐              ┌─────────────┐                    │
│ │ Attacker    │   SYN Flood  │   Server    │                    │
│ │ (Spoofed)   │ ────────────→│             │                    │
│ │             │              │ SYN-RCVD    │                    │
│ │ No Response │              │ State Full  │                    │
│ └─────────────┘              └─────────────┘                    │
│                                                                 │
│ IMPACT: TCP connection table exhaustion                         │
│ MITIGATION:                                                     │
│ • SYN cookies                                                   │
│ • Rate limiting SYN packets                                     │
│ • Increase connection table size                                │
│ • SYN proxy/firewall                                            │
│                                                                 │
│ UDP FLOOD ATTACK                                                │
│ High volume of UDP packets to random ports                      │
│ MITIGATION:                                                     │
│ • UDP rate limiting                                             │
│ • Port-based filtering                                          │
│ • Upstream provider filtering                                   │
└─────────────────────────────────────────────────────────────────┘

LAYER 7 ATTACKS (Application):
┌─────────────────────────────────────────────────────────────────┐
│ HTTP FLOOD ATTACK                                               │
│ ┌─────────────┐              ┌─────────────┐                    │
│ │ Botnet      │   HTTP GET   │ Web Server  │                    │
│ │ 10,000 bots │ ────────────→│             │                    │
│ │             │   Requests   │ Overloaded  │                    │
│ └─────────────┘              └─────────────┘                    │
│                                                                 │
│ CHARACTERISTICS:                                                │
│ • Legitimate-looking HTTP requests                              │
│ • Targets expensive operations                                  │
│ • Hard to distinguish from real traffic                        │
│                                                                 │
│ SLOWLORIS ATTACK                                                │
│ Keeps many connections open with slow HTTP requests             │
│ MITIGATION:                                                     │
│ • Connection timeouts                                           │
│ • Request header timeouts                                       │
│ • Connection limits per IP                                      │
│ • Reverse proxy buffering                                       │
└─────────────────────────────────────────────────────────────────┘

AMPLIFICATION ATTACKS:
┌─────────────────────────────────────────────────────────────────┐
│ DNS AMPLIFICATION                                               │
│                                                                 │
│ ┌─────────────┐              ┌─────────────┐              ┌──── │
│ │ Attacker    │    Small     │ DNS Server  │     Large    │ Vic │
│ │             │ ───────────→ │ (Open       │ ───────────→ │ tim │
│ │ Spoofed IP  │   Query      │ Resolver)   │   Response   │     │
│ │ = Victim    │              │             │              │     │
│ └─────────────┘              └─────────────┘              └──── │
│                                                                 │
│ AMPLIFICATION RATIO: Up to 179:1 for DNS                       │
│                                                                 │
│ OTHER AMPLIFICATION PROTOCOLS:                                  │
│ • NTP (556:1 ratio)                                             │
│ • SSDP (30:1 ratio)                                             │
│ • Memcached (51,000:1 ratio)                                    │
│                                                                 │
│ MITIGATION:                                                     │
│ • Disable open resolvers                                        │
│ • Source IP validation (BCP 38)                                │
│ • Rate limiting responses                                       │
│ • Ingress filtering                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

##### 🛡️ **DDoS Protection Architecture**

```
LAYERED DDOS PROTECTION ARCHITECTURE
═══════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│                      INTERNET                                   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│               LAYER 1: ISP/TRANSIT                              │
│ • Blackhole routing                                             │
│ • Upstream filtering                                            │
│ • Traffic scrubbing centers                                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│               LAYER 2: CDN/CLOUD                                │
│ • Anycast network                                               │
│ • Geographic distribution                                       │
│ • Automatic traffic filtering                                   │
│ • Rate limiting at edge                                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│               LAYER 3: FIREWALL/WAF                             │
│ • Stateful packet inspection                                    │
│ • Application layer filtering                                   │
│ • Geo-blocking                                                  │
│ • Signature-based detection                                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│               LAYER 4: LOAD BALANCER                            │
│ • Health checks                                                 │
│ • Connection limits                                             │
│ • Failover mechanisms                                           │
│ • SSL termination                                               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│               LAYER 5: APPLICATION                              │
│ • Rate limiting                                                 │
│ • CAPTCHA challenges                                            │
│ • Behavioral analysis                                           │
│ • Circuit breakers                                              │
└─────────────────────────────────────────────────────────────────┘

DETECTION METHODS:
┌─────────────────────────────────────────────────────────────────┐
│ TRAFFIC ANALYSIS                                                │
│ • Sudden traffic spikes                                         │
│ • Unusual request patterns                                      │
│ • Geographic anomalies                                          │
│ • Protocol distribution changes                                 │
│                                                                 │
│ BEHAVIORAL ANALYSIS                                             │
│ • Request frequency per IP                                      │
│ • User-agent patterns                                           │
│ • Session behavior analysis                                     │
│ • Referrer header analysis                                      │
│                                                                 │
│ REPUTATION ANALYSIS                                             │
│ • IP reputation databases                                       │
│ • Known botnet IPs                                              │
│ • Tor exit node detection                                       │
│ • Proxy/VPN detection                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

#### 🛠️ **Practice (2 hours)**

##### **Exercise 1: Rate Limiting Implementation**

```
API RATE LIMITING DESIGN
═══════════════════════════════════════════════════════════════════

REQUIREMENTS:
• Different limits for different user tiers
• Burst allowance for premium users  
• Graceful degradation
• Redis-based distributed limiting

IMPLEMENTATION STRATEGY:
┌─────────────────────────────────────────────────────────────────┐
│ USER TIERS & LIMITS                                             │
│ ┌─────────────────┬─────────────────┬─────────────────────────┐ │
│ │ Tier            │ Rate Limit      │ Burst Allowance         │ │
│ ├─────────────────┼─────────────────┼─────────────────────────┤ │
│ │ Free            │ 100 req/hour    │ 10 req/minute           │ │
│ │ Basic           │ 1000 req/hour   │ 50 req/minute           │ │
│ │ Premium         │ 10000 req/hour  │ 200 req/minute          │ │
│ │ Enterprise      │ 100000 req/hour │ 1000 req/minute         │ │
│ └─────────────────┴─────────────────┴─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

REDIS DATA STRUCTURE:
Key: rate_limit:{user_id}:{window}
Value: {
  "count": 45,
  "reset_time": 1640995200,
  "tier": "premium",
  "burst_used": 12
}

ALGORITHM PSEUDOCODE:
function checkRateLimit(userId, endpoint):
    userTier = getUserTier(userId)
    limits = getTierLimits(userTier)
    
    // Check hourly limit
    hourlyKey = f"rate_limit:{userId}:hour:{currentHour}"
    hourlyCount = redis.get(hourlyKey) or 0
    
    if (hourlyCount >= limits.hourly):
        return RATE_LIMITED
    
    // Check burst limit (minute window)
    minuteKey = f"rate_limit:{userId}:minute:{currentMinute}"
    minuteCount = redis.get(minuteKey) or 0
    
    if (minuteCount >= limits.burst):
        return BURST_LIMITED
    
    // Increment counters with expiration
    redis.incr(hourlyKey)
    redis.expire(hourlyKey, 3600)  // 1 hour
    redis.incr(minuteKey) 
    redis.expire(minuteKey, 60)    // 1 minute
    
    return ALLOWED

RESPONSE HEADERS:
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 955
X-RateLimit-Reset: 1640995200
X-RateLimit-Burst: 50
X-RateLimit-Burst-Remaining: 38
```

**Задание:** Реализовать distributed rate limiter с поддержкой multiple tiers и graceful degradation

---

##### **Exercise 2: DDoS Protection Plan**

```
E-COMMERCE PLATFORM DDOS PROTECTION
═══════════════════════════════════════════════════════════════════

THREAT ASSESSMENT:
┌─────────────────────────────────────────────────────────────────┐
│ HIGH-VALUE TARGETS                                              │
│ • Login page (credential stuffing)                             │
│ • Search functionality (expensive queries)                     │
│ • Checkout process (business impact)                           │
│ • Product catalog (database load)                              │
│ • API endpoints (partner integrations)                         │
│                                                                 │
│ ATTACK SCENARIOS                                                │
│ • Black Friday traffic surge + attack                          │
│ • Competitor sabotage during launches                          │
│ • Extortion attempts                                            │
│ • State-sponsored attacks                                       │
└─────────────────────────────────────────────────────────────────┘

PROTECTION LAYERS:
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 1: UPSTREAM (ISP/CLOUD)                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ • Cloudflare/AWS Shield Advanced                            │ │
│ │ • 100 Tbps mitigation capacity                              │ │
│ │ • Anycast network (200+ locations)                         │ │
│ │ • Automatic DDoS detection                                  │ │
│ │ • BGP blackhole routing                                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ LAYER 2: APPLICATION FIREWALL                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ • WAF rules for common attacks                              │ │
│ │ • Geo-blocking (high-risk countries)                       │ │
│ │ • Rate limiting per IP/session                              │ │
│ │ • Bot detection and CAPTCHA                                 │ │
│ │ • JavaScript challenge for browsers                         │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ LAYER 3: APPLICATION LEVEL                                     │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ • API rate limiting                                         │ │
│ │ • Circuit breakers for backend services                     │ │
│ │ • Cached responses for expensive operations                 │ │
│ │ • Queue-based request processing                            │ │
│ │ • Graceful degradation modes                                │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

INCIDENT RESPONSE PLAN:
┌─────────────────────────────────────────────────────────────────┐
│ DETECTION (< 2 minutes)                                         │
│ • Automated monitoring alerts                                   │
│ • Traffic anomaly detection                                     │
│ • Performance degradation alerts                               │
│ • Customer complaints                                           │
│                                                                 │
│ ASSESSMENT (< 5 minutes)                                        │
│ • Identify attack type and source                              │
│ • Assess business impact                                        │
│ • Determine mitigation strategy                                 │
│ • Activate incident response team                               │
│                                                                 │
│ MITIGATION (< 10 minutes)                                       │
│ • Enable aggressive rate limiting                               │
│ • Activate WAF challenge mode                                   │
│ • Scale up infrastructure                                       │
│ • Implement geo-blocking if needed                              │
│ • Contact upstream providers                                    │
│                                                                 │
│ RECOVERY (< 30 minutes)                                         │
│ • Monitor attack cessation                                      │
│ • Gradually remove restrictions                                 │
│ • Validate service functionality                                │
│ • Document incident details                                     │
│                                                                 │
│ POST-INCIDENT (< 24 hours)                                      │
│ • Root cause analysis                                           │
│ • Update protection rules                                       │
│ • Customer communication                                        │
│ • Lessons learned documentation                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 📖 Chapter 5.5: Security by Design Principles

#### 🔍 **Theory (2 hours)**

##### 🔐 **Principle of Least Privilege**

```
LEAST PRIVILEGE IMPLEMENTATION
═══════════════════════════════════════════════════════════════════

ROLE-BASED ACCESS CONTROL (RBAC):
┌─────────────────────────────────────────────────────────────────┐
│                    RBAC HIERARCHY                               │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                     ADMIN                                   │ │
│ │ • Full system access                                        │ │
│ │ • User management                                           │ │
│ │ • System configuration                                      │ │
│ └─────────────────────┬───────────────────────────────────────┘ │
│                       │                                         │
│ ┌─────────────────────▼───────────────────────────────────────┐ │
│ │                   MANAGER                                   │ │
│ │ • Team data access                                          │ │
│ │ • Report generation                                         │ │
│ │ • User role assignment                                      │ │
│ └─────────────────────┬───────────────────────────────────────┘ │
│                       │                                         │
│ ┌─────────────────────▼───────────────────────────────────────┐ │
│ │                    USER                                     │ │
│ │ • Own data access                                           │ │
│ │ • Read public resources                                     │ │
│ │ • Create/update own content                                 │ │
│ └─────────────────────┬───────────────────────────────────────┘ │
│                       │                                         │
│ ┌─────────────────────▼───────────────────────────────────────┐ │
│ │                   GUEST                                     │ │
│ │ • Read-only public access                                   │ │
│ │ • No data modification                                      │ │
│ │ • Limited functionality                                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

ATTRIBUTE-BASED ACCESS CONTROL (ABAC):
┌─────────────────────────────────────────────────────────────────┐
│ POLICY: Allow if (Subject.department == Resource.department      │
│                   AND Action == "read"                          │
│                   AND Time between 9AM-5PM                      │
│                   AND Request.location == "office")             │
│                                                                 │
│ SUBJECT ATTRIBUTES:                                             │
│ • User ID: john.doe                                             │
│ • Department: finance                                           │
│ • Role: analyst                                                 │
│ • Clearance: confidential                                       │
│                                                                 │
│ RESOURCE ATTRIBUTES:                                            │
│ • Type: financial_report                                        │
│ • Department: finance                                           │
│ • Classification: confidential                                  │
│ • Owner: finance_team                                           │
│                                                                 │
│ ENVIRONMENT ATTRIBUTES:                                         │
│ • Time: 2:30 PM                                                │
│ • Location: office_network                                      │
│ • Device: corporate_laptop                                      │
│ • Network: VPN_connected                                        │
│                                                                 │
│ ACTION ATTRIBUTES:                                              │
│ • Operation: read                                               │
│ • Purpose: analysis                                             │
│ • Bulk_operation: false                                         │
└─────────────────────────────────────────────────────────────────┘

MICROSERVICE PERMISSIONS:
┌─────────────────────────────────────────────────────────────────┐
│ SERVICE A (User Management)                                     │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ GRANTED PERMISSIONS:                                        │ │
│ │ • users:read                                                │ │
│ │ • users:create                                              │ │
│ │ • users:update                                              │ │
│ │ • profiles:read                                             │ │
│ │                                                             │ │
│ │ DENIED PERMISSIONS:                                         │ │
│ │ • orders:* (handled by Order Service)                      │ │
│ │ • payments:* (handled by Payment Service)                  │ │
│ │ • admin:* (admin operations restricted)                    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ SERVICE B (Order Management)                                    │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ GRANTED PERMISSIONS:                                        │ │
│ │ • orders:read                                               │ │
│ │ • orders:create                                             │ │
│ │ • orders:update                                             │ │
│ │ • inventory:read (read-only access)                         │ │
│ │ • users:read (lookup user details)                          │ │
│ │                                                             │ │
│ │ DENIED PERMISSIONS:                                         │ │
│ │ • users:write (cannot modify users)                        │ │
│ │ • payments:write (cannot process payments)                 │ │
│ │ • inventory:write (cannot modify inventory)                │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

##### 🛡️ **Zero Trust Architecture**

```
ZERO TRUST SECURITY MODEL
═══════════════════════════════════════════════════════════════════

TRADITIONAL PERIMETER SECURITY:
┌─────────────────────────────────────────────────────────────────┐
│                    CORPORATE NETWORK                            │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 🏢 TRUSTED ZONE                                             │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │ │
│ │ │ Server  │ │ Server  │ │ Server  │ │ Server  │           │ │
│ │ │    A    │ │    B    │ │    C    │ │    D    │           │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘           │ │
│ │               ↑ Full Trust, No Verification               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                              │                                  │
│           ┌──────────────────┴──────────────────┐               │
│           │          FIREWALL                   │               │
│           │      (Single Point of Control)      │               │
│           └──────────────────┬──────────────────┘               │
└────────────────────────────────────────────────────────────────┘
                               │
                    🌐 UNTRUSTED INTERNET

ZERO TRUST MODEL:
┌─────────────────────────────────────────────────────────────────┐
│ "NEVER TRUST, ALWAYS VERIFY"                                   │
│                                                                 │
│ ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐       │
│ │ Service │    │ Service │    │ Service │    │ Service │       │
│ │    A    │    │    B    │    │    C    │    │    D    │       │
│ └─────────┘    └─────────┘    └─────────┘    └─────────┘       │
│      │              │              │              │           │
│      ▼              ▼              ▼              ▼           │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │              POLICY ENFORCEMENT                             │ │
│ │ • Identity verification                                     │ │
│ │ • Device compliance check                                   │ │
│ │ • Behavioral analysis                                       │ │
│ │ • Continuous monitoring                                     │ │
│ │ • Micro-segmentation                                        │ │
│ │ • Encrypted communication                                   │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

ZERO TRUST PRINCIPLES:
┌─────────────────────────────────────────────────────────────────┐
│ 1. VERIFY EXPLICITLY                                           │
│    • Always authenticate and authorize                         │
│    • Use all available data points                             │
│    • Multi-factor authentication                               │
│                                                                 │
│ 2. USE LEAST PRIVILEGE ACCESS                                   │
│    • Limit access with just-in-time (JIT)                     │
│    • Risk-based adaptive policies                              │
│    • Data classification and protection                        │
│                                                                 │
│ 3. ASSUME BREACH                                                │
│    • Minimize blast radius                                      │
│    • Segment access by network, user, devices                  │
│    • Verify end-to-end encryption                              │
│    • Use analytics for visibility and threat detection         │
└─────────────────────────────────────────────────────────────────┘

IMPLEMENTATION ARCHITECTURE:
┌─────────────────────────────────────────────────────────────────┐
│                    ZERO TRUST COMPONENTS                       │
│                                                                 │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│ │   IDENTITY      │ │    DEVICE       │ │   APPLICATION   │   │
│ │   PROVIDER      │ │   MANAGEMENT    │ │    GATEWAY      │   │
│ │                 │ │                 │ │                 │   │
│ │ • User auth     │ │ • Device trust  │ │ • App access    │   │
│ │ • MFA           │ │ • Compliance    │ │ • Policy engine │   │
│ │ • Risk scoring  │ │ • Certificates  │ │ • Micro-tunnels │   │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│          │                    │                    │          │
│          └────────────────────┼────────────────────┘          │
│                               │                               │
│ ┌─────────────────────────────▼─────────────────────────────┐ │
│ │              POLICY ENGINE                               │ │
│ │ • Risk assessment                                        │ │
│ │ • Dynamic policy enforcement                             │ │
│ │ • Continuous trust evaluation                            │ │
│ │ • Analytics and ML-based detection                       │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                               │                               │
│ ┌─────────────────────────────▼─────────────────────────────┐ │
│ │              SECURE COMMUNICATION                        │ │
│ │ • mTLS between services                                  │ │
│ │ • Service mesh (Istio/Linkerd)                           │ │
│ │ • Encrypted data in transit/at rest                     │ │
│ │ • Network micro-segmentation                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

##### 🔧 **DevSecOps Pipeline**

```
SECURITY-INTEGRATED DEVELOPMENT PIPELINE
═══════════════════════════════════════════════════════════════════

SHIFT-LEFT SECURITY:
┌─────────────────────────────────────────────────────────────────┐
│                   DEVELOPMENT LIFECYCLE                         │
│                                                                 │
│ PLAN → CODE → BUILD → TEST → DEPLOY → MONITOR                  │
│   ↓      ↓      ↓      ↓       ↓        ↓                      │
│ Threat  SAST   SAST   DAST   Security  Runtime               │
│ Model   SCA    Image  Pen     Config   Security              │
│ Design  Linting Scan  Test    Scan     Monitoring            │
│ Review  IDE    Vuln   IAST    Policy   Incident              │
│         Plugin Check  API     Verify   Response              │
│                       Test                                    │
└─────────────────────────────────────────────────────────────────┘

PIPELINE STAGES:
┌─────────────────────────────────────────────────────────────────┐
│ 1. COMMIT STAGE                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ • Pre-commit hooks                                          │ │
│ │ • Static code analysis (SonarQube)                         │ │
│ │ • Secret detection (GitLeaks)                              │ │
│ │ • License compliance check                                  │ │
│ │ • Code quality gates                                        │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 2. BUILD STAGE                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ • Dependency vulnerability scan (OWASP Dependency Check)    │ │
│ │ • Container image scanning (Trivy, Clair)                  │ │
│ │ • Base image vulnerability check                            │ │
│ │ • Malware scanning                                          │ │
│ │ • Supply chain verification                                 │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 3. TEST STAGE                                                   │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ • Unit test security coverage                               │ │
│ │ • Integration security tests                                │ │
│ │ • API security testing (OWASP ZAP)                         │ │
│ │ • Dynamic application security testing (DAST)              │ │
│ │ • Infrastructure as Code security (Terraform)              │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 4. DEPLOY STAGE                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ • Infrastructure security validation                        │ │
│ │ • Configuration security check                              │ │
│ │ • Runtime security policies                                 │ │
│ │ • Network security policies                                 │ │
│ │ • RBAC validation                                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 5. MONITOR STAGE                                                │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ • Runtime security monitoring                               │ │
│ │ • Anomaly detection                                         │ │
│ │ • Compliance monitoring                                     │ │
│ │ • Incident response automation                              │ │
│ │ • Security metrics and reporting                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

SECURITY TOOLS INTEGRATION:
┌─────────────────────────────────────────────────────────────────┐
│ STATIC ANALYSIS (SAST):                                         │
│ • SonarQube (code quality + security)                          │
│ • Checkmarx (commercial SAST)                                  │
│ • Semgrep (pattern-based analysis)                             │
│ • CodeQL (GitHub's semantic analysis)                          │
│                                                                 │
│ DYNAMIC ANALYSIS (DAST):                                        │
│ • OWASP ZAP (web app scanner)                                  │
│ • Burp Suite (commercial scanner)                              │
│ • Nessus (vulnerability scanner)                               │
│ • w3af (web application attack framework)                      │
│                                                                 │
│ DEPENDENCY SCANNING (SCA):                                      │
│ • OWASP Dependency Check                                       │
│ • Snyk (commercial SCA)                                        │
│ • GitHub Dependabot                                            │
│ • npm audit / pip audit                                        │
│                                                                 │
│ CONTAINER SECURITY:                                             │
│ • Trivy (container vulnerability scanner)                      │
│ • Clair (static analysis of containers)                        │
│ • Falco (runtime security monitoring)                          │
│ • Aqua Security (commercial platform)                          │
│                                                                 │
│ INFRASTRUCTURE AS CODE:                                         │
│ • Terraform security (tfsec, checkov)                          │
│ • Kubernetes security (kube-score, falco)                      │
│ • AWS Config Rules                                             │
│ • Azure Security Center                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

#### 🛠️ **Practice (2 hours)**

##### **Exercise 1: Security Architecture Review**

```
SCENARIO: Fintech Application Security Review
═══════════════════════════════════════════════════════════════════

CURRENT ARCHITECTURE:
┌─────────────────────────────────────────────────────────────────┐
│ ┌─────────────┐     ┌─────────────┐     ┌─────────────┐         │
│ │   React     │────→│   Node.js   │────→│  PostgreSQL │         │
│ │   Frontend  │     │   API       │     │  Database   │         │
│ └─────────────┘     └─────────────┘     └─────────────┘         │
│        │                   │                   │                │
│        │            ┌─────────────┐     ┌─────────────┐         │
│        └───────────→│   Redis     │     │   AWS S3    │         │
│                     │   Cache     │     │  File Store │         │
│                     └─────────────┘     └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘

SECURITY ISSUES IDENTIFIED:
┌─────────────────────────────────────────────────────────────────┐
│ 🚨 CRITICAL ISSUES:                                             │
│ • No API authentication/authorization                           │
│ • Database credentials in environment variables                 │
│ • Client-side storage of sensitive data                        │
│ • No encryption for data in transit                            │
│ • Admin functions accessible via same API                      │
│                                                                 │
│ ⚠️ HIGH ISSUES:                                                 │
│ • No rate limiting on API endpoints                            │
│ • Error messages expose internal details                       │
│ • No input validation on financial amounts                     │
│ • Session tokens don't expire                                  │
│ • No audit logging for financial transactions                  │
│                                                                 │
│ 📋 MEDIUM ISSUES:                                               │
│ • No CSRF protection                                            │
│ • Missing security headers                                      │
│ • No dependency vulnerability scanning                         │
│ • Insufficient monitoring and alerting                         │
│ • No backup encryption                                          │
└─────────────────────────────────────────────────────────────────┘

RECOMMENDED SECURE ARCHITECTURE:
┌─────────────────────────────────────────────────────────────────┐
│ ┌─────────────┐                                                 │
│ │   React     │                                                 │
│ │  Frontend   │                                                 │
│ │  + Auth0    │                                                 │
│ └─────────────┘                                                 │
│        │ HTTPS                                                  │
│        ▼                                                        │
│ ┌─────────────┐                                                 │
│ │   WAF +     │                                                 │
│ │ Rate Limit  │                                                 │
│ └─────────────┘                                                 │
│        │                                                        │
│        ▼                                                        │
│ ┌─────────────┐                                                 │
│ │ API Gateway │                                                 │
│ │ + JWT Auth  │                                                 │
│ └─────────────┘                                                 │
│        │                                                        │
│   ┌────┴────┐                                                   │
│   ▼         ▼                                                   │
│ ┌─────────────┐     ┌─────────────┐                             │
│ │   User      │     │   Admin     │                             │
│ │ Microservice│     │Microservice │                             │
│ │             │     │             │                             │
│ └─────────────┘     └─────────────┘                             │
│        │                   │                                    │
│        ▼                   ▼                                    │
│ ┌─────────────┐     ┌─────────────┐                             │
│ │  Encrypted  │     │ Key Mgmt    │                             │
│ │ PostgreSQL  │     │ Service     │                             │
│ │ + Audit Log │     │ (AWS KMS)   │                             │
│ └─────────────┘     └─────────────┘                             │
│        │                                                        │
│        ▼                                                        │
│ ┌─────────────┐                                                 │
│ │  Encrypted  │                                                 │
│ │   Backups   │                                                 │
│ └─────────────┘                                                 │
└─────────────────────────────────────────────────────────────────┘

IMPLEMENTATION PRIORITIES:
1. Implement OAuth2/JWT authentication (Week 1)
2. Add HTTPS/TLS encryption (Week 1)  
3. Separate admin and user APIs (Week 2)
4. Add rate limiting and WAF (Week 2)
5. Encrypt database and enable audit logging (Week 3)
6. Implement secrets management (Week 3)
7. Add comprehensive monitoring (Week 4)
```

**Задание:** Провести полный security review с приоритизацией fixes и планом внедрения

---

##### **Exercise 2: DevSecOps Pipeline Design**

```
SECURE CI/CD PIPELINE FOR MICROSERVICES
═══════════════════════════════════════════════════════════════════

PIPELINE CONFIGURATION:
┌─────────────────────────────────────────────────────────────────┐
│ .github/workflows/secure-pipeline.yml                          │
│                                                                 │
│ name: Secure CI/CD Pipeline                                     │
│                                                                 │
│ stages:                                                         │
│   - security-scan                                               │
│   - build                                                       │
│   - test                                                        │
│   - security-test                                               │
│   - deploy                                                      │
│   - monitor                                                     │
│                                                                 │
│ security-scan:                                                  │
│   - Secret detection (GitLeaks)                                │
│   - SAST scan (SonarQube)                                      │
│   - License compliance                                          │
│   - Code quality gates                                          │
│                                                                 │
│ build:                                                          │
│   - Dependency vulnerability scan                               │
│   - Container image build                                       │
│   - Image vulnerability scan (Trivy)                           │
│   - Sign container image                                        │
│                                                                 │
│ test:                                                           │
│   - Unit tests with security coverage                          │
│   - Integration tests                                           │
│   - Contract tests                                              │
│                                                                 │
│ security-test:                                                  │
│   - DAST scan (OWASP ZAP)                                      │
│   - API security testing                                        │
│   - Infrastructure security scan                               │
│                                                                 │
│ deploy:                                                         │
│   - Security configuration check                               │
│   - Deploy with security policies                              │
│   - Runtime security monitoring                                │
│                                                                 │
│ monitor:                                                        │
│   - Security metrics collection                                │
│   - Anomaly detection setup                                     │
│   - Incident response integration                               │
└─────────────────────────────────────────────────────────────────┘

SECURITY GATES:
┌─────────────────────────────────────────────────────────────────┐
│ MANDATORY SECURITY CHECKS (Block Deployment):                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ❌ Critical/High severity vulnerabilities                   │ │
│ │ ❌ Secrets in code repository                               │ │
│ │ ❌ Container images with known CVEs                         │ │
│ │ ❌ Missing security headers in API responses                │ │
│ │ ❌ Unauthenticated admin endpoints                          │ │
│ │ ❌ Hardcoded passwords/keys                                 │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ WARNING SECURITY CHECKS (Allow with Approval):                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ⚠️ Medium severity vulnerabilities                          │ │
│ │ ⚠️ Code coverage below 80%                                  │ │
│ │ ⚠️ Missing rate limiting                                    │ │
│ │ ⚠️ Insecure dependencies (with fixes available)            │ │
│ │ ⚠️ Missing monitoring/logging                               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ AUTOMATED REMEDIATION:                                          │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 🔧 Dependency updates (Dependabot)                          │ │
│ │ 🔧 Container base image updates                             │ │
│ │ 🔧 Security header injection                                │ │
│ │ 🔧 Certificate renewal                                       │ │
│ │ 🔧 Security policy enforcement                              │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

COMPLIANCE REPORTING:
┌─────────────────────────────────────────────────────────────────┐
│ AUTOMATED COMPLIANCE DASHBOARD                                  │
│                                                                 │
│ ┌─────────────────┬─────────────────┬─────────────────────────┐ │
│ │ Service         │ Security Score  │ Compliance Status       │ │
│ ├─────────────────┼─────────────────┼─────────────────────────┤ │
│ │ user-service    │ 95/100 ✅       │ SOC2: ✅ PCI: ✅        │ │
│ │ payment-service │ 92/100 ✅       │ SOC2: ✅ PCI: ✅        │ │
│ │ order-service   │ 87/100 ⚠️       │ SOC2: ✅ PCI: N/A       │ │
│ │ admin-service   │ 78/100 ❌       │ SOC2: ⚠️ PCI: N/A       │ │
│ └─────────────────┴─────────────────┴─────────────────────────┘ │
│                                                                 │
│ TREND ANALYSIS:                                                 │
│ Security Score: 📈 +5% this month                              │
│ Vulnerability Backlog: 📉 -12 issues                           │
│ Compliance Violations: 📉 -3 this week                         │
│ Security Training: 📈 85% team completion                      │
└─────────────────────────────────────────────────────────────────┘
```

**Задание:** Создать complete DevSecOps pipeline с automated security testing и compliance reporting

---

## 🎯 Контрольные задания блока 5

```
 ░▒▓█  FINAL ASSESSMENT  █▓▒░
═══════════════════════════════════════════════════════════════════════════════════
```

### **Project 1: Secure Architecture для финтех приложения**

**Требования:**
- PCI DSS compliance
- Multi-region deployment  
- Real-time fraud detection
- 99.99% availability SLA
- GDPR compliance

**Задачи:**
1. Полная threat model с STRIDE анализом
2. Detailed security architecture
3. Encryption strategy (data at rest/in transit)
4. Authentication/authorization design
5. DDoS protection plan
6. Incident response procedures
7. Compliance mapping

---

### **Project 2: Security Audit существующей системы**

**Сценарий:** E-commerce платформа с выявленными уязвимостями

**Задачи:**
1. Приоритизация security issues
2. Risk assessment и business impact
3. Remediation roadmap с временными рамками
4. Security controls implementation
5. Continuous monitoring strategy

---

### **Теоретический тест:** 25 вопросов по всем темам блока

**Примеры вопросов:**
- Объяснить разницу между RBAC и ABAC
- Выбрать правильный OAuth2 flow для SPA приложения
- Рассчитать risk score для конкретной угрозы
- Спроектировать rate limiting для API с разными user tiers

---

## 📊 Результат блока 5

По завершении этого блока вы будете способны:

✅ **Проектировать secure by design архитектуры**  
✅ **Реализовывать современные authentication/authorization системы**  
✅ **Защищать от DDoS атак и implement rate limiting**  
✅ **Проводить threat modeling и security audits**  
✅ **Интегрировать security в DevOps процессы**  
✅ **Обеспечивать compliance с industry standards**  

```
🎓 CERTIFICATION LEVEL: SECURITY ARCHITECT
═══════════════════════════════════════════════════════════════════════════════════
Ready for Senior/Staff Security Engineer positions
Qualified to lead security architecture initiatives  
Capable of conducting security design reviews
```

---

## 📚 Дополнительные ресурсы

### **Книги:**
- "Web Application Security" - Andrew Hoffman
- "The Tangled Web" - Michal Zalewski  
- "Security Engineering" - Ross Anderson
- "Threat Modeling" - Adam Shostack

### **Стандарты и Frameworks:**
- NIST Cybersecurity Framework
- ISO 27001/27002
- PCI DSS Requirements
- SOC 2 Type II
- GDPR Technical Safeguards

### **Практические инструменты:**
- OWASP WebGoat (vulnerable app for practice)
- Damn Vulnerable Web Application (DVWA)
- ThreatDragon (threat modeling tool)
- Security Champions playbook

### **Онлайн ресурсы:**
- OWASP Project resources
- SANS Reading Room
- CIS Controls
- Cloud Security Alliance (CSA)

---

*Это завершает Block 5 образовательного материала. Готов создать следующий блок по вашему запросу!*