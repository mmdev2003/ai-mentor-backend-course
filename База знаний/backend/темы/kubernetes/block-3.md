# 🌐 Блок 3: Сетевое взаимодействие и хранение данных

**⏱️ Продолжительность:** 2-3 недели  
**🎯 Цель:** Освоить сложные аспекты сетей и персистентного хранения

---

## 3.1 Ingress и Ingress Controllers (4-5 дней)

### Проблема внешнего доступа к приложениям

**Ограничения Services для внешнего доступа:**

```
SERVICE LIMITATIONS FOR EXTERNAL ACCESS
──────────────────────────────────────────

NodePort:
├── Порты в диапазоне 30000-32767
├── Один Service = один порт на всех узлах
├── Нет HTTP маршрутизации
└── ❌ Не подходит для production

LoadBalancer:
├── Каждый Service = один LoadBalancer
├── Дорого (каждый LB стоит денег)
├── Нет продвинутой маршрутизации
└── ❌ Не масштабируется для множества сервисов
```

### Что такое Ingress

Ingress — это **API объект**, который управляет внешним доступом к сервисам в кластере, обычно HTTP/HTTPS:

```
INGRESS CONCEPT
─────────────────────────────────────────

Internet
    ↓
┌─────────────────────────────────────┐
│         Ingress Controller          │
│    (NGINX, Traefik, Istio, etc)    │
└─────────────────────────────────────┘
    ↓ (routes based on rules)
┌─────────────────────────────────────┐
│            Ingress Rules            │
│                                     │
│ api.example.com     → API Service   │
│ web.example.com     → Web Service   │
│ admin.example.com   → Admin Service │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│              Services               │
│   ┌─────────┐ ┌─────────┐ ┌───────┐ │
│   │   API   │ │   Web   │ │ Admin │ │
│   │ Service │ │ Service │ │Service│ │
│   └─────────┘ └─────────┘ └───────┘ │
└─────────────────────────────────────┘
```

### Ingress vs Service: Ключевые отличия

```
INGRESS vs SERVICES COMPARISON
─────────────────────────────────────

Service (LoadBalancer):
├── Layer 4 (TCP/UDP)
├── Один IP = один Service
├── Простая балансировка нагрузки
└── Дорого для множественных приложений

Ingress:
├── Layer 7 (HTTP/HTTPS)
├── Один IP = множество приложений
├── Host-based и path-based маршрутизация
├── SSL termination
├── URL rewriting
└── Экономически эффективно
```

### Анатомия Ingress

```
INGRESS RESOURCE STRUCTURE
─────────────────────────────────────

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /v1
        pathType: Prefix
        backend:
          service:
            name: api-v1-service
            port: 80
      - path: /v2  
        pathType: Prefix
        backend:
          service:
            name: api-v2-service
            port: 80
```

### Типы маршрутизации в Ingress

#### 1. Host-based Routing (виртуальные хосты)
```
HOST-BASED ROUTING
─────────────────────────────────────

Request: api.example.com/users
    ↓
Ingress Controller checks Host header
    ↓
Routes to: api-service

Request: web.example.com/home
    ↓  
Ingress Controller checks Host header
    ↓
Routes to: web-service
```

#### 2. Path-based Routing
```
PATH-BASED ROUTING  
─────────────────────────────────────

example.com/api/*     → API Service
example.com/web/*     → Web Service  
example.com/admin/*   → Admin Service
example.com/docs/*    → Docs Service

Same host, different paths!
```

#### 3. Combined Routing
```
COMBINED HOST + PATH ROUTING
─────────────────────────────────────

api.example.com/v1/*     → API v1 Service
api.example.com/v2/*     → API v2 Service
web.example.com/app/*    → Web App Service
web.example.com/assets/* → Static Assets Service
```

### PathType: типы совпадения путей

```
PATH TYPES EXPLAINED
─────────────────────────────────────

Exact:
├── /api/users → matches only /api/users
└── /api/users/ → NO match

Prefix:  
├── /api → matches /api, /api/, /api/users, /api/v1/users
└── Most commonly used

ImplementationSpecific:
├── Depends on Ingress Controller
└── NGINX: regex support, Traefik: middleware
```

### Популярные Ingress Controllers

#### 1. NGINX Ingress Controller
```
NGINX INGRESS FEATURES
─────────────────────────────────────

✅ Mature and stable
✅ High performance
✅ Rich annotation support
✅ Rate limiting, auth, caching
✅ WebSocket support
✅ Custom NGINX configuration

Архитектура:
Internet → NGINX Pod → Service → Backend Pods
```

