# БЛОК 3: ПРАКТИЧЕСКАЯ РАЗРАБОТКА

---

## 🎯 **ЦЕЛЬ БЛОКА**
**Освоение практических навыков разработки с брокерами сообщений**

**Продолжительность:** 5-6 недель  
**Результат:** Умение создавать полнофункциональные приложения с использованием различных брокеров сообщений

---

## 📋 **СТРУКТУРА БЛОКА**

```
БЛОК 3: ПРАКТИЧЕСКАЯ РАЗРАБОТКА
├── 3.1 Глубокое погружение в Apache Kafka (1.5 недели)
├── 3.2 Разработка Producer и Consumer приложений (2 недели)
├── 3.3 Практика с RabbitMQ (1 неделя)
├── 3.4 Сериализация и форматы данных (1 неделя)
└── 3.5 Обработка ошибок и надежность (0.5 недели)
```

---

## ⚡ **ГЛАВА 3.1: ГЛУБОКОЕ ПОГРУЖЕНИЕ В APACHE KAFKA**

### **🏗️ Production-Ready Kafka Cluster Setup**

#### **Архитектура кластера**
```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION KAFKA CLUSTER                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   ZOOKEEPER ENSEMBLE                       ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        ││
│  │  │ZooKeeper 1  │  │ZooKeeper 2  │  │ZooKeeper 3  │        ││
│  │  │   (Leader)  │  │ (Follower)  │  │ (Follower)  │        ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘        ││
│  └─────────────────────────────────────────────────────────────┘│
│                               │                                 │
│  ┌─────────────────────────────┼─────────────────────────────────┐│
│  │             KAFKA BROKERS   │                               ││
│  │  ┌─────────────┐  ┌─────────▼───┐  ┌─────────────┐        ││
│  │  │  Broker 1   │  │  Broker 2   │  │  Broker 3   │        ││
│  │  │  (ID: 1)    │  │  (ID: 2)    │  │  (ID: 3)    │        ││
│  │  │             │  │             │  │             │        ││
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │        ││
│  │  │ │Topic A  │ │  │ │Topic A  │ │  │ │Topic A  │ │        ││
│  │  │ │Part 0(L)│ │  │ │Part 1(L)│ │  │ │Part 2(L)│ │        ││
│  │  │ │Part 1(F)│ │  │ │Part 2(F)│ │  │ │Part 0(F)│ │        ││
│  │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │        ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘        ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘

---

### **📝 Confluent Schema Registry Integration**

#### **Producer с Schema Registry**
```java
// AvroProducerExample.java
import org.apache.kafka.clients.producer.*;
import io.confluent.kafka.serializers.KafkaAvroSerializer;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;

public class AvroProducerExample {
    
    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);
        props.put("schema.registry.url", "http://localhost:8081");
        
        // Define Avro schema
        String schemaString = """
            {
              "type": "record",
              "name": "User",
              "fields": [
                {"name": "id", "type": "long"},
                {"name": "name", "type": "string"},
                {"name": "email", "type": "string"}
              ]
            }
        """;
        
        Schema schema = new Schema.Parser().parse(schemaString);
        
        try (KafkaProducer<String, GenericRecord> producer = new KafkaProducer<>(props)) {
            
            for (int i = 0; i < 100; i++) {
                // Create Avro record
                GenericRecord user = new GenericData.Record(schema);
                user.put("id", (long) i);
                user.put("name", "User " + i);
                user.put("email", "user" + i + "@example.com");
                
                ProducerRecord<String, GenericRecord> record = 
                    new ProducerRecord<>("user-topic", "user-" + i, user);
                
                producer.send(record, (metadata, exception) -> {
                    if (exception != null) {
                        System.err.println("Error: " + exception.getMessage());
                    } else {
                        System.out.println("Sent user " + i + " to " + 
                            metadata.topic() + ":" + metadata.partition() + 
                            " at offset " + metadata.offset());
                    }
                });
            }
        }
    }
}
```

#### **Consumer с Schema Registry**
```java
// AvroConsumerExample.java
import org.apache.kafka.clients.consumer.*;
import io.confluent.kafka.serializers.KafkaAvroDeserializer;
import org.apache.avro.generic.GenericRecord;
import java.time.Duration;
import java.util.Collections;

public class AvroConsumerExample {
    
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "avro-consumer-group");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, KafkaAvroDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, KafkaAvroDeserializer.class);
        props.put("schema.registry.url", "http://localhost:8081");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        
        try (KafkaConsumer<String, GenericRecord> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList("user-topic"));
            
            while (true) {
                ConsumerRecords<String, GenericRecord> records = 
                    consumer.poll(Duration.ofMillis(1000));
                
                for (ConsumerRecord<String, GenericRecord> record : records) {
                    GenericRecord user = record.value();
                    
                    System.out.println("Received user: " +
                        "id=" + user.get("id") +
                        ", name=" + user.get("name") +
                        ", email=" + user.get("email"));
                }
            }
        }
    }
}
```

---

### **🛡️ Protocol Buffers Implementation**

#### **protobuf Schema Definition**
```protobuf
// user.proto
syntax = "proto3";

package com.company.user;

option java_package = "com.company.user";
option java_outer_classname = "UserProtos";

message User {
  int64 id = 1;
  string name = 2;
  string email = 3;
  string phone = 4;
  int64 created_at = 5;
  
  enum Status {
    UNKNOWN = 0;
    ACTIVE = 1;
    INACTIVE = 2;
    SUSPENDED = 3;
  }
  
  Status status = 6;
  
  message Address {
    string street = 1;
    string city = 2;
    string country = 3;
    string postal_code = 4;
  }
  
  repeated Address addresses = 7;
}
```

#### **Protocol Buffers Producer**
```java
// ProtobufProducerExample.java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.ByteArraySerializer;
import org.apache.kafka.common.serialization.StringSerializer;
import com.company.user.UserProtos.User;

public class ProtobufProducerExample {
    
    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, ByteArraySerializer.class);
        
        try (KafkaProducer<String, byte[]> producer = new KafkaProducer<>(props)) {
            
            for (int i = 0; i < 100; i++) {
                // Build protobuf message
                User user = User.newBuilder()
                    .setId(i)
                    .setName("User " + i)
                    .setEmail("user" + i + "@example.com")
                    .setPhone("+1-555-000-" + String.format("%04d", i))
                    .setCreatedAt(System.currentTimeMillis())
                    .setStatus(User.Status.ACTIVE)
                    .addAddresses(User.Address.newBuilder()
                        .setStreet(i + " Main St")
                        .setCity("Anytown")
                        .setCountry("US")
                        .setPostalCode(String.format("%05d", 10000 + i)))
                    .build();
                
                // Serialize to bytes
                byte[] userBytes = user.toByteArray();
                
                ProducerRecord<String, byte[]> record = 
                    new ProducerRecord<>("user-protobuf-topic", "user-" + i, userBytes);
                
                producer.send(record);
                System.out.println("Sent protobuf user " + i + " (" + userBytes.length + " bytes)");
            }
        }
    }
}
```

---

### **⚡ Performance Comparison**

#### **Serialization Benchmark**
```java
// SerializationBenchmark.java
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.io.*;
import org.apache.avro.specific.SpecificDatumWriter;
import org.apache.avro.specific.SpecificDatumReader;
import com.company.user.UserProtos.User;

public class SerializationBenchmark {
    
    private static final int ITERATIONS = 100_000;
    private static final ObjectMapper JSON_MAPPER = new ObjectMapper();
    
    public static void main(String[] args) throws Exception {
        System.out.println("=== SERIALIZATION BENCHMARK ===");
        System.out.println("Iterations: " + ITERATIONS);
        System.out.println();
        
        // Test data
        UserData userData = createTestUser();
        
        // JSON Benchmark
        long jsonStart = System.currentTimeMillis();
        int jsonSize = 0;
        for (int i = 0; i < ITERATIONS; i++) {
            byte[] jsonBytes = JSON_MAPPER.writeValueAsBytes(userData);
            jsonSize = jsonBytes.length;
        }
        long jsonTime = System.currentTimeMillis() - jsonStart;
        
        // Avro Benchmark
        long avroStart = System.currentTimeMillis();
        int avroSize = 0;
        for (int i = 0; i < ITERATIONS; i++) {
            byte[] avroBytes = serializeAvro(userData);
            avroSize = avroBytes.length;
        }
        long avroTime = System.currentTimeMillis() - avroStart;
        
        // Protocol Buffers Benchmark
        long protobufStart = System.currentTimeMillis();
        int protobufSize = 0;
        for (int i = 0; i < ITERATIONS; i++) {
            byte[] protobufBytes = serializeProtobuf(userData);
            protobufSize = protobufBytes.length;
        }
        long protobufTime = System.currentTimeMillis() - protobufStart;
        
        // Results
        printResults("JSON", jsonTime, jsonSize);
        printResults("Avro", avroTime, avroSize);
        printResults("Protobuf", protobufTime, protobufSize);
        
        // Compression ratios
        System.out.println("\n=== COMPRESSION RATIOS ===");
        System.out.printf("Avro vs JSON: %.1fx smaller\n", (double)jsonSize / avroSize);
        System.out.printf("Protobuf vs JSON: %.1fx smaller\n", (double)jsonSize / protobufSize);
    }
    
