# 🏗️ Блок 4: Инфраструктура как код (IaC)
*Полное руководство по управлению инфраструктурой через код*

---

## 📋 Введение в блок

**Цель блока:** Освоить принципы Infrastructure as Code, научиться управлять инфраструктурой декларативно с помощью Terraform, Ansible и cloud-платформ.

**Время изучения:** 2-3 месяца  
**Сложность:** Средняя-высокая  
**Практическая направленность:** 60% теории, 40% практики

---

## 🎯 Глава 4.1: Terraform основы

### Что такое Infrastructure as Code?

**Infrastructure as Code (IaC)** - это практика управления и провизионирования инфраструктуры через машинно-читаемые файлы определений, а не через физическую конфигурацию оборудования или интерактивные инструменты конфигурации.

### Проблемы традиционного подхода

```
Традиционная инфраструктура:
Manual Setup ──► Configuration Drift ──► Inconsistency
     │                    │                    │
  Click-ops          Snowflake            Debugging
  Scripts            Servers              Nightmare
     │                    │                    │
  No Version         No Rollback         Production
  Control            Capability          Issues

------------------------------------------------

IaC подход:
Code ──► Version Control ──► Automated Deploy ──► Consistent Infrastructure
  │            │                     │                      │
Source of    Git History         Repeatable           Predictable
Truth        Rollback           Process              Results
  │            │                     │                      │
Peer         Audit Trail        Testing             Infrastructure
Review                          Possible            Documentation
```

### Принципы Infrastructure as Code

#### 1. Декларативный подход
```
Императивный стиль (КАК делать):
1. Создать VPC
2. Создать subnet в VPC
3. Создать Internet Gateway
4. Присоединить Gateway к VPC
5. Создать Route Table
6. Добавить маршруты в таблицу

--------------------------------------------

Декларативный стиль (ЧТО нужно):
Желаемое состояние:
├── VPC с CIDR 10.0.0.0/16
├── Public subnet 10.0.1.0/24
├── Internet Gateway
├── Route Table с маршрутом в интернет
└── EC2 instance в subnet
```

#### 2. Идемпотентность
```
Идемпотентные операции:

Первый запуск:
terraform apply
├── Создается VPC
├── Создается Subnet  
├── Создается EC2
└── Результат: Infrastructure created

Второй запуск (без изменений):
terraform apply
├── VPC существует ✓
├── Subnet существует ✓
├── EC2 существует ✓
└── Результат: No changes needed

Третий запуск (с изменениями):
terraform apply
├── VPC существует ✓
├── Subnet существует ✓
├── EC2 модифицируется (instance type)
└── Результат: Infrastructure updated
```

### Terraform архитектура и компоненты

```
Terraform Workflow:

Write ──► Plan ──► Apply ──► State
  │         │        │        │
 .tf       Preview  Execute   Track
Files     Changes   Changes   Resources
  │         │        │        │
HCL      terraform terraform terraform
Code     plan      apply     state
  │         │        │        │
  └─────────┼────────┼────────┘
            │        │
         Terraform   Provider
         Core        APIs
            │        │
            └────────┘
```

#### Core Components

**1. Providers - интерфейсы к API**
```
Provider Ecosystem:

Cloud Providers:
├── AWS Provider
├── Azure Provider (azurerm)
├── Google Cloud Provider
├── Alibaba Cloud Provider
└── Oracle Cloud Provider

Infrastructure Providers:
├── Kubernetes Provider
├── Docker Provider
├── Helm Provider
├── Consul Provider
└── Vault Provider

Monitoring & Tools:
├── Datadog Provider
├── New Relic Provider
├── PagerDuty Provider
├── Grafana Provider
└── GitHub Provider
```

**2. Resources - основные строительные блоки**
```
Resource Definition Structure:

resource "provider_type" "local_name" {
  ├── Required Arguments
  ├── Optional Arguments  
  ├── Meta-arguments:
  │   ├── depends_on
  │   ├── count
  │   ├── for_each
  │   ├── provider
  │   └── lifecycle
  └── Computed Attributes (read-only)
```

**3. Data Sources - чтение существующей инфраструктуры**
```
Data Source Usage Pattern:

External Infrastructure ──► Data Source ──► Reference in Resources
         │                      │                    │
    Existing VPC            data.aws_vpc         var.vpc_id
    Existing AMI           data.aws_ami          var.ami_id
    Remote State           data.terraform_      var.remote_state
                          remote_state
```

### HCL (HashiCorp Configuration Language)

#### Основные типы данных

```
HCL Data Types:

Primitive Types:
├── string: "hello world"
├── number: 42, 3.14159
├── bool: true, false
└── null: explicitly no value

Complex Types:
├── list: ["a", "b", "c"]
├── set: toset(["a", "b", "c"])
├── map: {key1 = "value1", key2 = "value2"}
├── object: {name = "John", age = 30}
└── tuple: ["a", 1, true]

Type Constraints:
├── any: any type allowed
├── string: only strings
├── list(string): list of strings
├── map(number): map with number values
└── object({name=string, age=number})
```

