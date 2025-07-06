# Блок 3: Паттерны проектирования
*От проверенных решений к экспертному мышлению*

---

## 🎯 Цели блока
- Изучить проверенные решения типовых задач программирования
- Научиться выбирать подходящие паттерны для конкретных ситуаций
- Понять, когда паттерны помогают, а когда могут навредить
- Развить архитектурное мышление через изучение классических решений

**Длительность:** 5-6 недель  
**Уровень:** Средний → Продвинутый

---

## 📚 Глава 1: Введение в паттерны проектирования

### Что такое паттерн проектирования?

```
🏗️  ПАТТЕРН = ПРОБЛЕМА + КОНТЕКСТ + РЕШЕНИЕ
```

**Паттерн проектирования** — это переиспользуемое решение часто встречающейся проблемы в проектировании программного обеспечения в определенном контексте.

### История паттернов

```
1977 → Christopher Alexander (архитектура зданий)
1987 → Beck & Cunningham (применение к ПО)
1994 → "Gang of Four" - классическая книга
2024 → Современная адаптация паттернов
```

### Структура описания паттерна

```
┌─────────────────────────────────────┐
│  📋 НАЗВАНИЕ ПАТТЕРНА              │
├─────────────────────────────────────┤
│  🎯 НАЗНАЧЕНИЕ                     │
│     Краткое описание цели          │
├─────────────────────────────────────┤
│  🔍 ПРОБЛЕМА                       │
│     Когда возникает необходимость  │
├─────────────────────────────────────┤
│  💡 РЕШЕНИЕ                        │
│     Как паттерн решает проблему    │
├─────────────────────────────────────┤
│  ⚖️  КОМПРОМИССЫ                   │
│     Плюсы и минусы применения      │
├─────────────────────────────────────┤
│  🛠️  РЕАЛИЗАЦИЯ                    │
│     Примеры кода                   │
└─────────────────────────────────────┘
```

### Классификация паттернов GoF

```
                    ПАТТЕРНЫ ПРОЕКТИРОВАНИЯ
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    ПОРОЖДАЮЩИЕ       СТРУКТУРНЫЕ        ПОВЕДЕНЧЕСКИЕ
   (Creational)       (Structural)       (Behavioral)
        │                  │                  │
    ┌───┴───┐          ┌───┴───┐          ┌───┴───┐
    │ • Singleton      │ • Adapter        │ • Observer
    │ • Factory        │ • Decorator      │ • Strategy
    │ • Builder        │ • Facade         │ • Command
    │ • Prototype      │ • Composite      │ • State
    └─────────┘        └─────────┘        └─────────┘
```

---

## 🏭 Глава 2: Порождающие паттерны (Creational Patterns)

*Как создавать объекты правильно*

### 2.1 Singleton (Одиночка)

#### 🎯 Назначение
Гарантирует, что у класса есть только один экземпляр, и предоставляет глобальную точку доступа к нему.

#### 🔍 Проблема
```
❌ Проблемы без Singleton:
┌─────────────────────────────────────┐
│  App creates: DatabaseConnection    │
│  Service creates: DatabaseConnection│  ← Дублирование ресурсов
│  Controller creates: DatabaseConnection │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Singleton:
┌─────────────────────────────────────┐
│           App                       │
│            │                        │
│       ┌────▼────┐                   │
│       │ Singleton│ ← Единственный   │
│       │ Instance │   экземпляр      │
│       └────▲────┘                   │
│            │                        │
│     Service │ Controller            │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

**Базовый Singleton:**
```java
public class DatabaseConnection {
    private static DatabaseConnection instance;
    
    private DatabaseConnection() {
        // Приватный конструктор
    }
    
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            instance = new DatabaseConnection();
        }
        return instance;
    }
}
```

**Thread-Safe Singleton:**
```java
public class DatabaseConnection {
    private static volatile DatabaseConnection instance;
    
    private DatabaseConnection() {}
    
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
}
```

**Enum Singleton (рекомендуемый):**
```java
public enum DatabaseConnection {
    INSTANCE;
    
    public void connect() {
        // логика подключения
    }
}

// Использование
DatabaseConnection.INSTANCE.connect();
```

#### ⚖️ Компромиссы

```
✅ ПЛЮСЫ                    ❌ МИНУСЫ
├─ Контроль создания       ├─ Глобальное состояние
├─ Экономия ресурсов       ├─ Сложность тестирования
├─ Ленивая инициализация   ├─ Нарушение SRP
└─ Гарантия единственности └─ Скрытые зависимости
```

#### 🚨 Когда НЕ использовать
- Для передачи данных между компонентами
- Когда нужна гибкость в количестве экземпляров
- В многопоточных приложениях без необходимости

---

### 2.2 Factory Method (Фабричный метод)

#### 🎯 Назначение
Создает объекты без указания их конкретных классов, делегируя решение подклассам.

#### 🔍 Проблема
```
❌ Без фабрики:
┌─────────────────────────────────────┐
│ if (type == "car") {                │
│     return new Car();               │ ← Жесткая связь
│ } else if (type == "truck") {       │
│     return new Truck();             │
│ }                                   │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С Factory Method:
┌─────────────────────────────────────┐
│         VehicleFactory              │
│    ┌─────────────────────────┐      │
│    │ + createVehicle()       │      │
│    └──────────┬──────────────┘      │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │   CarFactory        │          │
│    │ + createVehicle()   │          │
│    └─────────────────────┘          │
│                                     │
│    ┌─────────────────────┐          │
│    │   TruckFactory      │          │
│    │ + createVehicle()   │          │
│    └─────────────────────┘          │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Продукт
abstract class Vehicle {
    abstract void start();
}

class Car extends Vehicle {
    void start() { System.out.println("Car started"); }
}

class Truck extends Vehicle {
    void start() { System.out.println("Truck started"); }
}

// Создатель
abstract class VehicleFactory {
    // Фабричный метод
    abstract Vehicle createVehicle();
    
    // Бизнес-логика
    public Vehicle orderVehicle() {
        Vehicle vehicle = createVehicle();
        vehicle.start();
        return vehicle;
    }
}

// Конкретные создатели
class CarFactory extends VehicleFactory {
    Vehicle createVehicle() {
        return new Car();
    }
}

class TruckFactory extends VehicleFactory {
    Vehicle createVehicle() {
        return new Truck();
    }
}
```

#### 📊 Диаграмма последовательности
```
Client          Factory         Product
  │               │               │
  │─orderVehicle()→│               │
  │               │─createVehicle()→│
  │               │←──Vehicle────────│
  │               │─start()────────→│
  │←──Vehicle─────│               │
```

---

### 2.3 Builder (Строитель)

#### 🎯 Назначение
Создает сложные объекты пошагово, позволяя создавать разные представления объекта.

#### 🔍 Проблема
```
❌ Конструктор с множеством параметров:
┌─────────────────────────────────────┐
│ new Computer(                       │
│   "Intel i7",     // CPU            │
│   "16GB",         // RAM            │ ← Много параметров
│   "1TB SSD",      // Storage        │
│   "RTX 3080",     // GPU            │
│   true,           // hasWifi        │
│   false           // hasBluetooth   │
│ );                                  │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Builder:
┌─────────────────────────────────────┐
│ Computer computer = new Computer    │
│   .Builder()                        │
│   .cpu("Intel i7")                  │ ← Читаемо
│   .ram("16GB")                      │
│   .storage("1TB SSD")               │
│   .gpu("RTX 3080")                  │
│   .hasWifi(true)                    │
│   .build();                         │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
public class Computer {
    private String cpu;
    private String ram;
    private String storage;
    private String gpu;
    private boolean hasWifi;
    private boolean hasBluetooth;
    
    private Computer(Builder builder) {
        this.cpu = builder.cpu;
        this.ram = builder.ram;
        this.storage = builder.storage;
        this.gpu = builder.gpu;
        this.hasWifi = builder.hasWifi;
        this.hasBluetooth = builder.hasBluetooth;
    }
    