    private static void printResults(String format, long time, int size) {
        double throughput = (double) ITERATIONS / time * 1000;
        System.out.printf("%-10s: %4dms, %3d bytes, %8.0f ops/sec\n", 
            format, time, size, throughput);
    }
}
```

#### **Benchmark Results Example**
```
=== SERIALIZATION BENCHMARK ===
Iterations: 100,000

JSON      :  245ms, 151 bytes,   408,163 ops/sec
Avro      :   89ms,  42 bytes, 1,123,596 ops/sec  
Protobuf  :   67ms,  38 bytes, 1,492,537 ops/sec

=== COMPRESSION RATIOS ===
Avro vs JSON: 3.6x smaller
Protobuf vs JSON: 4.0x smaller

=== THROUGHPUT COMPARISON ===
┌─────────────────────────────────────────────────────────────────┐
│ JSON:     ████░░░░░░░░░░░░░░░░░░░░ 27% (408K ops/sec)           │
│ Avro:     ████████████████░░░░░░░ 75% (1.1M ops/sec)           │
│ Protobuf: ████████████████████░░░ 100% (1.5M ops/sec)          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ **ГЛАВА 3.5: ОБРАБОТКА ОШИБОК И НАДЕЖНОСТЬ**

### **🔄 Retry Policies и Exponential Backoff**

#### **Retry Strategy Implementation**
```java
// RetryableKafkaProducer.java
import org.apache.kafka.clients.producer.*;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;

public class RetryableKafkaProducer {
    private final KafkaProducer<String, String> producer;
    private final RetryPolicy retryPolicy;
    
    public RetryableKafkaProducer(Properties props, RetryPolicy retryPolicy) {
        this.producer = new KafkaProducer<>(props);
        this.retryPolicy = retryPolicy;
    }
    
    public void sendWithRetry(String topic, String key, String value) {
        ProducerRecord<String, String> record = new ProducerRecord<>(topic, key, value);
        
        int attempt = 0;
        Exception lastException = null;
        
        while (attempt < retryPolicy.getMaxRetries()) {
            try {
                RecordMetadata metadata = producer.send(record).get(
                    retryPolicy.getTimeoutMs(), TimeUnit.MILLISECONDS);
                
                System.out.println("Message sent successfully on attempt " + (attempt + 1) +
                    ": topic=" + metadata.topic() + 
                    ", partition=" + metadata.partition() + 
                    ", offset=" + metadata.offset());
                return;
                
            } catch (Exception e) {
                lastException = e;
                attempt++;
                
                if (attempt < retryPolicy.getMaxRetries()) {
                    long delayMs = calculateDelay(attempt);
                    System.err.println("Attempt " + attempt + " failed, retrying in " + 
                        delayMs + "ms: " + e.getMessage());
                    
                    try {
                        Thread.sleep(delayMs);
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                        throw new RuntimeException("Interrupted during retry", ie);
                    }
                }
            }
        }
        
        throw new RuntimeException("Failed to send message after " + 
            retryPolicy.getMaxRetries() + " attempts", lastException);
    }
    
    private long calculateDelay(int attempt) {
        switch (retryPolicy.getBackoffStrategy()) {
            case FIXED:
                return retryPolicy.getBaseDelayMs();
                
            case LINEAR:
                return retryPolicy.getBaseDelayMs() * attempt;
                
            case EXPONENTIAL:
                long delay = retryPolicy.getBaseDelayMs() * (1L << (attempt - 1));
                return Math.min(delay, retryPolicy.getMaxDelayMs());
                
            case EXPONENTIAL_JITTER:
                long exponentialDelay = retryPolicy.getBaseDelayMs() * (1L << (attempt - 1));
                exponentialDelay = Math.min(exponentialDelay, retryPolicy.getMaxDelayMs());
                
                // Add jitter (±25%)
                double jitterFactor = 0.75 + (ThreadLocalRandom.current().nextDouble() * 0.5);
                return (long) (exponentialDelay * jitterFactor);
                
            default:
                return retryPolicy.getBaseDelayMs();
        }
    }
}

// RetryPolicy.java
public class RetryPolicy {
    public enum BackoffStrategy {
        FIXED, LINEAR, EXPONENTIAL, EXPONENTIAL_JITTER
    }
    
    private final int maxRetries;
    private final long baseDelayMs;
    private final long maxDelayMs;
    private final long timeoutMs;
    private final BackoffStrategy backoffStrategy;
    
    public RetryPolicy(int maxRetries, long baseDelayMs, long maxDelayMs, 
                      long timeoutMs, BackoffStrategy backoffStrategy) {
        this.maxRetries = maxRetries;
        this.baseDelayMs = baseDelayMs;
        this.maxDelayMs = maxDelayMs;
        this.timeoutMs = timeoutMs;
        this.backoffStrategy = backoffStrategy;
    }
    
    // Static factory methods
    public static RetryPolicy exponentialBackoff() {
        return new RetryPolicy(5, 1000, 30000, 10000, BackoffStrategy.EXPONENTIAL_JITTER);
    }
    
    public static RetryPolicy fixedDelay() {
        return new RetryPolicy(3, 2000, 2000, 5000, BackoffStrategy.FIXED);
    }
    
    // Getters...
}
```

#### **Backoff Strategies Visualization**
```
┌─────────────────────────────────────────────────────────────────┐
│                    BACKOFF STRATEGIES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FIXED DELAY:                                                   │
│  Delay │                                                        │
│   (ms) │ ████████████████████████████████████████              │
│   2000 │ ████████████████████████████████████████              │
│   1000 │ ████████████████████████████████████████              │
│      0 └─────┴─────┴─────┴─────┴─────┴─────▶ Attempt            │
│          1     2     3     4     5     6                       │
│                                                                 │
│  EXPONENTIAL BACKOFF:                                           │
│  Delay │                                                        │
│   (ms) │                               ████████████████████    │
│   8000 │                               ████████████████████    │
│   4000 │                     ██████████████████████████████    │
│   2000 │           ████████████████████████████████████████    │
│   1000 │ ████████████████████████████████████████████████████  │
│      0 └─────┴─────┴─────┴─────┴─────┴─────▶ Attempt            │
│          1     2     3     4     5     6                       │
│                                                                 │
│  EXPONENTIAL WITH JITTER:                                       │
│  Delay │                                                        │
│   (ms) │                           ░░██████░░████████░░██      │
│   8000 │                           ░░██████░░████████░░██      │
│   4000 │                 ░░████░░██████████░░████████░░████    │
│   2000 │       ░░████░░████████░░██████████░░████████░░████    │
│   1000 │ ░░██░░████████░░████████░░██████████████████░░████░░  │
│      0 └─────┴─────┴─────┴─────┴─────┴─────▶ Attempt            │
│          1     2     3     4     5     6                       │
│                                                                 │
│  ░ = Jitter variation (±25%)                                   │
│  █ = Base exponential delay                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

### **⚡ Circuit Breaker Pattern**

#### **Circuit Breaker Implementation**
```java
// CircuitBreaker.java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.AtomicReference;

public class CircuitBreaker {
    
    public enum State {
        CLOSED,     // Normal operation
        OPEN,       // Failing fast
        HALF_OPEN   // Testing if service recovered
    }
    
    private final int failureThreshold;
    private final int successThreshold;
    private final long timeoutMs;
    private final AtomicInteger failureCount = new AtomicInteger(0);
    private final AtomicInteger successCount = new AtomicInteger(0);
    private final AtomicLong lastFailureTime = new AtomicLong(0);
    private final AtomicReference<State> state = new AtomicReference<>(State.CLOSED);
    
    public CircuitBreaker(int failureThreshold, int successThreshold, long timeoutMs) {
        this.failureThreshold = failureThreshold;
        this.successThreshold = successThreshold;
        this.timeoutMs = timeoutMs;
    }
    
    public boolean allowRequest() {
        State currentState = state.get();
        
        switch (currentState) {
            case CLOSED:
                return true;
                
            case OPEN:
                if (System.currentTimeMillis() - lastFailureTime.get() > timeoutMs) {
                    // Try to transition to HALF_OPEN
                    if (state.compareAndSet(State.OPEN, State.HALF_OPEN)) {
                        successCount.set(0);
                        return true;
                    }
                }
                return false;
                
            case HALF_OPEN:
                return successCount.get() < successThreshold;
                
            default:
                return false;
        }
    }
    
    public void recordSuccess() {
        State currentState = state.get();
        
        if (currentState == State.HALF_OPEN) {
            int successes = successCount.incrementAndGet();
            if (successes >= successThreshold) {
                // Service recovered, transition to CLOSED
                state.set(State.CLOSED);
                failureCount.set(0);
                System.out.println("Circuit breaker: HALF_OPEN -> CLOSED (service recovered)");
            }
        } else if (currentState == State.CLOSED) {
            // Reset failure count on success
            failureCount.set(0);
        }
    }
    
