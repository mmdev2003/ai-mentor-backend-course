# 🔒 Блок 6: Безопасность и DevSecOps
*Полное руководство по интеграции безопасности в DevOps процессы*

---

## 📋 Обзор блока

**Длительность:** 1-2 месяца  
**Сложность:** Продвинутый уровень  
**Предварительные требования:** Блоки 1-5

### Что вы освоите:
- Принципы DevSecOps и Shift-Left Security
- Автоматизацию security тестирования в CI/CD
- Управление секретами на enterprise уровне
- Обеспечение безопасности инфраструктуры
- Runtime security и мониторинг угроз

---

## 🎯 Глава 6.1: Security в CI/CD

### 🧠 Концептуальные основы

#### Что такое Shift-Left Security?

**Традиционный подход:**
```
Разработка → Тестирование → Security Review → Production
     ↓              ↓              ↓              ↓
   Быстро        Быстро        МЕДЛЕННО       ДОРОГО
```

**Shift-Left подход:**
```
Security Planning → Secure Development → Continuous Testing → Production
        ↓                    ↓                    ↓              ↓
   ПЛАНИРОВАНИЕ        АВТОМАТИЗАЦИЯ       НЕПРЕРЫВНОСТЬ    БЫСТРО
```

#### Почему Shift-Left критически важен?

**Стоимость исправления уязвимостей:**
- **Этап планирования:** $1
- **Этап разработки:** $10
- **Этап тестирования:** $100
- **Production:** $1000+

#### Принципы DevSecOps

```
Security as Code = Security + Automation + Collaboration
                        ↓
              Безопасность встроена в процесс,
                  а не добавлена сверху
```

---

### 🔍 Типы security тестирования

#### SAST (Static Application Security Testing)

**Что это:**
- Анализ исходного кода без его выполнения
- Поиск потенциальных уязвимостей в коде
- Анализ качества кода с точки зрения безопасности

**Как работает:**
```
Исходный код → Парсер → AST → Анализатор → Отчет
     ↓           ↓      ↓         ↓         ↓
   .java      Токены  Дерево   Правила   SQL Injection
   .py        Лексемы  Узлы    Паттерны  XSS Issues
   .js                                   Buffer Overflow
```

**Преимущества:**
- Раннее обнаружение проблем
- Покрытие всего кода
- Интеграция в IDE

**Ограничения:**
- Ложные срабатывания
- Не видит runtime проблемы
- Сложность конфигурации

#### DAST (Dynamic Application Security Testing)

**Что это:**
- Тестирование работающего приложения
- Имитация атак злоумышленника
- Black-box подход

**Процесс работы:**
```
Deployed App → Scanner → HTTP Requests → Response Analysis → Vulnerabilities
     ↓           ↓           ↓              ↓                ↓
   Running    Crawler   GET/POST      Status Codes       XSS
   Service    Spider    Headers       Response Body      SQLi
              Proxy     Payloads      Timing            CSRF
```

**Что находит:**
- SQL Injection
- Cross-Site Scripting (XSS)
- Authentication bypasses
- Configuration issues

#### SCA (Software Composition Analysis)

**Проблема зависимостей:**
```
Ваше приложение (10%)
     ↓
Прямые зависимости (20%)
     ↓
Транзитивные зависимости (70%)
     ↓
ОБЩИЙ РИСК = 100%
```

**Что анализирует SCA:**
- Известные уязвимости (CVE)
- Лицензионные конфликты
- Устаревшие компоненты
- Malicious packages

**Источники данных:**
- National Vulnerability Database (NVD)
- GitHub Advisory Database
- NPM Security Advisories
- Commercial threat intelligence

---

### 🏗️ Интеграция в CI/CD Pipeline

#### Security Gates концепция

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Commit    │    │    Build    │    │    Test     │    │   Deploy    │
│             │    │             │    │             │    │             │
├─────────────┤    ├─────────────┤    ├─────────────┤    ├─────────────┤
│• Pre-commit │    │• SAST       │    │• DAST       │    │• Runtime    │
│  hooks      │    │• SCA        │    │• IAST       │    │  monitoring │
│• Secret     │    │• Container  │    │• Pen test   │    │• Compliance │
│  detection  │    │  scanning   │    │• Load test  │    │  checking   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼
 FAIL FAST          QUALITY GATE       SECURITY GATE      PRODUCTION GATE
