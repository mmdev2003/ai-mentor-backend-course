# 🎯 DevOps собеседование: Полные ответы на 60 вопросов

*Комплексные ответы для подготовки к DevOps собеседованию от Junior до Expert уровня*

---

## 🎯 Блок 1: Основы и фундамент (12 вопросов)

### 1. Что такое DevOps и какие проблемы он решает?

**Основной ответ:**
DevOps — это культура, набор практик и инструментов, которые объединяют разработку (Development) и операционную деятельность (Operations) для ускорения и повышения качества доставки программного обеспечения.

**Проблемы, которые решает DevOps:**
- Медленные релизы из-за ручных процессов
- Плохая коммуникация между командами разработки и эксплуатации
- Частые сбои в production из-за отсутствия автоматизированного тестирования
- Долгое время восстановления после инцидентов

**Углубление:**
- **Пример улучшения:** В моем опыте внедрение CI/CD pipeline сократило время релиза с 2 недель до 2 часов, уменьшило количество багов в production на 60%
- **Метрики успеха:** Lead Time (время от коммита до production), Deployment Frequency, Mean Time to Recovery (MTTR), Change Failure Rate
- **Отличие от Waterfall:** DevOps использует итеративный подход с быстрой обратной связью, автоматизацией и continuous delivery, в отличие от последовательных фаз Waterfall

### 2. Объясните разницу между непрерывной интеграцией (CI) и непрерывной доставкой (CD)

**Основной ответ:**
- **CI (Continuous Integration)** — практика частого слияния изменений кода в общий репозиторий с автоматическим тестированием
- **CD (Continuous Delivery)** — расширение CI, где код автоматически подготавливается к релизу, но deployment в production требует ручного одобрения
- **Continuous Deployment** — полностью автоматический процесс до production без ручного вмешательства

**Углубление:**
- **Готовность к production:** Код проходит все automated tests (unit, integration, performance), security scanning, code quality checks
- **Этапы CI pipeline:** Source → Build → Test → Package → Archive artifacts
- **CD vs Continuous Deployment:** CD останавливается на staging с manual approval gate, Continuous Deployment идет до production автоматически

### 3. Как работает файловая система Linux? Объясните структуру каталогов

**Основной ответ:**
Linux использует hierarchical file system начиная с root (/) каталога:
- `/bin` — основные команды системы
- `/etc` — конфигурационные файлы
- `/home` — домашние каталоги пользователей
- `/var` — переменные данные (логи, кеши)
- `/usr` — пользовательские программы и библиотеки
- `/tmp` — временные файлы

**Углубление:**
- **Hard link vs Symbolic link:** Hard link — прямая ссылка на inode, работает только в пределах файловой системы. Symbolic link — ссылка на path, может указывать на файлы в других FS
- **chmod 755:** Owner: read(4)+write(2)+execute(1)=7, Group: read(4)+execute(1)=5, Others: read(4)+execute(1)=5
- **Команда выполнения:** `cd /var/log` переходит в каталог логов, `ls -la` показывает подробный список файлов включая скрытые, с правами доступа и метаданными

### 4. Что такое процессы в Linux? Как управлять ими?

**Основной ответ:**
Процесс — это выполняющаяся программа в памяти. Каждый процесс имеет PID (Process ID), PPID (Parent Process ID), состояние (running, sleeping, zombie).

**Команды управления:**
- `ps aux` — список всех процессов
- `top/htop` — мониторинг в реальном времени
- `kill PID` — завершение процесса
- `nohup command &` — запуск в фоне

**Углубление:**
- **Поиск процесса по порту:** `netstat -tulpn | grep :8080` или `lsof -i :8080`
- **Различия команд kill:** `kill` — отправляет SIGTERM конкретному PID, `killall` — завершает все процессы по имени, `pkill` — завершает по pattern
- **Zombie процессы:** Завершенные процессы, информация о которых не была считана родительским процессом. Решение: `kill -9 PPID` или restart родительского процесса

### 5. Напишите bash скрипт для мониторинга использования диска

**Основной ответ:**
```bash
#!/bin/bash
THRESHOLD=90
DISK_USAGE=$(df / | grep -vE '^Filesystem' | awk '{print $5}' | sed 's/%//g')

if [ $DISK_USAGE -gt $THRESHOLD ]; then
    echo "WARNING: Disk usage is ${DISK_USAGE}%"
    df -h
    # Send alert
fi
```

**Углубление:**
- **Error handling:**
```bash
#!/bin/bash
set -euo pipefail  # Fail on errors, undefined vars, pipe failures

LOG_FILE="/var/log/disk_monitor.log"
THRESHOLD=90

check_disk() {
    local mount_point=$1
    local usage=$(df "$mount_point" 2>/dev/null | grep -vE '^Filesystem' | awk '{print $5}' | sed 's/%//g')
    
    if [[ ! "$usage" =~ ^[0-9]+$ ]]; then
        echo "ERROR: Cannot get disk usage for $mount_point" | tee -a "$LOG_FILE"
        return 1
    fi
    
    echo "$usage"
}
```

- **Автоматизация через cron:** `*/5 * * * * /path/to/disk_monitor.sh`
- **Логирование:** `echo "$(date): Disk usage $DISK_USAGE%" >> /var/log/disk_monitor.log`

### 6. Объясните модель TCP/IP. Что происходит при запросе к веб-сайту?

**Основной ответ:**
TCP/IP состоит из 4 уровней:
1. **Application Layer** (HTTP, HTTPS, DNS)
2. **Transport Layer** (TCP, UDP)
3. **Internet Layer** (IP)
4. **Network Access Layer** (Ethernet)

**Процесс запроса:**
1. DNS resolution — получение IP адреса
2. TCP handshake — установка соединения
3. HTTP request — отправка запроса
4. HTTP response — получение ответа
5. TCP teardown — закрытие соединения

**Углубление:**
- **Роль DNS:** Преобразует domain name в IP адрес через иерархию DNS серверов (local cache → recursive resolver → root servers → TLD servers → authoritative servers)
- **TCP vs UDP:** TCP — надежный, с контролем ошибок и упорядочиванием пакетов; UDP — быстрый, без гарантий доставки
- **TCP handshake:** SYN → SYN-ACK → ACK для установки параметров соединения

### 7. Как работает HTTP/HTTPS? В чем разница?

**Основной ответ:**
- **HTTP** — протокол передачи гипертекста, работает поверх TCP на порту 80
- **HTTPS** — HTTP с SSL/TLS шифрованием на порту 443

**Структура HTTP:**
- Request: Method (GET/POST/PUT/DELETE) + Headers + Body
- Response: Status Code + Headers + Body

**Углубление:**
- **SSL handshake:** Client Hello → Server Hello + Certificate → Client verifies certificate → Key exchange → Finished
- **HTTP статус коды:** 502 Bad Gateway (upstream server error), 504 Gateway Timeout (upstream timeout)
- **HTTP/2 преимущества:** Multiplexing (несколько запросов в одном соединении), Header compression, Server push