#### Variables и Outputs

```
Variable Definition Pattern:

Input Variables ──► Processing ──► Output Values
      │                │               │
variable "instance_type" {           output "instance_ip" {
  description = "EC2 type"             value = aws_instance.web.public_ip
  type        = string                 description = "Public IP"
  default     = "t3.micro"             sensitive   = false
  validation {                       }
    condition = contains([
      "t3.micro", "t3.small"
    ], var.instance_type)
    error_message = "Invalid type"
  }
}
```

#### Locals и Functions

```
Locals for Computed Values:

locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    Owner       = var.owner
    CreatedBy   = "Terraform"
    CreatedAt   = timestamp()
  }
  
  instance_name = "${var.project_name}-${var.environment}-web"
  
  # Conditional logic
  instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"
  
  # Complex calculations
  subnet_cidrs = [
    for i in range(var.az_count) : 
    cidrsubnet(var.vpc_cidr, 8, i)
  ]
}
```

### State Management

Terraform State - это критически важный компонент, который отслеживает соответствие между конфигурацией и реальными ресурсами.

```
State Management Flow:

Configuration ──► Plan ──► Apply ──► State Update
      │            │        │           │
   Desired      Compare   Execute    Record
   State        States    Changes    Reality
      │            │        │           │
      └────────────┼────────┼───────────┘
                   │        │
               Current    Real
               State      Infrastructure
                   │        │
              terraform.  Provider
              tfstate     APIs
```

#### Local vs Remote State

```
State Storage Comparison:

Local State:
├── File: terraform.tfstate
├── Pros: Simple, fast
├── Cons: No collaboration, no locking
└── Use case: Personal projects, learning

Remote State:
├── Backends: S3, Azure Blob, GCS, Consul
├── Pros: Collaboration, locking, encryption
├── Cons: Network dependency, complexity
└── Use case: Team projects, production

State Locking:
Current Operation ──► Lock State ──► Execute ──► Unlock
       │                   │          │         │
   terraform apply      Prevent     Modify    Release
       │              Concurrent   Resources   Lock
       │              Operations      │         │
   Other terraform ──► Wait ─────────────────────┘
   operations
```

#### Remote Backends Configuration

```
Backend Types and Use Cases:

S3 Backend (AWS):
terraform {
  backend "s3" {
    ├── bucket: State storage
    ├── key: State file path
    ├── region: AWS region
    ├── encrypt: Encryption at rest
    ├── dynamodb_table: State locking
    └── versioning: State history
  }
}

Azure Backend:
terraform {
  backend "azurerm" {
    ├── storage_account_name: Account
    ├── container_name: Container
    ├── key: Blob name
    └── access_key: Authentication
  }
}

Terraform Cloud:
terraform {
  backend "remote" {
    ├── organization: TF Cloud org
    ├── hostname: app.terraform.io
    └── workspaces: Workspace config
  }
}
```

---

## 🔧 Глава 4.2: Terraform продвинутые техники

### Modules - переиспользование и организация кода

```
Module Structure:

Root Module
├── main.tf (root configuration)
├── variables.tf (input variables)
├── outputs.tf (output values)
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── compute/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── database/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── terraform.tfvars
```

#### Module Design Patterns

```
Module Composition Patterns:

1. Foundational Modules (Infrastructure):
vpc ──► subnets ──► security_groups ──► routing
 │        │            │                │
Base     Network     Firewall         Traffic
Layer    Layer       Layer            Layer

2. Service Modules (Applications):
compute ──► database ──► cache ──► monitoring
   │           │          │         │
  EC2/ECS    RDS/       Redis/     CloudWatch/
  Instances  DynamoDB   ElastiCache Datadog

3. Composite Modules (Complete Solutions):
web_app_stack
├── Uses: vpc module
├── Uses: compute module  
├── Uses: database module
├── Uses: monitoring module
└── Provides: Complete application infrastructure
```

#### Module Versioning Strategy

```
Module Versioning:

Git Tags for Versions:
├── v1.0.0: Initial release
├── v1.1.0: Feature addition
├── v1.1.1: Bug fix
└── v2.0.0: Breaking changes

Module Source References:
module "vpc" {
  source = "git::https://github.com/company/tf-modules.git//vpc?ref=v1.2.0"
  
  # or from Terraform Registry
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"
}

Versioning Best Practices:
├── Semantic versioning (MAJOR.MINOR.PATCH)
├── Changelog maintenance
├── Backward compatibility consideration
├── Testing matrix for versions
└── Deprecation notices
```

### Workspaces и Environment Management