    public void recordFailure() {
        lastFailureTime.set(System.currentTimeMillis());
        
        State currentState = state.get();
        
        if (currentState == State.HALF_OPEN) {
            // Failed during testing, go back to OPEN
            state.set(State.OPEN);
            System.out.println("Circuit breaker: HALF_OPEN -> OPEN (test failed)");
        } else if (currentState == State.CLOSED) {
            int failures = failureCount.incrementAndGet();
            if (failures >= failureThreshold) {
                // Too many failures, open circuit
                state.set(State.OPEN);
                System.out.println("Circuit breaker: CLOSED -> OPEN (failure threshold reached)");
            }
        }
    }
    
    public State getState() {
        return state.get();
    }
    
    public int getFailureCount() {
        return failureCount.get();
    }
}
```

#### **Circuit Breaker в действии**
```java
// CircuitBreakerKafkaProducer.java
public class CircuitBreakerKafkaProducer {
    private final KafkaProducer<String, String> producer;
    private final CircuitBreaker circuitBreaker;
    
    public CircuitBreakerKafkaProducer(Properties props) {
        this.producer = new KafkaProducer<>(props);
        this.circuitBreaker = new CircuitBreaker(5, 2, 60000); // 5 failures, 2 successes, 60s timeout
    }
    
    public void send(String topic, String key, String value) throws Exception {
        if (!circuitBreaker.allowRequest()) {
            throw new RuntimeException("Circuit breaker is OPEN - failing fast");
        }
        
        try {
            RecordMetadata metadata = producer.send(
                new ProducerRecord<>(topic, key, value)).get();
            
            circuitBreaker.recordSuccess();
            System.out.println("Message sent successfully: " + metadata);
            
        } catch (Exception e) {
            circuitBreaker.recordFailure();
            System.err.println("Failed to send message: " + e.getMessage());
            throw e;
        }
    }
}
```

#### **Circuit Breaker State Transitions**
```
┌─────────────────────────────────────────────────────────────────┐
│                CIRCUIT BREAKER STATE MACHINE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                   ┌─────────────┐                               │
│         ┌────────▶│   CLOSED    │◀──────────┐                   │
│         │         │ (Normal)    │           │                   │
│         │         └─────┬───────┘           │                   │
│         │               │                   │                   │
│         │     failures ≥│ threshold         │ successes ≥      │
│         │     threshold │                   │ threshold         │
│         │               ▼                   │                   │
│         │         ┌─────────────┐           │                   │
│  timeout│         │    OPEN     │           │                   │
│  elapsed│         │ (Fail Fast) │           │                   │
│         │         └─────┬───────┘           │                   │
│         │               │                   │                   │
│         │     timeout   │ elapsed           │                   │
│         │     elapsed   │                   │                   │
│         │               ▼                   │                   │
│         │         ┌─────────────┐           │                   │
│         └─────────│  HALF_OPEN  │───────────┘                   │
│          failure  │ (Testing)   │ success                       │
│                   └─────────────┘                               │
│                                                                 │
│  Behavior in each state:                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ CLOSED:    Allow all requests, count failures              ││
│  │ OPEN:      Reject all requests (fail fast)                 ││
│  │ HALF_OPEN: Allow limited requests to test service health   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

### **🔍 Message Deduplication**

#### **Idempotent Consumer Pattern**
```java
// IdempotentConsumer.java
import java.util.concurrent.ConcurrentHashMap;
import java.util.Set;
import java.util.concurrent.ConcurrentSkipListSet;

public class IdempotentConsumer {
    private final Set<String> processedMessages = new ConcurrentSkipListSet<>();
    private final KafkaConsumer<String, String> consumer;
    
    // Cleanup old message IDs periodically
    private final long MESSAGE_ID_TTL_MS = 3600000; // 1 hour
    private final ConcurrentHashMap<String, Long> messageTimestamps = new ConcurrentHashMap<>();
    
    public IdempotentConsumer(Properties props) {
        this.consumer = new KafkaConsumer<>(props);
        
        // Start cleanup thread
        startCleanupTask();
    }
    
    public void consume(List<String> topics) {
        consumer.subscribe(topics);
        
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
            
            for (ConsumerRecord<String, String> record : records) {
                String messageId = extractMessageId(record);
                
                if (messageId != null && isAlreadyProcessed(messageId)) {
                    System.out.println("Skipping duplicate message: " + messageId);
                    continue;
                }
                
                try {
                    processMessage(record);
                    
                    if (messageId != null) {
                        markAsProcessed(messageId);
                    }
                    
                } catch (Exception e) {
                    System.err.println("Failed to process message: " + e.getMessage());
                    // Don't mark as processed if failed
                }
            }
            
            consumer.commitSync();
        }
    }
    
    private String extractMessageId(ConsumerRecord<String, String> record) {
        // Try to extract message ID from headers
        Header messageIdHeader = record.headers().lastHeader("message-id");
        if (messageIdHeader != null) {
            return new String(messageIdHeader.value());
        }
        
        // Fallback: use key + offset as unique ID
        return record.key() + "-" + record.partition() + "-" + record.offset();
    }
    
    private boolean isAlreadyProcessed(String messageId) {
        return processedMessages.contains(messageId);
    }
    
    private void markAsProcessed(String messageId) {
        processedMessages.add(messageId);
        messageTimestamps.put(messageId, System.currentTimeMillis());
    }
    
    private void processMessage(ConsumerRecord<String, String> record) {
        // Simulate message processing
        System.out.println("Processing message: " + record.value());
        
        // Your business logic here
        // This should be idempotent by nature
    }
    
    private void startCleanupTask() {
        Thread cleanupThread = new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(300000); // Cleanup every 5 minutes
                    cleanupOldMessageIds();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        
        cleanupThread.setDaemon(true);
        cleanupThread.start();
    }
    
    private void cleanupOldMessageIds() {
        long now = System.currentTimeMillis();
        int removedCount = 0;
        
        for (Map.Entry<String, Long> entry : messageTimestamps.entrySet()) {
            if (now - entry.getValue() > MESSAGE_ID_TTL_MS) {
                String messageId = entry.getKey();
                processedMessages.remove(messageId);
                messageTimestamps.remove(messageId);
                removedCount++;
            }
        }
        
        if (removedCount > 0) {
            System.out.println("Cleaned up " + removedCount + " old message IDs");
        }
    }
}
```

---

### **💾 Transactional Messaging**

#### **Kafka Transactions Example**
```java
// TransactionalKafkaExample.java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.TopicPartition;
import java.util.Map;
import java.util.HashMap;

public class TransactionalKafkaExample {
    
    public static class TransactionalProducer {
        private final KafkaProducer<String, String> producer;
        
        public TransactionalProducer(String transactionalId) {
            Properties props = new Properties();
            props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
            props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
            props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
            
            // Transactional settings
            props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, transactionalId);
            props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
            props.put(ProducerConfig.ACKS_CONFIG, "all");
            props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);
            props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 1);
            
            this.producer = new KafkaProducer<>(props);
            this.producer.initTransactions();
        }
        
        public void processAndForward(ConsumerRecords<String, String> records, 
                                     Map<TopicPartition, OffsetAndMetadata> offsets) {
            try {
                producer.beginTransaction();
                
                // Process messages and send to output topic
                for (ConsumerRecord<String, String> record : records) {
                    String processedValue = processMessage(record.value());
                    
                    ProducerRecord<String, String> outputRecord = 
                        new ProducerRecord<>("processed-orders", record.key(), processedValue);
                    
                    producer.send(outputRecord);
                }
                
                // Commit consumer offsets as part of transaction
                producer.sendOffsetsToTransaction(offsets, "order-processor-group");
                
                // Commit transaction
                producer.commitTransaction();
                System.out.println("Transaction committed successfully");
                
            } catch (Exception e) {
                System.err.println("Transaction failed, aborting: " + e.getMessage());
                producer.abortTransaction();
                throw new RuntimeException(e);
            }
        }
        
        private String processMessage(String input) {
            // Simulate message processing
            return "PROCESSED: " + input;
        }
        
        public void close() {
            producer.close();
        }
    }
    
    public static class TransactionalConsumer {
        private final KafkaConsumer<String, String> consumer;
        
        public TransactionalConsumer() {
            Properties props = new Properties();
            props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
            props.put(ConsumerConfig.GROUP_ID_CONFIG, "order-processor-group");
            props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
            props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
            
            // Read only committed messages
            props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");
            props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
            
            this.consumer = new KafkaConsumer<>(props);
        }
        
        public void consumeAndProcess() {
            consumer.subscribe(Collections.singletonList("orders"));
            TransactionalProducer producer = new TransactionalProducer("order-processor");
            
            try {
                while (true) {
                    ConsumerRecords<String, String> records = 
                        consumer.poll(Duration.ofMillis(1000));
                    
                    if (!records.isEmpty()) {
                        // Prepare offset commit map
                        Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();
                        for (ConsumerRecord<String, String> record : records) {
                            TopicPartition partition = 
                                new TopicPartition(record.topic(), record.partition());
                            offsets.put(partition, 
                                new OffsetAndMetadata(record.offset() + 1));
                        }
                        
                        // Process in transaction
                        producer.processAndForward(records, offsets);
                    }
                }
            } finally {
                producer.close();
                consumer.close();
            }
        }
    }
}
```