### 8. Настройте nginx как reverse proxy для приложения на порту 3000

**Основной ответ:**
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Углубление:**
- **SSL конфигурация:**
```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

- **Load balancing:**
```nginx
upstream backend {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}
```

- **Кеширование статики:**
```nginx
location ~* \.(css|js|png|jpg|jpeg|gif|ico)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 9. Объясните Git workflow для команды разработчиков

**Основной ответ:**
**Gitflow workflow:**
1. `main` — production ready код
2. `develop` — интеграционная ветка
3. `feature/*` — новые функции
4. `release/*` — подготовка релиза
5. `hotfix/*` — исправления в production

**Процесс:**
- Создание feature branch из develop
- Разработка и коммиты
- Pull request с code review
- Merge в develop после approval

**Углубление:**
- **Merge конфликт:** `git merge feature-branch` → resolve conflicts → `git add .` → `git commit`
- **Merge vs Rebase:** Merge сохраняет историю веток, Rebase создает линейную историю
- **reset vs revert:** `git reset` изменяет историю (опасно для shared branches), `git revert` создает новый коммит отменяющий изменения

### 10. Что такое Git hooks? Приведите примеры использования

**Основной ответ:**
Git hooks — скрипты, которые автоматически выполняются при определенных Git событиях:
- `pre-commit` — перед коммитом
- `pre-push` — перед push
- `post-receive` — после получения push на сервере

**Примеры использования:**
- Проверка code style
- Запуск тестов
- Автоматический deployment

**Углубление:**
- **Pre-commit hook для code style:**
```bash
#!/bin/sh
# .git/hooks/pre-commit
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed. Please fix errors before committing."
    exit 1
fi
```

- **Deployment через hooks:** Да, используя `post-receive` hook на Git сервере
- **Общие hooks для команды:** Использовать tools как `pre-commit` framework или shared Git templates

### 11. У вас приложение работает медленно. Как будете диагностировать проблему?

**Основной ответ:**
**Пошаговая диагностика:**
1. Проверить системные ресурсы
2. Анализ логов приложения
3. Профилирование приложения
4. Анализ базы данных
5. Проверка сети

**Инструменты:**
- `top`, `htop` — CPU и память
- `iotop` — дисковая активность
- `netstat`, `ss` — сетевые соединения

**Углубление:**
- **Команды для bottleneck:** `top` (CPU), `free -h` (память), `df -h` (диск), `iotop` (I/O), `netstat -i` (сеть)
- **Детальный анализ:** `strace` для system calls, `tcpdump` для сетевого трафика, `perf` для профилирования
- **Анализ логов:** `grep ERROR /var/log/app.log | tail -50`, `journalctl -u service-name -f`

### 12. Как обеспечить безопасность SSH соединения?

**Основной ответ:**
**Основные меры:**
- Отключить root login
- Использовать SSH ключи вместо паролей
- Изменить порт по умолчанию
- Настроить fail2ban
- Ограничить пользователей

**Конфигурация `/etc/ssh/sshd_config`:**
```
Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers username
```

**Углубление:**
- **SSH ключи vs пароли:** Ключи используют асимметричное шифрование, практически невозможно подобрать, не передаются по сети
- **Ограничение по IP:** `AllowUsers user@192.168.1.0/24` в sshd_config или использование iptables
- **SSH Agent Forwarding:** Позволяет использовать локальные SSH ключи на удаленном сервере, полезно для git операций, но может быть небезопасно

---

## 🐳 Блок 2: Контейнеризация и оркестрация (10 вопросов)

### 13. В чем разница между контейнерами и виртуальными машинами?

**Основной ответ:**
- **VM:** Полная виртуализация с собственной ОС, гипервизор
- **Контейнеры:** Виртуализация на уровне ОС, общее ядро

**Отличия:**
- Ресурсы: VM тяжелее, контейнеры легче
- Время запуска: VM минуты, контейнеры секунды
- Изоляция: VM полная, контейнеры процессная

**Углубление:**
- **Когда использовать:** Контейнеры для микросервисов и cloud-native apps, VM для legacy apps или разных ОС
- **Изоляция контейнеров:** Linux namespaces (PID, Network, Mount, User), cgroups для ресурсов
- **Общие ресурсы:** Ядро ОС, базовые библиотеки, файловая система (copy-on-write)

### 14. Напишите Dockerfile для Node.js приложения

**Основной ответ:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

USER node