```
Workspace Management Strategy:

Single Repository Approach:
main.tf ──► workspace: dev ──► AWS Account: Development
       ├─► workspace: staging ──► AWS Account: Staging  
       └─► workspace: prod ──► AWS Account: Production

Multi-Repository Approach:
├── terraform-dev/ ──► Development environment
├── terraform-staging/ ──► Staging environment
└── terraform-prod/ ──► Production environment

Workspace Operations:
├── terraform workspace list
├── terraform workspace new <name>
├── terraform workspace select <name>
├── terraform workspace delete <name>
└── terraform workspace show
```

#### Environment-specific Configuration

```
Environment Configuration Patterns:

Pattern 1: Workspace Variables
locals {
  environment_config = {
    dev = {
      instance_type = "t3.micro"
      min_size     = 1
      max_size     = 2
    }
    staging = {
      instance_type = "t3.small"
      min_size     = 2
      max_size     = 4
    }
    prod = {
      instance_type = "t3.large"
      min_size     = 3
      max_size     = 10
    }
  }
  
  current_env = local.environment_config[terraform.workspace]
}

Pattern 2: Variable Files
├── dev.tfvars
├── staging.tfvars
└── prod.tfvars

terraform apply -var-file="prod.tfvars"

Pattern 3: Environment Directories
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
```

### Advanced Terraform Features

#### Dynamic Blocks

```
Dynamic Block Usage:

Static Configuration:
security_group_rule {
  type        = "ingress"
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

security_group_rule {
  type        = "ingress"
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

----------------------------------------

Dynamic Configuration:
variable "ingress_rules" {
  default = [
    { port = 80, protocol = "tcp", cidr = ["0.0.0.0/0"] },
    { port = 443, protocol = "tcp", cidr = ["0.0.0.0/0"] },
    { port = 22, protocol = "tcp", cidr = ["10.0.0.0/8"] }
  ]
}

dynamic "ingress" {
  for_each = var.ingress_rules
  content {
    from_port   = ingress.value.port
    to_port     = ingress.value.port
    protocol    = ingress.value.protocol
    cidr_blocks = ingress.value.cidr
  }
}
```

#### For Expressions и Count/For Each

```
Iteration Patterns:

Count (Simple Iteration):
resource "aws_instance" "web" {
  count = var.instance_count
  
  ami           = var.ami_id
  instance_type = var.instance_type
  
  tags = {
    Name = "web-${count.index + 1}"
  }
}

For Each (Complex Iteration):
variable "instances" {
  default = {
    web = { type = "t3.micro", az = "us-east-1a" }
    db  = { type = "t3.small", az = "us-east-1b" }
    cache = { type = "t3.nano", az = "us-east-1c" }
  }
}

resource "aws_instance" "servers" {
  for_each = var.instances
  
  ami               = var.ami_id
  instance_type     = each.value.type
  availability_zone = each.value.az
  
  tags = {
    Name = each.key
    Type = each.value.type
  }
}

For Expression (Data Transformation):
locals {
  # Create list of instance IDs
  instance_ids = [for i in aws_instance.servers : i.id]
  
  # Create map of names to IPs
  instance_ips = {
    for k, v in aws_instance.servers : k => v.private_ip
  }
  
  # Conditional filtering
  production_instances = [
    for i in aws_instance.servers : i
    if i.tags.Environment == "production"
  ]
}
```

### Import и State Operations

```
State Management Operations:

Import Existing Resources:
terraform import aws_instance.web i-1234567890abcdef0
├── Updates state file
├── Requires resource configuration
├── No actual infrastructure change
└── Enables Terraform management

State Manipulation:
├── terraform state list
├── terraform state show <resource>
├── terraform state mv <source> <destination>
├── terraform state rm <resource>
└── terraform state pull/push

Resource Lifecycle Management:
resource "aws_instance" "web" {
  lifecycle {
    ├── create_before_destroy = true
    ├── prevent_destroy = true
    ├── ignore_changes = [tags, user_data]
    └── replace_triggered_by = [aws_ami.web]
  }
}
```

---

## 🎭 Глава 4.3: Ansible и конфигурационное управление

### Ansible архитектура и принципы

Ansible использует агентless архитектуру для управления конфигурацией:

```
Ansible Architecture:

Control Node ──SSH/WinRM──► Managed Nodes
     │                           │
┌─────────────┐              ┌─────────────┐
│  Ansible    │              │   Target    │
│  Engine     │              │   Servers   │
│             │              │             │
│ ├─Inventory │              │ ├─Python    │
│ ├─Playbooks│              │ ├─SSH       │
│ ├─Modules  │              │ ├─Sudo      │
│ └─Plugins  │              │ └─Services  │
└─────────────┘              └─────────────┘
      │                           │
  Push Model                 No Agent
  (vs Pull)                  Required
```

### Inventory Management

```
Inventory Structure:

Static Inventory (INI format):
[webservers]
web1.example.com ansible_host=10.0.1.10
web2.example.com ansible_host=10.0.1.11

[databases]
db1.example.com ansible_host=10.0.2.10
db2.example.com ansible_host=10.0.2.11

[production:children]
webservers
databases

[production:vars]
ansible_user=admin
environment=prod

----------------------------------------

Dynamic Inventory (YAML format):
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
  - us-west-2
keyed_groups:
  - key: tags.Environment
    prefix: env
  - key: instance_type
    prefix: type
hostnames:
  - ip-address
  - dns-name
```

