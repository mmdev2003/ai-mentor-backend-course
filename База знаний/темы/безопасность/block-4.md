# Блок 4: Управление инцидентами и реагирование

---

**📋 Продолжительность:** 3-4 месяца  
**🎯 Цель блока:** Освоить процессы обнаружения, реагирования и восстановления после инцидентов ИБ

---

## 🔍 Глава 4.1: Мониторинг и обнаружение угроз
**⏰ Продолжительность:** 4 недели

### 📚 Темы изучения

#### SIEM системы (Security Information and Event Management)
```
┌─────────────────────────────────────────────────────────┐
│                    SIEM ARCHITECTURE                   │
├─────────────────────────────────────────────────────────┤
│  Data Sources → Collection → Normalization → Analysis   │
│                                ↓                       │
│              Correlation → Alerting → Response         │
└─────────────────────────────────────────────────────────┘
```

**Основные SIEM решения:**
- **Splunk** - коммерческая платформа с мощными возможностями анализа
- **ELK Stack** (Elasticsearch, Logstash, Kibana) - open-source решение
- **IBM QRadar** - корпоративная SIEM система
- **ArcSight** - традиционная SIEM от Micro Focus

#### Threat Hunting (Охота на угрозы)
```
🎯 THREAT HUNTING CYCLE
──────────────────────────
1. Hypothesis Formation
   ↓
2. Data Collection
   ↓
3. Investigation
   ↓
4. Analysis & Pattern Recognition
   ↓
5. Response & Documentation
   ↓
6. Lessons Learned
```

**Основные методики:**
- **IOC-based hunting** - поиск по индикаторам компрометации
- **TTP-based hunting** - поиск по тактикам, техникам и процедурам
- **Hypothesis-driven hunting** - поиск на основе гипотез
- **Machine learning hunting** - автоматизированная охота

#### Индикаторы компрометации (IoC)
```
┌─────────────────────────────────────────┐
│              ТИПЫ IoC                  │
├─────────────────────────────────────────┤
│ • File Hashes (MD5, SHA1, SHA256)      │
│ • IP Addresses                         │
│ • Domain Names                         │
│ • URLs                                 │
│ • Registry Keys                        │
│ • Mutex Names                          │
│ • Network Signatures                   │
│ • Email Patterns                       │
└─────────────────────────────────────────┘
```

#### SOC (Security Operations Center)
```
┌────────────────────────────────────────────────────────┐
│                    SOC STRUCTURE                       │
├────────────────────────────────────────────────────────┤
│  Level 1 Analysts  │  Level 2 Analysts  │  Level 3     │
│  (Monitoring)      │  (Investigation)   │  (Expert)    │
│                    │                    │              │
│  • Alert triage    │  • Deep analysis   │  • Threat    │
│  • Initial         │  • Incident        │    hunting   │
│    assessment      │    response        │  • Advanced  │
│  • Escalation      │  • Malware         │    forensics │
│                    │    analysis        │              │
└────────────────────────────────────────────────────────┘
```

### 🛠️ Практические задания

#### Задание 1: Настройка SIEM системы
```bash
# Установка ELK Stack
docker-compose up elasticsearch logstash kibana

# Конфигурация Logstash для сбора Windows Event Logs
input {
  beats {
    port => 5044
  }
}

filter {
  if [event][provider] == "Microsoft-Windows-Security-Auditing" {
    # Парсинг логов безопасности Windows
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "security-logs-%{+YYYY.MM.dd}"
  }
}
```

#### Задание 2: Создание правил корреляции
```yaml
# Правило обнаружения подозрительной активности
rule_name: "Multiple Failed Logins"
description: "Обнаружение атак методом перебора паролей"
condition: |
  count(failed_login_events) > 10 AND
  timeframe = 5_minutes AND
  same_source_ip = true
severity: HIGH
action: ["alert", "block_ip"]
```

#### Задание 3: Threat Hunting кампания
```
🔍 HUNTING SCENARIO: "Lateral Movement Detection"
─────────────────────────────────────────────────

Гипотеза: Злоумышленник использует WMI для латерального движения

Поисковые запросы:
1. Процессы WMI с необычными аргументами
2. Сетевые соединения от WmiPrvSE.exe
3. Создание новых сервисов через WMI
4. Запуск PowerShell через WMI

Индикаторы для анализа:
• Время выполнения команд
• Источник и цель соединений
• Частота использования WMI
• Корреляция с другими событиями
```

---

## 🚨 Глава 4.2: Реагирование на инциденты
**⏰ Продолжительность:** 3-4 недели

### 📚 Темы изучения