CMD ["npm", "start"]
```

**Углубление:**
- **Оптимизация размера:**
```dockerfile
# Multi-stage build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS production
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY --from=builder /app/dist ./dist
USER node
CMD ["npm", "start"]
```

- **Multi-stage builds:** Используются для уменьшения размера финального образа, отделяя build dependencies от runtime
- **Безопасность:** Не запускать от root, минимальные base images, сканирование vulnerabilities

### 15. Что происходит при выполнении `docker run -d -p 8080:80 nginx`?

**Основной ответ:**
1. Docker ищет образ nginx локально
2. Если не найден, скачивает из Docker Hub
3. Создает контейнер из образа
4. Запускает контейнер в detached режиме (-d)
5. Пробрасывает порт 8080 хоста на порт 80 контейнера (-p)

**Углубление:**
- **Флаги:** `-d` (detached mode), `-p` (port mapping 8080:80)
- **Docker networking:** Создается bridge network, контейнер получает внутренний IP, NAT для port forwarding
- **Bridge network:** Виртуальная сеть для связи контейнеров на одном хосте, изоляция от host network

### 16. Как работает Docker Compose? Создайте compose файл для веб-приложения с базой данных

**Основной ответ:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
      - DB_USER=myuser
      - DB_PASSWORD=mypassword
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Углубление:**
- **Service discovery:** Контейнеры находят друг друга по имени сервиса через internal DNS
- **Порядок запуска:** `depends_on` обеспечивает порядок, но для готовности БД используйте health checks или wait scripts
- **Secrets management:** Используйте Docker secrets или external secrets (HashiCorp Vault)

### 17. Объясните архитектуру Kubernetes кластера

**Основной ответ:**
**Control Plane (Master Node):**
- **kube-apiserver** — API gateway
- **etcd** — хранилище состояния
- **kube-scheduler** — размещение подов
- **kube-controller-manager** — контроллеры состояния

**Worker Nodes:**
- **kubelet** — агент узла
- **kube-proxy** — сетевая прокси
- **container runtime** — Docker/containerd

**Углубление:**
- **Master node компоненты:** API Server (REST API), Scheduler (размещение), Controller Manager (desired state), etcd (distributed storage)
- **kubelet функции:** Управление подами, health checks, регистрация узла, взаимодействие с container runtime
- **Kubernetes DNS:** CoreDNS для service discovery, автоматическое создание DNS записей для сервисов

### 18. В чем разница между Pod, Deployment и Service в Kubernetes?

**Основной ответ:**
- **Pod** — минимальная единица развертывания, группа контейнеров
- **Deployment** — управляет репликацией и обновлением подов
- **Service** — абстракция для доступа к подам

**Назначение:**
- Pod: Исполнение приложения
- Deployment: Управление жизненным циклом
- Service: Сетевой доступ и балансировка

**Углубление:**
- **Pod как atomic unit:** Все контейнеры в поде share network и storage, планируются на один узел
- **ReplicaSet vs Deployment:** ReplicaSet только управляет количеством реплик, Deployment добавляет rolling updates и rollback
- **Типы Services:** ClusterIP (internal), NodePort (external port on nodes), LoadBalancer (cloud LB), ExternalName (DNS alias)

### 19. Как работает auto-scaling в Kubernetes?

**Основной ответ:**
**Horizontal Pod Autoscaler (HPA):**
- Масштабирует количество подов
- Основан на метриках (CPU, память, custom)
- Проверяет каждые 15 секунд

**Vertical Pod Autoscaler (VPA):**
- Изменяет ресурсы подов
- Может потребовать restart

**Пример HPA:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Углубление:**
- **Метрики для HPA:** CPU utilization, memory utilization, requests per second, queue length
- **HPA vs VPA:** HPA увеличивает replicas, VPA увеличивает resources; VPA может конфликтовать с HPA
- **Custom metrics:** Prometheus adapter для метрик типа requests/sec, queue depth

### 20. Ваше приложение в Kubernetes не может подключиться к базе данных. Как диагностировать?

**Основной ответ:**
**Последовательность диагностики:**
1. Проверить состояние подов
2. Проверить сервисы
3. Проверить networking
4. Проверить DNS resolution
5. Проверить конфигурацию

**Команды:**
```bash
kubectl get pods
kubectl describe pod app-pod
kubectl logs app-pod
kubectl get svc
kubectl exec -it app-pod -- nslookup db-service
```

**Углубление:**
- **kubectl команды:** `kubectl get events`, `kubectl describe`, `kubectl logs -f`, `kubectl exec -it pod -- /bin/sh`
- **Проверка networking:** `kubectl exec -it pod -- nc -zv db-service 5432`, проверка NetworkPolicies
- **Анализ событий:** `kubectl get events --sort-by=.metadata.creationTimestamp`

### 21. Что такое ConfigMap и Secret? В чем разница?

**Основной ответ:**
- **ConfigMap** — хранение конфигурационных данных (не секретных)
- **Secret** — хранение чувствительных данных (пароли, ключи)

**Различия:**
- Secret кодируется в base64
- Secret можно монтировать в tmpfs
- Разные RBAC политики

**Пример:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_host: "db.example.com"
  log_level: "info"

---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  password: cGFzc3dvcmQ=  # base64 encoded
```

**Углубление:**
- **Хранение в etcd:** Secrets хранятся в base64, но не зашифрованы по умолчанию; нужно включать encryption at rest
- **Изменение ConfigMap:** Pod нужно restart для обновления env vars, но mounted volumes обновляются автоматически
- **Ротация секретов:** Использовать external secret operators (External Secrets Operator, SecretProviderClass)

### 22. Объясните Helm и его архитектуру

**Основной ответ:**
Helm — пакетный менеджер для Kubernetes.

**Компоненты:**
- **Chart** — пакет Kubernetes манифестов
- **Release** — экземпляр chart в кластере  
- **Repository** — хранилище charts

**Архитектура Helm 3:**
- Клиент-серверная архитектура убрана
- Прямое взаимодействие с Kubernetes API
- Информация о релизах в secrets

**Углубление:**
- **Helm templates:** Go template engine с функциями sprig, values.yaml для параметризации
- **Helm 2 vs 3:** Убран Tiller (security issues), улучшена безопасность, namespace scope
- **Зависимости charts:** Chart.yaml dependencies, `helm dependency update`

---

## ⚡ Блок 3: CI/CD и автоматизация (10 вопросов)

### 23. Спроектируйте CI/CD pipeline для веб-приложения

**Основной ответ:**
**CI Pipeline:**
1. Source code checkout
2. Build application
3. Run unit tests
4. Static code analysis
5. Security scanning
6. Build Docker image
7. Push to registry

**CD Pipeline:**
1. Deploy to staging
2. Integration tests
3. Performance tests
4. Manual approval
5. Deploy to production
6. Health checks

**Углубление:**
- **Этапы тестирования:** Unit tests → Integration tests → End-to-end tests → Performance tests → Security tests
- **Rollback стратегия:** Blue-green deployment, feature flags, automated health checks с automatic rollback
- **Security scanning:** SAST (static analysis), DAST (dynamic analysis), dependency scanning, container scanning

### 24. В чем разница между Blue-Green и Canary deployment?

**Основной ответ:**
**Blue-Green Deployment:**
- Два идентичных environments (blue и green)
- Переключение трафика между ними
- Быстрый rollback

**Canary Deployment:**
- Постепенный перевод трафика на новую версию
- Мониторинг метрик на каждом этапе
- Постепенное увеличение процента трафика

**Углубление:**
- **Когда использовать:** Blue-Green для critical apps с требованием zero-downtime, Canary для gradual rollout с risk mitigation
- **Canary analysis:** Автоматический анализ error rate, latency, business metrics; tools как Flagger, Argo Rollouts
- **Метрики для решений:** Error rate, response time, throughput, business KPIs; автоматический rollback при превышении thresholds

### 25. Создайте Jenkins pipeline для автоматического тестирования и deployment

**Основной ответ:**
```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/company/app.git'
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit'
                    }
                }
                stage('Lint') {
                    steps {
                        sh 'npm run lint'
                    }
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    def image = docker.build("app:${BUILD_NUMBER}")
                    docker.withRegistry('https://registry.company.com', 'docker-registry-credentials') {
                        image.push()
                        image.push("latest")
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                sh 'kubectl set image deployment/app app=registry.company.com/app:${BUILD_NUMBER}'
            }
        }
        
        stage('Integration Tests') {
            steps {
                sh 'npm run test:integration'
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                sh 'kubectl set image deployment/app app=registry.company.com/app:${BUILD_NUMBER} -n production'
            }
        }
    }
    
    post {
        always {
            publishTestResults testResultsPattern: 'test-results.xml'
            cleanWs()
        }
        failure {
            mail to: 'team@company.com',
                 subject: "Pipeline Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                 body: "Pipeline failed. Check: ${env.BUILD_URL}"
        }
    }
}
```

**Углубление:**
- **Parallel execution:** Использование `parallel` блоков для одновременного выполнения независимых задач
- **Secrets management:** Jenkins credentials store, использование `withCredentials()` wrapper
- **Approval gates:** `input` step для manual approval, можно добавить timeout и specific approvers

### 26. Как работает GitLab CI/CD? Объясните структуру .gitlab-ci.yml

**Основной ответ:**
```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - develop

test:
  stage: test
  script:
    - npm install
    - npm run test
  coverage: '/Coverage: \d+\.\d+%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

deploy_staging:
  stage: deploy
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy_production:
  stage: deploy
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE -n production
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main
```