#### **Transaction Flow Diagram**
```
┌─────────────────────────────────────────────────────────────────┐
│                    KAFKA TRANSACTIONS FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. BEGIN TRANSACTION:                                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──beginTransaction()──▶ Transaction Coordinator    ││
│  │                                        │                    ││
│  │                                        ▼                    ││
│  │                                 Assign Transaction ID       ││
│  │                                 Create Transaction Log      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  2. SEND MESSAGES:                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──send(record)──▶ Topic Partition                  ││
│  │                                  │                          ││
│  │                                  ▼                          ││
│  │                           Mark as part of TX               ││
│  │                           (not visible to consumers yet)    ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  3. COMMIT OFFSETS (optional):                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──sendOffsetsToTransaction()──▶ __consumer_offsets ││
│  │                                               │             ││
│  │                                               ▼             ││
│  │                                        Mark as part of TX   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  4. COMMIT TRANSACTION:                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──commitTransaction()──▶ Transaction Coordinator   ││
│  │                                        │                    ││
│  │                                        ▼                    ││
│  │                                 Mark TX as committed        ││
│  │                                        │                    ││
│  │                                        ▼                    ││
│  │                                 Messages become visible     ││
│  │                                 to read_committed consumers ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ABORT SCENARIO:                                                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──abortTransaction()──▶ Transaction Coordinator    ││
│  │                                        │                    ││
│  │                                        ▼                    ││
│  │                                 Mark TX as aborted          ││
│  │                                        │                    ││
│  │                                        ▼                    ││
│  │                                 Messages are discarded      ││
│  │                                 (never visible to consumers)││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **ИТОГИ БЛОКА 3**

### **✅ Что вы освоили:**

1. **Production Kafka Setup** — настройка enterprise-ready кластера
2. **Advanced Producer/Consumer** — высокопроизводительные приложения
3. **RabbitMQ Advanced Features** — сложная маршрутизация и DLX
4. **Serialization Formats** — Avro, Protocol Buffers, Schema Registry
5. **Error Handling & Reliability** — retry, circuit breaker, idempotency, transactions

### **🛠️ Практические навыки:**

- Настройка production-ready инфраструктуры
- Написание fault-tolerant приложений
- Оптимизация производительности
- Обеспечение надежности доставки сообщений
- Работа с schema evolution

### **📊 Performance Best Practices:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE SUMMARY                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  KAFKA PRODUCER TUNING:                                         │
│  ✅ batch.size = 65536 (64KB)                                  │
│  ✅ linger.ms = 10                                             │
│  ✅ compression.type = lz4                                     │
│  ✅ acks = all (for reliability)                               │
│                                                                 │
│  KAFKA CONSUMER TUNING:                                         │
│  ✅ fetch.min.bytes = 1024                                     │
│  ✅ max.poll.records = 1000                                    │
│  ✅ Parallel processing with thread pools                      │
│  ✅ Manual offset commits                                       │
│                                                                 │
│  SERIALIZATION:                                                 │
│  ✅ Use Avro/Protobuf for production                           │
│  ✅ Schema Registry for schema evolution                       │
│  ✅ Avoid JSON for high-throughput scenarios                   │
│                                                                 │
│  RELIABILITY:                                                   │
│  ✅ Implement retry with exponential backoff                   │
│  ✅ Use circuit breakers for external dependencies             │
│  ✅ Ensure idempotent message processing                       │
│  ✅ Use transactions for exactly-once semantics                │
└─────────────────────────────────────────────────────────────────┘
```

### **🚀 Следующие шаги:**

Переходите к **Блоку 4: Проектирование и архитектура**, где вы изучите Enterprise Integration Patterns, Event Sourcing, CQRS и построение distributed систем!

---

## 📚 **Практические задания для закрепления**

### **🎯 Задание 1: High-Throughput Producer**
Создайте Kafka producer, способный отправлять 100K+ сообщений в секунду с гарантией доставки.

### **🎯 Задание 2: Fault-Tolerant Consumer**
Реализуйте consumer с circuit breaker, retry логикой и idempotent processing.

### **🎯 Задание 3: Schema Evolution**
Создайте Avro schema и проведите несколько эволюций, тестируя backward/forward compatibility.

### **🎯 Задание 4: Transaction Processing**
Реализуйте exactly-once processing между двумя Kafka топиками с использованием транзакций.

---

**Время на изучение блока: 5-6 недель**  
**Следующий блок: Проектирование и архитектура** 🏗️
     │                       │                       │
     ▼                       ▼                       ▼
┌──────────┐          ┌──────────┐          ┌──────────┐
│ Client   │          │ Client   │          │ Client   │
│Apps/APIs │          │Apps/APIs │          │Apps/APIs │
└──────────┘          └──────────┘          └──────────┘

L = Leader, F = Follower
```

---

### **⚙️ Детальная конфигурация Kafka**

#### **server.properties - Production Configuration**
```properties
############################ Server Basics ############################
broker.id=1
listeners=PLAINTEXT://0.0.0.0:9092
advertised.listeners=PLAINTEXT://kafka-1.internal:9092
num.network.threads=8
num.io.threads=16
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

############################ Log Basics ############################
log.dirs=/var/kafka-logs
num.partitions=6
default.replication.factor=3
min.insync.replicas=2
log.retention.hours=168
log.retention.bytes=1073741824
log.segment.bytes=1073741824
log.cleanup.policy=delete

############################ Zookeeper ############################
zookeeper.connect=zk-1.internal:2181,zk-2.internal:2181,zk-3.internal:2181
zookeeper.connection.timeout.ms=6000

############################ Performance Tuning ############################
# Producer config
compression.type=lz4
batch.size=16384
linger.ms=5
buffer.memory=33554432

# Consumer config
fetch.min.bytes=1
fetch.max.wait.ms=500
max.partition.fetch.bytes=1048576

# Replication
replica.fetch.max.bytes=1048576
replica.socket.timeout.ms=30000
replica.socket.receive.buffer.bytes=65536
```

#### **JVM и OS настройки**
```bash
#!/bin/bash
# kafka-server-start-tuned.sh

# JVM Heap размер (рекомендуется 6GB для production)
export KAFKA_HEAP_OPTS="-Xmx6g -Xms6g"

# GC настройки для низкой latency
export KAFKA_JVM_PERFORMANCE_OPTS="-server -XX:+UseG1GC -XX:MaxGCPauseMillis=20 \
    -XX:InitiatingHeapOccupancyPercent=35 -XX:+ExplicitGCInvokesConcurrent \
    -XX:MaxInlineLevel=15 -Djava.awt.headless=true"

# OS level настройки
echo 'vm.swappiness=1' >> /etc/sysctl.conf
echo 'vm.dirty_ratio=80' >> /etc/sysctl.conf
echo 'vm.dirty_background_ratio=5' >> /etc/sysctl.conf
echo 'net.core.rmem_default = 262144' >> /etc/sysctl.conf
echo 'net.core.rmem_max = 16777216' >> /etc/sysctl.conf

# File descriptor limits
echo 'kafka soft nofile 100000' >> /etc/security/limits.conf
echo 'kafka hard nofile 100000' >> /etc/security/limits.conf

# Start Kafka
kafka-server-start.sh /opt/kafka/config/server.properties
```

---

### **📊 Kafka Manager и мониторинг**

#### **Prometheus метрики конфигурация**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'kafka'
    static_configs:
      - targets: ['kafka-1:9308', 'kafka-2:9308', 'kafka-3:9308']
    metrics_path: /metrics
    scrape_interval: 10s
    
  - job_name: 'kafka-jmx'
    static_configs:
      - targets: ['kafka-1:9999', 'kafka-2:9999', 'kafka-3:9999']
    metrics_path: /metrics
    scrape_interval: 30s
```