#### Group Variables и Host Variables

```
Variable Hierarchy (Order of Precedence):

1. Command line values (ansible-playbook -e)
2. Role defaults
3. Inventory file variables
4. Inventory group_vars/all
5. Inventory group_vars/*
6. Inventory host_vars/*
7. Host facts discovered by setup
8. Play vars
9. Play vars_prompt
10. Play vars_files
11. Role vars
12. Block vars
13. Task vars
14. Include vars
15. Set_facts / registered vars
16. Role (and include_role) params
17. Include params
18. Extra vars (always win precedence)

Directory Structure:
inventory/
├── production/
│   ├── hosts.yml
│   ├── group_vars/
│   │   ├── all.yml
│   │   ├── webservers.yml
│   │   └── databases.yml
│   └── host_vars/
│       ├── web1.example.com.yml
│       └── db1.example.com.yml
```

### Playbooks и Tasks

```
Playbook Structure:

Playbook
├── Play 1
│   ├── hosts: webservers
│   ├── vars: play variables
│   ├── tasks:
│   │   ├── Task 1 (module + parameters)
│   │   ├── Task 2 (conditional)
│   │   └── Task 3 (loop)
│   └── handlers:
│       └── Handler 1 (triggered by notify)
├── Play 2
│   ├── hosts: databases
│   └── tasks: [...]
└── Play 3
    ├── hosts: all
    └── tasks: [...]
```

#### Task Execution Flow

```
Task Execution Model:

Playbook Start
     │
   Gather Facts ──► Host1, Host2, Host3
     │                 │      │      │
   Task 1 ──────────► Exec   Exec   Exec
     │                 │      │      │
   Wait for completion ◄┴──────┴──────┘
     │
   Task 2 ──────────► Parallel execution
     │
   Task 3 ──────────► Serial execution (serial: 1)
     │
   Handlers ────────► Triggered handlers only
     │
   Playbook End

Execution Strategies:
├── Linear (default): Wait for all hosts per task
├── Free: Hosts execute as fast as possible
├── Debug: Interactive debugging
└── Custom: User-defined strategies
```

### Roles - структурированная организация

```
Role Directory Structure:

roles/
└── webserver/
    ├── tasks/
    │   ├── main.yml          # Entry point for tasks
    │   ├── install.yml       # Package installation
    │   ├── configure.yml     # Configuration tasks
    │   └── security.yml      # Security hardening
    ├── handlers/
    │   └── main.yml          # Service restart handlers
    ├── templates/
    │   ├── nginx.conf.j2     # Jinja2 templates
    │   └── site.conf.j2
    ├── files/
    │   ├── index.html        # Static files
    │   └── ssl-cert.pem
    ├── vars/
    │   └── main.yml          # Role variables
    ├── defaults/
    │   └── main.yml          # Default variables
    ├── meta/
    │   └── main.yml          # Role metadata & dependencies
    └── README.md             # Role documentation
```

#### Role Dependencies

```
Role Dependency Management:

meta/main.yml:
dependencies:
  - role: common
    vars:
      some_parameter: 3
  - role: apache
    vars:
      apache_port: 80
  - role: postgres
    vars:
      postgres_version: 13

Dependency Resolution:
common ──► apache ──► postgres ──► webserver
  │         │          │           │
Base      Web        Database    Application
Config    Server     Server      Specific
```

### Ansible Vault для секретов

```
Vault Management Workflow:

Sensitive Data ──► Encrypt ──► Version Control ──► Decrypt ──► Use
      │             │              │               │          │
   Passwords     ansible-vault   Git Repository  Runtime    Playbook
   API Keys      encrypt                        Decryption  Execution
   Certificates     │              │               │          │
      │         Encrypted       Secure          ansible-     │
      │         Files          Storage         vault        │
      └─────────────────────────────────────────────────────┘

Vault Operations:
├── ansible-vault create secrets.yml
├── ansible-vault edit secrets.yml
├── ansible-vault encrypt vars/secrets.yml
├── ansible-vault decrypt vars/secrets.yml
├── ansible-vault view secrets.yml
└── ansible-vault rekey secrets.yml

Multiple Vault IDs:
├── --vault-id dev@prompt
├── --vault-id prod@~/.vault_pass
├── --vault-id testing@vault_script.py
└── Allows different keys for different environments
```

### Jinja2 Templating