**Углубление:**
- **GitLab Runners:** Shared runners (GitLab.com), specific runners (own infrastructure), docker executor, shell executor
- **Кеширование:** `cache` для node_modules, build artifacts; `artifacts` для передачи между jobs
- **Environments и deployments:** Tracking deployments, manual actions, protected environments

### 27. Ваш CI/CD pipeline работает медленно. Как оптимизировать?

**Основной ответ:**
**Основные bottlenecks:**
- Медленные тесты
- Большие Docker images
- Последовательное выполнение
- Отсутствие кеширования

**Способы оптимизации:**
- Распараллеливание задач
- Кеширование зависимостей
- Оптимизация Docker builds
- Selective testing

**Углубление:**
- **Частые bottlenecks:** Docker image builds, dependency installation, slow tests, sequential execution
- **Параллелизация тестов:** Test splitting, parallel test runners, matrix builds
- **Оптимизация Docker:** Multi-stage builds, layer caching, smaller base images, build cache

### 28. Как обеспечить качество кода в CI/CD pipeline?

**Основной ответ:**
**Инструменты и практики:**
- Static code analysis (SonarQube, ESLint)
- Code coverage requirements
- Security scanning
- Code review процесс
- Automated testing

**Quality Gates:**
- Minimum code coverage (80%+)
- No critical security vulnerabilities
- Code review approval
- All tests passing

**Углубление:**
- **Static analysis tools:** SonarQube (code quality), ESLint/Pylint (linting), Semgrep (security), CodeQL (security analysis)
- **Quality gates:** Coverage thresholds, security rating, maintainability rating, reliability rating
- **Code coverage:** Line coverage, branch coverage, function coverage; интеграция с pull requests

### 29. Что такое Infrastructure as Code в контексте CI/CD?

**Основной ответ:**
Infrastructure as Code (IaC) — управление инфраструктурой через код вместо ручных процессов.

**Принципы:**
- Версионирование инфраструктуры
- Автоматизация deployment
- Reproducible environments
- Infrastructure testing

**Инструменты:**
- Terraform, CloudFormation
- Ansible, Puppet
- Pulumi

**Углубление:**
- **Версионирование:** Git для infrastructure code, branch strategies, pull requests для changes
- **Тестирование IaC:** Unit tests (terraform validate), integration tests (terratest), compliance tests (policy as code)
- **Immutable infrastructure:** Infrastructure replacement вместо modification, blue-green для infrastructure

### 30. Как управлять artifacts в CI/CD процессе?

**Основной ответ:**
**Типы artifacts:**
- Build artifacts (JAR, WAR, executables)
- Docker images
- Test reports
- Documentation

**Управление:**
- Artifact repositories (Nexus, Artifactory)
- Versioning strategy
- Retention policies
- Security scanning

**Углубление:**
- **Создаваемые artifacts:** Application binaries, Docker images, Helm charts, test reports, security scan results
- **Versioning и traceability:** Semantic versioning, build metadata, Git commit SHA, pipeline tracking
- **Cleanup strategies:** Retention по времени, количеству версий, disk usage; automated cleanup jobs

### 31. Настройте автоматический deployment в разные environments

**Основной ответ:**
```yaml
# GitLab CI example
stages:
  - build
  - deploy-dev
  - deploy-staging
  - deploy-prod

deploy_dev:
  stage: deploy-dev
  script:
    - helm upgrade --install app ./helm-chart 
      --namespace dev 
      --values values-dev.yaml
      --set image.tag=$CI_COMMIT_SHA
  environment:
    name: development
  only:
    - develop

deploy_staging:
  stage: deploy-staging
  script:
    - helm upgrade --install app ./helm-chart 
      --namespace staging 
      --values values-staging.yaml
      --set image.tag=$CI_COMMIT_SHA
  environment:
    name: staging
  only:
    - main

deploy_prod:
  stage: deploy-prod
  script:
    - helm upgrade --install app ./helm-chart 
      --namespace production 
      --values values-prod.yaml
      --set image.tag=$CI_COMMIT_SHA
  environment:
    name: production
  when: manual
  only:
    - main
```

**Углубление:**
- **Promotion между environments:** Gitflow с разными ветками, tag-based deployments, artifact promotion
- **Configuration management:** Environment-specific values files, external config management (Consul, etcd)
- **Data consistency:** Database migrations, feature flags, backward compatibility

### 32. Как обеспечить zero-downtime deployment?

**Основной ответ:**
**Техники:**
- Rolling updates
- Blue-green deployment
- Load balancer switching
- Health checks
- Graceful shutdown

**Kubernetes Rolling Update:**
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

**Углубление:**
- **Используемые техники:** Rolling updates, blue-green, canary deployments, feature toggles
- **Rolling update в Kubernetes:** Постепенная замена подов, configurable maxUnavailable/maxSurge
- **Тестирование:** Automated health checks, smoke tests, load testing с production-like traffic

---

## 🏗️ Блок 4: Инфраструктура как код (10 вопросов)

### 33. Объясните принципы Infrastructure as Code

**Основной ответ:**
**Основные принципы:**
- **Declarative** — описание желаемого состояния
- **Version controlled** — инфраструктура в Git
- **Idempotent** — повторное выполнение дает тот же результат
- **Immutable** — замена вместо изменения

**Преимущества:**
- Reproducible environments
- Faster provisioning
- Reduced errors
- Cost optimization

**Углубление:**
- **Преимущества IaC:** Consistency across environments, faster disaster recovery, cost tracking, compliance
- **Idempotency:** Terraform plan показывает изменения, multiple applies безопасны
- **Testing инфраструктуры:** Unit tests, integration tests, compliance tests, security tests

### 34. Создайте Terraform конфигурацию для веб-приложения в AWS

**Основной ответ:**
```hcl
# main.tf
provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "main-vpc"
  }
}

# Subnets
resource "aws_subnet" "public" {
  count = 2
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

# Load Balancer
resource "aws_lb" "main" {
  name               = "main-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = aws_subnet.public[*].id
}

# Auto Scaling Group
resource "aws_autoscaling_group" "main" {
  name                = "main-asg"
  vpc_zone_identifier = aws_subnet.public[*].id
  target_group_arns   = [aws_lb_target_group.main.arn]
  health_check_type   = "ELB"

  min_size         = 2
  max_size         = 10
  desired_capacity = 2

  launch_template {
    id      = aws_launch_template.main.id
    version = "$Latest"
  }
}

# Launch Template
resource "aws_launch_template" "main" {
  name_prefix   = "main-"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = base64encode(templatefile("user_data.sh", {
    app_version = var.app_version
  }))
}
```

**Углубление:**
- **Структура для больших проектов:** Modules, environments separation, remote state, workspaces
- **Terraform modules:** Reusable components, input/output variables, module versioning
- **Безопасность state:** Remote backend (S3 + DynamoDB), state encryption, access controls

### 35. Как работает Terraform state? Почему он важен?

**Основной ответ:**
Terraform state — файл, который отслеживает соответствие между конфигурацией и реальными ресурсами.