#### **Key Performance Indicators (KPIs)**
```
┌─────────────────────────────────────────────────────────────────┐
│                      KAFKA METRICS DASHBOARD                   │
├─────────────────────────────────────────────────────────────────┤
│  THROUGHPUT METRICS:                                            │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ • Messages in/sec:  ████████████░ 85K msg/s                ││
│  │ • Bytes in/sec:     ████████░░░░░ 120 MB/s                 ││
│  │ • Bytes out/sec:    ██████████░░░ 200 MB/s                 ││
│  │ • Requests/sec:     ████████████░ 12K req/s                ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  LATENCY METRICS:                                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ • Producer latency: ██░░░░░░░░░░░ 5ms (p99)                 ││
│  │ • Consumer lag:     ████░░░░░░░░░ 100ms (max)               ││
│  │ • Request latency:  ███░░░░░░░░░░ 3ms (avg)                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  RESOURCE METRICS:                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ • CPU Usage:        ████████░░░░░ 70%                       ││
│  │ • Memory Usage:     ██████░░░░░░░ 60%                       ││
│  │ • Disk Usage:       ███░░░░░░░░░░ 30%                       ││
│  │ • Network I/O:      █████████░░░░ 80%                       ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

#### **Критические алерты**
```yaml
# alerts.yml
groups:
  - name: kafka-alerts
    rules:
    - alert: KafkaConsumerLag
      expr: kafka_consumer_lag_max > 1000
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High consumer lag detected"
        
    - alert: KafkaBrokerDown
      expr: up{job="kafka"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Kafka broker is down"
        
    - alert: KafkaUnderReplicatedPartitions
      expr: kafka_server_replicamanager_underreplicatedpartitions > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Under-replicated partitions detected"
```

---

### **🗂️ Schema Registry**

#### **Что такое Schema Registry?**
```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEMA REGISTRY ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              CONFLUENT SCHEMA REGISTRY                     ││
│  │                                                             ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        ││
│  │  │ Schema v1   │  │ Schema v2   │  │ Schema v3   │        ││
│  │  │ (user.avsc) │  │ (user.avsc) │  │ (user.avsc) │        ││
│  │  │             │  │ + phone     │  │ + address   │        ││
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │        ││
│  │  │ │id: 1    │ │  │ │id: 2    │ │  │ │id: 3    │ │        ││
│  │  │ │name     │ │  │ │name     │ │  │ │name     │ │        ││
│  │  │ │email    │ │  │ │email    │ │  │ │email    │ │        ││
│  │  │ └─────────┘ │  │ │phone    │ │  │ │phone    │ │        ││
│  │  └─────────────┘  │ └─────────┘ │  │ │address  │ │        ││
│  │                   └─────────────┘  │ └─────────┘ │        ││
│  │                                    └─────────────┘        ││
│  └─────────────────────────────────────────────────────────────┘│
│                               │                                 │
│  ┌─────────────────────────────┼─────────────────────────────────┐│
│  │              KAFKA CLUSTER  │                               ││
│  │                             │                               ││
│  │     Producer ──[schema_id]──┼──▶ Topic ──[schema_id]──▶ Consumer││
│  │         │                   │              │             │  ││
│  │         ▼                   │              ▼             ▼  ││
│  │   ┌──────────┐             │        ┌──────────┐ ┌──────────┐││
│  │   │ Validate │             │        │ Validate │ │Deserializ│││
│  │   │& Serializ│             │        │&Deserial.│ │   Data   │││
│  │   └──────────┘             │        └──────────┘ └──────────┘││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

#### **Avro Schema Example**
```json
{
  "type": "record",
  "name": "User",
  "namespace": "com.company.user",
  "fields": [
    {
      "name": "id",
      "type": "long",
      "doc": "Unique user identifier"
    },
    {
      "name": "name",
      "type": "string",
      "doc": "User full name"
    },
    {
      "name": "email",
      "type": "string",
      "doc": "User email address"
    },
    {
      "name": "phone",
      "type": ["null", "string"],
      "default": null,
      "doc": "Optional phone number"
    },
    {
      "name": "created_at",
      "type": {
        "type": "long",
        "logicalType": "timestamp-millis"
      },
      "doc": "Account creation timestamp"
    }
  ]
}
```

#### **Schema Evolution правила**
```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEMA EVOLUTION COMPATIBILITY               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BACKWARD COMPATIBLE (default):                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ✅ Delete fields                                            ││
│  │ ✅ Add optional fields (with defaults)                     ││
│  │ ❌ Add required fields                                      ││
│  │ ❌ Change field types                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  FORWARD COMPATIBLE:                                            │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ✅ Add fields                                               ││
│  │ ✅ Delete optional fields                                   ││
│  │ ❌ Delete required fields                                   ││
│  │ ❌ Change field types                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  FULL COMPATIBLE:                                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ✅ Add optional fields (with defaults)                     ││
│  │ ✅ Delete optional fields                                   ││
│  │ ❌ Add/delete required fields                               ││
│  │ ❌ Change field types                                       ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

### **🛠️ Практическое задание: Production Kafka Setup**

#### **Docker Compose для Full Stack**
```yaml
version: '3.8'
services:
  zookeeper-1:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_SERVER_ID: 1
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
      ZOOKEEPER_SERVERS: zookeeper-1:2888:3888;zookeeper-2:2888:3888;zookeeper-3:2888:3888
    volumes:
      - zk1-data:/var/lib/zookeeper/data
      - zk1-logs:/var/lib/zookeeper/log

  kafka-1:
    image: confluentinc/cp-kafka:latest
    depends_on: [zookeeper-1, zookeeper-2, zookeeper-3]
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper-1:2181,zookeeper-2:2181,zookeeper-3:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-1:9092
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: false
      KAFKA_DELETE_TOPIC_ENABLE: true
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 3
      KAFKA_JMX_PORT: 9999
      KAFKA_JMX_HOSTNAME: kafka-1
    volumes:
      - kafka1-data:/var/lib/kafka/data

  schema-registry:
    image: confluentinc/cp-schema-registry:latest
    depends_on: [kafka-1, kafka-2, kafka-3]
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: kafka-1:9092,kafka-2:9092,kafka-3:9092
      SCHEMA_REGISTRY_LISTENERS: http://0.0.0.0:8081
    ports:
      - "8081:8081"

  kafka-manager:
    image: hlebalbau/kafka-manager:stable
    depends_on: [kafka-1, kafka-2, kafka-3]
    environment:
      ZK_HOSTS: zookeeper-1:2181,zookeeper-2:2181,zookeeper-3:2181
      APPLICATION_SECRET: "random-secret"
    ports:
      - "9000:9000"

volumes:
  zk1-data:
  zk1-logs:
  kafka1-data:
```

---

## 🚀 **ГЛАВА 3.2: РАЗРАБОТКА PRODUCER И CONSUMER ПРИЛОЖЕНИЙ**

### **📤 Advanced Producer Development**

#### **High-Performance Producer Configuration**
```java
// HighPerformanceKafkaProducer.java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import java.util.Properties;
import java.util.concurrent.Future;

public class HighPerformanceKafkaProducer {
    private final KafkaProducer<String, String> producer;
    
    public HighPerformanceKafkaProducer() {
        Properties props = new Properties();
        
        // Connection settings
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, 
                 "kafka-1:9092,kafka-2:9092,kafka-3:9092");
        
        // Performance tuning
        props.put(ProducerConfig.BATCH_SIZE_CONFIG, 65536);        // 64KB batches
        props.put(ProducerConfig.LINGER_MS_CONFIG, 10);            // Wait 10ms for batching
        props.put(ProducerConfig.BUFFER_MEMORY_CONFIG, 67108864);  // 64MB buffer
        props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "lz4");   // Fast compression
        
        // Reliability settings
        props.put(ProducerConfig.ACKS_CONFIG, "all");              // Wait for all replicas
        props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE); // Infinite retries
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 1); // Order guarantee
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true); // Exactly-once semantics
        
        // Timeouts
        props.put(ProducerConfig.REQUEST_TIMEOUT_MS_CONFIG, 30000);
        props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 120000);
        
        // Serializers
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        
        this.producer = new KafkaProducer<>(props);
    }
    
    public Future<RecordMetadata> sendAsync(String topic, String key, String value) {
        ProducerRecord<String, String> record = new ProducerRecord<>(topic, key, value);
        
        return producer.send(record, new Callback() {
            @Override
            public void onCompletion(RecordMetadata metadata, Exception exception) {
                if (exception != null) {
                    // Log error and implement retry logic
                    System.err.println("Failed to send message: " + exception.getMessage());
                } else {
                    System.out.println("Message sent successfully: " + 
                        "topic=" + metadata.topic() + 
                        ", partition=" + metadata.partition() + 
                        ", offset=" + metadata.offset());
                }
            }
        });
    }
    
    public void close() {
        producer.close();
    }
}
```

#### **Partitioning Strategies**
```java
// CustomPartitioner.java
import org.apache.kafka.clients.producer.Partitioner;
import org.apache.kafka.common.Cluster;
import java.util.Map;

public class CustomPartitioner implements Partitioner {
    
    @Override
    public int partition(String topic, Object key, byte[] keyBytes, 
                        Object value, byte[] valueBytes, Cluster cluster) {
        
        int numPartitions = cluster.partitionCountForTopic(topic);
        
        if (key == null) {
            // Round-robin для null keys
            return (int) (System.currentTimeMillis() % numPartitions);
        }
        
        String keyStr = (String) key;
        
        // Специальная логика для VIP пользователей
        if (keyStr.startsWith("VIP_")) {
            return 0; // Всегда отправляем в partition 0
        }
        
        // Географическое партицирование
        if (keyStr.contains("_US_")) {
            return 1;
        } else if (keyStr.contains("_EU_")) {
            return 2;
        } else if (keyStr.contains("_ASIA_")) {
            return 3;
        }
        
        // Default hash partitioning
        return Math.abs(keyStr.hashCode()) % numPartitions;
    }
    