```
Template Processing Flow:

Template File ──► Ansible Variables ──► Jinja2 Engine ──► Final File
     │                    │                  │               │
nginx.conf.j2        host_vars/          Processing      nginx.conf
     │              group_vars/              │         (on target)
   {{ var }}         facts                Filters            │
   {% if %}          playbook vars       Functions      Deployed
   {% for %}              │                  │               │
     │                    │                  │               │
     └────────────────────┼──────────────────┘               │
                          │                                  │
                    Combined Context ─────────────────────────┘

Template Examples:

Variables:
server_name: {{ ansible_fqdn }}
listen_port: {{ nginx_port | default(80) }}

Conditionals:
{% if ssl_enabled %}
ssl_certificate {{ ssl_cert_path }};
{% endif %}

Loops:
{% for upstream in backend_servers %}
server {{ upstream.host }}:{{ upstream.port }};
{% endfor %}

Filters:
{{ user_list | join(', ') }}
{{ password | b64encode }}
{{ config_file | to_nice_json }}
```

---

## ☁️ Глава 4.4: Cloud platforms основы

### Multi-Cloud Architecture Patterns

```
Cloud Strategy Approaches:

Single Cloud (Cloud-Native):
Applications ──► AWS/Azure/GCP Services
     │                    │
  Vendor Lock-in      Maximum Integration
     │                    │
  Lower Complexity    Vendor-specific Features

Multi-Cloud (Best-of-Breed):
Applications ──► Multiple Cloud Providers
     │                    │
  Vendor Independence   Higher Complexity
     │                    │
  Risk Distribution     Consistent Interfaces

Hybrid Cloud:
On-Premises ──► Private Cloud ──► Public Cloud
     │               │                │
  Legacy Apps    Sensitive Data   Scalable Workloads
     │               │                │
  Compliance    Internal Apps    Burst Capacity
```

### AWS Core Services

```
AWS Service Categories:

Compute:
├── EC2: Virtual machines
├── Lambda: Serverless functions
├── ECS/EKS: Container orchestration
├── Batch: Batch processing
└── Lightsail: Simple VPS

Storage:
├── S3: Object storage
├── EBS: Block storage
├── EFS: Network file system
├── FSx: High-performance file systems
└── Storage Gateway: Hybrid storage

Networking:
├── VPC: Virtual private cloud
├── CloudFront: CDN
├── Route 53: DNS
├── Direct Connect: Dedicated connection
└── API Gateway: API management

Database:
├── RDS: Relational databases
├── DynamoDB: NoSQL database
├── Redshift: Data warehouse
├── ElastiCache: In-memory cache
└── DocumentDB: Document database
```

#### AWS VPC Architecture

```
VPC Network Design:

AWS Region (us-east-1)
├── VPC (10.0.0.0/16)
    ├── Availability Zone A
    │   ├── Public Subnet (10.0.1.0/24)
    │   │   ├── Internet Gateway
    │   │   ├── NAT Gateway
    │   │   └── Load Balancer
    │   └── Private Subnet (10.0.10.0/24)
    │       ├── Application Servers
    │       └── Database Servers
    ├── Availability Zone B
    │   ├── Public Subnet (10.0.2.0/24)
    │   └── Private Subnet (10.0.20.0/24)
    └── Availability Zone C
        ├── Public Subnet (10.0.3.0/24)
        └── Private Subnet (10.0.30.0/24)

Traffic Flow:
Internet ──► IGW ──► Public Subnet ──► NAT Gateway ──► Private Subnet
    │           │          │              │              │
  External    Entry     Load Balancer   Outbound      Application
  Access      Point     Web Servers     Internet      Servers
    │           │          │              │              │
    └───────────┴──────────┴──────────────┴──────────────┘
```

### Azure Core Services

```
Azure Service Organization:

Resource Groups:
├── Logical containers for resources
├── Lifecycle management
├── RBAC scope
├── Billing scope
└── Policy application

Core Services:
Compute:
├── Virtual Machines: IaaS compute
├── App Service: PaaS web apps
├── Functions: Serverless compute
├── Container Instances: Container hosting
└── Kubernetes Service: Managed K8s

Storage:
├── Blob Storage: Object storage
├── Files: Network file shares
├── Queue: Message queuing
├── Table: NoSQL key-value
└── Disk: VM disk storage

Networking:
├── Virtual Network: Software-defined networking
├── Load Balancer: Layer 4 load balancing
├── Application Gateway: Layer 7 load balancing
├── VPN Gateway: Site-to-site connectivity
└── ExpressRoute: Dedicated connectivity
```

#### Azure Resource Manager (ARM)

```
ARM Template Structure:

{
  "$schema": "https://schema.management.azure.com/...",
  "contentVersion": "1.0.0.0",
  "parameters": {
    ├── Input values for template
    └── Runtime customization
  },
  "variables": {
    ├── Computed values
    └── Complex expressions
  },
  "resources": [
    ├── Resource definitions
    ├── Dependencies
    └── Configuration
  ],
  "outputs": {
    ├── Return values
    └── Reference for other templates
  }
}

Template Deployment Flow:
Template ──► Validation ──► Deployment ──► Monitoring
    │            │             │            │
  ARM JSON    Syntax Check   Resource      Activity
  Bicep       Dependency     Creation      Logs
    │            │             │            │
  Parameters  Access Check   Configuration  Status
    │            │             │            │
    └────────────┼─────────────┼────────────┘
                 │             │
            Resource Graph  Resource
            API Calls       Management
```