    public static class Builder {
        private String cpu;
        private String ram;
        private String storage;
        private String gpu;
        private boolean hasWifi;
        private boolean hasBluetooth;
        
        public Builder cpu(String cpu) {
            this.cpu = cpu;
            return this;
        }
        
        public Builder ram(String ram) {
            this.ram = ram;
            return this;
        }
        
        public Builder storage(String storage) {
            this.storage = storage;
            return this;
        }
        
        public Builder gpu(String gpu) {
            this.gpu = gpu;
            return this;
        }
        
        public Builder hasWifi(boolean hasWifi) {
            this.hasWifi = hasWifi;
            return this;
        }
        
        public Builder hasBluetooth(boolean hasBluetooth) {
            this.hasBluetooth = hasBluetooth;
            return this;
        }
        
        public Computer build() {
            return new Computer(this);
        }
    }
}
```

#### 🎯 Использование
```java
// Игровой компьютер
Computer gamingPC = new Computer.Builder()
    .cpu("Intel i9")
    .ram("32GB")
    .storage("2TB SSD")
    .gpu("RTX 4090")
    .hasWifi(true)
    .hasBluetooth(true)
    .build();

// Офисный компьютер
Computer officePC = new Computer.Builder()
    .cpu("Intel i5")
    .ram("8GB")
    .storage("500GB SSD")
    .hasWifi(true)
    .build();
```

---

### 2.4 Prototype (Прототип)

#### 🎯 Назначение
Создает новые объекты путем клонирования существующих прототипов.

#### 🔍 Проблема
```
❌ Создание сложных объектов с нуля:
┌─────────────────────────────────────┐
│ Document doc1 = new Document();     │
│ doc1.setTitle("Report");            │ ← Много настроек
│ doc1.setFormat("PDF");              │
│ doc1.addHeader("Company Logo");     │
│ doc1.addFooter("Page X of Y");      │
│                                     │
│ // Нужен похожий документ...        │
│ Document doc2 = new Document();     │ ← Дублирование кода
│ doc2.setTitle("Report 2");          │
│ doc2.setFormat("PDF");              │
│ // ... повторение настроек          │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Prototype:
┌─────────────────────────────────────┐
│         Prototype                   │
│    ┌─────────────────────────┐      │
│    │ + clone()               │      │
│    └──────────┬──────────────┘      │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │   Document          │          │
│    │ + clone()           │ ← Копирует│
│    └─────────────────────┘   себя   │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Интерфейс прототипа
interface Prototype {
    Prototype clone();
}

// Конкретный прототип
class Document implements Prototype {
    private String title;
    private String format;
    private List<String> headers;
    private List<String> footers;
    
    public Document(String title, String format) {
        this.title = title;
        this.format = format;
        this.headers = new ArrayList<>();
        this.footers = new ArrayList<>();
    }
    
    // Конструктор копирования
    public Document(Document document) {
        this.title = document.title;
        this.format = document.format;
        this.headers = new ArrayList<>(document.headers);
        this.footers = new ArrayList<>(document.footers);
    }
    
    @Override
    public Document clone() {
        return new Document(this);
    }
    
    // Getters и setters...
}

// Реестр прототипов
class DocumentRegistry {
    private Map<String, Document> prototypes = new HashMap<>();
    
    public void addPrototype(String key, Document prototype) {
        prototypes.put(key, prototype);
    }
    
    public Document getPrototype(String key) {
        Document prototype = prototypes.get(key);
        return prototype != null ? prototype.clone() : null;
    }
}
```

#### 🎯 Использование
```java
// Создаем прототипы
DocumentRegistry registry = new DocumentRegistry();

Document reportTemplate = new Document("Report Template", "PDF");
reportTemplate.addHeader("Company Logo");
reportTemplate.addFooter("Confidential");
registry.addPrototype("report", reportTemplate);

Document letterTemplate = new Document("Letter Template", "DOCX");
letterTemplate.addHeader("Letterhead");
registry.addPrototype("letter", letterTemplate);

// Клонируем прототипы
Document monthlyReport = registry.getPrototype("report");
monthlyReport.setTitle("Monthly Sales Report");

Document clientLetter = registry.getPrototype("letter");
clientLetter.setTitle("Thank You Letter");
```

---

## 🔧 Глава 3: Структурные паттерны (Structural Patterns)

*Как объекты и классы объединяются в более крупные структуры*

### 3.1 Adapter (Адаптер)

#### 🎯 Назначение
Позволяет объектам с несовместимыми интерфейсами работать вместе.

#### 🔍 Проблема
```
❌ Несовместимые интерфейсы:
┌─────────────────────────────────────┐
│  Client                             │
│    │                                │
│    │ expects: charge()              │
│    ▼                                │
│  ╔══════════════════════════╗       │
│  ║      IPhoneCharger       ║ ← Новый│
│  ║   + charge()             ║   API  │
│  ╚══════════════════════════╝       │
│                                     │
│  ╔══════════════════════════╗       │
│  ║    AndroidCharger        ║ ← Старый│
│  ║   + plugIn()             ║   API  │
│  ╚══════════════════════════╝       │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Adapter:
┌─────────────────────────────────────┐
│  Client                             │
│    │                                │
│    │ charge()                       │
│    ▼                                │
│  ╔══════════════════════════╗       │
│  ║       Adapter            ║       │
│  ║   + charge()             ║       │
│  ║     │                    ║       │
│  ║     └─► plugIn()         ║       │
│  ╚══════════════════════════╝       │
│           │                         │
│           ▼                         │
│  ╔══════════════════════════╗       │
│  ║    AndroidCharger        ║       │
│  ║   + plugIn()             ║       │
│  ╚══════════════════════════╝       │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Целевой интерфейс (то, что ожидает клиент)
interface IPhoneCharger {
    void charge();
}

// Адаптируемый класс (несовместимый интерфейс)
class AndroidCharger {
    public void plugIn() {
        System.out.println("Android charging...");
    }
}

// Адаптер
class AndroidToIPhoneAdapter implements IPhoneCharger {
    private AndroidCharger androidCharger;
    
    public AndroidToIPhoneAdapter(AndroidCharger androidCharger) {
        this.androidCharger = androidCharger;
    }
    
    @Override
    public void charge() {
        // Адаптируем вызов
        androidCharger.plugIn();
    }
}

// Клиент
class Phone {
    private IPhoneCharger charger;
    
    public Phone(IPhoneCharger charger) {
        this.charger = charger;
    }
    
    public void chargePhone() {
        charger.charge();
    }
}
```

#### 🎯 Использование
```java
// Используем адаптер
AndroidCharger androidCharger = new AndroidCharger();
IPhoneCharger adapter = new AndroidToIPhoneAdapter(androidCharger);
Phone iPhone = new Phone(adapter);
iPhone.chargePhone(); // Выведет: "Android charging..."
```

---

### 3.2 Decorator (Декоратор)

#### 🎯 Назначение
Динамически добавляет объектам новую функциональность, оборачивая их в полезные "обертки".

#### 🔍 Проблема
```
❌ Взрывной рост количества классов:
┌─────────────────────────────────────┐
│ Coffee                              │
│ CoffeeWithMilk                      │ ← Много классов
│ CoffeeWithSugar                     │   для комбинаций
│ CoffeeWithMilkAndSugar              │
│ CoffeeWithMilkAndSugarAndWhip       │
│ ...                                 │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Decorator:
┌─────────────────────────────────────┐
│         Component                   │
│    ┌─────────────────────────┐      │
│    │ + operation()           │      │
│    └──────────┬──────────────┘      │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │ ConcreteComponent   │          │
│    └─────────────────────┘          │
│                                     │
│    ┌─────────────────────┐          │
│    │ Decorator           │ ← Обертка │
│    │ + operation()       │          │
│    │   component.operation() +      │
│    │   дополнительная логика        │
│    └─────────────────────┘          │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Базовый компонент
interface Coffee {
    String getDescription();
    double getCost();
}

// Конкретный компонент
class SimpleCoffee implements Coffee {
    @Override
    public String getDescription() {
        return "Simple coffee";
    }
    