```

#### Стратегии обработки результатов

**Пороговые значения:**
```
Критические уязвимости: 0 (FAIL)
Высокие уязвимости: ≤ 2 (WARNING)
Средние уязвимости: ≤ 10 (PASS)
Низкие уязвимости: Unlimited (INFO)
```

**Политики безопасности:**
- **Strict Mode:** Любая уязвимость = остановка pipeline
- **Graduated Mode:** Разные пороги для разных сред
- **Advisory Mode:** Только уведомления, без блокировки

---

### 📊 Metrics и KPI для DevSecOps

#### Ключевые метрики

**Mean Time To Fix (MTTF):**
```
MTTF = Время от обнаружения до исправления уязвимости
     = (Дата исправления - Дата обнаружения)

Цель: < 30 дней для критических, < 90 дней для остальных
```

**Security Debt:**
```
Security Debt = Количество открытых уязвимостей × Время существования
              = Σ(Severity Weight × Days Open)

Tracking: Тренд должен быть нисходящим
```

**False Positive Rate:**
```
FPR = (Ложные срабатывания / Общее количество найденных проблем) × 100%

Цель: < 20% для production pipelines
```

---

## 🗝️ Глава 6.2: Управление секретами

### 🔐 Проблемы с секретами

#### Антипаттерны (чего НЕ делать)

**1. Hardcoded secrets:**
```
❌ ПЛОХО:
database_url = "postgresql://admin:password123@db.example.com/prod"
api_key = "sk-1234567890abcdef"
```

**2. Secrets в переменных окружения:**
```
❌ ПЛОХО:
export DB_PASSWORD="super_secret_password"
# Видно в ps aux, docker inspect, kubernetes describe
```

**3. Secrets в configuration файлах:**
```
❌ ПЛОХО:
config.yaml:
  database:
    password: "plaintext_password"
# Попадает в git, logs, backups
```

#### Принципы безопасного управления секретами

**1. Принцип наименьших привилегий:**
```
Приложение A → Только secrets для DB_A
Приложение B → Только secrets для DB_B
Admin User → Доступ к управлению secrets
Dev User → Только read access к dev secrets
```

**2. Временные секреты:**
```
Статический секрет (BAD):
  password: "same_password_forever"
  
Динамический секрет (GOOD):
  lease_duration: 1h
  renewable: true
  max_ttl: 24h
```

**3. Audit trail:**
```
Каждое действие с секретом должно логироваться:
- Кто запросил
- Когда запросил
- Какой секрет
- Откуда (IP, User-Agent)
- Результат операции
```

---

### 🏛️ HashiCorp Vault архитектура

#### Основные компоненты

```
┌─────────────────────────────────────────────────────────────┐
│                        VAULT CLUSTER                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Active    │  │  Standby    │  │  Standby    │         │
│  │    Node     │  │    Node     │  │    Node     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────────┤
│  │                STORAGE BACKEND                          │
│  │  • Consul       • AWS S3      • PostgreSQL             │
│  │  • etcd         • Azure Blob  • In-Memory              │
│  └─────────────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────┘
```

#### Secret Engines

**Key-Value Engine:**
```
path/data/myapp/
├── database/
│   ├── username: "app_user"
│   └── password: "generated_password"
├── api/
│   └── token: "api_token_here"
└── certificates/
    ├── cert.pem
    └── key.pem
```

**Dynamic Secrets Engine:**
```
Database Engine:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Request   │───▶│    Vault    │───▶│  Database   │
│             │    │             │    │             │
│ GET /db/    │    │ CREATE USER │    │ new_user_   │
│ creds/role  │    │ GRANT perms │    │ 1234567890  │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │ Return:     │
                   │ user: temp_ │
                   │ pass: xyz   │
                   │ ttl: 1h     │
                   └─────────────┘
```

---

### 🔄 Lifecycle Management

#### Secret Rotation стратегии

**1. Manual Rotation:**
```
Admin → Vault → Update Secret → Notify Apps
  ↓       ↓          ↓            ↓
 Time   Manual    Downtime    Coordination