#### 2. Traefik
```
TRAEFIK FEATURES
─────────────────────────────────────

✅ Automatic service discovery
✅ Built-in Let's Encrypt
✅ Dashboard UI
✅ Middleware system
✅ Multiple backends support
✅ Cloud-native design

Архитектура:
Internet → Traefik Pod → Automatic discovery → Services
```

#### 3. Istio Gateway
```
ISTIO GATEWAY FEATURES
─────────────────────────────────────

✅ Part of service mesh
✅ Advanced traffic management
✅ Security policies
✅ Observability
✅ Circuit breakers
✅ Retry mechanisms

Архитектура:
Internet → Envoy Proxy → Service Mesh → Services
```

#### 4. HAProxy Ingress
```
HAPROXY INGRESS FEATURES
─────────────────────────────────────

✅ Enterprise-grade load balancing
✅ High availability
✅ Advanced health checks
✅ Blue-green deployments
✅ Canary releases
✅ TCP and HTTP support
```

### SSL/TLS Termination

Ingress поддерживает **автоматическое** управление SSL сертификатами:

```
SSL TERMINATION FLOW
─────────────────────────────────────

Client (HTTPS) → Ingress Controller → Service (HTTP)
    ↓                    ↓
 Encrypted         Decrypts here
 Traffic           Forwards as HTTP

Benefits:
├── Centralized certificate management
├── Offloads SSL processing from apps
├── Automatic certificate renewal
└── SNI (Server Name Indication) support
```

### Автоматические SSL сертификаты с cert-manager

```
CERT-MANAGER WORKFLOW
─────────────────────────────────────

1. Ingress created with TLS config
2. cert-manager detects new Ingress
3. Creates Certificate resource
4. Initiates ACME challenge with Let's Encrypt
5. Stores certificate in Secret
6. Ingress Controller uses certificate

┌─────────────────────────────────────┐
│           cert-manager              │
│                                     │
│ Monitors Ingress → Creates Cert →   │
│ ACME Challenge → Gets Certificate → │
│ Stores in Secret → Updates Ingress  │
└─────────────────────────────────────┘
```

### Annotations: расширенная конфигурация

Annotations позволяют **тонко настроить** поведение Ingress Controller:

```
COMMON NGINX INGRESS ANNOTATIONS
─────────────────────────────────────

Traffic Control:
├── nginx.ingress.kubernetes.io/rate-limit: "100"
├── nginx.ingress.kubernetes.io/connection-limit: "10"
└── nginx.ingress.kubernetes.io/bandwidth: "1M"

Authentication:
├── nginx.ingress.kubernetes.io/auth-type: "basic"
├── nginx.ingress.kubernetes.io/auth-secret: "basic-auth"
└── nginx.ingress.kubernetes.io/auth-realm: "Protected Area"

URL Manipulation:
├── nginx.ingress.kubernetes.io/rewrite-target: "/"
├── nginx.ingress.kubernetes.io/ssl-redirect: "true"
└── nginx.ingress.kubernetes.io/permanent-redirect: "https://new.example.com"

Backend Configuration:
├── nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
├── nginx.ingress.kubernetes.io/upstream-hash-by: "$request_uri"
└── nginx.ingress.kubernetes.io/proxy-timeout: "300"
```

---

## 3.2 Network Policies: безопасность сети (3-4 дней)

### Проблема сетевой безопасности по умолчанию

**По умолчанию в Kubernetes:**

```
DEFAULT NETWORK BEHAVIOR
─────────────────────────────────────

All Pods can communicate with ALL other Pods
    ↓
┌─────────────────────────────────────┐
│  Frontend  ←→  Backend  ←→  Database │
│      ↑           ↑          ↑       │
│      └───────────┼──────────┘       │
│                  ↓                  │
│            Any External Pod         │
└─────────────────────────────────────┘

⚠️  Security Risk: No network segmentation!
```

### Принципы Network Segmentation

Network Policies реализуют принцип **Zero Trust** в сети:

```
ZERO TRUST NETWORK MODEL
─────────────────────────────────────

Default: DENY ALL
    ↓
Explicitly ALLOW only required connections
    ↓
┌─────────────────────────────────────┐
│  Frontend  ──→  Backend  ──→  DB    │
│      ↑           ↑          ↑       │
│      ❌          ✅         ✅      │
│   (blocked)   (allowed)  (allowed)  │
│                                     │
│  External Pod ❌ (blocked from all) │
└─────────────────────────────────────┘
```

### Что такое Network Policy

Network Policy — это **спецификация**, описывающая как группы Pod'ов могут общаться:

```
NETWORK POLICY STRUCTURE
─────────────────────────────────────

NetworkPolicy
├── podSelector: which pods this policy applies to
├── policyTypes: [Ingress, Egress, or both]
├── ingress: rules for incoming traffic
│   ├── from: source selection
│   └── ports: allowed ports
└── egress: rules for outgoing traffic
    ├── to: destination selection  
    └── ports: allowed ports
```

### Селекторы в Network Policies

#### 1. podSelector
```
POD SELECTOR
─────────────────────────────────────

Selects pods by labels within SAME namespace:

podSelector:
  matchLabels:
    app: database
    
Applies to: all pods with app=database label
```

#### 2. namespaceSelector
```
NAMESPACE SELECTOR
─────────────────────────────────────

Selects ALL pods in matching namespaces:

namespaceSelector:
  matchLabels:
    environment: production
    
Applies to: all pods in namespaces with environment=production
```

#### 3. Combined Selectors
```
COMBINED SELECTORS
─────────────────────────────────────

Both namespace AND pod must match:

- namespaceSelector:
    matchLabels:
      environment: production
  podSelector:
    matchLabels:
      app: frontend
      
Applies to: frontend pods in production namespaces
```

### Типы правил: Ingress vs Egress

#### Ingress Rules (входящий трафик)
```
INGRESS RULES
─────────────────────────────────────

Controls WHO can connect TO this pod:

    Other Pods
        ↓ (incoming)
   ┌─────────────┐
   │ Target Pod  │ ← Network Policy applies here
   └─────────────┘

Example: Only frontend pods can connect to backend
```

#### Egress Rules (исходящий трафик)
```
EGRESS RULES
─────────────────────────────────────

Controls WHERE this pod can connect TO:

   ┌─────────────┐
   │ Source Pod  │ ← Network Policy applies here  
   └─────────────┘
        ↓ (outgoing)
    Other Pods/External

Example: Backend can only connect to database
```

### Практические примеры Network Policies

#### 1. Default Deny All
```
DEFAULT DENY POLICY
─────────────────────────────────────

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}  # Empty = all pods
  policyTypes:
  - Ingress
  - Egress
  # No ingress/egress rules = deny all

Result: Complete network isolation
```

#### 2. Allow Only Frontend to Backend
```
FRONTEND → BACKEND POLICY
─────────────────────────────────────

Target: Backend pods (app=backend)
Allow: Only from Frontend pods (app=frontend)

spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

#### 3. Allow Database Access Only from Backend
```
BACKEND → DATABASE POLICY
─────────────────────────────────────

Target: Database pods (app=database)
Allow: Only from Backend pods (app=backend)

spec:
  podSelector:
    matchLabels:
      app: database  
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 5432
```

#### 4. Cross-Namespace Communication
```
CROSS-NAMESPACE POLICY
─────────────────────────────────────

Allow production frontend to access staging API:

spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress  
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          environment: production
      podSelector:
        matchLabels:
          app: frontend
```

### Egress Policies: контроль исходящего трафика

#### 1. Allow DNS Resolution
```
DNS EGRESS POLICY
─────────────────────────────────────

All pods need DNS, so allow DNS queries:

egress:
- to: []  # any destination
  ports:
  - protocol: UDP
    port: 53
  - protocol: TCP  
    port: 53
```

#### 2. Allow External API Access
```
EXTERNAL API EGRESS
─────────────────────────────────────

Allow backend to call external payment API:

egress:
- to: []  # external (outside cluster)
  ports:
  - protocol: TCP
    port: 443  # HTTPS
- to:  # internal DNS
  - namespaceSelector:
      matchLabels:
        name: kube-system
  ports:
  - protocol: UDP
    port: 53
```

### IP Block Selectors

Network Policies могут ограничивать доступ по **IP-адресам**:

```
IP BLOCK EXAMPLES
─────────────────────────────────────

Allow only specific IP ranges:
- to:
  - ipBlock:
      cidr: 10.0.0.0/8
      except:
      - 10.1.0.0/16  # Block this subnet

Block internet access:
- to:
  - ipBlock:
      cidr: 10.0.0.0/8  # Only internal
  - namespaceSelector: {}  # Any namespace
```

### Debugging Network Policies

#### 1. Проверка применения политик
```
DEBUGGING WORKFLOW
─────────────────────────────────────

1. Check if CNI supports Network Policies
   kubectl get nodes -o wide
   
2. Verify policy existence
   kubectl get networkpolicies
   
3. Check policy details  
   kubectl describe networkpolicy <name>
   
4. Test connectivity
   kubectl exec -it pod1 -- nc -zv pod2-ip 8080
   
5. Check logs
   - CNI plugin logs
   - kube-proxy logs