### Google Cloud Platform (GCP)

```
GCP Service Hierarchy:

Organization
├── Folders (optional)
    ├── Projects
        ├── Resources
            ├── Compute Engine (VMs)
            ├── Cloud Storage (Object storage)
            ├── Cloud SQL (Managed databases)
            ├── Kubernetes Engine (GKE)
            └── Cloud Functions (Serverless)

Core Services:
Compute:
├── Compute Engine: Virtual machines
├── App Engine: PaaS platform
├── Cloud Run: Containerized apps
├── Cloud Functions: Event-driven functions
└── Kubernetes Engine: Managed Kubernetes

Storage & Databases:
├── Cloud Storage: Object storage
├── Cloud SQL: Relational databases
├── Firestore: NoSQL document database
├── Bigtable: Wide-column NoSQL
└── Memorystore: Managed Redis/Memcached

Networking:
├── VPC: Virtual private cloud
├── Cloud Load Balancing: Global load balancing
├── Cloud CDN: Content delivery
├── Cloud DNS: Domain name system
└── Cloud Interconnect: Dedicated connectivity
```

### FinOps и Cost Optimization

```
Cloud Cost Management Framework:

Cost Visibility:
├── Tagging Strategy
│   ├── Environment (dev/staging/prod)
│   ├── Project (application name)
│   ├── Owner (team/individual)
│   ├── Cost Center (business unit)
│   └── Purpose (function/service)
├── Cost Allocation
│   ├── Chargeback (exact costs)
│   ├── Showback (awareness)
│   └── Budgets & Alerts
└── Reporting & Analytics
    ├── Cost trends
    ├── Usage patterns
    └── Optimization opportunities

Cost Optimization Strategies:

Right-sizing:
Current ──► Monitor ──► Analyze ──► Resize ──► Monitor
  │           │          │          │          │
Over-        CPU/Memory  Usage      Smaller    Validate
provisioned  Metrics    Patterns   Instance   Performance
  │           │          │          │          │
Waste       Historical  Rightsizing Savings   Continuous
Identified  Data       Recommendations        Optimization

Reserved Instances:
On-Demand ──► Analyze ──► Purchase ──► Manage ──► Renewal
    │          │          │           │          │
  Flexible   Usage      Reserved     Utilization Planning
  Pricing    Patterns   Capacity     Monitoring    │
    │          │          │           │          │
  Higher     Commitment  Lower       Optimization Next
  Cost       Planning   Cost        Tracking    Period
```

### Infrastructure Security

```
Cloud Security Shared Responsibility Model:

Customer Responsibility:
├── Data encryption (in transit & at rest)
├── Identity and access management
├── Operating system updates
├── Network traffic protection
├── Application-level security
└── Configuration management

Cloud Provider Responsibility:
├── Physical infrastructure security
├── Hypervisor security
├── Network infrastructure
├── Service availability
├── Hardware maintenance
└── Compliance certifications

Security Implementation Layers:

Network Security:
├── VPC/VNet configuration
├── Security groups / NSGs
├── NACLs / Route tables
├── Web Application Firewall
└── DDoS protection

Identity & Access:
├── Principle of least privilege
├── Multi-factor authentication
├── Service accounts / Managed identities
├── Role-based access control
└── Regular access reviews

Data Protection:
├── Encryption at rest (AES-256)
├── Encryption in transit (TLS 1.2+)
├── Key management (KMS/Key Vault)
├── Data classification
└── Backup and recovery
```

---

## 🔄 Интеграция IaC с CI/CD

### GitOps для Infrastructure

```
GitOps Infrastructure Workflow:

Git Repository ──► CI Pipeline ──► Infrastructure Deployment
      │               │                    │
Infrastructure     Plan &               Apply Changes
Code Changes      Validate                  │
      │               │                    │
   ┌─────────┐    ┌─────────┐        ┌─────────┐
   │  .tf    │    │terraform│        │ AWS/    │
   │  .yml   │    │ plan    │        │ Azure/  │
   │ files   │    │validate │        │ GCP     │
   └─────────┘    └─────────┘        └─────────┘
      │               │                    │
   Pull Request   Automated Tests      State Update
   Review         Security Scan           │
      │               │                    │
   Approve ───────────┼────────────────────┘
                      │
                 Merge to main
```

### Infrastructure Pipeline Design