**Назначение:**
- Mapping конфигурации к реальным ресурсам
- Metadata о ресурсах
- Performance optimization
- Collaboration между командой

**Важность:**
- Без state Terraform не знает что управлять
- Содержит чувствительные данные
- Критичен для команды

**Углубление:**
- **Потеря state файла:** Terraform import для восстановления, recreate resources, backup restoration
- **State locking:** Предотвращает concurrent modifications, DynamoDB для AWS, Consul для других
- **Миграция state:** terraform state mv, remote backend migration, state файл копирование

### 36. Как управлять разными environments в Terraform?

**Основной ответ:**
**Способы:**
1. **Terraform Workspaces**
2. **Separate directories**
3. **Git branches**
4. **Terraform modules**

**Пример с workspaces:**
```bash
terraform workspace new staging
terraform workspace new production
terraform workspace select staging
terraform apply -var-file="staging.tfvars"
```

**Пример структуры:**
```
environments/
├── dev/
│   ├── main.tf
│   └── terraform.tfvars
├── staging/
│   ├── main.tf
│   └── terraform.tfvars
└── prod/
    ├── main.tf
    └── terraform.tfvars
```

**Углубление:**
- **Terraform workspaces:** Shared configuration, separate state, workspace-specific variables
- **Variables для сред:** tfvars файлы, environment variables, workspace interpolation
- **Изоляция environments:** Separate AWS accounts, separate state backends, access controls

### 37. Что такое Ansible и как он работает?

**Основной ответ:**
Ansible — агентless инструмент автоматизации для configuration management, application deployment, и task automation.

**Архитектура:**
- **Control node** — откуда запускается Ansible
- **Managed nodes** — целевые серверы
- **Inventory** — список управляемых узлов
- **Playbooks** — YAML файлы с задачами

**Работа:**
- SSH подключение к узлам
- Выполнение модулей Python
- Возврат результатов

**Углубление:**
- **Push vs Pull:** Ansible использует push модель (отправляет команды), в отличие от pull (Chef, Puppet)
- **Ansible inventory:** Static (файлы), dynamic (scripts, plugins), групповые переменные
- **Idempotency:** Модули проверяют текущее состояние, изменения только при необходимости

### 38. Создайте Ansible playbook для настройки веб-сервера

**Основной ответ:**
```yaml
---
- name: Configure web server
  hosts: webservers
  become: yes
  vars:
    app_user: webapp
    app_dir: /opt/webapp
    
  tasks:
    - name: Update package cache
      package:
        update_cache: yes

    - name: Install required packages
      package:
        name:
          - nginx
          - python3
          - python3-pip
          - git
        state: present

    - name: Create application user
      user:
        name: "{{ app_user }}"
        shell: /bin/bash
        home: "{{ app_dir }}"
        create_home: yes

    - name: Clone application repository
      git:
        repo: https://github.com/company/webapp.git
        dest: "{{ app_dir }}/app"
        version: main
      become_user: "{{ app_user }}"

    - name: Install Python dependencies
      pip:
        requirements: "{{ app_dir }}/app/requirements.txt"
        virtualenv: "{{ app_dir }}/venv"
      become_user: "{{ app_user }}"

    - name: Configure nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/webapp
      notify: restart nginx

    - name: Enable nginx site
      file:
        src: /etc/nginx/sites-available/webapp
        dest: /etc/nginx/sites-enabled/webapp
        state: link
      notify: restart nginx

    - name: Create systemd service
      template:
        src: webapp.service.j2
        dest: /etc/systemd/system/webapp.service
      notify:
        - reload systemd
        - restart webapp

    - name: Start and enable services
      systemd:
        name: "{{ item }}"
        state: started
        enabled: yes
      loop:
        - nginx
        - webapp

  handlers:
    - name: restart nginx
      systemd:
        name: nginx
        state: restarted

    - name: reload systemd
      systemd:
        daemon_reload: yes

    - name: restart webapp
      systemd:
        name: webapp
        state: restarted
```

**Углубление:**
- **Ansible roles:** Организация в roles/, galaxy для sharing, role dependencies
- **Secrets в Ansible:** Ansible Vault для encryption, external password managers
- **Тестирование playbooks:** Molecule для testing, check mode для dry-run, syntax checking

### 39. Как интегрировать Terraform и Ansible?

**Основной ответ:**
**Подходы интеграции:**
1. **Terraform создает инфраструктуру → Ansible настраивает**
2. **Terraform local-exec provisioner**
3. **Terraform генерирует Ansible inventory**
4. **CI/CD pipeline с последовательным выполнением**

**Пример интеграции:**
```hcl
# Terraform
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  
  provisioner "local-exec" {
    command = "ansible-playbook -i '${self.public_ip},' playbook.yml"
  }
}

# Generate inventory
resource "local_file" "ansible_inventory" {
  content = templatefile("inventory.tpl", {
    web_servers = aws_instance.web[*].public_ip
  })
  filename = "inventory.ini"
}
```

**Углубление:**
- **Когда использовать:** Terraform для infrastructure provisioning, Ansible для configuration management
- **Передача данных:** Terraform outputs → Ansible variables, inventory generation
- **Consistent state:** Terraform для infrastructure state, Ansible для configuration compliance

### 40. Объясните основные сервисы AWS и их использование

**Основной ответ:**
**Compute:**
- **EC2** — виртуальные серверы
- **ECS** — container orchestration
- **EKS** — managed Kubernetes
- **Lambda** — serverless functions

**Storage:**
- **S3** — object storage
- **EBS** — block storage для EC2
- **EFS** — managed NFS

**Database:**
- **RDS** — managed relational databases
- **DynamoDB** — NoSQL database

**Networking:**
- **VPC** — virtual private cloud
- **ELB** — load balancers
- **CloudFront** — CDN

**Углубление:**
- **EC2 vs ECS vs EKS:** EC2 для VM-based apps, ECS для простой containerization, EKS для complex Kubernetes needs
- **AWS IAM:** Users, groups, roles, policies; principle of least privilege
- **Cost optimization:** Reserved instances, spot instances, rightsizing, lifecycle policies

### 41. Ваша Terraform конфигурация упала с ошибкой в середине apply. Что делать?

**Основной ответ:**
**Шаги восстановления:**
1. **Анализ ошибки** — читаем error message
2. **Проверка state** — `terraform show`
3. **Планирование** — `terraform plan`
4. **Исправление** — fix configuration или manual cleanup
5. **Повторное применение** — `terraform apply`

**Возможные проблемы:**
- Недостаточно прав IAM
- Ресурсы уже существуют
- Лимиты AWS
- Сетевые проблемы

**Углубление:**
- **Диагностика:** terraform plan для понимания drift, AWS Console для проверки ресурсов
- **Восстановление состояния:** terraform import для ресурсов вне state, terraform state rm для проблемных ресурсов
- **Предотвращение:** terraform validate, terraform plan в CI/CD, gradual changes

### 42. Как обеспечить compliance и governance в IaC?

