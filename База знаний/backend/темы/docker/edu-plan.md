# Docker: Путь от новичка до эксперта
*Комплексный план изучения с практическими заданиями и ресурсами*

---

## 🎯 Общая информация о курсе

**Продолжительность:** 20-25 недель  
**Уровень:** От начинающего до эксперта  
**Время в неделю:** 8-12 часов  
**Итоговая цель:** Стать экспертом Docker с глубоким пониманием контейнеризации

---

## 📚 Блок 1: Основы контейнеризации (2-3 недели)

### Глава 1.1: Введение в контейнеризацию
**Время:** 3-4 дня

**Теория:**
- Что такое контейнеры и зачем они нужны
- Проблемы, которые решает контейнеризация
- Сравнение контейнеров с виртуальными машинами
- История развития: от chroot до Docker

**Ресурсы для изучения:**
- 📖 [What is a Container? - Docker Documentation](https://www.docker.com/resources/what-container/)
- 🎥 YouTube: "Containers vs VMs: What's the difference?"
- 📄 Статья: "The History of Containers"

**Практическое задание:**
- Создать диаграмму сравнения контейнеров и ВМ
- Написать эссе на 500 слов: "Почему контейнеры изменили мир разработки"

### Глава 1.2: Установка и первое знакомство с Docker
**Время:** 4-5 дней

**Теория:**
- Архитектура Docker (Client-Server)
- Docker Desktop vs Docker Engine
- Системные требования и особенности установки

**Ресурсы для изучения:**
- 📖 [Install Docker Desktop](https://docs.docker.com/desktop/)
- 🎥 YouTube: "Docker Installation Tutorial"
- 📄 Docker Architecture Overview

**Практические задания:**
1. **Установить Docker** на свою ОС
2. **Первые команды:**
   ```bash
   docker --version
   docker info
   docker run hello-world
   docker run -it ubuntu bash
   ```
3. **Исследовать Docker Desktop** (если используете)
4. **Настроить автозапуск** Docker daemon

**Чек-лист проверки:**
- [ ] Docker успешно установлен
- [ ] Команда `docker run hello-world` работает
- [ ] Понимаете разницу между daemon и client
- [ ] Можете запустить интерактивный контейнер

### Глава 1.3: Основные концепции Docker
**Время:** 5-6 дней

**Теория:**
- Images (образы): что это и как работают
- Containers (контейнеры): жизненный цикл
- Docker Hub и реестры образов
- Слои образов и Copy-on-Write

**Ресурсы для изучения:**
- 📖 [Docker Images and Containers](https://docs.docker.com/get-started/)
- 🎥 YouTube: "Docker Images vs Containers"
- 📄 "Understanding Docker Image Layers"

**Практические задания:**
1. **Работа с образами:**
   ```bash
   docker images
   docker pull nginx
   docker pull ubuntu:20.04
   docker inspect nginx
   ```

2. **Управление контейнерами:**
   ```bash
   docker run -d --name my-nginx nginx
   docker ps
   docker logs my-nginx
   docker exec -it my-nginx bash
   docker stop my-nginx
   docker start my-nginx
   docker rm my-nginx
   ```

3. **Исследование Docker Hub:**
   - Найти 5 популярных образов
   - Изучить их документацию
   - Понять систему тегов

**Проект недели:**
Создать простой веб-сервер на Python и запустить его в контейнере nginx как статический сайт.

---

## 🛠 Блок 2: Работа с образами и контейнерами (3-4 недели)

### Глава 2.1: Управление образами
**Время:** 5-6 дней

**Теория:**
- Поиск образов в реестрах
- Стратегии тегирования
- Очистка неиспользуемых образов
- Размер образов и оптимизация

**Ресурсы для изучения:**
- 📖 [Docker Image Management](https://docs.docker.com/engine/reference/commandline/images/)
- 🎥 "Docker Image Best Practices"
- 📄 "Docker Image Optimization Techniques"

**Практические задания:**
1. **Работа с тегами:**
   ```bash
   docker tag nginx my-nginx:v1.0
   docker tag nginx my-nginx:latest
   docker images | grep my-nginx
   ```

2. **Анализ образов:**
   ```bash
   docker history nginx
   docker inspect nginx
   docker image ls --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
   ```

3. **Очистка системы:**
   ```bash
   docker system df
   docker image prune
   docker system prune -a
   ```

**Задание повышенной сложности:**
Написать bash-скрипт для автоматической очистки старых образов (старше 30 дней).

### Глава 2.2: Dockerfile - создание образов
**Время:** 7-8 дней

**Теория:**
- Синтаксис Dockerfile
- Основные инструкции: FROM, RUN, COPY, ADD, WORKDIR, EXPOSE, CMD, ENTRYPOINT
- Лучшие практики написания Dockerfile
- Многоэтапная сборка (Multi-stage builds)

**Ресурсы для изучения:**
- 📖 [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- 🎥 "Dockerfile Tutorial"
- 📄 "Dockerfile Best Practices"

**Практические задания:**

1. **Простой Dockerfile для Node.js приложения:**
   ```dockerfile
   FROM node:16-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   EXPOSE 3000
   CMD ["npm", "start"]
   ```

2. **Python Flask приложение:**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```

3. **Multi-stage build для Go приложения:**
   ```dockerfile
   # Стадия сборки
   FROM golang:1.19-alpine AS builder
   WORKDIR /app
   COPY . .
   RUN go build -o main .
   
   # Финальная стадия
   FROM alpine:latest
   RUN apk --no-cache add ca-certificates
   WORKDIR /root/
   COPY --from=builder /app/main .
   CMD ["./main"]
   ```

**Проекты недели:**
1. Создать Dockerfile для существующего проекта
2. Оптимизировать размер образа с помощью multi-stage build
3. Создать образ с кастомной конфигурацией nginx

### Глава 2.3: Управление контейнерами
**Время:** 6-7 дней

**Теория:**
- Жизненный цикл контейнера
- Порты и сетевые настройки
- Переменные окружения
- Ограничения ресурсов
- Restart policies

**Ресурсы для изучения:**
- 📖 [Container Management](https://docs.docker.com/engine/reference/run/)
- 🎥 "Docker Container Lifecycle"
- 📄 "Container Resource Management"

**Практические задания:**

1. **Управление портами:**
   ```bash
   docker run -d -p 8080:80 --name web nginx
   docker run -d -p 3000:3000 -p 8080:8080 --name app my-app
   ```

2. **Переменные окружения:**
   ```bash
   docker run -e NODE_ENV=production -e PORT=3000 my-node-app
   docker run --env-file .env my-app
   ```

3. **Ограничения ресурсов:**
   ```bash
   docker run -d --memory="256m" --cpus="0.5" nginx
   docker stats
   ```

4. **Restart policies:**
   ```bash
   docker run -d --restart=unless-stopped nginx
   docker run -d --restart=on-failure:3 my-app
   ```

**Лабораторная работа:**
Создать мониторинг-дашборд с несколькими контейнерами: веб-приложение, база данных, и система мониторинга.

---

## 🌐 Блок 3: Сеть и хранение данных (2-3 недели)

### Глава 3.1: Сетевые возможности Docker
**Время:** 5-6 дней

**Теория:**
- Типы сетей: bridge, host, overlay, macvlan
- Пользовательские сети
- DNS в Docker сетях
- Связь между контейнерами

**Ресурсы для изучения:**
- 📖 [Docker Networking](https://docs.docker.com/network/)
- 🎥 "Docker Networking Deep Dive"
- 📄 "Container-to-Container Communication"

**Практические задания:**

1. **Исследование сетей:**
   ```bash
   docker network ls
   docker network inspect bridge
   docker network create my-network
   ```

2. **Связь между контейнерами:**
   ```bash
   docker network create app-network
   docker run -d --network app-network --name database postgres
   docker run -d --network app-network --name web nginx
   docker exec web ping database
   ```

3. **Различные типы сетей:**
   ```bash
   # Bridge network
   docker run -d --name container1 nginx
   
   # Host network
   docker run -d --network host --name container2 nginx
   
   # Custom bridge
   docker network create --driver bridge custom-bridge
   docker run -d --network custom-bridge --name container3 nginx
   ```

**Проект:**
Создать микросервисную архитектуру с фронтендом, API, и базой данных, используя пользовательские сети.

### Глава 3.2: Управление данными
**Время:** 5-6 дней

**Теория:**
- Volumes vs Bind mounts vs tmpfs mounts
- Именованные тома и анонимные тома
- Драйверы томов
- Резервное копирование данных

**Ресурсы для изучения:**
- 📖 [Docker Storage](https://docs.docker.com/storage/)
- 🎥 "Docker Volumes Explained"
- 📄 "Data Persistence in Docker"

**Практические задания:**

1. **Работа с volumes:**
   ```bash
   docker volume create my-volume
   docker volume ls
   docker volume inspect my-volume
   docker run -d -v my-volume:/data nginx
   ```

2. **Bind mounts:**
   ```bash
   docker run -d -v /host/path:/container/path nginx
   docker run -d -v $(pwd):/app node:16 npm start
   ```

3. **Backup и restore:**
   ```bash
   # Backup
   docker run --rm -v my-volume:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /data .
   
   # Restore
   docker run --rm -v my-volume:/data -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /data
   ```

**Лабораторная работа:**
Настроить PostgreSQL с персистентным хранилищем и создать систему бэкапа.

### Глава 3.3: Безопасность в Docker
**Время:** 4-5 дней

**Теория:**
- Пользователи и права доступа в контейнерах
- Сканирование образов на уязвимости
- Secrets management
- Принцип наименьших привилегий

**Ресурсы для изучения:**
- 📖 [Docker Security](https://docs.docker.com/engine/security/)
- 🎥 "Docker Security Best Practices"
- 📄 "Container Security Fundamentals"

**Практические задания:**

1. **Работа с пользователями:**
   ```dockerfile
   FROM node:16-alpine
   RUN addgroup -g 1001 -S nodejs
   RUN adduser -S nextjs -u 1001
   USER nextjs
   ```

2. **Сканирование образов:**
   ```bash
   docker scan nginx
   docker scout cves nginx
   ```

3. **Secrets и переменные окружения:**
   ```bash
   # Использование secrets file
   docker run -d --env-file secrets.env my-app
   
   # Монтирование секретов
   docker run -d -v /host/secrets:/run/secrets my-app
   ```

**Задание на безопасность:**
Создать Dockerfile с применением всех изученных практик безопасности.

---

## 🔧 Блок 4: Docker Compose и оркестрация (3-4 недели)

### Глава 4.1: Введение в Docker Compose
**Время:** 6-7 дней

**Теория:**
- YAML синтаксис и структура
- Сервисы, сети, тома в Compose
- Команды docker-compose
- Переменные окружения в Compose

**Ресурсы для изучения:**
- 📖 [Docker Compose Documentation](https://docs.docker.com/compose/)
- 🎥 "Docker Compose Tutorial"
- 📄 "YAML for Beginners"

**Практические задания:**

1. **Простой docker-compose.yml:**
   ```yaml
   version: '3.8'
   services:
     web:
       image: nginx
       ports:
         - "8080:80"
     database:
       image: postgres:13
       environment:
         POSTGRES_PASSWORD: password
       volumes:
         - db_data:/var/lib/postgresql/data
   
   volumes:
     db_data:
   ```

2. **Веб-приложение с базой данных:**
   ```yaml
   version: '3.8'
   services:
     app:
       build: .
       ports:
         - "3000:3000"
       depends_on:
         - database
       environment:
         - DATABASE_URL=postgresql://user:password@database:5432/mydb
     
     database:
       image: postgres:13
       environment:
         POSTGRES_USER: user
         POSTGRES_PASSWORD: password
         POSTGRES_DB: mydb
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

3. **Команды управления:**
   ```bash
   docker-compose up -d
   docker-compose logs -f
   docker-compose exec app bash
   docker-compose down
   docker-compose pull
   ```

**Проект недели:**
Создать полноценное веб-приложение с фронтендом (React), бэкендом (Node.js/Python), базой данных (PostgreSQL) и Redis для кеширования.

### Глава 4.2: Продвинутые возможности Compose
**Время:** 6-7 дней

**Теория:**
- Override файлы и множественные Compose файлы
- Профили (Profiles)
- Healthchecks
- Зависимости между сервисами
- Масштабирование сервисов

**Ресурсы для изучения:**
- 📖 [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- 🎥 "Advanced Docker Compose"
- 📄 "Production-Ready Compose Files"

**Практические задания:**

1. **Override файлы:**
   ```yaml
   # docker-compose.yml
   version: '3.8'
   services:
     app:
       image: my-app
       ports:
         - "3000:3000"
   
   # docker-compose.override.yml
   version: '3.8'
   services:
     app:
       environment:
         - NODE_ENV=development
       volumes:
         - .:/app
   
   # docker-compose.prod.yml
   version: '3.8'
   services:
     app:
       environment:
         - NODE_ENV=production
       restart: unless-stopped
   ```

2. **Healthchecks:**
   ```yaml
   services:
     web:
       image: nginx
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:80"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s
   ```

3. **Profiles:**
   ```yaml
   services:
     web:
       image: nginx
     
     database:
       image: postgres
       profiles: ["production"]
     
     debug:
       image: my-debug-tools
       profiles: ["debug"]
   ```

4. **Масштабирование:**
   ```bash
   docker-compose up --scale web=3
   ```

**Продвинутый проект:**
Создать микросервисную архитектуру с API Gateway, несколькими бэкенд-сервисами, базами данных, и системой мониторинга.

### Глава 4.3: Основы оркестрации
**Время:** 5-6 дней

**Теория:**
- Введение в Docker Swarm
- Сравнение Docker Swarm и Kubernetes
- Когда использовать оркестрацию
- Основы отказоустойчивости

**Ресурсы для изучения:**
- 📖 [Docker Swarm Documentation](https://docs.docker.com/engine/swarm/)
- 🎥 "Docker Swarm vs Kubernetes"
- 📄 "Container Orchestration Comparison"

**Практические задания:**

1. **Создание Swarm кластера:**
   ```bash
   # На manager ноде
   docker swarm init
   
   # На worker ноде
   docker swarm join --token <token> <manager-ip>:2377
   ```

2. **Развертывание стека:**
   ```yaml
   # stack.yml
   version: '3.8'
   services:
     web:
       image: nginx
       ports:
         - "80:80"
       deploy:
         replicas: 3
         update_config:
           parallelism: 1
           delay: 10s
         restart_policy:
           condition: on-failure
   ```

   ```bash
   docker stack deploy -c stack.yml my-stack
   docker service ls
   docker service scale my-stack_web=5
   ```

**Исследовательское задание:**
Сравнить Docker Swarm, Kubernetes, и Nomad по различным критериям и написать отчет.

---

## 🚀 Блок 5: CI/CD и автоматизация (3-4 недели)

### Глава 5.1: Docker в CI/CD пайплайнах
**Время:** 7-8 дней

**Теория:**
- Контейнеризация сборочных процессов
- Интеграция с популярными CI/CD системами
- Стратегии тестирования в контейнерах
- Безопасность в CI/CD с Docker

**Ресурсы для изучения:**
- 📖 [Docker in CI/CD](https://docs.docker.com/ci-cd/)
- 🎥 "CI/CD with Docker"
- 📄 "Container-based Testing Strategies"

**Практические задания:**

1. **GitHub Actions с Docker:**
   ```yaml
   # .github/workflows/ci.yml
   name: CI
   on: [push, pull_request]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Build Docker image
           run: docker build -t my-app .
         - name: Run tests
           run: docker run --rm my-app npm test
         - name: Push to registry
           run: |
             echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
             docker push my-app:${{ github.sha }}
   ```

2. **GitLab CI с Docker:**
   ```yaml
   # .gitlab-ci.yml
   stages:
     - build
     - test
     - deploy
   
   variables:
     DOCKER_DRIVER: overlay2
   
   services:
     - docker:dind
   
   build:
     stage: build
     script:
       - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
       - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
   
   test:
     stage: test
     script:
       - docker run --rm $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA npm test
   ```

3. **Jenkins Pipeline:**
   ```groovy
   pipeline {
       agent any
       stages {
           stage('Build') {
               steps {
                   script {
                       docker.build("my-app:${env.BUILD_ID}")
                   }
               }
           }
           stage('Test') {
               steps {
                   script {
                       docker.image("my-app:${env.BUILD_ID}").inside {
                           sh 'npm test'
                       }
                   }
               }
           }
           stage('Deploy') {
               steps {
                   script {
                       docker.image("my-app:${env.BUILD_ID}").push()
                   }
               }
           }
       }
   }
   ```

**Проект недели:**
Настроить полный CI/CD пайплайн для своего проекта с автоматическими тестами, сборкой образов, и развертыванием.

### Глава 5.2: Автоматизация сборки
**Время:** 5-6 дней

**Теория:**
- Docker BuildKit и продвинутые возможности
- Оптимизация кеширования слоев
- Параллельная сборка
- Build contexts и .dockerignore

**Ресурсы для изучения:**
- 📖 [Docker BuildKit](https://docs.docker.com/build/buildkit/)
- 🎥 "Optimizing Docker Builds"
- 📄 "Docker Build Performance"

**Практические задания:**

1. **Включение BuildKit:**
   ```bash
   export DOCKER_BUILDKIT=1
   docker build .
   ```

2. **Оптимизированный Dockerfile с кешированием:**
   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM node:16-alpine
   
   WORKDIR /app
   
   # Копируем только package.json для лучшего кеширования
   COPY package*.json ./
   RUN npm ci --only=production
   
   # Копируем исходный код
   COPY . .
   
   # Используем multi-stage для уменьшения размера
   FROM node:16-alpine as production
   WORKDIR /app
   COPY --from=0 /app .
   CMD ["npm", "start"]
   ```

3. **BuildKit кеш:**
   ```bash
   # Inline кеш
   docker build --cache-from my-app:latest -t my-app:new .
   
   # Registry кеш
   docker build --cache-from type=registry,ref=my-registry/my-app:cache -t my-app .
   ```

4. **.dockerignore оптимизация:**
   ```dockerignore
   node_modules
   npm-debug.log
   .git
   .gitignore
   README.md
   .env
   coverage
   .nyc_output
   ```

**Лабораторная работа:**
Оптимизировать существующий Dockerfile для уменьшения времени сборки в 2-3 раза.

### Глава 5.3: Реестры и развертывание
**Время:** 5-6 дней

**Теория:**
- Частные Docker Registry
- Стратегии развертывания (Blue-Green, Rolling, Canary)
- Управление версиями образов
- Harbor, ECR, и другие enterprise решения

**Ресурсы для изучения:**
- 📖 [Docker Registry](https://docs.docker.com/registry/)
- 🎥 "Private Docker Registry Setup"
- 📄 "Deployment Strategies with Containers"

**Практические задания:**

1. **Настройка частного registry:**
   ```yaml
   # registry-compose.yml
   version: '3.8'
   services:
     registry:
       image: registry:2
       ports:
         - "5000:5000"
       volumes:
         - registry_data:/var/lib/registry
       environment:
         REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
   
   volumes:
     registry_data:
   ```

2. **Работа с частным registry:**
   ```bash
   # Пуш в частный registry
   docker tag my-app localhost:5000/my-app:v1.0
   docker push localhost:5000/my-app:v1.0
   
   # Pull из частного registry
   docker pull localhost:5000/my-app:v1.0
   ```

3. **Blue-Green развертывание:**
   ```bash
   # Blue окружение
   docker-compose -f docker-compose.blue.yml up -d
   
   # Тестирование
   curl http://blue.example.com/health
   
   # Переключение на Green
   docker-compose -f docker-compose.green.yml up -d
   
   # Остановка Blue после успешного переключения
   docker-compose -f docker-compose.blue.yml down
   ```

**Финальный проект блока:**
Создать систему развертывания с использованием частного registry и одной из стратегий развертывания.

---

## 📊 Блок 6: Мониторинг и production (2-3 недели)

### Глава 6.1: Логирование и мониторинг
**Время:** 5-6 дней

**Теория:**
- Централизованное логирование с ELK Stack
- Мониторинг метрик с Prometheus и Grafana
- Distributed tracing
- Алерты и уведомления

**Ресурсы для изучения:**
- 📖 [Docker Logging](https://docs.docker.com/config/containers/logging/)
- 🎥 "Container Monitoring with Prometheus"
- 📄 "ELK Stack for Container Logs"

**Практические задания:**

1. **ELK Stack для логирования:**
   ```yaml
   version: '3.8'
   services:
     elasticsearch:
       image: elasticsearch:7.17.0
       environment:
         - discovery.type=single-node
       volumes:
         - elasticsearch_data:/usr/share/elasticsearch/data
   
     logstash:
       image: logstash:7.17.0
       volumes:
         - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
       depends_on:
         - elasticsearch
   
     kibana:
       image: kibana:7.17.0
       ports:
         - "5601:5601"
       depends_on:
         - elasticsearch
   
     app:
       image: my-app
       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"
   
   volumes:
     elasticsearch_data:
   ```

2. **Prometheus мониторинг:**
   ```yaml
   version: '3.8'
   services:
     prometheus:
       image: prom/prometheus
       ports:
         - "9090:9090"
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml
         - prometheus_data:/prometheus
   
     grafana:
       image: grafana/grafana
       ports:
         - "3000:3000"
       volumes:
         - grafana_data:/var/lib/grafana
       environment:
         - GF_SECURITY_ADMIN_PASSWORD=admin
   
     node-exporter:
       image: prom/node-exporter
       ports:
         - "9100:9100"
   
   volumes:
     prometheus_data:
     grafana_data:
   ```

3. **Конфигурация Prometheus:**
   ```yaml
   # prometheus.yml
   global:
     scrape_interval: 15s
   
   scrape_configs:
     - job_name: 'prometheus'
       static_configs:
         - targets: ['localhost:9090']
   
     - job_name: 'node-exporter'
       static_configs:
         - targets: ['node-exporter:9100']
   
     - job_name: 'docker-containers'
       static_configs:
         - targets: ['app:8080']
   ```

**Проект:**
Настроить полную систему мониторинга для микросервисного приложения.

### Глава 6.2: Оптимизация производительности
**Время:** 4-5 дней

**Теория:**
- Профилирование контейнеров
- Оптимизация использования ресурсов
- Настройка лимитов CPU и памяти
- Оптимизация сетевых операций

**Ресурсы для изучения:**
- 📖 [Runtime Metrics](https://docs.docker.com/config/containers/runmetrics/)
- 🎥 "Docker Performance Tuning"
- 📄 "Container Resource Management"

**Практические задания:**

1. **Мониторинг ресурсов:**
   ```bash
   # Мониторинг в реальном времени
   docker stats
   
   # Лимиты ресурсов
   docker run -d --memory="512m" --cpus="1.5" my-app
   
   # Анализ использования ресурсов
   docker exec container_name cat /sys/fs/cgroup/memory/memory.usage_in_bytes
   ```

2. **Оптимизация образов:**
   ```dockerfile
   # Многоэтапная сборка для минимизации размера
   FROM node:16-alpine AS builder
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production
   
   FROM node:16-alpine AS runtime
   RUN addgroup -g 1001 -S nodejs && \
       adduser -S nextjs -u 1001
   WORKDIR /app
   COPY --from=builder --chown=nextjs:nodejs /app .
   USER nextjs
   CMD ["node", "server.js"]
   ```

3. **Профилирование приложений:**
   ```bash
   # Использование perf для профилирования
   docker run --cap-add=SYS_ADMIN my-app
   
   # Memory profiling
   docker run --memory="1g" --oom-kill-disable my-app
   ```

**Задание на оптимизацию:**
Оптимизировать реальное приложение для уменьшения использования памяти на 50% и увеличения производительности на 30%.

### Глава 6.3: Production-ready настройки
**Время:** 4-5 дней

**Теория:**
- Health checks и liveness probes
- Graceful shutdown
- Secrets management в production
- Backup и disaster recovery стратегии

**Ресурсы для изучения:**
- 📖 [Production Checklist](https://docs.docker.com/config/containers/start-containers-automatically/)
- 🎥 "Docker in Production"
- 📄 "Container Security in Production"

**Практические задания:**

1. **Health checks:**
   ```dockerfile
   FROM nginx
   COPY . /usr/share/nginx/html/
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
     CMD curl -f http://localhost/ || exit 1
   ```

2. **Graceful shutdown:**
   ```javascript
   // Node.js example
   process.on('SIGTERM', () => {
     console.log('SIGTERM received, shutting down gracefully');
     server.close(() => {
       console.log('Process terminated');
     });
   });
   ```

3. **Production Compose файл:**
   ```yaml
   version: '3.8'
   services:
     app:
       image: my-app:latest
       restart: unless-stopped
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s
       environment:
         - NODE_ENV=production
       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"
       deploy:
         resources:
           limits:
             memory: 512M
             cpus: '0.5'
   ```

**Production проект:**
Подготовить существующее приложение к production развертыванию со всеми необходимыми настройками.

---

## 🎓 Блок 7: Экспертный уровень (4-5 недель)

### Глава 7.1: Продвинутые техники
**Время:** 8-9 дней

**Теория:**
- Custom container runtimes
- Docker plugins и расширения
- Работа с GPU в контейнерах
- Интеграция с облачными платформами (AWS, GCP, Azure)

**Ресурсы для изучения:**
- 📖 [Container Runtime](https://docs.docker.com/engine/alternative-runtimes/)
- 🎥 "Advanced Docker Features"
- 📄 "GPU Computing in Containers"

**Практические задания:**

1. **GPU поддержка:**
   ```bash
   # Установка nvidia-docker
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   
   # Запуск с GPU
   docker run --gpus all nvidia/cuda:11.0-base nvidia-smi
   ```

2. **Custom runtime:**
   ```json
   {
     "runtimes": {
       "nvidia": {
         "path": "nvidia-container-runtime",
         "runtimeArgs": []
       }
     }
   }
   ```

3. **AWS интеграция:**
   ```bash
   # ECR login
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
   
   # Push в ECR
   docker tag my-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
   ```

**Экспертное задание:**
Создать систему ML обучения с использованием GPU контейнеров и облачной интеграции.

### Глава 7.2: Архитектурные паттерны
**Время:** 8-9 дней

**Теория:**
- Микросервисная архитектура с Docker
- Service mesh (Istio, Linkerd)
- Sidecar pattern
- Event-driven архитектура
- CQRS и Event Sourcing в контейнерах

**Ресурсы для изучения:**
- 📖 [Microservices with Docker](https://docs.docker.com/get-started/microservices/)
- 🎥 "Service Mesh Architecture"
- 📄 "Event-Driven Microservices"

**Практические задания:**

1. **Микросервисная архитектура:**
   ```yaml
   version: '3.8'
   services:
     # API Gateway
     gateway:
       image: nginx:alpine
       ports:
         - "80:80"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
   
     # User Service
     user-service:
       build: ./user-service
       environment:
         - DATABASE_URL=postgresql://user:pass@user-db:5432/users
   
     user-db:
       image: postgres:13
       environment:
         POSTGRES_DB: users
         POSTGRES_USER: user
         POSTGRES_PASSWORD: pass
   
     # Order Service
     order-service:
       build: ./order-service
       environment:
         - DATABASE_URL=postgresql://user:pass@order-db:5432/orders
         - USER_SERVICE_URL=http://user-service:3000
   
     order-db:
       image: postgres:13
       environment:
         POSTGRES_DB: orders
         POSTGRES_USER: user
         POSTGRES_PASSWORD: pass
   
     # Message Queue
     rabbitmq:
       image: rabbitmq:3-management
       ports:
         - "15672:15672"
   ```

2. **Event-driven архитектура:**
   ```javascript
   // Event publisher
   const amqp = require('amqplib');
   
   async function publishEvent(eventType, data) {
     const connection = await amqp.connect('amqp://rabbitmq');
     const channel = await connection.createChannel();
     await channel.assertExchange('events', 'topic');
     channel.publish('events', eventType, Buffer.from(JSON.stringify(data)));
   }
   ```

3. **Sidecar pattern:**
   ```yaml
   services:
     app:
       image: my-app
       volumes:
         - shared-data:/data
   
     sidecar:
       image: my-sidecar
       volumes:
         - shared-data:/data
       command: ["./monitor.sh"]
   
   volumes:
     shared-data:
   ```

**Архитектурный проект:**
Спроектировать и реализовать полную микросервисную систему с event-driven архитектурой.

### Глава 7.3: Экосистема и будущее
**Время:** 6-7 дней

**Теория:**
- Container runtime ecosystem (containerd, CRI-O, runc)
- Kubernetes и его отношение к Docker
- OCI стандарты
- Подман как альтернатива Docker
- Будущее контейнеризации

**Ресурсы для изучения:**
- 📖 [OCI Specifications](https://opencontainers.org/)
- 🎥 "Container Runtime Landscape"
- 📄 "Future of Container Technology"

**Практические задания:**

1. **Работа с containerd:**
   ```bash
   # Установка containerd
   sudo apt-get install containerd
   
   # Использование ctr
   sudo ctr images pull docker.io/library/nginx:latest
   sudo ctr run docker.io/library/nginx:latest nginx-test
   ```

2. **Podman как альтернатива:**
   ```bash
   # Установка Podman
   sudo apt-get install podman
   
   # Использование (совместимо с Docker CLI)
   podman run -d --name web nginx
   podman generate systemd --new --files --name web
   ```

3. **Исследование OCI спецификации:**
   ```bash
   # Создание OCI bundle
   mkdir oci-bundle
   cd oci-bundle
   runc spec
   # Редактирование config.json
   runc run mycontainer
   ```

**Исследовательские задания:**
1. Сравнить производительность Docker, Podman, и containerd
2. Создать презентацию о будущем контейнерных технологий
3. Написать техническую статью о выборе container runtime

---

## 🏆 Финальные проекты и сертификация

### Капстоун проект (2 недели)
Выберите один из проектов:

1. **E-commerce платформа:**
   - Микросервисная архитектура
   - CI/CD пайплайн
   - Мониторинг и логирование
   - Production развертывание

2. **ML платформа:**
   - GPU вычисления
   - Масштабируемая обработка данных
   - Model serving
   - Automated retraining

3. **DevOps платформа:**
   - Self-hosted CI/CD
   - Container registry
   - Мониторинг инфраструктуры
   - Автоматизация развертывания

### Подготовка к сертификации

**Docker Certified Associate (DCA):**
- 📖 [DCA Study Guide](https://docker.com/certification)
- 🎯 Практические тесты
- 📝 Mock экзамены

**Дополнительные сертификации:**
- Kubernetes (CKA, CKAD)
- AWS Container Services
- Azure Container Instances

---

## 📚 Дополнительные ресурсы

### Книги:
- "Docker in Action" - Jeff Nickoloff
- "Docker Deep Dive" - Nigel Poulton
- "Kubernetes in Action" - Marko Luksa

### Онлайн курсы:
- Docker Mastery (Udemy)
- Kubernetes Course (A Cloud Guru)
- Container Orchestration (Pluralsight)

### Практические платформы:
- Play with Docker
- Katacoda Docker scenarios
- Docker Labs

### Сообщества:
- Docker Community Slack
- r/docker на Reddit
- Stack Overflow

---

## ✅ Чек-лист прогресса

### Блок 1: Основы
- [ ] Понимаю концепцию контейнеризации
- [ ] Установил и настроил Docker
- [ ] Могу работать с образами и контейнерами
- [ ] Понимаю Docker Hub

### Блок 2: Образы и контейнеры
- [ ] Умею писать Dockerfile
- [ ] Использую multi-stage builds
- [ ] Оптимизирую размер образов
- [ ] Управляю жизненным циклом контейнеров

### Блок 3: Сеть и данные
- [ ] Настраиваю сети Docker
- [ ] Работаю с различными типами storage
- [ ] Применяю практики безопасности
- [ ] Делаю backup данных

### Блок 4: Compose и оркестрация
- [ ] Создаю сложные compose файлы
- [ ] Использую продвинутые возможности
- [ ] Понимаю основы оркестрации
- [ ] Знаком с Docker Swarm

### Блок 5: CI/CD
- [ ] Интегрирую Docker в CI/CD
- [ ] Оптимизирую сборки
- [ ] Работаю с registry
- [ ] Применяю стратегии развертывания

### Блок 6: Production
- [ ] Настраиваю мониторинг
- [ ] Оптимизирую производительность
- [ ] Готовлю к production
- [ ] Реализую disaster recovery

### Блок 7: Экспертный уровень
- [ ] Использую продвинутые возможности
- [ ] Проектирую архитектуры
- [ ] Знаком с экосистемой
- [ ] Планирую будущее развитие

---

**Удачи в изучении Docker! 🐳**