```

#### 2. Распространенные ошибки
```
COMMON NETWORK POLICY MISTAKES
─────────────────────────────────────

❌ Forgetting DNS egress rules
   Result: Pods can't resolve service names
   
❌ Empty podSelector without policyTypes
   Result: Policy doesn't apply
   
❌ Mixing ingress/egress in wrong direction
   Result: Asymmetric connectivity
   
❌ Not understanding namespace isolation
   Result: Cross-namespace communication blocked
   
❌ CNI doesn't support Network Policies
   Result: Policies ignored silently
```

### CNI и поддержка Network Policies

```
CNI NETWORK POLICY SUPPORT
─────────────────────────────────────

✅ Supported:
├── Calico
├── Cilium  
├── Weave Net
├── Antrea
└── Kube-router

❌ Not Supported:
├── Flannel (basic)
├── Bridge
└── Host-local

⚠️  Check your CNI before implementing policies!
```

---

## 3.3 Volumes и Persistent Volumes (4-5 дней)

### Проблема хранения данных в контейнерах

**Контейнеры ephemeral (эфемерные):**

```
CONTAINER STORAGE PROBLEM
─────────────────────────────────────

Container Start:
┌─────────────────────────────────┐
│  Container Filesystem           │
│  ├── /app (application)         │
│  ├── /tmp (temporary files)     │
│  └── /data (application data)   │
└─────────────────────────────────┘

Container Dies:
┌─────────────────────────────────┐
│         ALL DATA LOST! ❌       │
└─────────────────────────────────┘

Problem: Data doesn't survive container restarts
```

### Концепция Volumes в Kubernetes

Volume — это **директория**, доступная всем контейнерам в Pod'е:

```
VOLUME CONCEPT
─────────────────────────────────────

Pod
├── Container 1 ─┐
├── Container 2 ─┤ ──→ Volume (shared storage)
└── Container 3 ─┘
                   ↑
            Survives container restarts
```

### Типы Volumes

#### 1. emptyDir
**Временное хранилище**, существует только пока жив Pod:

```
EMPTYDIR VOLUME
─────────────────────────────────────

Pod Start:
┌─────────────────────────────────┐
│ Pod                             │
│ ├── Container A ─┐              │
│ └── Container B ─┤ ─→ emptyDir   │
│                  └─→ /shared     │
└─────────────────────────────────┘

Pod Dies:
┌─────────────────────────────────┐
│      emptyDir deleted ❌        │
└─────────────────────────────────┘

Use cases:
├── Scratch space
├── Cache
├── Inter-container communication
└── Temporary processing
```

#### 2. hostPath
**Монтирует директорию** с узла в Pod:

```
HOSTPATH VOLUME
─────────────────────────────────────

Node Filesystem:
/var/log/app/ ←──┐
                 │
Pod:             │
┌─────────────────────────────────┐
│ Container      │                │
│ /app/logs ─────┘                │
└─────────────────────────────────┘

⚠️  Security Risk: Access to node filesystem
⚠️  Not portable: Tied to specific node
```

#### 3. configMap Volume
**Монтирует ConfigMap** как файлы:

```
CONFIGMAP VOLUME
─────────────────────────────────────

ConfigMap:
├── database.conf = "host=db.example.com"
└── app.properties = "debug=true"

Pod:
┌─────────────────────────────────┐
│ Container                       │
│ /etc/config/                    │
│ ├── database.conf               │
│ └── app.properties              │
└─────────────────────────────────┘

Updates: ConfigMap changes → Files update automatically
```

#### 4. secret Volume
**Монтирует Secret** как файлы:

```
SECRET VOLUME
─────────────────────────────────────

Secret:
├── username = "admin"
└── password = "secret123"

Pod:
┌─────────────────────────────────┐
│ Container                       │
│ /etc/secrets/                   │
│ ├── username (file)             │
│ └── password (file)             │
└─────────────────────────────────┘

Security: Files created with restricted permissions (0400)
```

### Проблемы обычных Volumes

```
VOLUME LIMITATIONS
─────────────────────────────────────

❌ Tied to Pod lifecycle
❌ No sharing between Pods  
❌ Manual storage provisioning
❌ No dynamic allocation
❌ Cloud storage integration issues
❌ No storage classes
❌ Backup/restore complexity

Need: Independent storage lifecycle!
```

### Persistent Volumes (PV) - Концепция

PV — это **кластерный ресурс** для хранения данных, независимый от Pod'ов:

```
PERSISTENT VOLUME CONCEPT
─────────────────────────────────────

Traditional:
Pod → Volume (dies with Pod) ❌

Kubernetes PV:
Pod → PVC → PV (independent lifecycle) ✅