**Основной ответ:**
**Policy as Code:**
- **Terraform Sentinel** — policy engine
- **Open Policy Agent (OPA)** — general-purpose policy engine
- **AWS Config** — compliance monitoring
- **Security scanning** — Checkov, tfsec

**Governance practices:**
- Code review для IaC
- Automated policy checking
- Resource tagging standards
- Cost controls

**Углубление:**
- **Policy as code:** Automated compliance checking, preventive controls, governance rules
- **Terraform Sentinel/OPA:** Policy языки для validation rules, integration с Terraform Cloud/Enterprise
- **Automated compliance:** CI/CD integration, fail на policy violations, compliance reporting

---

## 📊 Блок 5: Мониторинг и логирование (8 вопросов)

### 43. Спроектируйте monitoring solution для микросервисной архитектуры

**Основной ответ:**
**Компоненты решения:**
- **Metrics collection** — Prometheus
- **Visualization** — Grafana
- **Alerting** — Alertmanager
- **Logging** — ELK Stack
- **Tracing** — Jaeger/Zipkin
- **APM** — Application Performance Monitoring

**Архитектура:**
```
Services → Prometheus → Grafana
       ↓
   Alertmanager → PagerDuty/Slack
       ↓
    ELK Stack → Kibana
       ↓
    Jaeger → Tracing UI
```

**Углубление:**
- **Типы метрик:** RED (Rate, Errors, Duration), USE (Utilization, Saturation, Errors), business metrics
- **Observability across services:** Distributed tracing, correlation IDs, service mesh metrics
- **SLI/SLO установка:** Error rate < 0.1%, P99 latency < 100ms, availability > 99.9%

### 44. Как работает Prometheus? Объясните его архитектуру

**Основной ответ:**
**Архитектура Prometheus:**
- **Prometheus Server** — scraping и storage
- **Pushgateway** — для short-lived jobs
- **Alertmanager** — handling alerts
- **Exporters** — metrics exposition
- **Service Discovery** — target discovery

**Принцип работы:**
- Pull-based модель
- HTTP endpoints для метрик
- Time-series database
- PromQL для запросов

**Углубление:**
- **PromQL эффективные запросы:** Rate/increase для counters, histogram_quantile для latency, aggregation operators
- **Service discovery:** Kubernetes SD, Consul SD, file-based SD, static configuration
- **High availability:** Prometheus federation, recording rules, external storage (Thanos, Cortex)

### 45. Настройте alerting для критических метрик

**Основной ответ:**
```yaml
# alerting-rules.yml
groups:
  - name: critical-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} for {{ $labels.service }}"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "99th percentile latency is {{ $value }}s"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"

# alertmanager.yml
route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'

receivers:
  - name: 'web.hook'
    slack_configs:
      - api_url: 'SLACK_WEBHOOK_URL'
        channel: '#alerts'
        
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'PAGERDUTY_SERVICE_KEY'
```

**Углубление:**
- **Избежание alert fatigue:** Правильные thresholds, grouping, rate limiting, alert correlation
- **Escalation policies:** Different receivers для разных severity levels, time-based escalation
- **Best practices:** Actionable alerts, clear runbooks, SLO-based alerting

### 46. Что такое distributed tracing и зачем он нужен?

**Основной ответ:**
Distributed tracing — отслеживание запросов через несколько сервисов в распределенной системе.

**Компоненты:**
- **Trace** — полный путь запроса
- **Span** — единица работы в сервисе
- **Trace ID** — уникальный идентификатор
- **Span ID** — идентификатор операции

**Зачем нужен:**
- Debugging performance problems
- Understanding service dependencies
- Root cause analysis
- Optimization opportunities

**Углубление:**
- **OpenTelemetry:** Vendor-neutral стандарт для observability, автоматическая инструментация
- **Jaeger vs Zipkin:** Jaeger от Uber с лучшей Kubernetes интеграцией, Zipkin более простой
- **Correlation traces с logs:** Trace ID в logs, unified observability, context propagation

### 47. Спроектируйте centralized logging solution

**Основной ответ:**
**ELK Stack Architecture:**
```
Applications → Filebeat → Logstash → Elasticsearch → Kibana
            ↓
         Fluentd → Kafka → Logstash → Elasticsearch
```

**Компоненты:**
- **Log Shippers** — Filebeat, Fluentd
- **Processing** — Logstash, Fluentd
- **Storage** — Elasticsearch, ClickHouse
- **Visualization** — Kibana, Grafana

**Конфигурация:**
```yaml
# filebeat.yml
filebeat.inputs:
  - type: log
    paths:
      - /var/log/app/*.log
    fields:
      service: myapp
      environment: production

output.logstash:
  hosts: ["logstash:5044"]

# logstash pipeline
input {
  beats {
    port => 5044
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
  }
  
  date {
    match => [ "timestamp", "ISO8601" ]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

**Углубление:**
- **Log parsing и enrichment:** Grok patterns, JSON parsing, field extraction, geo enrichment
- **Storage optimization:** Index lifecycle management, hot/warm/cold architecture, compression
- **Security для logs:** Field masking, RBAC, encryption in transit/at rest

### 48. Как анализировать performance проблемы в production?

**Основной ответ:**
**Подход к анализу:**
1. **Identify symptoms** — high latency, errors, resource usage
2. **Narrow down scope** — specific service, endpoint, user segment
3. **Drill down** — traces, profiling, database queries
4. **Root cause** — code issues, infrastructure, dependencies

**Инструменты:**
- **APM** — New Relic, DataDog, Dynatrace
- **Profiling** — pprof, async-profiler, Pyflame
- **Database** — slow query logs, explain plans
- **Infrastructure** — system metrics, resource utilization

**Углубление:**
- **Profiling tools:** CPU profiling, memory profiling, I/O profiling, flame graphs
- **Correlating observability data:** Traces + metrics + logs, unified dashboards, correlation analysis
- **Root cause analysis:** 5 whys methodology, fishbone diagrams, statistical correlation

### 49. Что такое SRE и error budgets?

**Основной ответ:**
**Site Reliability Engineering (SRE)** — подход Google к управлению large-scale systems через software engineering practices.

**Error Budget:**
- Допустимое количество ошибок в период времени
- 99.9% SLA = 0.1% error budget
- Баланс между reliability и feature velocity

**Принципы SRE:**
- Service Level Indicators (SLI)
- Service Level Objectives (SLO)
- Service Level Agreements (SLA)
- Toil reduction

**Углубление:**
- **Расчет error budget:** (1 - SLO) × time period; например, 99.9% SLO = 43.2 минуты downtime в месяц
- **Превышение error budget:** Feature freeze, focus на reliability work, post-mortem analysis
- **Balance reliability и velocity:** Error budget позволяет принимать риски, reliability work при превышении

### 50. Ваше приложение показывает высокую latency. Как диагностировать?

**Основной ответ:**
**Пошаговая диагностика:**
1. **Check overall metrics** — P50, P95, P99 latency
2. **Identify scope** — specific endpoints, user segments, geographic regions
3. **Analyze infrastructure** — CPU, memory, network, disk I/O
4. **Database performance** — slow queries, connection pool
5. **External dependencies** — third-party APIs, services
6. **Application profiling** — code-level analysis

**Инструменты:**
```bash
# Infrastructure metrics
top, htop, iostat, sar
# Network analysis
netstat, ss, tcpdump
# Application profiling
pprof, flame graphs, APM tools
```

**Углубление:**
- **Первые метрики:** Response time percentiles, error rates, throughput, resource utilization
- **Distributed tracing:** Service map, trace analysis, bottleneck identification
- **Определение bottleneck:** CPU bound, I/O bound, network bound, database bound analysis

---

## 🔒 Блок 6: Безопасность и DevSecOps (6 вопросов)

### 51. Как интегрировать security в CI/CD pipeline?

**Основной ответ:**
**Shift-Left Security approach:**
- **Pre-commit** — IDE security plugins, git hooks
- **Build stage** — SAST, dependency scanning
- **Test stage** — DAST, container scanning
- **Deploy stage** — infrastructure scanning, runtime protection

**Пример pipeline:**
```yaml
stages:
  - build
  - security-scan
  - test
  - deploy