#### Жизненный цикл инцидента (NIST SP 800-61)
```
┌─────────────────────────────────────────────────────────┐
│               INCIDENT RESPONSE LIFECYCLE               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. PREPARATION    →  2. DETECTION &   →  3. CONTAINMENT │
│    • Policies         ANALYSIS           • Isolation    │
│    • Tools            • Identification   • Eradication  │
│    • Training         • Classification   • Recovery     │
│                      • Prioritization                   │
│                           ↓                             │
│ 4. POST-INCIDENT  ←──────────────────────────────────── │
│    ACTIVITY                                             │
│    • Lessons learned                                    │
│    • Evidence retention                                 │
│    • Process improvement                                │
└─────────────────────────────────────────────────────────┘
```

#### Классификация инцидентов
```
┌─────────────────────────────────────────┐
│           SEVERITY LEVELS               │
├─────────────────────────────────────────┤
│ 🔴 CRITICAL (P1)                       │
│    • Полная остановка бизнеса          │
│    • Массовая утечка данных            │
│    • Компрометация критических систем   │
│                                         │
│ 🟠 HIGH (P2)                           │
│    • Значительное влияние на бизнес    │
│    • Компрометация важных систем       │
│    • Потенциальная утечка PII          │
│                                         │
│ 🟡 MEDIUM (P3)                         │
│    • Ограниченное влияние              │
│    • Подозрительная активность         │
│    • Нарушение политик безопасности    │
│                                         │
│ 🟢 LOW (P4)                            │
│    • Минимальное влияние               │
│    • Информационные события            │
│    • Плановые уведомления              │
└─────────────────────────────────────────┘
```

#### Процедуры эскалации
```
┌─────────────────────────────────────────────────────────┐
│                 ESCALATION MATRIX                       │
├─────────────────────────────────────────────────────────┤
│ Time Frame │ P1 (Critical) │ P2 (High) │ P3/P4 (Low)   │
├─────────────────────────────────────────────────────────┤
│ 0-15 min   │ SOC Manager   │ L2 Analyst│ L1 Analyst    │
│ 15-30 min  │ CISO         │ SOC Mgr   │ L2 Analyst    │
│ 30-60 min  │ CTO/CEO      │ CISO      │ SOC Manager   │
│ 1+ hours   │ Board/Legal  │ CTO       │ CISO          │
└─────────────────────────────────────────────────────────┘
```

### 🛠️ Практические задания

#### Задание 1: Разработка плана реагирования
```markdown
# INCIDENT RESPONSE PLAYBOOK
## Malware Infection Response

### IMMEDIATE ACTIONS (0-15 minutes)
─────────────────────────────────────
1. ✅ Identify affected systems
2. ✅ Isolate infected machines
3. ✅ Preserve evidence
4. ✅ Notify SOC Manager
5. ✅ Begin containment

### INVESTIGATION (15-60 minutes)
──────────────────────────────────
1. Collect system artifacts
2. Analyze malware sample
3. Determine attack vector
4. Assess data impact
5. Update stakeholders

### RECOVERY (1-4 hours)
────────────────────────
1. Remove malware
2. Patch vulnerabilities
3. Restore from backups
4. Monitor for reinfection
5. Document lessons learned
```

#### Задание 2: Симуляция инцидента
```
🎭 SCENARIO: "Ransomware Attack Simulation"
───────────────────────────────────────────

Исходная ситуация:
• 14:30 - Получены множественные алерты от антивируса
• Пользователи сообщают о недоступности файлов
• На экранах появляется сообщение о шифровании

Ваши действия:
1. Первичная оценка (5 минут)
2. Активация группы реагирования (10 минут)
3. Изоляция пораженных систем (15 минут)
4. Сбор доказательств (30 минут)
5. Коммуникация с руководством (45 минут)

Документирование:
• Временная шкала событий
• Предпринятые действия
• Обнаруженные IoC
• Рекомендации по улучшению
```

---

## 🕵️ Глава 4.3: Цифровая криминалистика
**⏰ Продолжительность:** 4 недели

### 📚 Темы изучения

#### Принципы цифровой криминалистики
```
┌─────────────────────────────────────────────────────────┐
│               FORENSIC PROCESS FLOW                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. IDENTIFICATION  →  2. PRESERVATION  →  3. COLLECTION │
│    • Crime scene       • Chain of        • Forensic     │
│      assessment          custody           imaging      │
│    • Evidence          • Write-blocking   • Hash        │
│      location            devices            validation  │
│                                                         │
│ 6. PRESENTATION  ←  5. ANALYSIS  ←  4. EXAMINATION      │
│    • Expert           • Timeline        • File system   │
│      testimony          reconstruction    analysis      │
│    • Court            • Correlation     • Data          │
│      reporting          analysis          recovery     │
└─────────────────────────────────────────────────────────┘
```