┌─────────────────────────────────┐
│         Cluster Level           │
│                                 │
│  PV1 (100Gi)  PV2 (50Gi)      │
│      ↑             ↑           │
│    PVC1          PVC2          │
│      ↑             ↑           │
│    Pod1          Pod2          │
└─────────────────────────────────┘
```

### PV vs PVC: разделение ответственности

```
PV vs PVC RESPONSIBILITIES
─────────────────────────────────────

Persistent Volume (PV):
├── Cluster Administrator creates
├── Defines actual storage (NFS, AWS EBS, etc)
├── Capacity, access modes, policies
└── Infrastructure concern

Persistent Volume Claim (PVC):
├── Developer/User creates
├── Requests storage with requirements
├── Size, access mode needed
└── Application concern

Binding Process:
PVC (request) → Kubernetes → PV (matches) → Bound
```

### Жизненный цикл PV и PVC

```
PV/PVC LIFECYCLE
─────────────────────────────────────

1. Provisioning:
   ├── Static: Admin creates PV manually
   └── Dynamic: StorageClass auto-creates PV

2. Binding:
   PVC → finds matching PV → Bound

3. Using:
   Pod → mounts PVC → accesses storage

4. Releasing:
   PVC deleted → PV becomes "Released"

5. Reclaiming:
   ├── Retain: PV kept, manual cleanup
   ├── Delete: PV and storage deleted
   └── Recycle: PV data wiped, reusable (deprecated)
```

### Access Modes (режимы доступа)

```
ACCESS MODES EXPLAINED
─────────────────────────────────────

ReadWriteOnce (RWO):
├── One node can mount read-write
├── Multiple pods on SAME node can share
└── Most common for databases

ReadOnlyMany (ROX):  
├── Multiple nodes can mount read-only
├── Good for shared configuration
└── Static content distribution

ReadWriteMany (RWX):
├── Multiple nodes can mount read-write  
├── Requires special storage (NFS, CephFS)
└── Shared application data

ReadWriteOncePod (RWOP):
├── Only ONE pod can mount read-write
├── Kubernetes 1.22+
└── Strict single-pod access
```

### Типы хранилищ и поддерживаемые режимы

```
STORAGE TYPES vs ACCESS MODES
─────────────────────────────────────

AWS EBS:        RWO only
GCE PD:         RWO only
Azure Disk:     RWO only

NFS:            RWO, ROX, RWX
CephFS:         RWO, ROX, RWX
GlusterFS:      RWO, ROX, RWX

Local Storage:  RWO only
HostPath:       RWO only
```

### Reclaim Policies (политики освобождения)

```
RECLAIM POLICIES
─────────────────────────────────────

Retain (по умолчанию):
├── PV остается после удаления PVC
├── Данные сохраняются
├── Требует ручной очистки
└── Самый безопасный вариант

Delete:
├── PV удаляется с PVC
├── Underlying storage тоже удаляется
├── Автоматическая очистка
└── ⚠️ Данные теряются навсегда!

Recycle (deprecated):
├── PV данные очищаются (rm -rf)
├── PV становится доступным снова
└── ❌ Не используйте в production
```

---

## 3.4 Storage Classes и динамическое выделение (3-4 дня)

### Проблема статического provisioning

**Статическое создание PV:**

```
STATIC PROVISIONING PROBLEMS
─────────────────────────────────────

1. Admin manually creates PVs:
   kubectl apply -f pv1.yaml
   kubectl apply -f pv2.yaml
   ...

2. Developer creates PVC:
   kubectl apply -f pvc.yaml

3. Problems:
   ❌ Manual overhead
   ❌ Pre-provisioning required
   ❌ Waste of resources
   ❌ No on-demand allocation
   ❌ Doesn't scale
```

### Что такое Storage Class

Storage Class — это **"рецепт"** для динамического создания PV:

```
STORAGE CLASS CONCEPT
─────────────────────────────────────

Storage Class = Template for PV creation

┌─────────────────────────────────┐
│        Storage Class            │
│                                 │
│ Provisioner: aws-ebs            │
│ Parameters:                     │
│   type: gp3                     │
│   iops: 3000                    │
│   encrypted: true               │
└─────────────────────────────────┘
         ↓ (creates PV when needed)
┌─────────────────────────────────┐
│     Dynamic PV Creation         │
│                                 │
│ PVC created → SC provisions →   │
│ PV created automatically        │
└─────────────────────────────────┘
```

### Динамическое provisioning workflow

```
DYNAMIC PROVISIONING FLOW
─────────────────────────────────────

1. Developer creates PVC:
   storageClassName: fast-ssd
   
2. Kubernetes finds Storage Class "fast-ssd"