sast-scan:
  stage: security-scan
  script:
    - sonar-scanner
    - semgrep --config=auto .
  allow_failure: false

dependency-scan:
  stage: security-scan
  script:
    - npm audit
    - snyk test
  artifacts:
    reports:
      dependency_scanning: gl-dependency-scanning-report.json

container-scan:
  stage: security-scan
  script:
    - trivy image $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy
```

**Углубление:**
- **Типы security scanning:** SAST (static), DAST (dynamic), IAST (interactive), SCA (dependencies)
- **Vulnerability management:** CVE scanning, prioritization по CVSS, automated patching
- **Automated compliance:** Policy as code, compliance testing, audit trails

### 52. Как работает HashiCorp Vault? Спроектируйте secrets management solution

**Основной ответ:**
**Архитектура Vault:**
- **Storage Backend** — Consul, etcd, cloud storage
- **Auth Methods** — LDAP, AWS IAM, Kubernetes
- **Secret Engines** — KV, Database, PKI, AWS
- **Policies** — path-based access control

**Пример конфигурации:**
```hcl
# vault policy
path "secret/data/myapp/*" {
  capabilities = ["read"]
}

path "database/creds/readonly" {
  capabilities = ["read"]
}

# Enable secret engine
vault secrets enable -path=secret kv-v2
vault secrets enable database

# Configure database
vault write database/config/postgres \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb" \
  allowed_roles="readonly"
```

**Интеграция с Kubernetes:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: vault-auth
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      serviceAccountName: vault-auth
      initContainers:
      - name: vault-init
        image: vault:latest
        command: ['sh', '-c']
        args:
        - |
          vault auth -method=kubernetes role=myapp
          vault kv get -field=password secret/myapp/db > /shared/db-password
        volumeMounts:
        - name: shared-data
          mountPath: /shared
```

**Углубление:**
- **High availability:** Vault cluster с Raft или Consul backend, multiple instances
- **Интеграция с Kubernetes:** Vault Agent sidecar, CSI Secret Store, External Secrets Operator
- **Automated secrets rotation:** Database credentials rotation, certificate renewal, API key rotation

### 53. Обеспечьте security для Kubernetes кластера

**Основной ответ:**
**Security layers:**
1. **Cluster security** — API server, etcd encryption
2. **Node security** — OS hardening, kubelet configuration
3. **Network security** — Network Policies, service mesh
4. **Pod security** — Security Contexts, Pod Security Standards
5. **RBAC** — Role-based access control

**Пример конфигураций:**
```yaml
# Pod Security Policy
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'

# Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

# RBAC
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

**Углубление:**
- **Pod Security Standards:** Privileged, Baseline, Restricted levels для pod security
- **RBAC настройка:** Least privilege principle, service accounts, cluster roles vs roles
- **Network segmentation:** Calico, Cilium для advanced networking, microsegmentation

### 54. Как проводить security audit infrastructure?

**Основной ответ:**
**Аудит процесс:**
1. **Asset inventory** — все компоненты инфраструктуры
2. **Vulnerability scanning** — automated tools
3. **Configuration review** — security baselines
4. **Access review** — permissions audit
5. **Compliance check** — regulatory requirements

**Инструменты:**
- **Infrastructure scanning** — Nessus, OpenVAS, AWS Inspector
- **Configuration audit** — Lynis, CIS benchmarks
- **Cloud security** — Prowler, ScoutSuite, CloudSploit
- **Kubernetes** — kube-bench, kube-hunter

**Углубление:**
- **Scanning tools:** Nessus, Qualys, Rapid7, cloud-native scanners
- **Compliance frameworks:** CIS benchmarks, NIST, SOC 2, PCI DSS
- **Automated remediation:** Ansible playbooks, Terraform fixes, auto-patching

### 55. Разработайте incident response plan для security breach

**Основной ответ:**
**Incident Response фазы:**
1. **Preparation** — team, tools, procedures
2. **Identification** — detection и analysis
3. **Containment** — short-term и long-term
4. **Eradication** — remove threat
5. **Recovery** — restore systems
6. **Lessons Learned** — post-incident review

**Response team:**
- **Incident Commander** — coordination
- **Security Analyst** — threat analysis
- **DevOps Engineer** — system recovery
- **Communication Lead** — stakeholder updates
- **Legal/Compliance** — regulatory requirements

**Playbook example:**
```markdown
# Security Incident Response Playbook

## Phase 1: Identification (0-15 minutes)
- [ ] Alert received and validated
- [ ] Incident severity assessment
- [ ] Incident Commander assigned
- [ ] Response team activated

## Phase 2: Containment (15-60 minutes)
- [ ] Isolate affected systems
- [ ] Preserve evidence
- [ ] Block malicious traffic
- [ ] Secure admin access

## Phase 3: Analysis (1-4 hours)
- [ ] Forensic investigation
- [ ] Impact assessment
- [ ] Root cause analysis
- [ ] Threat attribution

## Phase 4: Recovery (4-24 hours)
- [ ] System cleanup
- [ ] Security patches
- [ ] Monitoring enhancement
- [ ] Gradual service restoration
```

**Углубление:**
- **Response procedures:** Automated containment, evidence preservation, communication templates
- **Forensics capabilities:** Log collection, memory dumps, network packet capture, timeline analysis
- **Post-incident review:** Timeline reconstruction, lessons learned, process improvements

### 56. Что такое Zero Trust architecture?

**Основной ответ:**
**Zero Trust принципы:**
- "Never trust, always verify"
- Assume breach
- Verify explicitly
- Least privilege access
- Continuous monitoring

**Компоненты:**
- **Identity verification** — multi-factor authentication
- **Device trust** — device compliance
- **Network segmentation** — microsegmentation
- **Data protection** — encryption, DLP
- **Application security** — secure by design

**Архитектура:**
```
User/Device → Identity Provider → Policy Engine → Resource Access
     ↓              ↓                ↓              ↓
  MFA/Device    Risk Assessment   Access Decision   Monitoring