```
IaC Pipeline Stages:

1. Validate ──► 2. Plan ──► 3. Security ──► 4. Apply ──► 5. Test ──► 6. Notify
     │              │           │             │           │          │
  Syntax        Resource     Compliance    Resource     Infrastructure Stakeholder
  Check         Changes      Scanning      Creation     Validation    Communication
     │              │           │             │           │          │
  Linting       Cost         Policy        State        Smoke        Slack/Teams
  terraform     Estimation   Validation    Management   Tests        Email
  validate         │           │             │           │          │
     │         terraform    tfsec/         terraform    Integration   │
  YAML/JSON      plan       checkov        apply        Tests         │
  validation        │           │             │           │          │
     │              │           │             │           │          │
     └──────────────┼───────────┼─────────────┼───────────┼──────────┘
                    │           │             │           │
               Plan Review   Security      Approval     Success
               (PR Comment)  Gate          Gate         Metrics
```

### Multi-Environment Strategy

```
Environment Promotion Flow:

Development ──► Staging ──► Production
     │             │            │
  Feature       Integration   Release
  Branches       Branch       Tags
     │             │            │
  ┌─────────┐  ┌─────────┐  ┌─────────┐
  │Auto     │  │Manual   │  │Manual   │
  │Deploy   │  │Approval │  │Approval │
  │         │  │Required │  │+ Timer  │
  └─────────┘  └─────────┘  └─────────┘
     │             │            │
  terraform    terraform    terraform
  workspace:   workspace:   workspace:
  dev          staging      production

Configuration Management:
environments/
├── dev/
│   ├── terraform.tfvars
│   └── backend.tf
├── staging/
│   ├── terraform.tfvars
│   └── backend.tf
└── production/
    ├── terraform.tfvars
    └── backend.tf

Variable Hierarchy:
Global Defaults ──► Environment Specific ──► Runtime Override
      │                     │                     │
   defaults.tf          staging.tfvars       -var="..."
      │                     │                     │
   Common values        Environment values   Pipeline values
```

---

## 📊 Best Practices и паттерны

### Infrastructure as Code Best Practices

#### 1. Code Organization

```
Repository Structure Best Practices:

Monorepo Approach:
infrastructure/
├── modules/                    # Reusable modules
│   ├── vpc/
│   ├── compute/
│   └── database/
├── environments/              # Environment-specific configs
│   ├── dev/
│   ├── staging/
│   └── production/
├── policies/                  # Security and compliance policies
├── scripts/                   # Automation scripts
└── docs/                     # Documentation

Multi-repo Approach:
├── terraform-modules/         # Shared modules repository
├── infrastructure-dev/        # Development environment
├── infrastructure-staging/    # Staging environment
├── infrastructure-prod/       # Production environment
└── platform-policies/        # Governance repository
```

#### 2. Security and Compliance

```
Security Implementation Strategy:

Policy as Code:
├── Open Policy Agent (OPA)
├── Terraform Sentinel
├── Azure Policy
├── AWS Config Rules
└── GCP Organization Policy

Security Scanning Integration:
Source Code ──► Static Analysis ──► Plan Review ──► Runtime Monitoring
     │              │                  │                │
  Git hooks      tfsec/checkov     Manual review    Cloud security
     │              │                  │                │
  Pre-commit    Automated fixes    Cost analysis    Continuous
  validation    Policy violations   Impact assessment monitoring
     │              │                  │                │
     └──────────────┼──────────────────┼────────────────┘
                    │                  │
               Security Gate      Approval Gate
```

#### 3. State Management

```
State Management Best Practices:

State Isolation:
├── Environment separation
├── Service/component separation
├── Blast radius minimization
└── Team ownership boundaries

State Backend Configuration:
production/
├── networking/
│   └── terraform.tf (backend: s3, key: prod/networking)
├── security/
│   └── terraform.tf (backend: s3, key: prod/security)
└── applications/
    ├── web-app/
    │   └── terraform.tf (backend: s3, key: prod/web-app)
    └── api-service/
        └── terraform.tf (backend: s3, key: prod/api-service)

Cross-State References:
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "company-terraform-state"
    key    = "prod/networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use networking outputs
subnet_id = data.terraform_remote_state.networking.outputs.private_subnet_id
```

### Testing Infrastructure Code

```
Testing Pyramid for Infrastructure:

                    /\
                   /  \
                  /    \
                 / E2E  \      ← Integration tests
                /  Tests \     ← Full environment
               /          \    ← Real cloud resources
              /____________\
             /              \
            / Contract Tests \  ← Interface testing
           /                  \ ← Module boundaries
          /____________________\
         /                      \
        /    Unit Tests          \ ← Logic testing
       /                          \← Static analysis
      /____________________________\← Syntax validation

Testing Tools and Approaches:

Static Testing:
├── terraform validate (syntax)
├── terraform fmt (formatting)
├── tflint (linting)
├── tfsec (security)
└── checkov (compliance)

Unit Testing:
├── Terratest (Go-based testing)
├── Kitchen-Terraform (Ruby-based)
├── Terraform module tests
└── Mock providers

Integration Testing:
├── Deploy to test environment
├── Validate infrastructure state
├── Test application deployment
├── Validate connectivity
└── Performance testing

Contract Testing:
├── Module interface validation
├── Output verification
├── Dependency testing
└── API compatibility
```

---