Intensive Process  Possible    Required
```

**2. Automatic Rotation:**
```
Scheduler → Vault → Generate New → Update Apps → Retire Old
    ↓        ↓         ↓           ↓          ↓
   Cron    Policy   Background   Rolling    Grace Period
  Event   Engine    Process     Update     (overlap)
```

**3. Just-in-Time (JIT):**
```
App Request → Vault → Generate → Return → Auto-Expire
     ↓         ↓        ↓         ↓         ↓
  On-Demand  Dynamic  Fresh    Short     No Cleanup
   Access   Creation Secret    TTL       Needed
```

#### Rotation сценарии

**Database Credentials:**
```
Phase 1: Generate new credentials
Phase 2: Update application config
Phase 3: Test connectivity
Phase 4: Rollback old credentials if needed
Phase 5: Monitor for issues
Phase 6: Retire old credentials
```

**API Keys:**
```
Overlapping Strategy:
Old Key ████████████░░░░ (active → deprecated → expired)
New Key     ████████████████ (testing → active)
        │   │        │    │
      Gen  Test    Switch Retire
      New  Both    Primary Old
```

---

## 🏰 Глава 6.3: Infrastructure Security

### 🌐 Network Security в Cloud

#### VPC (Virtual Private Cloud) архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                      VPC (10.0.0.0/16)                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│ │ Public Subnet   │ │ Private Subnet  │ │ Database Subnet │ │
│ │ (10.0.1.0/24)   │ │ (10.0.2.0/24)   │ │ (10.0.3.0/24)   │ │
│ │                 │ │                 │ │                 │ │
│ │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────────┐ │ │
│ │ │Load Balancer│ │ │ │App Servers  │ │ │ │ Databases   │ │ │
│ │ │   (ALB)     │ │ │ │   (EC2)     │ │ │ │   (RDS)     │ │ │
│ │ └─────────────┘ │ │ └─────────────┘ │ │ └─────────────┘ │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘ │
│         │                     │                     │       │
│         ▼                     ▼                     ▼       │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│ │Security Group   │ │Security Group   │ │Security Group   │ │
│ │- Port 80/443    │ │- Port 8080      │ │- Port 5432      │ │
│ │- From Internet  │ │- From ALB only  │ │- From App only  │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Security Groups vs NACLs

**Security Groups (Stateful):**
```
Inbound Rules:
Type    Protocol  Port    Source          Description
HTTP    TCP       80      0.0.0.0/0      Public web access
HTTPS   TCP       443     0.0.0.0/0      Secure web access
SSH     TCP       22      10.0.0.0/16    Internal admin

Outbound Rules:
Type    Protocol  Port    Destination     Description
All     All       All     0.0.0.0/0      Allow all outbound
```

**NACLs (Stateless):**
```
Inbound Rules:
Rule #  Type    Protocol  Port    Source          Allow/Deny
100     HTTP    TCP       80      0.0.0.0/0      ALLOW
200     HTTPS   TCP       443     0.0.0.0/0      ALLOW
300     SSH     TCP       22      10.0.0.0/16    ALLOW
*       All     All       All     0.0.0.0/0      DENY

Outbound Rules:
Rule #  Type      Protocol  Port      Destination   Allow/Deny
100     HTTP      TCP       80        0.0.0.0/0     ALLOW
200     HTTPS     TCP       443       0.0.0.0/0     ALLOW
300     Ephemeral TCP       1024-65535 0.0.0.0/0    ALLOW
*       All       All       All       0.0.0.0/0     DENY
```

---

### 🔑 Identity and Access Management (IAM)

#### Принципы IAM

**1. Principle of Least Privilege:**
```
User/Service → Minimum Permissions → Specific Resources
     ↓                 ↓                    ↓
  John Doe     ReadOnly S3 Bucket    my-app-logs-bucket
  App Server   Read/Write Database   production-db
  CI/CD        Deploy to K8s         staging-namespace
```

**2. Defense in Depth:**
```
Layer 1: Network (VPC, Security Groups)
    ↓
Layer 2: IAM (User permissions)
    ↓
Layer 3: Application (Authentication)
    ↓