    @Override
    public double getCost() {
        return 2.0;
    }
}

// Базовый декоратор
abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;
    
    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }
}

// Конкретные декораторы
class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + " + milk";
    }
    
    @Override
    public double getCost() {
        return coffee.getCost() + 0.5;
    }
}

class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) {
        super(coffee);
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + " + sugar";
    }
    
    @Override
    public double getCost() {
        return coffee.getCost() + 0.3;
    }
}

class WhipDecorator extends CoffeeDecorator {
    public WhipDecorator(Coffee coffee) {
        super(coffee);
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + " + whip";
    }
    
    @Override
    public double getCost() {
        return coffee.getCost() + 0.7;
    }
}
```

#### 🎯 Использование
```java
// Создаем кофе с различными добавками
Coffee coffee = new SimpleCoffee();
System.out.println(coffee.getDescription() + " - $" + coffee.getCost());
// "Simple coffee - $2.0"

coffee = new MilkDecorator(coffee);
System.out.println(coffee.getDescription() + " - $" + coffee.getCost());
// "Simple coffee + milk - $2.5"

coffee = new SugarDecorator(coffee);
System.out.println(coffee.getDescription() + " - $" + coffee.getCost());
// "Simple coffee + milk + sugar - $2.8"

coffee = new WhipDecorator(coffee);
System.out.println(coffee.getDescription() + " - $" + coffee.getCost());
// "Simple coffee + milk + sugar + whip - $3.5"
```

---

### 3.3 Facade (Фасад)

#### 🎯 Назначение
Предоставляет простой интерфейс к сложной подсистеме.

#### 🔍 Проблема
```
❌ Сложное взаимодействие с подсистемой:
┌─────────────────────────────────────┐
│ Client                              │
│   │                                 │
│   ├─► AudioSystem.initialize()      │ ← Много вызовов
│   ├─► VideoSystem.setup()           │
│   ├─► ProjectorSystem.turnOn()      │
│   ├─► LightingSystem.dim()          │
│   └─► SoundSystem.setVolume()       │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Facade:
┌─────────────────────────────────────┐
│ Client                              │
│   │                                 │
│   └─► HomeTheaterFacade             │ ← Один вызов
│          .watchMovie()              │
│                │                    │
│                ├─► AudioSystem      │
│                ├─► VideoSystem      │
│                ├─► ProjectorSystem  │
│                ├─► LightingSystem   │
│                └─► SoundSystem      │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Сложные подсистемы
class AudioSystem {
    public void turnOn() { System.out.println("Audio system on"); }
    public void setVolume(int volume) { System.out.println("Volume: " + volume); }
    public void turnOff() { System.out.println("Audio system off"); }
}

class VideoSystem {
    public void turnOn() { System.out.println("Video system on"); }
    public void setSource(String source) { System.out.println("Source: " + source); }
    public void turnOff() { System.out.println("Video system off"); }
}

class ProjectorSystem {
    public void turnOn() { System.out.println("Projector on"); }
    public void setMode(String mode) { System.out.println("Mode: " + mode); }
    public void turnOff() { System.out.println("Projector off"); }
}

class LightingSystem {
    public void dim(int level) { System.out.println("Lights dimmed to " + level + "%"); }
    public void brighten() { System.out.println("Lights brightened"); }
}

// Фасад
class HomeTheaterFacade {
    private AudioSystem audioSystem;
    private VideoSystem videoSystem;
    private ProjectorSystem projectorSystem;
    private LightingSystem lightingSystem;
    
    public HomeTheaterFacade() {
        this.audioSystem = new AudioSystem();
        this.videoSystem = new VideoSystem();
        this.projectorSystem = new ProjectorSystem();
        this.lightingSystem = new LightingSystem();
    }
    
    public void watchMovie(String movie) {
        System.out.println("Get ready to watch " + movie + "...");
        lightingSystem.dim(20);
        audioSystem.turnOn();
        audioSystem.setVolume(8);
        videoSystem.turnOn();
        videoSystem.setSource("Netflix");
        projectorSystem.turnOn();
        projectorSystem.setMode("Movie");
        System.out.println("Movie started!");
    }
    
    public void endMovie() {
        System.out.println("Shutting down movie theater...");
        projectorSystem.turnOff();
        videoSystem.turnOff();
        audioSystem.turnOff();
        lightingSystem.brighten();
        System.out.println("Movie theater shut down.");
    }
}
```

#### 🎯 Использование
```java
HomeTheaterFacade homeTheater = new HomeTheaterFacade();

// Простой вызов вместо сложной последовательности
homeTheater.watchMovie("The Matrix");
// ... смотрим фильм ...
homeTheater.endMovie();
```

---

### 3.4 Composite (Компоновщик)

#### 🎯 Назначение
Группирует объекты в древовидные структуры для представления иерархии "часть-целое".

#### 🔍 Проблема
```
❌ Разная обработка листьев и контейнеров:
┌─────────────────────────────────────┐
│ if (element instanceof File) {      │
│     // обработка файла              │ ← Разная логика
│ } else if (element instanceof Folder) {│
│     // обработка папки              │
│     for (child : folder.children) { │
│         // рекурсивная обработка    │
│     }                               │
│ }                                   │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Composite:
┌─────────────────────────────────────┐
│         Component                   │
│    ┌─────────────────────────┐      │
│    │ + operation()           │      │
│    └──────────┬──────────────┘      │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │ Leaf                │          │ ← Одинаковый
│    │ + operation()       │          │   интерфейс
│    └─────────────────────┘          │
│                                     │
│    ┌─────────────────────┐          │
│    │ Composite           │          │
│    │ + operation()       │          │
│    │ + add(Component)    │          │
│    │ + remove(Component) │          │
│    └─────────────────────┘          │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Базовый компонент
abstract class FileSystemElement {
    protected String name;
    
    public FileSystemElement(String name) {
        this.name = name;
    }
    
    public abstract void display(int depth);
    public abstract int getSize();
}

// Лист (файл)
class File extends FileSystemElement {
    private int size;
    
    public File(String name, int size) {
        super(name);
        this.size = size;
    }
    
    @Override
    public void display(int depth) {
        System.out.println(" ".repeat(depth) + "📄 " + name + " (" + size + " KB)");
    }
    
    @Override
    public int getSize() {
        return size;
    }
}

// Композит (папка)
class Folder extends FileSystemElement {
    private List<FileSystemElement> children = new ArrayList<>();
    
    public Folder(String name) {
        super(name);
    }
    
    public void add(FileSystemElement element) {
        children.add(element);
    }
    
    public void remove(FileSystemElement element) {
        children.remove(element);
    }
    
    @Override
    public void display(int depth) {
        System.out.println(" ".repeat(depth) + "📁 " + name + "/");
        for (FileSystemElement child : children) {
            child.display(depth + 2);
        }
    }
    
    @Override
    public int getSize() {
        return children.stream()
                      .mapToInt(FileSystemElement::getSize)
                      .sum();
    }
}
```

#### 🎯 Использование
```java
// Создаем файловую структуру
Folder root = new Folder("Project");

Folder src = new Folder("src");
src.add(new File("Main.java", 15));
src.add(new File("Utils.java", 8));

Folder tests = new Folder("tests");
tests.add(new File("MainTest.java", 12));

Folder docs = new Folder("docs");
docs.add(new File("README.md", 5));
docs.add(new File("API.md", 20));

root.add(src);
root.add(tests);
root.add(docs);
root.add(new File("pom.xml", 3));

// Единообразная работа с деревом
root.display(0);
System.out.println("Total size: " + root.getSize() + " KB");