3. Storage Class calls Provisioner

4. Provisioner creates actual storage:
   ├── AWS: Creates EBS volume
   ├── GCP: Creates PD volume  
   ├── Azure: Creates Disk
   └── On-prem: Creates volume on SAN

5. Kubernetes creates PV automatically

6. PVC binds to new PV

7. Pod mounts PVC
```

### Популярные Provisioners

#### 1. Cloud Provisioners
```
CLOUD PROVISIONERS
─────────────────────────────────────

AWS:
├── ebs.csi.aws.com (EBS CSI Driver)
├── efs.csi.aws.com (EFS CSI Driver)
└── fsx.csi.aws.com (FSx CSI Driver)

GCP:
├── pd.csi.storage.gke.io (Persistent Disk)
└── filestore.csi.storage.gke.io (Filestore)

Azure:
├── disk.csi.azure.com (Azure Disk)
├── file.csi.azure.com (Azure Files)
└── blob.csi.azure.com (Azure Blob)
```

#### 2. On-premises Provisioners
```
ON-PREMISES PROVISIONERS  
─────────────────────────────────────

Ceph:
├── rook-ceph.rbd.csi.ceph.com
└── rook-ceph.cephfs.csi.ceph.com

OpenEBS:
├── openebs.io/provisioner-iscsi
└── local.cstor.openebs.io

Longhorn:
└── driver.longhorn.io

NetApp:
└── csi.trident.netapp.io
```

### Parameters: настройка Storage Class

```
STORAGE CLASS PARAMETERS
─────────────────────────────────────

AWS EBS Example:
parameters:
  type: gp3              # Volume type
  iops: "3000"          # IOPS performance
  throughput: "125"     # MB/s throughput
  encrypted: "true"     # Encryption
  kmsKeyId: "alias/..."  # KMS key

GCP PD Example:
parameters:
  type: pd-ssd          # SSD type
  zones: us-central1-a,us-central1-b
  replication-type: regional-pd

Azure Disk Example:
parameters:
  skuName: Premium_LRS   # Performance tier
  location: eastus       # Region
  cachingmode: ReadOnly  # Caching
```

### allowVolumeExpansion: расширение томов

```
VOLUME EXPANSION
─────────────────────────────────────

Storage Class with expansion:
allowVolumeExpansion: true

Expansion process:
1. Edit PVC spec (increase size)
2. Storage driver expands underlying volume
3. Kubernetes updates PV
4. File system expanded (if needed)

┌─────────────────────────────────┐
│ PVC: 10Gi → edit → 20Gi        │
│                ↓                │
│ Underlying storage: 10Gi → 20Gi │
│                ↓                │
│ Filesystem: resize2fs/xfs_growfs│
└─────────────────────────────────┘

⚠️ Can only INCREASE size, never decrease!
```

### Default Storage Class

```
DEFAULT STORAGE CLASS
─────────────────────────────────────

Annotation marks default:
annotations:
  storageclass.kubernetes.io/is-default-class: "true"

Behavior:
├── PVC without storageClassName uses default
├── Only one default allowed per cluster
└── Can be changed by annotation

Check default:
kubectl get storageclass
NAME              PROVISIONER         AGE
fast-ssd          ebs.csi.aws.com     1d
standard (default) ebs.csi.aws.com    5d
```

### Volume Snapshots

```
VOLUME SNAPSHOT WORKFLOW
─────────────────────────────────────

1. Create VolumeSnapshotClass:
   driver: ebs.csi.aws.com
   
2. Create VolumeSnapshot:
   source: pvc-name
   
3. Restore from snapshot:
   dataSource:
     kind: VolumeSnapshot
     name: my-snapshot

┌─────────────────────────────────┐
│ Original PVC → Snapshot → New PVC│
│                                 │
│ Point-in-time data recovery     │
└─────────────────────────────────┘
```

### CSI (Container Storage Interface)

CSI — это **стандартный интерфейс** для подключения storage систем:

```
CSI ARCHITECTURE
─────────────────────────────────────

┌─────────────────────────────────┐
│         Kubernetes              │
└─────────────────────────────────┘
              ↓ (CSI API)
┌─────────────────────────────────┐
│         CSI Driver              │
│                                 │
│ ├── Controller Plugin           │
│ │   (provision, attach, snapshot)│
│ └── Node Plugin                 │
│     (mount, unmount)            │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│      Storage System             │
│   (AWS EBS, Ceph, NetApp...)    │
└─────────────────────────────────┘
```

---

## 3.5 StatefulSets для stateful приложений (3-4 дня)

### Проблема stateful приложений с Deployments

**Deployment характеристики:**

```
DEPLOYMENT CHARACTERISTICS
─────────────────────────────────────