Layer 4: Data (Encryption)
    ↓
Layer 5: Monitoring (Audit logs)
```

**3. Zero Trust Model:**
```
Traditional: Trust inside network boundary
Zero Trust: Verify everything, trust nothing

┌─────────────────────────────────────┐
│           Every Request             │
├─────────────────────────────────────┤
│ 1. Authenticate Identity            │
│ 2. Authorize Access                 │
│ 3. Validate Device                  │
│ 4. Check Context (time, location)   │
│ 5. Evaluate Risk                    │
│ 6. Grant Minimal Access             │
│ 7. Monitor Continuously             │
└─────────────────────────────────────┘
```

#### Role-Based Access Control (RBAC)

**AWS IAM Example:**
```
├── Groups
│   ├── Developers
│   │   ├── Policy: DeveloperAccess
│   │   └── Users: [alice, bob, charlie]
│   ├── DevOps
│   │   ├── Policy: DevOpsAccess
│   │   └── Users: [david, eve]
│   └── ReadOnly
│       ├── Policy: ReadOnlyAccess
│       └── Users: [frank, grace]
│
├── Roles
│   ├── EC2-Role
│   │   ├── Trust: EC2 Service
│   │   └── Policy: S3ReadWrite
│   ├── Lambda-Role
│   │   ├── Trust: Lambda Service
│   │   └── Policy: DynamoDBAccess
│   └── Cross-Account-Role
│       ├── Trust: External Account
│       └── Policy: LimitedAccess
```

---

### 📋 Compliance Frameworks

#### SOC 2 (Service Organization Control 2)

**Trust Services Criteria:**
```
Security:
├── Access Controls
├── Network Security
├── Data Protection
└── Monitoring & Logging

Availability:
├── System Uptime
├── Disaster Recovery
└── Incident Response

Processing Integrity:
├── Data Validation
├── Error Handling
└── Quality Assurance

Confidentiality:
├── Data Classification
├── Access Restrictions
└── Secure Transmission

Privacy:
├── Data Collection
├── Data Usage
├── Data Retention
└── Data Destruction
```

#### PCI DSS (Payment Card Industry Data Security Standard)

**12 Requirements Overview:**
```
Build and Maintain Secure Networks:
1. Install firewall configuration
2. Change vendor defaults

Protect Cardholder Data:
3. Protect stored cardholder data
4. Encrypt transmission of cardholder data

Maintain Vulnerability Management:
5. Protect against malware
6. Develop secure systems

Implement Strong Access Control:
7. Restrict access by business need-to-know
8. Identify and authenticate access
9. Restrict physical access

Regularly Monitor and Test:
10. Track and monitor network access
11. Regularly test security systems

Maintain Information Security Policy:
12. Maintain policy addressing information security
```

---

## 🛡️ Глава 6.4: Runtime Security

### 🐳 Container Security

#### Container Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│                   CONTAINER RUNTIME                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Container 1 │ │ Container 2 │ │ Container 3 │           │
│  │             │ │             │ │             │           │
│  │ App Code    │ │ App Code    │ │ App Code    │           │
│  │ Libraries   │ │ Libraries   │ │ Libraries   │           │
│  │ Base OS     │ │ Base OS     │ │ Base OS     │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
├─────────────────────────────────────────────────────────────┤
│                    ORCHESTRATION                            │
│              (Kubernetes / Docker Swarm)                    │
├─────────────────────────────────────────────────────────────┤
│                     HOST OS KERNEL                          │
├─────────────────────────────────────────────────────────────┤
│                    HARDWARE / VM                            │
└─────────────────────────────────────────────────────────────┘
```

#### Image Security Scanning

**Vulnerability Layers:**
```
Base Image (ubuntu:20.04)
├── CVE-2021-3711 (OpenSSL)
├── CVE-2021-22946 (curl)
└── CVE-2021-3737 (Python)

Package Manager (apt/yum)
├── Outdated packages
├── Unnecessary packages
└── Configuration issues

Application Dependencies
├── Language packages (npm, pip, maven)
├── Known vulnerabilities
└── License compliance

Application Code
├── Custom vulnerabilities
├── Secrets in code
└── Configuration issues
```