/* Вывод:
📁 Project/
  📁 src/
    📄 Main.java (15 KB)
    📄 Utils.java (8 KB)
  📁 tests/
    📄 MainTest.java (12 KB)
  📁 docs/
    📄 README.md (5 KB)
    📄 API.md (20 KB)
  📄 pom.xml (3 KB)
Total size: 63 KB
*/
```

---

## 🎭 Глава 4: Поведенческие паттерны (Behavioral Patterns)

*Как объекты взаимодействуют и распределяют ответственность*

### 4.1 Observer (Наблюдатель)

#### 🎯 Назначение
Определяет зависимость "один ко многим" между объектами так, что при изменении состояния одного объекта все зависящие от него оповещаются автоматически.

#### 🔍 Проблема
```
❌ Жесткая связь между объектами:
┌─────────────────────────────────────┐
│ WeatherStation                      │
│   │                                 │
│   ├─► Display1.update()             │ ← Прямые вызовы
│   ├─► Display2.update()             │
│   ├─► MobileApp.notify()            │
│   └─► Website.refresh()             │
│                                     │
│ Проблемы:                           │
│ • Сложно добавить новых наблюдателей│
│ • Нарушение Open/Closed принципа    │
│ • Тесная связанность               │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Observer:
┌─────────────────────────────────────┐
│         Subject                     │
│    ┌─────────────────────────┐      │
│    │ + attach(Observer)      │      │
│    │ + detach(Observer)      │ ← Список
│    │ + notify()              │   наблюдателей
│    └──────────┬──────────────┘      │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │ ConcreteSubject     │          │
│    └─────────────────────┘          │
│                                     │
│         Observer                    │
│    ┌─────────────────────────┐      │
│    │ + update()              │      │
│    └──────────┬──────────────┘      │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │ ConcreteObserver    │          │
│    └─────────────────────┘          │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Интерфейс наблюдателя
interface WeatherObserver {
    void update(float temperature, float humidity, float pressure);
}

// Интерфейс субъекта
interface WeatherSubject {
    void registerObserver(WeatherObserver observer);
    void removeObserver(WeatherObserver observer);
    void notifyObservers();
}

// Конкретный субъект
class WeatherStation implements WeatherSubject {
    private List<WeatherObserver> observers;
    private float temperature;
    private float humidity;
    private float pressure;
    
    public WeatherStation() {
        observers = new ArrayList<>();
    }
    
    @Override
    public void registerObserver(WeatherObserver observer) {
        observers.add(observer);
    }
    
    @Override
    public void removeObserver(WeatherObserver observer) {
        observers.remove(observer);
    }
    
    @Override
    public void notifyObservers() {
        for (WeatherObserver observer : observers) {
            observer.update(temperature, humidity, pressure);
        }
    }
    
    public void setMeasurements(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;
        notifyObservers(); // Автоматическое уведомление
    }
}

// Конкретные наблюдатели
class CurrentConditionsDisplay implements WeatherObserver {
    private String name;
    
    public CurrentConditionsDisplay(String name) {
        this.name = name;
    }
    
    @Override
    public void update(float temperature, float humidity, float pressure) {
        System.out.println(name + " - Current conditions: " + 
                          temperature + "°C, " + humidity + "% humidity");
    }
}

class ForecastDisplay implements WeatherObserver {
    private String name;
    
    public ForecastDisplay(String name) {
        this.name = name;
    }
    
    @Override
    public void update(float temperature, float humidity, float pressure) {
        String forecast = pressure > 1013 ? "Sunny" : "Rainy";
        System.out.println(name + " - Forecast: " + forecast);
    }
}

class StatisticsDisplay implements WeatherObserver {
    private String name;
    private List<Float> temperatures = new ArrayList<>();
    
    public StatisticsDisplay(String name) {
        this.name = name;
    }
    
    @Override
    public void update(float temperature, float humidity, float pressure) {
        temperatures.add(temperature);
        float avg = (float) temperatures.stream().mapToDouble(Float::doubleValue).average().orElse(0.0);
        System.out.println(name + " - Avg temperature: " + String.format("%.1f", avg) + "°C");
    }
}
```

#### 🎯 Использование
```java
// Создаем метеостанцию
WeatherStation weatherStation = new WeatherStation();

// Создаем и регистрируем наблюдателей
WeatherObserver currentDisplay = new CurrentConditionsDisplay("Mobile App");
WeatherObserver forecastDisplay = new ForecastDisplay("Website");
WeatherObserver statisticsDisplay = new StatisticsDisplay("Admin Panel");

weatherStation.registerObserver(currentDisplay);
weatherStation.registerObserver(forecastDisplay);
weatherStation.registerObserver(statisticsDisplay);

// Изменяем погодные данные
weatherStation.setMeasurements(25.5f, 65f, 1015f);
System.out.println("---");
weatherStation.setMeasurements(22.3f, 70f, 1010f);

/* Вывод:
Mobile App - Current conditions: 25.5°C, 65% humidity
Website - Forecast: Sunny
Admin Panel - Avg temperature: 25.5°C
---
Mobile App - Current conditions: 22.3°C, 70% humidity
Website - Forecast: Rainy
Admin Panel - Avg temperature: 23.9°C
*/
```

---

### 4.2 Strategy (Стратегия)

#### 🎯 Назначение
Определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми.

#### 🔍 Проблема
```
❌ Алгоритмы внутри класса:
┌─────────────────────────────────────┐
│ class PaymentProcessor {            │
│   void processPayment(type, amount) {│
│     if (type == "CREDIT_CARD") {    │ ← Много условий
│       // логика кредитной карты     │
│     } else if (type == "PAYPAL") {  │
│       // логика PayPal              │
│     } else if (type == "CRYPTO") {  │
│       // логика криптовалют         │
│     }                               │
│   }                                 │
│ }                                   │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Strategy:
┌─────────────────────────────────────┐
│         Strategy                    │
│    ┌─────────────────────────┐      │
│    │ + execute()             │      │
│    └──────────┬──────────────┘      │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │ CreditCardStrategy  │          │ ← Отдельные
│    └─────────────────────┘          │   алгоритмы
│    ┌─────────────────────┐          │
│    │ PayPalStrategy      │          │
│    └─────────────────────┘          │
│    ┌─────────────────────┐          │
│    │ CryptoStrategy      │          │
│    └─────────────────────┘          │
│                                     │
│         Context                     │
│    ┌─────────────────────────┐      │
│    │ - strategy: Strategy    │ ← Использует
│    │ + setStrategy()         │   стратегию
│    │ + executeStrategy()     │      │
│    └─────────────────────────┘      │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Интерфейс стратегии
interface PaymentStrategy {
    void pay(double amount);
    boolean validate();
}

// Конкретные стратегии
class CreditCardStrategy implements PaymentStrategy {
    private String cardNumber;
    private String cvv;
    
    public CreditCardStrategy(String cardNumber, String cvv) {
        this.cardNumber = cardNumber;
        this.cvv = cvv;
    }
    
    @Override
    public boolean validate() {
        return cardNumber.length() == 16 && cvv.length() == 3;
    }
    
    @Override
    public void pay(double amount) {
        if (validate()) {
            System.out.println("Paid $" + amount + " using Credit Card ending in " 
                             + cardNumber.substring(12));
        } else {
            System.out.println("Invalid credit card details");
        }
    }
}

class PayPalStrategy implements PaymentStrategy {
    private String email;
    private String password;
    
    public PayPalStrategy(String email, String password) {
        this.email = email;
        this.password = password;
    }
    
    @Override
    public boolean validate() {
        return email.contains("@") && password.length() >= 6;
    }
    
    @Override
    public void pay(double amount) {
        if (validate()) {
            System.out.println("Paid $" + amount + " using PayPal account " + email);
        } else {
            System.out.println("Invalid PayPal credentials");
        }
    }
}

class CryptoStrategy implements PaymentStrategy {
    private String walletAddress;
    
    public CryptoStrategy(String walletAddress) {
        this.walletAddress = walletAddress;
    }
    
    @Override
    public boolean validate() {
        return walletAddress.length() >= 26;
    }
    
    @Override
    public void pay(double amount) {
        if (validate()) {
            System.out.println("Paid $" + amount + " using crypto wallet " 
                             + walletAddress.substring(0, 6) + "...");
        } else {
            System.out.println("Invalid wallet address");
        }
    }
}