    @Override
    public void close() {}
    
    @Override
    public void configure(Map<String, ?> configs) {}
}
```

#### **Producer Patterns**
```
┌─────────────────────────────────────────────────────────────────┐
│                      PRODUCER PATTERNS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FIRE AND FORGET:                                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──send()──▶ Kafka ──▶ ❓ (don't care about result) ││
│  │                                                             ││
│  │ + Highest throughput                                        ││
│  │ - No delivery guarantee                                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  SYNCHRONOUS SEND:                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──send().get()──▶ Kafka ──▶ ✅/❌ ◀── wait for ACK ││
│  │                                                             ││
│  │ + Delivery guarantee                                        ││
│  │ - Lowest throughput                                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ASYNCHRONOUS SEND:                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──send(callback)──▶ Kafka ──▶ ✅/❌ ──▶ callback   ││
│  │                                                             ││
│  │ + High throughput + Error handling                          ││
│  │ - More complex logic                                        ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

### **📥 Advanced Consumer Development**

#### **High-Performance Consumer Configuration**
```java
// HighPerformanceKafkaConsumer.java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.StringDeserializer;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.*;

public class HighPerformanceKafkaConsumer {
    private final KafkaConsumer<String, String> consumer;
    private final ExecutorService executor;
    private volatile boolean running = true;
    
    public HighPerformanceKafkaConsumer(String groupId) {
        Properties props = new Properties();
        
        // Connection settings
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, 
                 "kafka-1:9092,kafka-2:9092,kafka-3:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        
        // Performance tuning
        props.put(ConsumerConfig.FETCH_MIN_BYTES_CONFIG, 1024);      // Min 1KB per fetch
        props.put(ConsumerConfig.FETCH_MAX_WAIT_MS_CONFIG, 500);     // Max wait 500ms
        props.put(ConsumerConfig.MAX_PARTITION_FETCH_BYTES_CONFIG, 1048576); // 1MB per partition
        props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 1000);     // Process 1000 records at once
        
        // Offset management
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);  // Manual offset commit
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        
        // Session management
        props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, 30000);
        props.put(ConsumerConfig.HEARTBEAT_INTERVAL_MS_CONFIG, 10000);
        props.put(ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, 300000); // 5 minutes
        
        // Deserializers
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        
        this.consumer = new KafkaConsumer<>(props);
        this.executor = Executors.newFixedThreadPool(10); // Thread pool for processing
    }
    
    public void consume(List<String> topics) {
        consumer.subscribe(topics);
        
        while (running) {
            try {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
                
                if (!records.isEmpty()) {
                    // Process records in parallel
                    List<Future<?>> futures = new ArrayList<>();
                    
                    for (ConsumerRecord<String, String> record : records) {
                        Future<?> future = executor.submit(() -> processRecord(record));
                        futures.add(future);
                    }
                    
                    // Wait for all processing to complete
                    for (Future<?> future : futures) {
                        future.get(); // This will throw exception if processing failed
                    }
                    
                    // Commit offsets only after successful processing
                    consumer.commitSync();
                }
                
            } catch (Exception e) {
                System.err.println("Error in consumer loop: " + e.getMessage());
                // Implement retry logic or dead letter queue
            }
        }
    }
    
    private void processRecord(ConsumerRecord<String, String> record) {
        try {
            // Simulate processing time
            Thread.sleep(10);
            
            System.out.println("Processed message: " + 
                "key=" + record.key() + 
                ", value=" + record.value() + 
                ", partition=" + record.partition() + 
                ", offset=" + record.offset());
                
        } catch (Exception e) {
            System.err.println("Failed to process record: " + e.getMessage());
            // Send to dead letter queue or retry
            throw new RuntimeException(e);
        }
    }
    
    public void shutdown() {
        running = false;
        consumer.close();
        executor.shutdown();
    }
}
```

#### **Consumer Groups и Partition Assignment**
```
┌─────────────────────────────────────────────────────────────────┐
│                    CONSUMER GROUP REBALANCING                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INITIAL STATE (3 consumers, 6 partitions):                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Topic: user-events                                          ││
│  │ ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌───┐││
│  │ │ Part 0  ││ Part 1  ││ Part 2  ││ Part 3  ││ Part 4  ││P5 │││
│  │ └─────────┘└─────────┘└─────────┘└─────────┘└─────────┘└───┘││
│  │     │          │          │          │          │        │  ││
│  │     ▼          ▼          ▼          ▼          ▼        ▼  ││
│  │ ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ ││
│  │ │  Consumer A    │  │  Consumer B    │  │  Consumer C    │ ││
│  │ │  (Part 0,1)    │  │  (Part 2,3)    │  │  (Part 4,5)    │ ││
│  │ └────────────────┘  └────────────────┘  └────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  AFTER CONSUMER B FAILURE (rebalancing):                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌───┐││
│  │ │ Part 0  ││ Part 1  ││ Part 2  ││ Part 3  ││ Part 4  ││P5 │││
│  │ └─────────┘└─────────┘└─────────┘└─────────┘└─────────┘└───┘││
│  │     │          │          │          │          │        │  ││
│  │     ▼          ▼          ▼          ▼          ▼        ▼  ││
│  │ ┌────────────────┐              ┌────────────────┐         ││
│  │ │  Consumer A    │              │  Consumer C    │         ││
│  │ │ (Part 0,1,2)   │              │ (Part 3,4,5)   │         ││
│  │ └────────────────┘              └────────────────┘         ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

#### **Offset Management Strategies**
```java
// OffsetManagementStrategies.java
public class OffsetManagementStrategies {
    
    // Strategy 1: Auto-commit (простой, но может привести к потере сообщений)
    public void autoCommitExample() {
        Properties props = new Properties();
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, true);
        props.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, 5000);
        
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        // Consumer автоматически коммитит offsets каждые 5 секунд
    }
    
    // Strategy 2: Manual commit after processing (надежнее)
    public void manualCommitExample() {
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
            
            for (ConsumerRecord<String, String> record : records) {
                processRecord(record); // Process first
            }
            
            try {
                consumer.commitSync(); // Then commit
            } catch (CommitFailedException e) {
                // Handle commit failure
                System.err.println("Commit failed: " + e.getMessage());
            }
        }
    }
    
    // Strategy 3: Commit specific offsets
    public void specificOffsetCommitExample() {
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();
        
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
            
            for (ConsumerRecord<String, String> record : records) {
                processRecord(record);
                
                // Track offset for each partition
                TopicPartition partition = new TopicPartition(record.topic(), record.partition());
                OffsetAndMetadata offset = new OffsetAndMetadata(record.offset() + 1);
                offsets.put(partition, offset);
            }
            
            // Commit specific offsets
            consumer.commitSync(offsets);
            offsets.clear();
        }
    }
}
```

---

### **⚖️ Consumer Load Balancing и Scaling**

#### **Dynamic Consumer Scaling**
```java
// DynamicConsumerScaler.java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.List;
import java.util.ArrayList;

public class DynamicConsumerScaler {
    private final List<Thread> consumerThreads = new ArrayList<>();
    private final AtomicInteger consumerCount = new AtomicInteger(0);
    private final String groupId;
    private final List<String> topics;
    
    public DynamicConsumerScaler(String groupId, List<String> topics) {
        this.groupId = groupId;
        this.topics = topics;
    }
    
    public void scaleUp(int additionalConsumers) {
        for (int i = 0; i < additionalConsumers; i++) {
            String consumerId = groupId + "-consumer-" + consumerCount.incrementAndGet();
            
            Thread consumerThread = new Thread(() -> {
                HighPerformanceKafkaConsumer consumer = 
                    new HighPerformanceKafkaConsumer(groupId);
                consumer.consume(topics);
            });
            
            consumerThread.setName(consumerId);
            consumerThread.start();
            consumerThreads.add(consumerThread);
            
            System.out.println("Started consumer: " + consumerId);
        }
    }
    
    public void scaleDown(int consumersToRemove) {
        int removed = 0;
        for (int i = consumerThreads.size() - 1; i >= 0 && removed < consumersToRemove; i--) {
            Thread thread = consumerThreads.get(i);
            thread.interrupt(); // Gracefully shutdown
            consumerThreads.remove(i);
            removed++;
            
            System.out.println("Stopped consumer: " + thread.getName());
        }
    }
    
    public int getCurrentConsumerCount() {
        return consumerThreads.size();
    }
}
```

#### **Consumer Lag Monitoring**
```java
// ConsumerLagMonitor.java
import org.apache.kafka.clients.admin.*;
import org.apache.kafka.clients.consumer.*;
import java.util.*;
import java.util.concurrent.ExecutionException;

public class ConsumerLagMonitor {
    private final AdminClient adminClient;
    private final Properties consumerProps;
    
    public ConsumerLagMonitor(String bootstrapServers) {
        Properties adminProps = new Properties();
        adminProps.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        this.adminClient = AdminClient.create(adminProps);
        
        consumerProps = new Properties();
        consumerProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        consumerProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        consumerProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    }
    