## 📈 Мониторинг и управление изменениями

### Infrastructure Drift Detection

```
Drift Detection Workflow:

Scheduled Scan ──► Compare ──► Report ──► Remediate
      │             │          │          │
  terraform plan  State vs    Drift       Auto-fix or
  (read-only)     Reality     Detection   Manual review
      │             │          │          │
  Cloud APIs      Differences  Alerting   Apply changes
      │             │          │          │
  Current state   Configuration Dashboard   State update
      │           drift           │          │
      └─────────────┼─────────────┼──────────┘
                    │             │
               Compliance      Change
               Monitoring      Management
```

### Change Management Process

```
Infrastructure Change Workflow:

Request ──► Planning ──► Review ──► Testing ──► Approval ──► Deploy ──► Verify
    │          │           │          │           │          │         │
 RFC/Ticket  Impact      Technical   Test       Change      Execute   Post-
 Submission  Analysis    Review      Environment Advisory    Plan      Deploy
    │          │           │          │        Board         │         │
 Business   Dependencies Security    Staging   Risk          Production Monitoring
 Justification Architecture Review  Validation Assessment   Deployment  │
    │          │           │          │           │          │         │
 Change      Cost         Compliance Rollback   Approval     Blue/Green Validation
 Category    Estimation   Check      Plan       Decision     Deploy     │
    │          │           │          │           │          │         │
    └──────────┼───────────┼──────────┼───────────┼──────────┼─────────┘
               │           │          │           │          │
          Architecture  Security    Test        Stakeholder Production
          Review        Gate        Results     Sign-off    Success
```

### Disaster Recovery для Infrastructure

```
DR Strategy for IaC:

Backup Strategy:
├── State file backups (automated)
├── Configuration repository (Git)
├── Secrets backup (encrypted)
├── Documentation (runbooks)
└── Dependency tracking

Recovery Procedures:
Primary Region Failure ──► Trigger DR ──► Deploy to DR Region
        │                     │               │
   Monitor health          Automated       terraform apply
   Detection               failover        (DR configuration)
        │                     │               │
   Alert systems          DNS update      Application
   Integration             Load balancer   deployment
        │                     │               │
        └─────────────────────┼───────────────┘
                              │
                        Full service
                        restoration

Multi-Region Architecture:
├── Active-Active (global load balancing)
├── Active-Passive (warm standby)
├── Backup-Restore (cold standby)
└── Pilot Light (minimal standby)
```

---

## 🎓 Заключение блока

### Ключевые выводы

1. **Infrastructure as Code трансформирует управление инфраструктурой**
   - Переход от manual operations к automation
   - Версионирование и rollback capabilities
   - Consistency и reproducibility

2. **Terraform обеспечивает декларативное управление**
   - Multi-cloud support через providers
   - State management для отслеживания изменений
   - Modules для code reusability

3. **Ansible дополняет Terraform конфигурационным управлением**
   - Agentless architecture для простоты
   - Powerful templating с Jinja2
   - Extensive module ecosystem

4. **Cloud platforms предоставляют building blocks**
   - Managed services снижают operational overhead
   - Pay-as-you-use модель оптимизирует costs
   - Global infrastructure обеспечивает scale

5. **Security и compliance должны быть встроены**
   - Policy as Code для automated enforcement
   - Secrets management на всех уровнях
   - Continuous monitoring и drift detection

### Практические навыки

После изучения этого блока вы сможете:
- ✅ Создавать и управлять инфраструктурой через код
- ✅ Использовать Terraform для multi-cloud deployments
- ✅ Автоматизировать конфигурацию с помощью Ansible
- ✅ Применять cloud-native архитектурные паттерны
- ✅ Внедрять security и compliance best practices
- ✅ Интегрировать IaC в CI/CD pipeline

### Подготовка к следующему блоку

Следующий **Блок 5: Мониторинг и логирование** покроет:
- Prometheus и Grafana для metrics
- ELK Stack для centralized logging
- Distributed tracing с Jaeger
- Observability best practices
- SLI/SLO/SLA определения
- Incident response automation

### Дополнительные ресурсы

**Книги:**
- "Terraform: Up & Running" - Yevgeniy Brikman
- "Ansible for DevOps" - Jeff Geerling
- "Cloud Native Infrastructure" - Justin Garrison, Kris Nova

**Сертификации:**
- HashiCorp Certified: Terraform Associate
- Red Hat Certified Specialist in Ansible Automation
- AWS Certified Solutions Architect
- Azure Solutions Architect Expert
- Google Cloud Professional Cloud Architect

**Практические проекты:**
1. Multi-tier application deployment с Terraform
2. Configuration management с Ansible playbooks
3. Multi-cloud infrastructure setup
4. GitOps workflow для infrastructure changes
5. Disaster recovery automation

---

*💡 Совет: Infrastructure as Code - это не только технология, но и культурный сдвиг. Начинайте с малого, автоматизируйте постепенно, и всегда документируйте свои решения для команды.*