// Контекст
class PaymentProcessor {
    private PaymentStrategy strategy;
    
    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }
    
    public void processPayment(double amount) {
        if (strategy == null) {
            System.out.println("Please select a payment method");
            return;
        }
        strategy.pay(amount);
    }
}
```

#### 🎯 Использование
```java
PaymentProcessor processor = new PaymentProcessor();
double amount = 99.99;

// Оплата кредитной картой
processor.setPaymentStrategy(new CreditCardStrategy("1234567890123456", "123"));
processor.processPayment(amount);

// Оплата через PayPal
processor.setPaymentStrategy(new PayPalStrategy("user@example.com", "password123"));
processor.processPayment(amount);

// Оплата криптовалютой
processor.setPaymentStrategy(new CryptoStrategy("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"));
processor.processPayment(amount);

/* Вывод:
Paid $99.99 using Credit Card ending in 3456
Paid $99.99 using PayPal account user@example.com
Paid $99.99 using crypto wallet 1A1zP1...
*/
```

---

### 4.3 Command (Команда)

#### 🎯 Назначение
Инкапсулирует запрос как объект, позволяя параметризовать клиентов с различными запросами, ставить запросы в очередь и поддерживать отмену операций.

#### 🔍 Проблема
```
❌ Прямая связь между отправителем и получателем:
┌─────────────────────────────────────┐
│ RemoteControl                       │
│   │                                 │
│   ├─► light.turnOn()                │ ← Прямые вызовы
│   ├─► fan.start()                   │
│   ├─► stereo.turnOn()               │
│   └─► tv.turnOn()                   │
│                                     │
│ Проблемы:                           │
│ • Невозможно отменить команды       │
│ • Сложно логировать действия        │
│ • Нет поддержки макрокоманд         │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном Command:
┌─────────────────────────────────────┐
│         Command                     │
│    ┌─────────────────────────┐      │
│    │ + execute()             │      │
│    │ + undo()                │      │
│    └──────────┬──────────────┘      │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │ ConcreteCommand     │ ← Команды как
│    │ - receiver          │   объекты
│    │ + execute()         │      │
│    │ + undo()            │      │
│    └─────────────────────┘          │
│                                     │
│         Invoker                     │
│    ┌─────────────────────────┐      │
│    │ - command: Command      │ ← Отправитель
│    │ + setCommand()          │      │
│    │ + pressButton()         │      │
│    └─────────────────────────┘      │
│                                     │
│         Receiver                    │
│    ┌─────────────────────────┐      │
│    │ + action()              │ ← Получатель
│    └─────────────────────────┘      │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Интерфейс команды
interface Command {
    void execute();
    void undo();
}

// Получатели (устройства)
class Light {
    private String location;
    private boolean isOn = false;
    
    public Light(String location) {
        this.location = location;
    }
    
    public void turnOn() {
        isOn = true;
        System.out.println(location + " light is ON");
    }
    
    public void turnOff() {
        isOn = false;
        System.out.println(location + " light is OFF");
    }
    
    public boolean isOn() {
        return isOn;
    }
}

class Stereo {
    private boolean isOn = false;
    private int volume = 0;
    
    public void turnOn() {
        isOn = true;
        System.out.println("Stereo is ON");
    }
    
    public void turnOff() {
        isOn = false;
        System.out.println("Stereo is OFF");
    }
    
    public void setVolume(int volume) {
        this.volume = volume;
        System.out.println("Stereo volume set to " + volume);
    }
    
    public int getVolume() {
        return volume;
    }
}

// Конкретные команды
class LightOnCommand implements Command {
    private Light light;
    
    public LightOnCommand(Light light) {
        this.light = light;
    }
    
    @Override
    public void execute() {
        light.turnOn();
    }
    
    @Override
    public void undo() {
        light.turnOff();
    }
}

class LightOffCommand implements Command {
    private Light light;
    
    public LightOffCommand(Light light) {
        this.light = light;
    }
    
    @Override
    public void execute() {
        light.turnOff();
    }
    
    @Override
    public void undo() {
        light.turnOn();
    }
}

class StereoOnWithVolumeCommand implements Command {
    private Stereo stereo;
    private int previousVolume;
    
    public StereoOnWithVolumeCommand(Stereo stereo) {
        this.stereo = stereo;
    }
    
    @Override
    public void execute() {
        previousVolume = stereo.getVolume();
        stereo.turnOn();
        stereo.setVolume(7);
    }
    
    @Override
    public void undo() {
        stereo.turnOff();
        stereo.setVolume(previousVolume);
    }
}

// Пустая команда (Null Object Pattern)
class NoCommand implements Command {
    @Override
    public void execute() {}
    
    @Override
    public void undo() {}
}

// Макрокоманда
class MacroCommand implements Command {
    private Command[] commands;
    
    public MacroCommand(Command[] commands) {
        this.commands = commands;
    }
    
    @Override
    public void execute() {
        for (Command command : commands) {
            command.execute();
        }
    }
    
    @Override
    public void undo() {
        // Отменяем в обратном порядке
        for (int i = commands.length - 1; i >= 0; i--) {
            commands[i].undo();
        }
    }
}

// Отправитель (пульт управления)
class RemoteControl {
    private Command[] onCommands;
    private Command[] offCommands;
    private Command lastCommand;
    
    public RemoteControl() {
        onCommands = new Command[7];
        offCommands = new Command[7];
        
        Command noCommand = new NoCommand();
        for (int i = 0; i < 7; i++) {
            onCommands[i] = noCommand;
            offCommands[i] = noCommand;
        }
        lastCommand = noCommand;
    }
    
    public void setCommand(int slot, Command onCommand, Command offCommand) {
        onCommands[slot] = onCommand;
        offCommands[slot] = offCommand;
    }
    
    public void onButtonPressed(int slot) {
        onCommands[slot].execute();
        lastCommand = onCommands[slot];
    }
    
    public void offButtonPressed(int slot) {
        offCommands[slot].execute();
        lastCommand = offCommands[slot];
    }
    
    public void undoButtonPressed() {
        lastCommand.undo();
    }
    
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("\n------ Remote Control ------\n");
        for (int i = 0; i < onCommands.length; i++) {
            sb.append("[slot ").append(i).append("] ")
              .append(onCommands[i].getClass().getSimpleName())
              .append("    ")
              .append(offCommands[i].getClass().getSimpleName())
              .append("\n");
        }
        return sb.toString();
    }
}
```

#### 🎯 Использование
```java
// Создаем устройства
Light livingRoomLight = new Light("Living Room");
Light kitchenLight = new Light("Kitchen");
Stereo stereo = new Stereo();

// Создаем команды
LightOnCommand livingRoomLightOn = new LightOnCommand(livingRoomLight);
LightOffCommand livingRoomLightOff = new LightOffCommand(livingRoomLight);
LightOnCommand kitchenLightOn = new LightOnCommand(kitchenLight);
LightOffCommand kitchenLightOff = new LightOffCommand(kitchenLight);

StereoOnWithVolumeCommand stereoOnWithVolume = new StereoOnWithVolumeCommand(stereo);

// Создаем пульт управления
RemoteControl remote = new RemoteControl();

// Настраиваем слоты
remote.setCommand(0, livingRoomLightOn, livingRoomLightOff);
remote.setCommand(1, kitchenLightOn, kitchenLightOff);
remote.setCommand(2, stereoOnWithVolume, new NoCommand());

System.out.println(remote);

// Используем пульт
remote.onButtonPressed(0);  // Включить свет в гостиной
remote.offButtonPressed(0); // Выключить свет в гостиной
remote.undoButtonPressed(); // Отменить (включить обратно)

remote.onButtonPressed(1);  // Включить свет на кухне
remote.onButtonPressed(2);  // Включить стерео
remote.undoButtonPressed(); // Отменить стерео

// Макрокоманда - "Режим вечеринки"
Command[] partyOn = {livingRoomLightOn, stereoOnWithVolume};
Command[] partyOff = {livingRoomLightOff, new NoCommand()};