    public Map<String, Long> getConsumerLag(String groupId) 
            throws ExecutionException, InterruptedException {
        
        Map<String, Long> lagPerPartition = new HashMap<>();
        
        // Get consumer group description
        DescribeConsumerGroupsResult groupResult = 
            adminClient.describeConsumerGroups(Collections.singletonList(groupId));
        ConsumerGroupDescription groupDescription = 
            groupResult.describedGroups().get(groupId).get();
        
        // Get committed offsets
        ListConsumerGroupOffsetsResult offsetsResult = 
            adminClient.listConsumerGroupOffsets(groupId);
        Map<TopicPartition, OffsetAndMetadata> committedOffsets = 
            offsetsResult.partitionsToOffsetAndMetadata().get();
        
        // Get end offsets for each partition
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps)) {
            Set<TopicPartition> partitions = committedOffsets.keySet();
            Map<TopicPartition, Long> endOffsets = consumer.endOffsets(partitions);
            
            // Calculate lag
            for (Map.Entry<TopicPartition, OffsetAndMetadata> entry : committedOffsets.entrySet()) {
                TopicPartition partition = entry.getKey();
                long committedOffset = entry.getValue().offset();
                long endOffset = endOffsets.get(partition);
                long lag = endOffset - committedOffset;
                
                lagPerPartition.put(partition.toString(), lag);
            }
        }
        
        return lagPerPartition;
    }
    
    public void printLagReport(String groupId) {
        try {
            Map<String, Long> lag = getConsumerLag(groupId);
            
            System.out.println("=== Consumer Lag Report for Group: " + groupId + " ===");
            System.out.println("┌─────────────────────────┬─────────────┐");
            System.out.println("│ Partition               │ Lag         │");
            System.out.println("├─────────────────────────┼─────────────┤");
            
            long totalLag = 0;
            for (Map.Entry<String, Long> entry : lag.entrySet()) {
                System.out.printf("│ %-23s │ %11d │%n", entry.getKey(), entry.getValue());
                totalLag += entry.getValue();
            }
            
            System.out.println("├─────────────────────────┼─────────────┤");
            System.out.printf("│ TOTAL LAG               │ %11d │%n", totalLag);
            System.out.println("└─────────────────────────┴─────────────┘");
            
        } catch (Exception e) {
            System.err.println("Failed to get lag information: " + e.getMessage());
        }
    }
}
```

---

## 🐰 **ГЛАВА 3.3: ПРАКТИКА С RABBITMQ**

### **🔀 Advanced Routing с Headers Exchange**

#### **Headers Exchange Implementation**
```java
// RabbitMQHeadersExchangeExample.java
import com.rabbitmq.client.*;
import java.util.HashMap;
import java.util.Map;

public class RabbitMQHeadersExchangeExample {
    
    private static final String EXCHANGE_NAME = "notification_headers";
    
    public static void setupExchangeAndQueues() throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        
        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {
            
            // Declare headers exchange
            channel.exchangeDeclare(EXCHANGE_NAME, "headers", true);
            
            // Declare queues
            channel.queueDeclare("email_queue", true, false, false, null);
            channel.queueDeclare("sms_queue", true, false, false, null);
            channel.queueDeclare("push_queue", true, false, false, null);
            channel.queueDeclare("high_priority_queue", true, false, false, null);
            
            // Binding for email notifications
            Map<String, Object> emailHeaders = new HashMap<>();
            emailHeaders.put("x-match", "all");
            emailHeaders.put("type", "email");
            channel.queueBind("email_queue", EXCHANGE_NAME, "", emailHeaders);
            
            // Binding for SMS notifications
            Map<String, Object> smsHeaders = new HashMap<>();
            smsHeaders.put("x-match", "all");
            smsHeaders.put("type", "sms");
            channel.queueBind("sms_queue", EXCHANGE_NAME, "", smsHeaders);
            
            // Binding for high priority (any type)
            Map<String, Object> highPriorityHeaders = new HashMap<>();
            highPriorityHeaders.put("x-match", "any");
            highPriorityHeaders.put("priority", "high");
            channel.queueBind("high_priority_queue", EXCHANGE_NAME, "", highPriorityHeaders);
        }
    }
    
    public static void publishMessage(String type, String priority, String content) throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        
        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {
            
            // Set message headers
            Map<String, Object> headers = new HashMap<>();
            headers.put("type", type);
            headers.put("priority", priority);
            headers.put("timestamp", System.currentTimeMillis());
            
            AMQP.BasicProperties props = new AMQP.BasicProperties.Builder()
                .headers(headers)
                .deliveryMode(2) // Persistent message
                .build();
            
            channel.basicPublish(EXCHANGE_NAME, "", props, content.getBytes());
            
            System.out.println("Published message: " + content + 
                " with headers: " + headers);
        }
    }
}
```

#### **Complex Routing Scenarios**
```
┌─────────────────────────────────────────────────────────────────┐
│                   COMPLEX ROUTING EXAMPLE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Message Headers: {type: "email", priority: "high", region: "US"}│
│                                                                 │
│                           │                                     │
│                           ▼                                     │
│                  ┌─────────────────┐                           │
│                  │ Headers Exchange│                           │
│                  └─────────┬───────┘                           │
│                           │                                     │
│          ┌────────────────┼────────────────┐                   │
│          │                │                │                   │
│          ▼                ▼                ▼                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │ Email Queue  │ │ High Priority│ │ US Region    │           │
│  │              │ │ Queue        │ │ Queue        │           │
│  │ Binding:     │ │              │ │              │           │
│  │ type=email   │ │ Binding:     │ │ Binding:     │           │
│  │ (x-match=all)│ │ priority=high│ │ region=US    │           │
│  │              │ │ (x-match=any)│ │ (x-match=all)│           │
│  └──────────────┘ └──────────────┘ └──────────────┘           │
│          │                │                │                   │
│          ▼                ▼                ▼                   │
│    ✅ Matches       ✅ Matches       ✅ Matches              │
│   (type=email)     (priority=high)   (region=US)              │
└─────────────────────────────────────────────────────────────────┘
```

---

### **💀 Dead Letter Exchanges**

#### **DLX Setup и Configuration**
```java
// DeadLetterExchangeSetup.java
public class DeadLetterExchangeSetup {
    
    public static void setupDLX() throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        
        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {
            
            // Main exchange and queue
            channel.exchangeDeclare("orders_exchange", "direct");
            
            Map<String, Object> mainQueueArgs = new HashMap<>();
            mainQueueArgs.put("x-dead-letter-exchange", "orders_dlx");
            mainQueueArgs.put("x-dead-letter-routing-key", "failed");
            mainQueueArgs.put("x-message-ttl", 300000); // 5 minutes TTL
            mainQueueArgs.put("x-max-retries", 3);
            
            channel.queueDeclare("orders_queue", true, false, false, mainQueueArgs);
            channel.queueBind("orders_queue", "orders_exchange", "new");
            
            // Dead Letter Exchange and Queue
            channel.exchangeDeclare("orders_dlx", "direct");
            channel.queueDeclare("orders_dlq", true, false, false, null);
            channel.queueBind("orders_dlq", "orders_dlx", "failed");
            
            // Retry mechanism setup
            setupRetryMechanism(channel);
        }
    }
    
    private static void setupRetryMechanism(Channel channel) throws Exception {
        // Retry queue with TTL
        Map<String, Object> retryQueueArgs = new HashMap<>();
        retryQueueArgs.put("x-message-ttl", 60000); // 1 minute delay
        retryQueueArgs.put("x-dead-letter-exchange", "orders_exchange");
        retryQueueArgs.put("x-dead-letter-routing-key", "retry");
        
        channel.queueDeclare("orders_retry_queue", true, false, false, retryQueueArgs);
        channel.queueBind("orders_retry_queue", "orders_dlx", "retry");
    }
}
```

#### **DLX Message Flow**
```
┌─────────────────────────────────────────────────────────────────┐
│                    DEAD LETTER EXCHANGE FLOW                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. NORMAL PROCESSING:                                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──▶ orders_exchange ──▶ orders_queue ──▶ Consumer  ││
│  │                                      │                      ││
│  │                                      ▼                      ││
│  │                               ✅ Success                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  2. FAILURE SCENARIO:                                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Producer ──▶ orders_exchange ──▶ orders_queue ──▶ Consumer  ││
│  │                                      │              │       ││
│  │                                      │              ▼       ││
│  │                                      │          ❌ NACK     ││
│  │                                      │              │       ││
│  │                                      ▼              │       ││
│  │                              x-dead-letter-exchange │       ││
│  │                                      │              │       ││
│  │                                      ▼              │       ││
│  │                               orders_dlx ◀──────────┘       ││
│  │                                      │                      ││
│  │                                      ▼                      ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │ RETRY LOGIC:                                            │││
│  │  │ ┌─────────────┐ TTL ┌─────────────┐ retry ┌──────────┐ │││
│  │  │ │retry_queue  │────▶│orders_exchange│────▶│main_queue│ │││
│  │  │ └─────────────┘     └─────────────┘     └──────────┘ │││
│  │  │                                                       │││
│  │  │ IF still fails after 3 retries:                      │││
│  │  │ ┌─────────────┐                                       │││
│  │  │ │  DLQ        │ ◀── Permanent failure storage        │││
│  │  │ │ (manual     │                                       │││
│  │  │ │ review)     │                                       │││
│  │  │ └─────────────┘                                       │││
│  │  └─────────────────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