**Security Scanning Tools Matrix:**
```
┌──────────────┬─────────┬─────────┬─────────┬─────────┐
│    Tool      │ Image   │ Runtime │ License │ Policy  │
├──────────────┼─────────┼─────────┼─────────┼─────────┤
│ Trivy        │   ✓     │   ✓     │   ✓     │   ✗     │
│ Clair        │   ✓     │   ✗     │   ✗     │   ✗     │
│ Anchore      │   ✓     │   ✓     │   ✓     │   ✓     │
│ Snyk         │   ✓     │   ✓     │   ✓     │   ✓     │
│ Twistlock    │   ✓     │   ✓     │   ✓     │   ✓     │
└──────────────┴─────────┴─────────┴─────────┴─────────┘
```

---

### ⚙️ Kubernetes Security

#### Pod Security Standards

**Privileged:**
```yaml
# Unrestricted policy (не рекомендуется для production)
# Разрешает все возможности
privileged: true
allowPrivilegeEscalation: true
runAsUser: 0  # root
capabilities:
  add: ["ALL"]
```

**Baseline:**
```yaml
# Минимальные ограничения
# Предотвращает известные эскалации привилегий
allowPrivilegeEscalation: false
runAsNonRoot: true
seccompProfile:
  type: RuntimeDefault
capabilities:
  drop: ["ALL"]
  add: ["NET_BIND_SERVICE"]  # Только необходимые
```

**Restricted:**
```yaml
# Сильно ограниченная политика
# Следует hardening best practices
allowPrivilegeEscalation: false
runAsNonRoot: true
runAsUser: 1000
runAsGroup: 1000
seccompProfile:
  type: RuntimeDefault
capabilities:
  drop: ["ALL"]
readOnlyRootFilesystem: true
```

#### Network Policies

**Default Deny All:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}  # Применяется ко всем подам
  policyTypes:
  - Ingress
  - Egress
  # Нет правил = запрет всего трафика
```

**Микросегментация:**
```
┌─────────────────────────────────────────────────────────────┐
│                      Kubernetes Cluster                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│ │ Frontend    │───▶│ Backend     │───▶│ Database    │       │
│ │ Namespace   │    │ Namespace   │    │ Namespace   │       │
│ │             │    │             │    │             │       │
│ │ Port: 80    │    │ Port: 8080  │    │ Port: 5432  │       │
│ │ From: LB    │    │ From: FE    │    │ From: BE    │       │
│ └─────────────┘    └─────────────┘    └─────────────┘       │
│        │                  │                  │             │
│        ▼                  ▼                  ▼             │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│ │NetworkPolicy│    │NetworkPolicy│    │NetworkPolicy│       │
│ │• Allow LB   │    │• Allow FE   │    │• Allow BE   │       │
│ │• Deny all   │    │• Deny all   │    │• Deny all   │       │
│ └─────────────┘    └─────────────┘    └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

### 🔍 Runtime Threat Detection

#### Behavioral Analytics

**Anomaly Detection:**
```
Normal Behavior Baseline:
├── Process patterns
│   ├── Expected executables
│   ├── Process relationships
│   └── Resource usage
├── Network patterns
│   ├── Communication flows
│   ├── Protocols used
│   └── Data volumes
└── File access patterns
    ├── Read/write operations
    ├── File modifications
    └── Permission changes

Anomaly Indicators:
├── Unexpected processes
├── Unusual network connections
├── Privilege escalation attempts
├── Suspicious file operations
└── Resource consumption spikes
```

#### MITRE ATT&CK Framework для Containers

**Tactics & Techniques:**
```
Initial Access:
├── Supply Chain Compromise
├── Valid Accounts
└── Exploit Public-Facing Application

Execution:
├── Container Administration Command
├── Deploy Container
└── User Execution

Persistence:
├── Container Orchestration Job
├── Implant Container Image
└── Valid Accounts

Privilege Escalation:
├── Privileged Container
├── Escape to Host
└── Access Cloud Resources

Defense Evasion:
├── Masquerading
├── Hidden Files and Directories
└── Rootkit

Credential Access:
├── Container API
├── Credentials in Files
└── Unsecured Credentials

Discovery:
├── Container and Resource Discovery
├── Network Service Scanning
└── Software Discovery

Lateral Movement:
├── Container Administration Command
├── Application Deployment Software
└── Remote Services

Collection:
├── Data from Configuration Repository
├── Data from Information Repositories
└── Data Staged

Exfiltration:
├── Data Transfer Size Limits
├── Exfiltration Over Web Service
└── Transfer Data to Cloud Account

Impact:
├── Resource Hijacking
├── Data Destruction
└── Service Stop
```