MacroCommand partyOnMacro = new MacroCommand(partyOn);
MacroCommand partyOffMacro = new MacroCommand(partyOff);

remote.setCommand(3, partyOnMacro, partyOffMacro);

System.out.println("\n--- Party Mode ---");
remote.onButtonPressed(3);  // Режим вечеринки ON
remote.undoButtonPressed(); // Отменить режим вечеринки
```

---

### 4.4 State (Состояние)

#### 🎯 Назначение
Позволяет объекту изменять свое поведение при изменении его внутреннего состояния.

#### 🔍 Проблема
```
❌ Сложная логика состояний:
┌─────────────────────────────────────┐
│ class VendingMachine {              │
│   enum State { NO_COIN, HAS_COIN,   │
│                SOLD, SOLD_OUT }     │
│                                     │
│   void insertCoin() {               │
│     if (state == NO_COIN) {         │ ← Много условий
│       // логика                     │
│     } else if (state == HAS_COIN) { │
│       // другая логика              │
│     } // ...                        │
│   }                                 │
│                                     │
│   void selectProduct() {            │
│     if (state == NO_COIN) {         │ ← Дублирование
│       // логика                     │   проверок
│     } else if (state == HAS_COIN) { │
│       // другая логика              │
│     } // ...                        │
│   }                                 │
│ }                                   │
└─────────────────────────────────────┘
```

#### 💡 Решение
```
✅ С паттерном State:
┌─────────────────────────────────────┐
│         State                       │
│    ┌─────────────────────────┐      │
│    │ + insertCoin()          │      │
│    │ + selectProduct()       │      │
│    │ + dispense()            │      │
│    └──────────┬──────────────┘      │
│               │                     │
│    ┌──────────▼──────────┐          │
│    │ NoCoinState         │          │ ← Каждое состояние -
│    └─────────────────────┘          │   отдельный класс
│    ┌─────────────────────┐          │
│    │ HasCoinState        │          │
│    └─────────────────────┘          │
│    ┌─────────────────────┐          │
│    │ SoldState           │          │
│    └─────────────────────┘          │
│                                     │
│         Context                     │
│    ┌─────────────────────────┐      │
│    │ - state: State          │ ← Текущее
│    │ + setState()            │   состояние
│    │ + insertCoin()          │      │
│    └─────────────────────────┘      │
└─────────────────────────────────────┘
```

#### 🛠️ Реализация

```java
// Контекст (торговый автомат)
class VendingMachine {
    private State noCoinState;
    private State hasCoinState;
    private State soldState;
    private State soldOutState;
    
    private State currentState;
    private int count = 0; // количество товаров
    
    public VendingMachine(int count) {
        noCoinState = new NoCoinState(this);
        hasCoinState = new HasCoinState(this);
        soldState = new SoldState(this);
        soldOutState = new SoldOutState(this);
        
        this.count = count;
        currentState = count > 0 ? noCoinState : soldOutState;
    }
    
    public void insertCoin() {
        currentState.insertCoin();
    }
    
    public void selectProduct() {
        currentState.selectProduct();
        currentState.dispense(); // Автоматически выдаем товар после выбора
    }
    
    public void setState(State state) {
        this.currentState = state;
    }
    
    public void releaseProduct() {
        System.out.println("A product comes rolling out...");
        if (count > 0) {
            count--;
        }
    }
    
    // Геттеры для состояний
    public State getNoCoinState() { return noCoinState; }
    public State getHasCoinState() { return hasCoinState; }
    public State getSoldState() { return soldState; }
    public State getSoldOutState() { return soldOutState; }
    public int getCount() { return count; }
    
    @Override
    public String toString() {
        return "VendingMachine{" +
                "state=" + currentState.getClass().getSimpleName() +
                ", count=" + count +
                '}';
    }
}

// Абстрактное состояние
abstract class State {
    public abstract void insertCoin();
    public abstract void selectProduct();
    public abstract void dispense();
}

// Состояние "Нет монеты"
class NoCoinState extends State {
    private VendingMachine vendingMachine;
    
    public NoCoinState(VendingMachine vendingMachine) {
        this.vendingMachine = vendingMachine;
    }
    
    @Override
    public void insertCoin() {
        System.out.println("You inserted a coin");
        vendingMachine.setState(vendingMachine.getHasCoinState());
    }
    
    @Override
    public void selectProduct() {
        System.out.println("You need to insert a coin first");
    }
    
    @Override
    public void dispense() {
        System.out.println("You need to pay first");
    }
}

// Состояние "Есть монета"
class HasCoinState extends State {
    private VendingMachine vendingMachine;
    
    public HasCoinState(VendingMachine vendingMachine) {
        this.vendingMachine = vendingMachine;
    }
    
    @Override
    public void insertCoin() {
        System.out.println("You can't insert another coin");
    }
    
    @Override
    public void selectProduct() {
        System.out.println("You selected a product...");
        vendingMachine.setState(vendingMachine.getSoldState());
    }
    
    @Override
    public void dispense() {
        System.out.println("You need to select a product first");
    }
}

// Состояние "Продано"
class SoldState extends State {
    private VendingMachine vendingMachine;
    
    public SoldState(VendingMachine vendingMachine) {
        this.vendingMachine = vendingMachine;
    }
    
    @Override
    public void insertCoin() {
        System.out.println("Please wait, we're already giving you a product");
    }
    
    @Override
    public void selectProduct() {
        System.out.println("Please wait, we're already giving you a product");
    }
    
    @Override
    public void dispense() {
        vendingMachine.releaseProduct();
        if (vendingMachine.getCount() > 0) {
            vendingMachine.setState(vendingMachine.getNoCoinState());
        } else {
            System.out.println("Oops, out of products!");
            vendingMachine.setState(vendingMachine.getSoldOutState());
        }
    }
}

// Состояние "Распродано"
class SoldOutState extends State {
    private VendingMachine vendingMachine;
    
    public SoldOutState(VendingMachine vendingMachine) {
        this.vendingMachine = vendingMachine;
    }
    
    @Override
    public void insertCoin() {
        System.out.println("Sorry, we're sold out");
    }
    
    @Override
    public void selectProduct() {
        System.out.println("Sorry, we're sold out");
    }
    
    @Override
    public void dispense() {
        System.out.println("Sorry, we're sold out");
    }
}
```

#### 🎯 Использование
```java
VendingMachine vendingMachine = new VendingMachine(2);

System.out.println(vendingMachine + "\n");

// Пытаемся купить без монеты
vendingMachine.selectProduct();
System.out.println();

// Вставляем монету и покупаем
vendingMachine.insertCoin();
vendingMachine.selectProduct();
System.out.println(vendingMachine + "\n");

// Покупаем второй товар
vendingMachine.insertCoin();
vendingMachine.selectProduct();
System.out.println(vendingMachine + "\n");

// Пытаемся купить когда товары закончились
vendingMachine.insertCoin();
vendingMachine.selectProduct();

/* Вывод:
VendingMachine{state=NoCoinState, count=2}

You need to insert a coin first

You inserted a coin
You selected a product...
A product comes rolling out...
VendingMachine{state=NoCoinState, count=1}

You inserted a coin
You selected a product...
A product comes rolling out...
Oops, out of products!
VendingMachine{state=SoldOutState, count=0}

Sorry, we're sold out
Sorry, we're sold out
*/
```

#### 📊 Диаграмма переходов состояний
```
      insertCoin()
   ┌─────────────────┐
   │                 ▼
[NoCoin] ────────► [HasCoin]
   ▲                 │
   │                 │ selectProduct()
   │                 ▼
   │              [Sold] ────► [SoldOut]
   │                 │           │
   │   dispense()    │           │ (если count == 0)
   │  (если count>0) │           │
   └─────────────────┘           │
                                 │
              Все действия       │
              возвращают         │
              "sold out"         │
                ▲                │
                └────────────────┘