#### Типы цифровых доказательств
```
📱 DEVICE TYPES
──────────────────────────────────────
• Desktop/Laptop Computers
• Mobile Devices (smartphones, tablets)
• Network Equipment (routers, firewalls)
• IoT Devices
• Cloud Storage
• Memory Dumps
• Network Traffic Captures

💾 DATA TYPES
──────────────────────────────────────
• File System Artifacts
• Registry Entries (Windows)
• Browser History
• Email Communications
• Chat/Messaging Apps
• Geolocation Data
• Cryptocurrency Transactions
```

#### Инструменты цифровой криминалистики
```
┌─────────────────────────────────────────┐
│            FORENSIC TOOLBOX             │
├─────────────────────────────────────────┤
│ 🔧 IMAGING TOOLS                       │
│ • FTK Imager                           │
│ • dd/ddrescue                          │
│ • EnCase                               │
│                                         │
│ 🔍 ANALYSIS TOOLS                      │
│ • Autopsy (Open Source)                │
│ • Volatility (Memory Analysis)         │
│ • Wireshark (Network Analysis)         │
│ • Sleuth Kit                           │
│                                         │
│ 📱 MOBILE FORENSICS                    │
│ • Cellebrite UFED                      │
│ • Oxygen Detective Suite               │
│ • XRY Mobile Forensics                 │
└─────────────────────────────────────────┘
```

### 🛠️ Практические задания

#### Задание 1: Форензик-анализ компьютера
```bash
# Создание образа диска
sudo dd if=/dev/sda of=/forensics/evidence.img bs=64K conv=noerror,sync
sha256sum /forensics/evidence.img > evidence.hash

# Анализ с помощью Autopsy
# 1. Создание нового кейса
# 2. Добавление образа диска
# 3. Анализ файловой системы
# 4. Поиск удаленных файлов
# 5. Анализ интернет-активности

# Ключевые артефакты для поиска:
# - Recent Documents
# - Browser History
# - Email Archives
# - System Logs
# - Registry Entries
# - Temporary Files
```

#### Задание 2: Анализ дампа памяти
```bash
# Использование Volatility для анализа памяти
volatility -f memory_dump.mem imageinfo

# Список запущенных процессов
volatility -f memory_dump.mem --profile=Win10x64_19041 pslist

# Сетевые соединения
volatility -f memory_dump.mem --profile=Win10x64_19041 netscan

# Анализ командной строки процессов
volatility -f memory_dump.mem --profile=Win10x64_19041 cmdline

# Поиск вредоносного кода
volatility -f memory_dump.mem --profile=Win10x64_19041 malfind
```

#### Задание 3: Сетевая криминалистика
```bash
# Анализ PCAP файла в Wireshark
# Фильтры для поиска подозрительной активности:

# HTTP POST запросы с данными
http.request.method == "POST" && http.content_length > 0

# DNS запросы к подозрительным доменам
dns && dns.qry.name contains "suspicious"

# Большие объемы исходящего трафика
tcp && tcp.len > 1460 && ip.src == internal_network

# Подозрительные User-Agent строки
http.user_agent contains "wget" || http.user_agent contains "curl"
```

---

## 🏢 Глава 4.4: Планирование непрерывности бизнеса
**⏰ Продолжительность:** 2-3 недели

### 📚 Темы изучения

#### Business Continuity Planning (BCP)
```
┌─────────────────────────────────────────────────────────┐
│               BCP DEVELOPMENT PROCESS                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. BUSINESS IMPACT    →  2. RISK ASSESSMENT           │
│    ANALYSIS (BIA)        • Threat identification       │
│    • Critical processes  • Vulnerability analysis      │
│    • Dependencies        • Risk prioritization         │
│    • RTO/RPO values                                    │
│                                ↓                       │
│ 4. TESTING &         ←  3. STRATEGY DEVELOPMENT        │
│    MAINTENANCE           • Recovery strategies          │
│    • Tabletop exercises  • Resource requirements       │
│    • Full-scale drills   • Alternate sites            │
│    • Plan updates        • Communication plans         │
└─────────────────────────────────────────────────────────┘
```

#### Ключевые метрики
```
📊 BUSINESS CONTINUITY METRICS
───────────────────────────────────────────
• RTO (Recovery Time Objective)
  Максимальное время восстановления
  
• RPO (Recovery Point Objective)
  Максимальная потеря данных
  
• MTTR (Mean Time To Recovery)
  Среднее время восстановления
  
• MTBF (Mean Time Between Failures)
  Среднее время между отказами

┌─────────────────────────────────────────┐
│          SERVICE TIERS                  │
├─────────────────────────────────────────┤
│ Tier 1 (Critical): RTO=1h, RPO=15min   │
│ Tier 2 (Important): RTO=4h, RPO=1h     │
│ Tier 3 (Standard): RTO=24h, RPO=4h     │
│ Tier 4 (Low): RTO=72h, RPO=24h         │
└─────────────────────────────────────────┘
```