✅ Good for stateless apps:
├── Pods are interchangeable  
├── Random names (pod-abc123)
├── Any pod can handle any request
└── Scale up/down easily

❌ Bad for stateful apps:
├── Databases need stable identity
├── Ordered startup/shutdown required
├── Persistent storage per instance
└── Network identity important
```

### Примеры stateful приложений

```
STATEFUL APPLICATIONS EXAMPLES
─────────────────────────────────────

Databases:
├── MySQL/PostgreSQL clusters
├── MongoDB replica sets
├── Cassandra clusters
└── Elasticsearch clusters

Message Queues:
├── Apache Kafka
├── RabbitMQ clusters
└── Redis clusters

Distributed Systems:
├── Apache Zookeeper
├── etcd clusters
└── Consul clusters
```

### Что такое StatefulSet

StatefulSet управляет **stateful приложениями** с гарантиями:

```
STATEFULSET GUARANTEES
─────────────────────────────────────

1. Stable Network Identity:
   pod-0, pod-1, pod-2 (predictable names)

2. Stable Storage:
   Each pod gets its own PVC

3. Ordered Deployment:
   pod-0 → pod-1 → pod-2 (sequential)

4. Ordered Termination:  
   pod-2 → pod-1 → pod-0 (reverse order)

5. Ordered Rolling Updates:
   Update pod-2, then pod-1, then pod-0
```

### StatefulSet vs Deployment

```
STATEFULSET vs DEPLOYMENT
─────────────────────────────────────

Deployment:
├── Pod names: web-7d4b9c8f-abc123
├── Any pod can be killed/replaced
├── Shared storage (if any)
├── Parallel scaling
└── Use case: Web servers, APIs

StatefulSet:
├── Pod names: web-0, web-1, web-2
├── Ordered operations required
├── Per-pod storage
├── Sequential scaling  
└── Use case: Databases, message queues
```

### Stable Network Identity

#### Pod Names
```
POD NAMING IN STATEFULSET
─────────────────────────────────────

StatefulSet name: mysql
Replicas: 3

Pod names:
├── mysql-0 (always the first)
├── mysql-1 (always the second)  
└── mysql-2 (always the third)

Even after restart, names stay the same!
```

#### Headless Service
StatefulSet **требует** Headless Service для DNS:

```
HEADLESS SERVICE FOR STATEFULSET
─────────────────────────────────────

Service: mysql-headless (ClusterIP: None)
StatefulSet: mysql

DNS Records:
├── mysql-0.mysql-headless.default.svc.cluster.local
├── mysql-1.mysql-headless.default.svc.cluster.local
└── mysql-2.mysql-headless.default.svc.cluster.local

Each pod gets its own DNS name!
```

### Persistent Storage per Pod

```
STATEFULSET STORAGE
─────────────────────────────────────

volumeClaimTemplates:
- metadata:
    name: data
  spec:
    storageClassName: fast-ssd
    accessModes: [ReadWriteOnce]
    resources:
      requests:
        storage: 10Gi

Result:
├── Pod mysql-0 → PVC data-mysql-0 → PV-1
├── Pod mysql-1 → PVC data-mysql-1 → PV-2  
└── Pod mysql-2 → PVC data-mysql-2 → PV-3

Each pod has its own dedicated storage!
```

### Ordered Deployment и Scaling

#### Ordered Startup
```
ORDERED STARTUP PROCESS
─────────────────────────────────────

StatefulSet creation:
1. mysql-0 created and READY
2. mysql-1 created and READY
3. mysql-2 created and READY

⚠️ Next pod waits for previous to be Ready!

Use case: Database clusters where order matters
```

#### Ordered Shutdown
```
ORDERED SHUTDOWN PROCESS
─────────────────────────────────────

StatefulSet deletion:
1. mysql-2 terminated
2. mysql-1 terminated  
3. mysql-0 terminated (last)

⚠️ Reverse order of creation!

Use case: Graceful cluster shutdown
```

#### Scaling Operations
```
SCALING STATEFULSET
─────────────────────────────────────

Scale up (2 → 3):
mysql-0, mysql-1 exist
└── Create mysql-2

Scale down (3 → 2):  
mysql-0, mysql-1, mysql-2 exist
└── Delete mysql-2 (highest ordinal first)

⚠️ Always highest ordinal removed first!
```

### Rolling Updates в StatefulSet

```
STATEFULSET ROLLING UPDATE
─────────────────────────────────────

updateStrategy: RollingUpdate