```

---

## 🚫 Глава 5: Антипаттерны и ошибки

*Когда паттерны становятся проблемой*

### 5.1 Распространенные антипаттерны

#### 🎭 Паттерномания (Pattern Fever)
```
❌ Чрезмерное использование паттернов:
┌─────────────────────────────────────┐
│ // Для простого приветствия:        │
│ AbstractGreetingStrategyFactory     │ ← Излишняя сложность
│   .createGreetingStrategy()         │
│   .greet("Hello");                  │
│                                     │
│ // Вместо простого:                 │
│ System.out.println("Hello");        │
└─────────────────────────────────────┘
```

**Решение:** Используйте паттерны только когда они решают реальную проблему!

#### 🏗️ Golden Hammer
```
❌ "Если у тебя есть молоток, всё кажется гвоздём"
┌─────────────────────────────────────┐
│ // Singleton для всего:             │
│ DatabaseSingleton.getInstance()     │ ← Один паттерн
│ CacheSingleton.getInstance()        │   для всех задач
│ LoggerSingleton.getInstance()       │
│ ConfigSingleton.getInstance()       │
└─────────────────────────────────────┘
```

**Решение:** Изучайте различные паттерны и выбирайте подходящий для каждой задачи.

#### 🕷️ God Object через паттерны
```
❌ Паттерн создает монстра:
┌─────────────────────────────────────┐
│ class UniversalFacade {             │
│   // 50+ методов для всех подсистем │ ← Нарушение SRP
│   void doEverything() { ... }       │
│   void handleAllCases() { ... }     │
│   // ...                            │
│ }                                   │
└─────────────────────────────────────┘
```

**Решение:** Разделяйте ответственность, создавайте несколько специализированных фасадов.

### 5.2 Когда НЕ нужно применять паттерны

#### ✅ Принципы правильного использования

```
🎯 ИСПОЛЬЗУЙТЕ ПАТТЕРНЫ КОГДА:
├─ Есть четко определенная проблема
├─ Паттерн решает именно эту проблему
├─ Польза превышает сложность
└─ Команда понимает паттерн

🚫 НЕ ИСПОЛЬЗУЙТЕ ПАТТЕРНЫ КОГДА:
├─ Проблемы на самом деле нет
├─ Простое решение работает лучше
├─ Паттерн добавляет ненужную сложность
└─ Не все понимают зачем он нужен
```

#### 📏 Критерии оценки

```
                 СТОИТ ЛИ ПРИМЕНЯТЬ ПАТТЕРН?
                           │
                    ┌──────┴──────┐
                   ДА            НЕТ
                    │              │
        ┌───────────▼───┐      ┌───▼───────────┐
        │ • Есть проблема│      │ • Код работает│
        │ • Паттерн решает│     │ • Простое решение│
        │ • Команда знает│      │ • Нет проблемы│
        │ • Польза > сложности│ │ • Преждевременная│
        └───────────────┘      │   оптимизация│
                               └───────────────┘
```

---

## 🌟 Глава 6: Паттерны в современном мире

*Эволюция и адаптация паттернов*

### 6.1 Паттерны в популярных фреймворках

#### 🌸 Spring Framework
```java
// Dependency Injection (фактически Service Locator)
@Autowired
private UserService userService; // ← DI контейнер

// Proxy Pattern для AOP
@Transactional // ← Динамический прокси
public void updateUser(User user) { ... }

// Template Method в JdbcTemplate
jdbcTemplate.query(sql, rowMapper); // ← Шаблонный метод

// Factory Pattern
ApplicationContext context = 
    new ClassPathXmlApplicationContext("config.xml"); // ← Фабрика бинов
```

#### ⚛️ React (Frontend)
```javascript
// Higher-Order Components (Decorator)
const withAuth = (Component) => { // ← Декоратор
  return (props) => {
    if (!isAuthenticated) return <Login />;
    return <Component {...props} />;
  };
};

// Render Props (Strategy)
<DataProvider
  render={data => <Dashboard data={data} />} // ← Стратегия рендеринга
/>

// Context API (Singleton + Observer)
const AuthContext = createContext(); // ← Глобальное состояние
```

#### 🎯 Express.js (Node.js)
```javascript
// Middleware Chain (Chain of Responsibility)
app.use(auth);        // ← Цепочка
app.use(validation);  //   обработчиков
app.use(logging);
app.use(errorHandler);

// Route Handlers (Command)
app.get('/users', getUsersCommand); // ← Команды
app.post('/users', createUserCommand);
```

### 6.2 Функциональные альтернативы ООП паттернам

#### 🔄 Strategy vs Higher-Order Functions
```javascript
// ❌ ООП Strategy
class PaymentStrategy {
  pay(amount) { throw new Error('Not implemented'); }
}

class CreditCardStrategy extends PaymentStrategy {
  pay(amount) { return `Paid ${amount} with credit card`; }
}

// ✅ Функциональный подход
const payWithCreditCard = (amount) => `Paid ${amount} with credit card`;
const payWithPayPal = (amount) => `Paid ${amount} with PayPal`;

const processPayment = (paymentMethod, amount) => paymentMethod(amount);
```

#### 🏭 Factory vs Factory Functions
```javascript
// ❌ ООП Factory
class VehicleFactory {
  static createVehicle(type) {
    switch(type) {
      case 'car': return new Car();
      case 'truck': return new Truck();
    }
  }
}

// ✅ Функциональный подход
const createVehicle = (type) => {
  const vehicles = {
    car: () => ({ type: 'car', wheels: 4 }),
    truck: () => ({ type: 'truck', wheels: 6 })
  };
  return vehicles[type]?.() || null;
};
```

#### 👁️ Observer vs Event Emitters/Reactive Streams
```javascript
// ❌ ООП Observer
class Subject {
  constructor() { this.observers = []; }
  attach(observer) { this.observers.push(observer); }
  notify(data) { this.observers.forEach(o => o.update(data)); }
}

// ✅ Функциональный подход (RxJS)
import { Subject } from 'rxjs';

const dataStream = new Subject();
dataStream.subscribe(data => console.log('Observer 1:', data));
dataStream.subscribe(data => console.log('Observer 2:', data));
dataStream.next('Hello World'); // Уведомить всех
```

### 6.3 Современные архитектурные паттерны

#### 🏛️ Микросервисы и паттерны
```
┌─────────────────────────────────────┐
│         МИКРОСЕРВИСНАЯ              │
│         АРХИТЕКТУРА                 │
│                                     │
│  ┌─────────┐    ┌─────────┐         │
│  │Service A│◄──►│Service B│ ← Circuit│
│  └─────────┘    └─────────┘   Breaker│
│       │              │              │
│       ▼              ▼              │
│  ┌─────────┐    ┌─────────┐         │
│  │Database │    │Cache    │ ← Каждый│
│  │   A     │    │         │   сервис│
│  └─────────┘    └─────────┘   изолирован│
│                                     │
│  API Gateway ← Facade для внешних   │
│  Event Bus   ← Observer между       │
│              сервисами              │
└─────────────────────────────────────┘
```

#### ☁️ Serverless и паттерны
```javascript
// Function as a Service (Command Pattern)
exports.handler = async (event) => { // ← Lambda функция как команда
  const command = CommandFactory.create(event.type);
  return await command.execute(event.data);
};

// Event-Driven Architecture (Observer)
// SNS Topic → SQS Queue → Lambda ← Асинхронные уведомления
```

### 6.4 Паттерны в Domain-Driven Design

#### 🏗️ Тактические паттерны DDD
```java
// Value Object (неизменяемый объект)
public class Money {
    private final BigDecimal amount;
    private final Currency currency;
    
    // Конструктор, equals, hashCode
    // Нет сеттеров - объект неизменяемый
}

// Entity (объект с идентичностью)
public class User {
    private UserId id; // ← Уникальный идентификатор
    private Email email;
    private Money balance;
    
    // Бизнес-методы, а не просто геттеры/сеттеры
    public void transferMoney(Money amount, User recipient) {
        // Бизнес-логика
    }
}