### **⏰ Message TTL и Queue Length Limits**

#### **TTL и Priority Queues**
```java
// TTLAndPriorityQueues.java
public class TTLAndPriorityQueues {
    
    public static void setupPriorityQueueWithTTL() throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        
        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {
            
            // Priority queue с TTL
            Map<String, Object> queueArgs = new HashMap<>();
            queueArgs.put("x-max-priority", 10);           // Priority levels 0-10
            queueArgs.put("x-message-ttl", 3600000);       // 1 hour TTL
            queueArgs.put("x-max-length", 10000);          // Max 10K messages
            queueArgs.put("x-max-length-bytes", 10485760); // Max 10MB
            queueArgs.put("x-overflow", "reject-publish"); // Reject when full
            
            channel.queueDeclare("priority_queue", true, false, false, queueArgs);
            
            // Publish message с priority
            publishPriorityMessage(channel, "High priority task", 8);
            publishPriorityMessage(channel, "Medium priority task", 5);
            publishPriorityMessage(channel, "Low priority task", 2);
        }
    }
    
    private static void publishPriorityMessage(Channel channel, String message, int priority) 
            throws Exception {
        
        AMQP.BasicProperties props = new AMQP.BasicProperties.Builder()
            .priority(priority)
            .expiration("300000") // 5 minutes per-message TTL
            .timestamp(new Date())
            .build();
        
        channel.basicPublish("", "priority_queue", props, message.getBytes());
        System.out.println("Published: " + message + " (priority: " + priority + ")");
    }
}
```

#### **Queue Length Management**
```
┌─────────────────────────────────────────────────────────────────┐
│                   QUEUE LENGTH MANAGEMENT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  OVERFLOW BEHAVIORS:                                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ DROP-HEAD (x-overflow: "drop-head"):                       ││
│  │                                                             ││
│  │ Queue: [msg1][msg2][msg3][msg4][msg5] ← maxlength=5        ││
│  │ New msg arrives: [msg6]                                     ││
│  │ Result: [msg2][msg3][msg4][msg5][msg6] (msg1 dropped)      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ REJECT-PUBLISH (x-overflow: "reject-publish"):             ││
│  │                                                             ││
│  │ Queue: [msg1][msg2][msg3][msg4][msg5] ← maxlength=5        ││
│  │ New msg arrives: [msg6]                                     ││
│  │ Result: [msg1][msg2][msg3][msg4][msg5] (msg6 rejected)     ││
│  │ Publisher receives: basic.nack                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ REJECT-PUBLISH-DLX (with dead letter exchange):            ││
│  │                                                             ││
│  │ Queue: [msg1][msg2][msg3][msg4][msg5] ← maxlength=5        ││
│  │ New msg arrives: [msg6]                                     ││
│  │ Result: [msg1][msg2][msg3][msg4][msg5]                     ││
│  │ msg6 ──▶ Dead Letter Exchange                              ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

### **🔌 RabbitMQ Plugins**

#### **Management Plugin Features**
```bash
# Enable management plugin
rabbitmq-plugins enable rabbitmq_management

# Access web interface at http://localhost:15672
# Default credentials: guest/guest
```

#### **Useful Plugins Setup**
```bash
# Federation plugin для multi-datacenter
rabbitmq-plugins enable rabbitmq_federation
rabbitmq-plugins enable rabbitmq_federation_management

# Shovel plugin для message transfer
rabbitmq-plugins enable rabbitmq_shovel
rabbitmq-plugins enable rabbitmq_shovel_management

# MQTT plugin для IoT devices
rabbitmq-plugins enable rabbitmq_mqtt

# STOMP plugin для web applications
rabbitmq-plugins enable rabbitmq_stomp
rabbitmq-plugins enable rabbitmq_web_stomp

# Delayed message plugin
# Download from: https://github.com/rabbitmq/rabbitmq-delayed-message-exchange
rabbitmq-plugins enable rabbitmq_delayed_message_exchange
```

#### **Federation Configuration**
```bash
# Setup federation link
rabbitmqctl set_parameter federation-upstream datacenter2 \
  '{"uri":"amqp://guest:guest@rabbit2.datacenter2.com","expires":3600000}'

# Create federated exchange
rabbitmqctl set_policy federate-exchanges "^federated\." \
  '{"federation-upstream-set":"all"}'
```

---

## 📦 **ГЛАВА 3.4: СЕРИАЛИЗАЦИЯ И ФОРМАТЫ ДАННЫХ**

### **🔄 JSON vs Avro vs Protocol Buffers**

#### **Format Comparison**
```
┌─────────────────────────────────────────────────────────────────┐
│                    SERIALIZATION FORMATS COMPARISON            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────┬──────────┬──────────┬──────────┬──────────────┐ │
│ │ Aspect      │   JSON   │   Avro   │ Protocol │  MessagePack │ │
│ │             │          │          │ Buffers  │              │ │
│ ├─────────────┼──────────┼──────────┼──────────┼──────────────┤ │
│ │ Size        │    ❌     │    ✅     │    ✅     │      ✅       │ │
│ │             │  Largest │ Compact  │ Smallest │   Compact    │ │
│ ├─────────────┼──────────┼──────────┼──────────┼──────────────┤ │
│ │ Speed       │    ❌     │    ✅     │    ✅     │      ✅       │ │
│ │             │   Slow   │   Fast   │ Fastest  │     Fast     │ │
│ ├─────────────┼──────────┼──────────┼──────────┼──────────────┤ │
│ │ Schema      │    ❌     │    ✅     │    ✅     │      ❌       │ │
│ │ Evolution   │   None   │ Advanced │ Limited  │    None      │ │
│ ├─────────────┼──────────┼──────────┼──────────┼──────────────┤ │
│ │ Human       │    ✅     │    ❌     │    ❌     │      ❌       │ │
│ │ Readable    │  Perfect │   None   │   None   │    None      │ │
│ ├─────────────┼──────────┼──────────┼──────────┼──────────────┤ │
│ │ Language    │    ✅     │    ✅     │    ✅     │      ✅       │ │
│ │ Support     │ Universal│   Good   │   Good   │    Good      │ │
│ └─────────────┴──────────┴──────────┴──────────┴──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

#### **Size Comparison Example**
```json
// JSON (151 bytes)
{
  "id": 12345,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "active": true,
  "created_at": "2024-01-15T10:30:00Z"
}

// Avro (Binary, ~40 bytes)
// Schema defined separately, data is just binary values

// Protocol Buffers (~35 bytes)
// Schema compiled into code, most compact binary format

// MessagePack (~42 bytes)
// JSON-like but binary, good middle ground
```

---

### **🔧 Avro Schema Evolution**

#### **Schema Evolution Examples**
```json
// Original Schema (v1)
{
  "type": "record",
  "name": "User",
  "namespace": "com.company.user",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"}
  ]
}

// Evolution v2 - Adding optional field (BACKWARD compatible)
{
  "type": "record",
  "name": "User",
  "namespace": "com.company.user",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "phone", "type": ["null", "string"], "default": null}
  ]
}

// Evolution v3 - Adding field with default (BACKWARD compatible)
{
  "type": "record",
  "name": "User",
  "namespace": "com.company.user",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "phone", "type": ["null", "string"], "default": null},
    {"name": "status", "type": "string", "default": "active"}
  ]
}
```

#### **Schema Evolution Patterns**
```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEMA EVOLUTION PATTERNS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BACKWARD COMPATIBILITY:                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ New Schema ──can read──▶ Old Data                          ││
│  │                                                             ││
│  │ Producer (old) ──v1 data──▶ Consumer (new)                 ││
│  │                                                             ││
│  │ ✅ Add optional fields with defaults                       ││
│  │ ✅ Remove fields                                            ││
│  │ ❌ Add required fields                                      ││
│  │ ❌ Change field types                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  FORWARD COMPATIBILITY:                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Old Schema ──can read──▶ New Data                          ││
│  │                                                             ││
│  │ Producer (new) ──v2 data──▶ Consumer (old)                 ││
│  │                                                             ││
│  │ ✅ Add fields                                               ││
│  │ ✅ Remove optional fields                                   ││
│  │ ❌ Remove required fields                                   ││
│  │ ❌ Change field types                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  FULL COMPATIBILITY:                                            │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Both directions work (BACKWARD + FORWARD)                   ││
│  │                                                             ││
│  │ ✅ Add/remove optional fields with defaults only           ││
│  │ ❌ Any other changes                                        ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