---

### 📊 Security Monitoring и Alerting

#### Key Security Metrics

**Detection Metrics:**
```
Mean Time to Detection (MTTD):
MTTD = Time from incident start to detection
Target: < 15 minutes for critical incidents

Mean Time to Response (MTTR):
MTTR = Time from detection to response initiation
Target: < 5 minutes for automated response

False Positive Rate:
FPR = (False Positives / Total Alerts) × 100%
Target: < 10% for high-priority alerts

Coverage:
Coverage = (Monitored Assets / Total Assets) × 100%
Target: > 95% for critical assets
```

#### Security Event Correlation

**SIEM Event Flow:**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Events    │───▶│ Correlation │───▶│  Incidents  │
│             │    │   Engine    │    │             │
│• Firewall   │    │             │    │• Priority   │
│• IDS/IPS    │    │• Rules      │    │• Category   │
│• WAF        │    │• ML Models  │    │• Severity   │
│• Auth logs  │    │• Threat     │    │• Response   │
│• App logs   │    │  Intel      │    │  Plan       │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Correlation Rules Example:**
```
Rule: Potential Brute Force Attack
Conditions:
- Failed login attempts > 10
- Time window: 5 minutes
- Same source IP
- Multiple user accounts

Action:
- Create high-priority incident
- Block source IP automatically
- Notify security team
- Trigger additional monitoring
```

---

## 🎯 Практические задания

### Задание 1: Security Pipeline Setup
1. Интегрируйте SAST сканирование в CI/CD
2. Настройте SCA для dependency checking
3. Создайте security gates с пороговыми значениями
4. Настройте автоматические уведомления

### Задание 2: Vault Implementation
1. Развертывание Vault кластера
2. Настройка database secret engine
3. Интеграция с Kubernetes через service account
4. Автоматическая ротация секретов

### Задание 3: Infrastructure Hardening
1. Создание secure VPC с proper subnetting
2. Настройка security groups по принципу least privilege
3. Внедрение network policies в Kubernetes
4. Конфигурация compliance scanning

### Задание 4: Runtime Security
1. Настройка Pod Security Standards
2. Deploy runtime threat detection
3. Создание incident response playbook
4. Настройка security monitoring dashboard

---

## 📚 Дополнительные ресурсы

### Книги
- "DevOpsSec" - Jim Bird
- "Container Security" - Liz Rice
- "Kubernetes Security" - Liz Rice, Michael Hausenblas

### Сертификации
- Certified Ethical Hacker (CEH)
- CISSP (Certified Information Systems Security Professional)
- AWS Certified Security - Specialty
- Certified Kubernetes Security Specialist (CKS)

### Инструменты
- **SAST:** SonarQube, Checkmarx, Veracode
- **DAST:** OWASP ZAP, Burp Suite, Nessus
- **SCA:** Snyk, WhiteSource, Black Duck
- **Secrets:** HashiCorp Vault, AWS Secrets Manager
- **Runtime:** Falco, Twistlock, Aqua Security

---

## ✅ Чек-лист освоения блока

- [ ] Понимание DevSecOps принципов и Shift-Left Security
- [ ] Настройка security scanning в CI/CD pipeline
- [ ] Работа с различными типами security тестирования
- [ ] Внедрение и управление Vault для секретов
- [ ] Проектирование secure cloud architecture
- [ ] Понимание compliance требований
- [ ] Настройка Kubernetes security policies
- [ ] Внедрение runtime threat detection
- [ ] Создание security monitoring и alerting
- [ ] Разработка incident response процедур

---

*🔒 Безопасность - это не продукт, это процесс. Внедряйте security practices постепенно, автоматизируйте где возможно, и всегда следите за новыми угрозами в индустрии!*