// Domain Service (когда логика не принадлежит Entity)
@Service
public class TransferService {
    public void transfer(User from, User to, Money amount) {
        // Сложная бизнес-логика между несколькими Entity
    }
}

// Repository (абстракция над хранилищем)
public interface UserRepository {
    User findById(UserId id);
    void save(User user);
    List<User> findByEmail(Email email);
}
```

---

## 🎯 Практические задания и упражнения

### Задание 1: Анализ существующего кода ⏰ 2-3 часа

```java
// 🔍 НАЙДИТЕ ПРОБЛЕМЫ В ЭТОМ КОДЕ:
public class FileProcessor {
    public void processFile(String type, String filepath) {
        if (type.equals("PDF")) {
            // 50 строк логики обработки PDF
            System.out.println("Processing PDF file: " + filepath);
            // Валидация PDF
            // Извлечение данных
            // Сохранение в базу
        } else if (type.equals("EXCEL")) {
            // 60 строк логики обработки Excel
            System.out.println("Processing Excel file: " + filepath);
            // Валидация Excel
            // Парсинг таблиц
            // Сохранение в базу
        } else if (type.equals("CSV")) {
            // 40 строк логики обработки CSV
            System.out.println("Processing CSV file: " + filepath);
            // Валидация CSV
            // Парсинг строк
            // Сохранение в базу
        }
        // TODO: добавить поддержку XML, JSON, TXT...
    }
}
```

**Ваши задачи:**
1. Определите, какие принципы SOLID нарушены
2. Предложите применение подходящих паттернов
3. Перепишите код используя паттерны Strategy и Factory
4. Добавьте возможность легкого расширения новыми типами файлов

---

### Задание 2: Проектирование системы уведомлений ⏰ 3-4 часа

**Требования:**
- Система должна отправлять уведомления через разные каналы (Email, SMS, Push, Slack)
- Пользователи могут подписываться/отписываться от типов уведомлений
- Должна быть возможность группировки уведомлений
- Система должна логировать все отправленные уведомления
- Возможность отложенной отправки

**Ваши задачи:**
1. Спроектируйте архитектуру используя подходящие паттерны
2. Реализуйте базовую версию системы
3. Продемонстрируйте гибкость системы, добавив новый канал уведомлений
4. Добавьте возможность отмены отправки (паттерн Command)

---

### Задание 3: Игровой движок ⏰ 4-5 часов

**Создайте простой игровой движок со следующими компонентами:**

```
🎮 ИГРОВОЙ ДВИЖОК
├─ GameEngine (управляет игровым циклом)
├─ GameObjects (игровые объекты)
│  ├─ Player
│  ├─ Enemy
│  └─ PowerUp
├─ Behaviors (поведения объектов)
│  ├─ MovementBehavior
│  ├─ AttackBehavior
│  └─ CollisionBehavior
├─ States (состояния игры)
│  ├─ MenuState
│  ├─ PlayingState
│  ├─ PausedState
│  └─ GameOverState
└─ Events (игровые события)
   ├─ PlayerMoved
   ├─ EnemyDefeated
   └─ PowerUpCollected
```

**Используйте паттерны:**
- **State** для состояний игры
- **Strategy** для различных поведений
- **Observer** для игровых событий
- **Command** для пользовательского ввода
- **Factory** для создания игровых объектов
- **Composite** для иерархии игровых объектов

---

### Задание 4: Система конфигурации ⏰ 2-3 часа

**Создайте гибкую систему конфигурации приложения:**

```java
// Пример использования:
Config config = ConfigBuilder
    .newConfig()
    .database()
        .host("localhost")
        .port(5432)
        .username("admin")
        .password("secret")
    .cache()
        .enabled(true)
        .ttl(Duration.ofMinutes(30))
        .provider("Redis")
    .logging()
        .level(LogLevel.INFO)
        .appender("Console", "File")
    .build();

// Использование
DatabaseConfig dbConfig = config.getDatabase();
CacheConfig cacheConfig = config.getCache();
```

**Используйте паттерны:**
- **Builder** для создания конфигурации
- **Singleton** для глобального доступа
- **Strategy** для различных провайдеров
- **Template Method** для загрузки из разных источников

---

## 📋 Чек-лист: Освоение паттернов проектирования

### ✅ Теоретическое понимание

```
□ Понимаю назначение каждого паттерна
□ Знаю проблемы, которые решает каждый паттерн
□ Могу объяснить структуру паттерна (участники, связи)
□ Понимаю компромиссы (плюсы и минусы) каждого паттерна
□ Знаю, когда НЕ нужно применять паттерн
```

### ✅ Практические навыки

```
□ Могу реализовать любой изученный паттерн с нуля
□ Умею адаптировать паттерн под конкретную задачу
□ Могу комбинировать несколько паттернов
□ Умею рефакторить существующий код с применением паттернов
□ Могу обосновать выбор конкретного паттерна
```

### ✅ Архитектурное мышление

```
□ Вижу возможности применения паттернов в реальных проектах
□ Понимаю связь паттернов с принципами SOLID
□ Могу спроектировать систему используя несколько паттернов
□ Умею балансировать между простотой и гибкостью
□ Могу провести код-ревью с фокусом на паттерны
```

---

## 🎓 Итоговая оценка блока

### Критерии оценки знаний:

#### 🥉 Базовый уровень (60-70%)
- Знает основные паттерны и их назначение
- Может реализовать простые паттерны по образцу
- Понимает базовые принципы применения

#### 🥈 Средний уровень (70-85%)
- Понимает проблемы, решаемые паттернами
- Может адаптировать паттерны под конкретные задачи
- Умеет рефакторить код с применением паттернов
- Понимает компромиссы и ограничения

#### 🥇 Продвинутый уровень (85-95%)
- Может комбинировать несколько паттернов
- Понимает связь с архитектурными принципами
- Умеет создавать собственные вариации паттернов
- Может обучать других применению паттернов

#### 🏆 Экспертный уровень (95-100%)
- Интуитивно понимает, когда применять паттерны
- Может критически оценивать применение паттернов
- Создает архитектуры, естественно использующие паттерны
- Вносит вклад в эволюцию паттернов

---

## 🚀 Следующие шаги

После освоения паттернов проектирования вы готовы к:

### 📖 Блок 4: Архитектурные стили и подходы
- Монолитная vs микросервисная архитектура
- Слоистая архитектура и Clean Architecture
- Event-Driven Architecture
- Hexagonal Architecture

### 🔧 Блок 5: Управление зависимостями
- Dependency Injection и IoC контейнеры
- Модульность и разделение ответственности
- Тестирование архитектуры

### ⚡ Блок 6: Производительность и масштабируемость
- Профилирование и оптимизация
- Стратегии кэширования
- Асинхронное программирование

---

## 📚 Дополнительные ресурсы

### 📖 Книги
- **"Design Patterns"** - Gang of Four (классика)
- **"Head First Design Patterns"** - Freeman & Robson (доступное изложение)
- **"Refactoring to Patterns"** - Joshua Kerievsky
- **"Pattern-Oriented Software Architecture"** - Buschmann et al.

### 🌐 Онлайн-ресурсы
- **Refactoring.Guru** - отличные объяснения с примерами
- **SourceMaking.com** - паттерны и принципы
- **Martin Fowler's Blog** - архитектурные инсайты

### 🛠️ Практика
- Анализируйте код популярных open-source проектов
- Участвуйте в код-ревью с фокусом на паттерны
- Рефакторите legacy код с применением паттернов
- Создавайте собственные pet-проекты

---

## 💡 Заключение

Паттерны проектирования — это не просто готовые решения, а **язык для общения между разработчиками** и **способ мышления** об архитектуре ПО. Главное — помнить, что паттерны должны **решать реальные проблемы**, а не создавать искусственную сложность.

```
🎯 ЗОЛОТОЕ ПРАВИЛО ПАТТЕРНОВ:
"Сначала сделайте так, чтобы работало.
Потом сделайте так, чтобы работало правильно.
И только потом думайте о паттернах."
```

Удачи в изучении и применении паттернов проектирования! 🚀