#### Disaster Recovery Planning (DRP)
```
🏗️ DR SITE TYPES
──────────────────────────────────────────

• HOT SITE (RTO: 1-4 hours)
  - Полностью оборудованный центр
  - Актуальные данные и приложения
  - Высокая стоимость

• WARM SITE (RTO: 12-24 hours)  
  - Базовая инфраструктура
  - Требует настройка и загрузка данных
  - Средняя стоимость

• COLD SITE (RTO: 1-7 days)
  - Только физическое пространство
  - Требует полная установка
  - Низкая стоимость

• CLOUD-BASED DR
  - Гибкие RTO/RPO
  - Pay-as-you-use модель
  - Высокая масштабируемость
```

### 🛠️ Практические задания

#### Задание 1: Анализ влияния на бизнес (BIA)
```markdown
# BUSINESS IMPACT ANALYSIS TEMPLATE
## Critical Business Function: Customer Portal

### IMPACT ASSESSMENT
─────────────────────────────────────────────

| Timeframe | Financial Impact | Operational Impact | Reputational Impact |
|-----------|------------------|-------------------|-------------------|
| 1 hour    | $10,000         | 100 customers     | Low              |
| 4 hours   | $50,000         | 1,000 customers   | Medium           |
| 8 hours   | $150,000        | 5,000 customers   | High             |
| 24 hours  | $500,000        | All customers     | Critical         |

### DEPENDENCIES
──────────────────────────────────────────────
• Internal: Database servers, Web servers, Network
• External: Payment gateway, CDN, DNS provider
• Personnel: System administrators, Support team

### RECOVERY REQUIREMENTS
──────────────────────────────────────────────
• RTO: 2 hours
• RPO: 30 minutes
• Minimum staffing: 3 technical personnel
• Communication requirements: Customer notifications
```

#### Задание 2: Разработка плана DRP
```yaml
# DISASTER RECOVERY PLAN
disaster_recovery:
  primary_site: "Moscow Data Center"
  dr_site: "St. Petersburg Data Center"
  
  recovery_procedures:
    network_recovery:
      - priority: 1
        action: "Activate backup network links"
        responsible: "Network Team"
        duration: "15 minutes"
    
    server_recovery:
      - priority: 2
        action: "Start critical application servers"
        responsible: "Infrastructure Team"
        duration: "30 minutes"
    
    data_recovery:
      - priority: 3
        action: "Restore databases from backup"
        responsible: "Database Team"
        duration: "60 minutes"

  communication_plan:
    internal_notifications:
      - stakeholder: "Executive Team"
        method: "Emergency hotline"
        timeframe: "15 minutes"
    
    external_notifications:
      - stakeholder: "Customers"
        method: "Website notice + Email"
        timeframe: "30 minutes"
```

#### Задание 3: Проведение учений
```
🎯 TABLETOP EXERCISE: "Cyber Attack Response"
──────────────────────────────────────────────

Сценарий:
• Обнаружена атака на корпоративную сеть
• Скомпрометированы критические серверы
• Необходимо активировать план восстановления

Участники:
• IT Director (decision maker)
• Security Manager (technical lead)
• Communications Manager (stakeholder management)
• Legal Counsel (compliance and legal issues)

Временная шкала:
T+0: Обнаружение инцидента
T+15: Принятие решения об активации DRP
T+30: Начало процедур восстановления
T+60: Коммуникация с клиентами
T+120: Полное восстановление сервисов

Вопросы для обсуждения:
1. Критерии активации плана DRP
2. Приоритизация восстановления систем
3. Коммуникационная стратегия
4. Правовые аспекты инцидента
```

---

## 📊 Результаты блока

### ✅ Полученные навыки:
- **Мониторинг безопасности**: Настройка и управление SIEM системами
- **Threat Hunting**: Проактивный поиск угроз в инфраструктуре
- **Реагирование на инциденты**: Координация действий во время кибератак
- **Цифровая криминалистика**: Сбор и анализ цифровых доказательств
- **Планирование непрерывности**: Обеспечение устойчивости бизнеса

### 🎯 Ключевые компетенции:
- Способность эффективно реагировать на инциденты ИБ
- Навыки проведения форензик-расследований
- Умение планировать и тестировать процедуры восстановления
- Опыт работы с SIEM системами и threat hunting

### 🏆 Рекомендуемые сертификации:
- **GCIH** (GIAC Certified Incident Handler)
- **GCFA** (GIAC Certified Forensic Analyst)
- **GNFA** (GIAC Network Forensic Analyst)
- **GCTI** (GIAC Cyber Threat Intelligence)

---

**Переход к Блоку 5:** После завершения данного блока студент готов к изучению стратегических аспектов управления информационной безопасностью, включая управление рисками и обеспечение соответствия требованиям.