Process:
1. Update mysql-2 (highest ordinal first)
2. Wait for mysql-2 to be Ready
3. Update mysql-1
4. Wait for mysql-1 to be Ready
5. Update mysql-0

⚠️ Reverse order of creation!
⚠️ Wait for Ready between updates!
```

### Partition Updates

```
PARTITION UPDATE STRATEGY
─────────────────────────────────────

updateStrategy:
  type: RollingUpdate
  rollingUpdate:
    partition: 1

Behavior:
├── Pods with ordinal ≥ partition updated
├── Pods with ordinal < partition unchanged
└── Allows canary deployments

Example: partition=1
├── mysql-2 → updated ✅
├── mysql-1 → not updated ❌
└── mysql-0 → not updated ❌
```

### Использование StatefulSet: практические примеры

#### 1. MySQL Cluster
```
MYSQL CLUSTER EXAMPLE
─────────────────────────────────────

StatefulSet: mysql-cluster
├── mysql-0: Master (read/write)
├── mysql-1: Slave (read-only)
└── mysql-2: Slave (read-only)

Init Containers:
├── Clone data from master
└── Configure replication

Persistent Storage:
├── Each pod: 20Gi SSD
└── Data survives pod restarts
```

#### 2. Apache Kafka
```
KAFKA CLUSTER EXAMPLE
─────────────────────────────────────

StatefulSet: kafka
├── kafka-0: Broker ID 0
├── kafka-1: Broker ID 1  
└── kafka-2: Broker ID 2

Each broker:
├── Stable network identity (broker.id)
├── Persistent storage for logs
└── Ordered startup for cluster formation
```

#### 3. Elasticsearch
```
ELASTICSEARCH CLUSTER EXAMPLE
─────────────────────────────────────

StatefulSet: elasticsearch
├── es-0: Master-eligible node
├── es-1: Data node
└── es-2: Data node

Features:
├── Stable node names for cluster discovery
├── Persistent storage for indices
└── Ordered shutdown to prevent data loss
```

### Когда НЕ использовать StatefulSet

```
WHEN NOT TO USE STATEFULSET
─────────────────────────────────────

❌ Stateless applications (use Deployment)
❌ Applications that don't need stable identity
❌ Load-balanced services without state
❌ Microservices APIs
❌ Frontend applications  
❌ Worker processes without persistent state

Use Deployment instead for:
├── Web servers
├── REST APIs
├── Microservices
└── Stateless workers
```

---

## 🏆 Полученные знания после Блока 3

После изучения этого блока вы будете понимать:

### Сетевые компетенции:
- **HTTP/HTTPS маршрутизация** через Ingress
- **Выбор и настройка** Ingress Controllers
- **SSL termination** и certificate management
- **Network segmentation** с Network Policies
- **Zero Trust** сетевая модель
- **Debugging** сетевых проблем

### Storage компетенции:
- **Архитектура хранилища** в Kubernetes
- **Различия** между Volume, PV, и PVC
- **Динамическое provisioning** через Storage Classes
- **Volume snapshots** и disaster recovery
- **CSI драйверы** и интеграция с storage
- **StatefulSet паттерны** для stateful приложений

### Архитектурные решения:
```
ADVANCED KUBERNETES ARCHITECTURE
─────────────────────────────────────

Internet
    ↓
Ingress Controller (SSL termination)
    ↓
Services (L7 routing)  
    ↓
Pods (Network Policies applied)
    ↓
Persistent Volumes (CSI managed)
    ↓
Underlying Storage (Cloud/On-prem)
```

### Производственные навыки:
- Проектирование сетевой архитектуры для production
- Настройка безопасной сегментации сети
- Планирование storage strategy для различных workload'ов
- Выбор подходящих patern'ов (Deployment vs StatefulSet)

### Интеграция с облачными платформами:
- AWS: ELB, EBS, EFS интеграция
- GCP: GKE Ingress, Persistent Disks
- Azure: Application Gateway, Azure Disks
- Multi-cloud storage strategies

---

## 📚 Практические задания для закрепления

### Задание 1: Ingress с SSL
Настройте Ingress для многоуровневого приложения с:
- Host-based routing для разных сервисов
- Автоматические SSL сертификаты через cert-manager
- Rate limiting и basic authentication

### Задание 2: Network Segmentation  
Реализуйте Zero Trust сеть:
- Default deny all policy
- Разрешите только необходимые соединения
- Протестируйте connectivity между компонентами

### Задание 3: Stateful Application
Разверните MongoDB replica set с:
- StatefulSet для стабильной идентичности
- Persistent storage для каждого replica
- Headless service для DNS discovery
- Backup strategy с volume snapshots

---

**Следующий блок**: Безопасность и управление доступом 🔒