```

**Углубление:**
- **Implementation в cloud:** IAM integration, conditional access, CASB, SASE
- **Инструменты:** Okta, Azure AD, Palo Alto Prisma, Zscaler, CrowdStrike
- **Migration strategy:** Phased approach, pilot groups, legacy system integration

---

## 🎖️ Блок 7: Экспертный уровень (4 вопроса)

### 57. Спроектируйте Internal Developer Platform для организации

**Основной ответ:**
**IDP компоненты:**
- **Self-service portal** — developer interface
- **Infrastructure automation** — Terraform, Pulumi
- **CI/CD platform** — GitLab, Jenkins, GitHub Actions
- **Container platform** — Kubernetes, service mesh
- **Observability stack** — metrics, logs, traces
- **Security scanning** — SAST, DAST, container scanning
- **Developer tools** — IDE integration, local development

**Архитектура:**
```
Developer Portal (Backstage)
    ↓
Platform APIs
    ↓
┌─────────────┬─────────────┬─────────────┐
│   Compute   │   Storage   │  Networking │
│ (Kubernetes)│    (S3)     │   (Istio)   │
└─────────────┴─────────────┴─────────────┘
```

**Пример с Backstage:**
```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-service
  annotations:
    github.com/project-slug: myorg/my-service
    backstage.io/kubernetes-id: my-service
spec:
  type: service
  lifecycle: production
  owner: team-backend
  system: core-platform
```

**Углубление:**
- **Platform capabilities:** Environment provisioning, database creation, CI/CD setup, monitoring configuration
- **Self-service features:** Service catalog, template gallery, automated onboarding, resource quotas
- **Developer experience metrics:** Lead time, deployment frequency, mean time to recovery, developer satisfaction

### 58. Как работает Service Mesh? Спроектируйте solution с Istio

**Основной ответ:**
**Service Mesh архитектура:**
- **Data plane** — sidecar proxies (Envoy)
- **Control plane** — configuration и management
- **Service discovery** — endpoint resolution
- **Load balancing** — traffic distribution
- **Security** — mTLS, authentication, authorization

**Istio компоненты:**
- **Pilot** — service discovery и configuration
- **Citadel** — certificate management
- **Galley** — configuration validation
- **Mixer** — telemetry и policy (deprecated)

**Конфигурация:**
```yaml
# Virtual Service
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: productpage
spec:
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: productpage
        subset: v2
      weight: 100
  - route:
    - destination:
        host: productpage
        subset: v1
      weight: 90
    - destination:
        host: productpage
        subset: v2
      weight: 10

# Destination Rule
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: productpage
spec:
  host: productpage
  trafficPolicy:
    circuitBreaker:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

**Углубление:**
- **Решаемые проблемы:** Service discovery, load balancing, failure recovery, metrics, security
- **Progressive delivery:** Traffic splitting, canary deployments, blue-green deployments
- **Security в mesh:** mTLS между сервисами, RBAC policies, JWT validation

### 59. Разработайте migration strategy от monolith к microservices

**Основной ответ:**
**Migration patterns:**
1. **Strangler Fig Pattern** — постепенная замена функций
2. **Database Decomposition** — разделение data model
3. **Event-Driven Architecture** — async communication
4. **API Gateway** — routing и versioning

**Поэтапный план:**
```
Phase 1: Assessment (2-4 weeks)
- [ ] Monolith analysis
- [ ] Domain identification
- [ ] Technical debt evaluation
- [ ] Team capability assessment

Phase 2: Foundation (4-8 weeks)
- [ ] CI/CD pipeline setup
- [ ] Container platform
- [ ] Monitoring infrastructure
- [ ] API Gateway deployment

Phase 3: Extraction (6+ months)
- [ ] Identify bounded contexts
- [ ] Extract first microservice
- [ ] Data migration strategy
- [ ] Gradual traffic routing

Phase 4: Optimization (ongoing)
- [ ] Performance tuning
- [ ] Cost optimization
- [ ] Team autonomy
- [ ] Platform maturity
```

**Углубление:**
- **Service boundaries:** Domain-driven design, bounded contexts, business capabilities
- **Decomposition patterns:** Database-per-service, shared databases, event sourcing, CQRS
- **Data consistency:** Eventual consistency, saga pattern, distributed transactions

### 60. Спланируйте disaster recovery strategy для cloud-native приложения

**Основной ответ:**
**DR компоненты:**
- **RTO** (Recovery Time Objective) — максимальное время восстановления
- **RPO** (Recovery Point Objective) — максимальная потеря данных
- **Multi-region architecture** — geographic distribution
- **Backup strategy** — data и configuration backups
- **Automated failover** — traffic routing

**DR стратегии:**
1. **Backup and Restore** (low cost, high RTO)
2. **Pilot Light** (medium cost, medium RTO)
3. **Warm Standby** (medium-high cost, low RTO)
4. **Hot Standby** (high cost, very low RTO)

**Cloud-native DR architecture:**
```yaml
# Multi-region setup
Primary Region (us-east-1):
  - EKS Cluster
  - RDS Primary
  - ElastiCache Primary
  - S3 Cross-region replication

Secondary Region (us-west-2):
  - EKS Cluster (standby)
  - RDS Read Replica
  - ElastiCache Backup
  - S3 Replica

Route 53 Health Checks:
  - Primary endpoint monitoring
  - Automatic failover
  - DNS-based traffic routing
```

**Углубление:**
- **RTO/RPO requirements:** Business impact analysis, критичность сервисов, cost-benefit analysis
- **Backup strategies:** Continuous backups, point-in-time recovery, cross-region replication
- **DR testing:** Regular drills, chaos engineering, automated testing, documentation updates

---

## 📈 Дополнительные материалы для изучения

### Рекомендуемые ресурсы:

**Книги:**
- "The DevOps Handbook" - Gene Kim
- "Site Reliability Engineering" - Google
- "Accelerate" - Nicole Forsgren
- "Infrastructure as Code" - Kief Morris

**Практические платформы:**
- Katacoda/O'Reilly Learning
- A Cloud Guru
- Linux Academy
- Hands-on labs в AWS/GCP/Azure

**Сертификации:**
- AWS Solutions Architect
- CKA (Certified Kubernetes Administrator)
- Terraform Associate
- Docker Certified Associate

**Open Source проекты для практики:**
- Kubernetes
- Prometheus
- Grafana
- Jenkins
- GitLab

---

## 💯 Заключение

Эти ответы покрывают весь спектр DevOps знаний от базовых концепций до экспертного уровня. Помните:

1. **Практический опыт** важнее теоретических знаний
2. **Понимание принципов** важнее запоминания команд
3. **Continuous learning** — ключ к успеху в DevOps
4. **Soft skills** также важны как технические навыки

Удачи на собеседовании! 🚀