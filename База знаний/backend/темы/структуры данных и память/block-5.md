# Блок 5: Специализированные структуры данных

**⏱️ Длительность:** 4-5 недель  
**🎯 Цель:** Освоить продвинутые структуры для специфических задач

---

## 📚 Введение в специализированные структуры

Специализированные структуры данных созданы для решения конкретных проблем, которые не могут быть эффективно решены стандартными структурами. Они часто используют специальные свойства данных или алгоритмические трюки для достижения лучшей производительности в специфических сценариях.

------

## 5.1 Структуры для работы со строками

### 🌳 Trie (Префиксное дерево)

**Концепция:** Дерево, где каждый узел представляет символ, а путь от корня до узла представляет префикс.

```
Визуализация Trie для слов: "cat", "car", "card", "care", "careful"

        root
         |
         c
         |
         a
         |
         r ——————— t*
         |         
    ┌────┼────┐   
    |    |    |   
    d*   e    *   
         |        
         ┌┴┐      
         | |      
         *  f     
            |     
            u     
            |     
            l     
            |     
            *     

* = конец слова
```

#### Реализация Trie на C++:

```cpp
class TrieNode {
public:
    std::unordered_map<char, TrieNode*> children;
    bool isEndOfWord;
    
    TrieNode() : isEndOfWord(false) {}
};

class Trie {
private:
    TrieNode* root;
    
public:
    Trie() {
        root = new TrieNode();
    }
    
    // Вставка слова O(m), где m - длина слова
    void insert(const std::string& word) {
        TrieNode* current = root;
        for (char ch : word) {
            if (current->children.find(ch) == current->children.end()) {
                current->children[ch] = new TrieNode();
            }
            current = current->children[ch];
        }
        current->isEndOfWord = true;
    }
    
    // Поиск слова O(m)
    bool search(const std::string& word) {
        TrieNode* current = root;
        for (char ch : word) {
            if (current->children.find(ch) == current->children.end()) {
                return false;
            }
            current = current->children[ch];
        }
        return current->isEndOfWord;
    }
    
    // Поиск слов с префиксом
    std::vector<std::string> wordsWithPrefix(const std::string& prefix) {
        TrieNode* current = root;
        
        // Переходим к узлу с префиксом
        for (char ch : prefix) {
            if (current->children.find(ch) == current->children.end()) {
                return {}; // Префикс не найден
            }
            current = current->children[ch];
        }
        
        std::vector<std::string> result;
        dfsCollect(current, prefix, result);
        return result;
    }
    
private:
    void dfsCollect(TrieNode* node, std::string currentWord, 
                   std::vector<std::string>& result) {
        if (node->isEndOfWord) {
            result.push_back(currentWord);
        }
        
        for (auto& [ch, child] : node->children) {
            dfsCollect(child, currentWord + ch, result);
        }
    }
};
```

#### Применения Trie:
- **Автодополнение** в поисковых системах
- **Проверка орфографии**
- **IP routing tables** в сетевом оборудовании
- **Сжатие данных** (используется в некоторых алгоритмах)

------

### 🌲 Суффиксные деревья и массивы

**Суффиксное дерево** - это сжатое trie всех суффиксов строки.

```
Для строки "banana$":
Суффиксы: banana$, anana$, nana$, ana$, na$, a$, $

Суффиксное дерево:
                root
         ┌───────┼───────────┐
         │       │           │
       banana$  a            $
                 │
            ┌────┼────┐
            │    │    │
           na$  nana$ $
                 │
                 $
```

#### Реализация суффиксного массива (более практичная альтернатива):

```cpp
class SuffixArray {
private:
    std::string text;
    std::vector<int> suffixArray;
    std::vector<int> lcp; // Longest Common Prefix
    
public:
    SuffixArray(const std::string& s) : text(s + "$") {
        buildSuffixArray();
        buildLCP();
    }
    
    void buildSuffixArray() {
        int n = text.length();
        std::vector<std::pair<std::string, int>> suffixes;
        
        for (int i = 0; i < n; i++) {
            suffixes.push_back({text.substr(i), i});
        }
        
        std::sort(suffixes.begin(), suffixes.end());
        
        suffixArray.resize(n);
        for (int i = 0; i < n; i++) {
            suffixArray[i] = suffixes[i].second;
        }
    }
    
    void buildLCP() {
        int n = text.length();
        lcp.resize(n - 1);
        
        for (int i = 0; i < n - 1; i++) {
            int pos1 = suffixArray[i];
            int pos2 = suffixArray[i + 1];
            
            int commonLength = 0;
            while (pos1 + commonLength < n && pos2 + commonLength < n &&
                   text[pos1 + commonLength] == text[pos2 + commonLength]) {
                commonLength++;
            }
            lcp[i] = commonLength;
        }
    }
    
    // Поиск паттерна O(m log n)
    std::vector<int> search(const std::string& pattern) {
        int left = 0, right = suffixArray.size() - 1;
        
        // Бинарный поиск первого вхождения
        while (left <= right) {
            int mid = (left + right) / 2;
            int pos = suffixArray[mid];
            
            if (text.substr(pos, pattern.length()) >= pattern) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        
        std::vector<int> result;
        int start = left;
        
        // Собираем все вхождения
        while (start < suffixArray.size()) {
            int pos = suffixArray[start];
            if (pos + pattern.length() <= text.length() &&
                text.substr(pos, pattern.length()) == pattern) {
                result.push_back(pos);
                start++;
            } else {
                break;
            }
        }
        
        return result;
    }
};
```

------

### 🔍 Автомат Ахо-Корасик

**Назначение:** Одновременный поиск множества паттернов в тексте за один проход.

```
Пример для паттернов: "he", "she", "his", "hers"

Автомат состояний:
     0 ——h——> 1 ——e——> 2* ——r——> 6 ——s——> 7*
     |        |       |               
     |        i       s               
     |        |       |               
     s        v       v               
     |        3*      5*              
     |                               
     h                               
     |                               
     v                               
     4 ——e——> 5*                     

* = финальное состояние
```

#### Реализация:

```cpp
class AhoCorasick {
private:
    struct Node {
        std::unordered_map<char, int> children;
        int failure;
        std::vector<int> output;
        
        Node() : failure(0) {}
    };
    
    std::vector<Node> trie;
    
public:
    AhoCorasick(const std::vector<std::string>& patterns) {
        buildTrie(patterns);
        buildFailureFunction();
        buildOutput();
    }
    
    void buildTrie(const std::vector<std::string>& patterns) {
        trie.push_back(Node()); // Корень
        
        for (int i = 0; i < patterns.size(); i++) {
            int current = 0;
            
            for (char ch : patterns[i]) {
                if (trie[current].children.find(ch) == 
                    trie[current].children.end()) {
                    trie[current].children[ch] = trie.size();
                    trie.push_back(Node());
                }
                current = trie[current].children[ch];
            }
            
            trie[current].output.push_back(i);
        }
    }
    
    void buildFailureFunction() {
        std::queue<int> queue;
        
        // Уровень 1
        for (auto& [ch, child] : trie[0].children) {
            queue.push(child);
        }
        
        while (!queue.empty()) {
            int current = queue.front();
            queue.pop();
            
            for (auto& [ch, child] : trie[current].children) {
                queue.push(child);
                
                int failure = trie[current].failure;
                
                while (failure != 0 && 
                       trie[failure].children.find(ch) == 
                       trie[failure].children.end()) {
                    failure = trie[failure].failure;
                }
                
                if (trie[failure].children.find(ch) != 
                    trie[failure].children.end() && 
                    trie[failure].children[ch] != child) {
                    failure = trie[failure].children[ch];
                }
                
                trie[child].failure = failure;
            }
        }
    }
    
    void buildOutput() {
        for (int i = 1; i < trie.size(); i++) {
            int failure = trie[i].failure;
            trie[i].output.insert(trie[i].output.end(),
                                 trie[failure].output.begin(),
                                 trie[failure].output.end());
        }
    }
    
    std::vector<std::pair<int, int>> search(const std::string& text) {
        std::vector<std::pair<int, int>> matches;
        int current = 0;
        
        for (int i = 0; i < text.length(); i++) {
            char ch = text[i];
            
            while (current != 0 && 
                   trie[current].children.find(ch) == 
                   trie[current].children.end()) {
                current = trie[current].failure;
            }
            
            if (trie[current].children.find(ch) != 
                trie[current].children.end()) {
                current = trie[current].children[ch];
            }
            
            for (int patternId : trie[current].output) {
                matches.push_back({i, patternId});
            }
        }
        
        return matches;
    }
};
```

------

## 5.2 Вероятностные структуры данных

### 🌸 Bloom Filter

**Принцип:** Компактная структура для проверки принадлежности элемента множеству с возможными ложноположительными ответами.

```
Bloom Filter схема:
Битовый массив размера m
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│0│1│1│0│1│0│0│1│1│0│
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
 0 1 2 3 4 5 6 7 8 9 10 11

k хеш-функций: h1, h2, ..., hk

Добавление элемента x:
- Вычисляем h1(x), h2(x), ..., hk(x)
- Устанавливаем биты в позициях h1(x), h2(x), ..., hk(x)

Проверка элемента x:
- Если все биты в позициях h1(x), h2(x), ..., hk(x) установлены → "возможно есть"
- Если хотя бы один бит не установлен → "точно нет"
```

#### Реализация:

```cpp
class BloomFilter {
private:
    std::vector<bool> bitArray;
    size_t size;
    size_t numHashes;
    size_t numElements;
    
    // Простые хеш-функции
    std::vector<std::function<size_t(const std::string&)>> hashFunctions;
    
public:
    BloomFilter(size_t expectedElements, double falsePositiveRate) {
        // Оптимальные параметры
        size = -(expectedElements * log(falsePositiveRate)) / (log(2) * log(2));
        numHashes = (size * log(2)) / expectedElements;
        numElements = 0;
        
        bitArray.resize(size, false);
        
        // Создаем хеш-функции
        for (size_t i = 0; i < numHashes; i++) {
            hashFunctions.push_back([i](const std::string& str) {
                std::hash<std::string> hasher;
                return hasher(str + std::to_string(i));
            });
        }
    }
    
    void add(const std::string& element) {
        for (auto& hashFunc : hashFunctions) {
            size_t index = hashFunc(element) % size;
            bitArray[index] = true;
        }
        numElements++;
    }
    
    bool mightContain(const std::string& element) {
        for (auto& hashFunc : hashFunctions) {
            size_t index = hashFunc(element) % size;
            if (!bitArray[index]) {
                return false; // Точно нет
            }
        }
        return true; // Возможно есть
    }
    
    // Текущая вероятность ложных срабатываний
    double currentFalsePositiveRate() {
        double ratio = static_cast<double>(numElements) / size;
        return pow(1.0 - exp(-numHashes * ratio), numHashes);
    }
};
```

#### Применения:
- **Веб-кэши** (проверка, есть ли страница в кэше)
- **База данных** (проверка существования записи перед дисковым поиском)
- **Сетевые маршрутизаторы** (фильтрация пакетов)
- **Биоинформатика** (поиск k-меров в геномных последовательностях)

------

### 📊 Count-Min Sketch

**Назначение:** Оценка частоты появления элементов в потоке данных с ограниченной памятью.

```
Count-Min Sketch структура:
Матрица счетчиков d × w

h1: ┌───┬───┬───┬───┬───┬───┐
    │ 3 │ 1 │ 5 │ 2 │ 0 │ 4 │
    └───┴───┴───┴───┴───┴───┘

h2: ┌───┬───┬───┬───┬───┬───┐
    │ 2 │ 4 │ 1 │ 3 │ 2 │ 1 │
    └───┴───┴───┴───┴───┴───┘

h3: ┌───┬───┬───┬───┬───┬───┐
    │ 1 │ 2 │ 4 │ 1 │ 3 │ 2 │
    └───┴───┴───┴───┴───┴───┘

Добавление элемента x:
- Для каждой строки i: увеличиваем счетчик matrix[i][hi(x)]

Оценка частоты x:
- Возвращаем min(matrix[i][hi(x)]) по всем строкам i
```

#### Реализация:

```cpp
class CountMinSketch {
private:
    std::vector<std::vector<int>> matrix;
    std::vector<std::function<size_t(const std::string&)>> hashFunctions;
    size_t depth;
    size_t width;
    
public:
    CountMinSketch(double epsilon, double delta) {
        width = ceil(2.71828 / epsilon);  // e/ε
        depth = ceil(log(1.0 / delta));   // ln(1/δ)
        
        matrix.resize(depth, std::vector<int>(width, 0));
        
        // Создаем независимые хеш-функции
        for (size_t i = 0; i < depth; i++) {
            hashFunctions.push_back([i](const std::string& str) {
                std::hash<std::string> hasher;
                return hasher(str + "salt" + std::to_string(i));
            });
        }
    }
    
    void add(const std::string& element, int count = 1) {
        for (size_t i = 0; i < depth; i++) {
            size_t j = hashFunctions[i](element) % width;
            matrix[i][j] += count;
        }
    }
    
    int estimate(const std::string& element) {
        int minCount = INT_MAX;
        
        for (size_t i = 0; i < depth; i++) {
            size_t j = hashFunctions[i](element) % width;
            minCount = std::min(minCount, matrix[i][j]);
        }
        
        return minCount;
    }
    
    // Оценка общего количества элементов
    long long totalCount() {
        long long total = 0;
        for (int count : matrix[0]) {
            total += count;
        }
        return total;
    }
};
```

------

### 🎯 HyperLogLog

**Цель:** Приближенный подсчет количества уникальных элементов в большом потоке данных.

```
HyperLogLog принцип:
1. Хешируем элемент → получаем битовую строку
2. Считаем ведущие нули в двоичном представлении
3. Обновляем максимум для соответствующего "ведра"

Пример:
hash("apple") = 11010110...
                ^^
Ведущие нули: 0, поэтому ρ = 1

hash("banana") = 00110101...
                 ^^^
Ведущие нули: 2, поэтому ρ = 3

Ведра (buckets):
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 3 │ 0 │ 2 │ 1 │ 0 │ 4 │ 1 │
└───┴───┴───┴───┴───┴───┴───┴───┘
```

#### Реализация:

```cpp
class HyperLogLog {
private:
    std::vector<int> buckets;
    int b; // Количество бит для выбора ведра
    int m; // Количество ведер (2^b)
    double alpha; // Константа коррекции
    
    // Подсчет ведущих нулей
    int leadingZeros(uint64_t hash, int maxZeros) {
        int zeros = 0;
        for (int i = 0; i < maxZeros; i++) {
            if (hash & (1ULL << (63 - i))) {
                break;
            }
            zeros++;
        }
        return zeros + 1;
    }
    
    // Хеш-функция
    uint64_t hash(const std::string& str) {
        std::hash<std::string> hasher;
        return hasher(str);
    }
    
public:
    HyperLogLog(int precision) : b(precision), m(1 << precision) {
        buckets.resize(m, 0);
        
        // Константа коррекции α_m
        if (m >= 128) {
            alpha = 0.7213 / (1.0 + 1.079 / m);
        } else if (m >= 64) {
            alpha = 0.709;
        } else if (m >= 32) {
            alpha = 0.697;
        } else {
            alpha = 0.5;
        }
    }
    
    void add(const std::string& element) {
        uint64_t hashValue = hash(element);
        
        // Первые b бит определяют ведро
        int bucket = hashValue & ((1 << b) - 1);
        
        // Остальные биты используем для подсчета нулей
        uint64_t w = hashValue >> b;
        int zeros = leadingZeros(w, 64 - b);
        
        // Обновляем максимум для ведра
        buckets[bucket] = std::max(buckets[bucket], zeros);
    }
    
    double estimate() {
        double harmonicMean = 0.0;
        int zeroCount = 0;
        
        for (int bucket : buckets) {
            harmonicMean += 1.0 / (1 << bucket);
            if (bucket == 0) zeroCount++;
        }
        
        double estimate = alpha * m * m / harmonicMean;
        
        // Коррекция для малых значений
        if (estimate <= 2.5 * m && zeroCount > 0) {
            estimate = m * log(static_cast<double>(m) / zeroCount);
        }
        
        return estimate;
    }
    
    // Объединение с другим HLL
    void merge(const HyperLogLog& other) {
        if (m != other.m) {
            throw std::invalid_argument("Cannot merge HLLs with different precisions");
        }
        
        for (int i = 0; i < m; i++) {
            buckets[i] = std::max(buckets[i], other.buckets[i]);
        }
    }
};
```

------

### 🎲 Skip Lists

**Концепция:** Вероятностная структура данных, альтернатива сбалансированным деревьям.

```
Skip List структура (4 уровня):
Level 3: 1 ――――――――――――――――――――――――――――→ 17 ――→ NULL
Level 2: 1 ―――――――→ 6 ――――――――――――――――→ 17 ――→ NULL  
Level 1: 1 ―――→ 4 ―→ 6 ―――→ 9 ――――――――→ 17 ――→ NULL
Level 0: 1 → 3 → 4 → 6 → 7 → 9 → 12 → 17 → 19 → NULL

Поиск 12:
1. Начинаем с головы на максимальном уровне
2. Движемся вправо, пока следующий элемент ≤ искомого
3. Спускаемся на уровень ниже
4. Повторяем до нахождения элемента
```

#### Реализация:

```cpp
class SkipListNode {
public:
    int value;
    std::vector<SkipListNode*> forward;
    
    SkipListNode(int val, int level) : value(val) {
        forward.resize(level + 1, nullptr);
    }
};

class SkipList {
private:
    SkipListNode* header;
    int maxLevel;
    int currentLevel;
    double probability;
    std::random_device rd;
    std::mt19937 gen;
    std::uniform_real_distribution<> dis;
    
    int randomLevel() {
        int level = 0;
        while (dis(gen) < probability && level < maxLevel) {
            level++;
        }
        return level;
    }
    
public:
    SkipList(int maxLvl = 16, double p = 0.5) 
        : maxLevel(maxLvl), currentLevel(0), probability(p), 
          gen(rd()), dis(0.0, 1.0) {
        header = new SkipListNode(-1, maxLevel);
    }
    
    void insert(int value) {
        std::vector<SkipListNode*> update(maxLevel + 1);
        SkipListNode* current = header;
        
        // Поиск позиции для вставки
        for (int i = currentLevel; i >= 0; i--) {
            while (current->forward[i] != nullptr && 
                   current->forward[i]->value < value) {
                current = current->forward[i];
            }
            update[i] = current;
        }
        
        current = current->forward[0];
        
        // Если элемент уже существует
        if (current != nullptr && current->value == value) {
            return;
        }
        
        // Создаем новый узел
        int newLevel = randomLevel();
        
        if (newLevel > currentLevel) {
            for (int i = currentLevel + 1; i <= newLevel; i++) {
                update[i] = header;
            }
            currentLevel = newLevel;
        }
        
        SkipListNode* newNode = new SkipListNode(value, newLevel);
        
        // Обновляем ссылки
        for (int i = 0; i <= newLevel; i++) {
            newNode->forward[i] = update[i]->forward[i];
            update[i]->forward[i] = newNode;
        }
    }
    
    bool search(int value) {
        SkipListNode* current = header;
        
        for (int i = currentLevel; i >= 0; i--) {
            while (current->forward[i] != nullptr && 
                   current->forward[i]->value < value) {
                current = current->forward[i];
            }
        }
        
        current = current->forward[0];
        return current != nullptr && current->value == value;
    }
    
    void remove(int value) {
        std::vector<SkipListNode*> update(maxLevel + 1);
        SkipListNode* current = header;
        
        for (int i = currentLevel; i >= 0; i--) {
            while (current->forward[i] != nullptr && 
                   current->forward[i]->value < value) {
                current = current->forward[i];
            }
            update[i] = current;
        }
        
        current = current->forward[0];
        
        if (current != nullptr && current->value == value) {
            for (int i = 0; i <= currentLevel; i++) {
                if (update[i]->forward[i] != current) {
                    break;
                }
                update[i]->forward[i] = current->forward[i];
            }
            
            delete current;
            
            // Обновляем уровень списка
            while (currentLevel > 0 && 
                   header->forward[currentLevel] == nullptr) {
                currentLevel--;
            }
        }
    }
    
    void display() {
        for (int i = currentLevel; i >= 0; i--) {
            std::cout << "Level " << i << ": ";
            SkipListNode* node = header->forward[i];
            while (node != nullptr) {
                std::cout << node->value << " ";
                node = node->forward[i];
            }
            std::cout << std::endl;
        }
    }
};
```

------

## 5.3 Persistent структуры данных

### 🔒 Immutable структуры и их преимущества

**Persistent структуры** сохраняют все предыдущие версии при модификации, используя **structural sharing** для эффективности.

```
Structural Sharing пример:
Исходный список: [1, 2, 3, 4]
Добавляем 0 в начало: [0, 1, 2, 3, 4]

Версия 1:     1 → 2 → 3 → 4 → NULL
               ↑
Версия 2: 0 ────┘

Обе версии разделяют узлы 1→2→3→4
```

#### Реализация Persistent Vector (упрощенная версия):

```cpp
class PersistentVector {
private:
    struct Node {
        std::vector<std::shared_ptr<Node>> children;
        std::vector<int> values;
        bool isLeaf;
        
        Node(bool leaf = false) : isLeaf(leaf) {
            if (isLeaf) {
                values.reserve(32);
            } else {
                children.reserve(32);
            }
        }
    };
    
    std::shared_ptr<Node> root;
    size_t size_;
    int height;
    
    static constexpr int BRANCHING_FACTOR = 32;
    static constexpr int SHIFT = 5; // log2(32)
    
public:
    PersistentVector() : root(std::make_shared<Node>(true)), size_(0), height(1) {}
    
    PersistentVector(std::shared_ptr<Node> r, size_t s, int h) 
        : root(r), size_(s), height(h) {}
    
    size_t size() const { return size_; }
    
    int get(size_t index) const {
        if (index >= size_) {
            throw std::out_of_range("Index out of range");
        }
        
        auto node = root;
        int level = height - 1;
        
        while (level > 0) {
            int childIndex = (index >> (level * SHIFT)) & (BRANCHING_FACTOR - 1);
            node = node->children[childIndex];
            level--;
        }
        
        int leafIndex = index & (BRANCHING_FACTOR - 1);
        return node->values[leafIndex];
    }
    
    PersistentVector push_back(int value) const {
        if (size_ == 0) {
            auto newRoot = std::make_shared<Node>(true);
            newRoot->values.push_back(value);
            return PersistentVector(newRoot, 1, 1);
        }
        
        // Если текущий лист заполнен, нужно расширить дерево
        if (size_ == (1ULL << (height * SHIFT))) {
            auto newRoot = std::make_shared<Node>(false);
            newRoot->children.push_back(root);
            
            auto newPath = createPath(height, value);
            newRoot->children.push_back(newPath);
            
            return PersistentVector(newRoot, size_ + 1, height + 1);
        }
        
        auto newRoot = insertIntoPath(root, height - 1, size_, value);
        return PersistentVector(newRoot, size_ + 1, height);
    }
    
private:
    std::shared_ptr<Node> createPath(int level, int value) const {
        if (level == 1) {
            auto leaf = std::make_shared<Node>(true);
            leaf->values.push_back(value);
            return leaf;
        }
        
        auto node = std::make_shared<Node>(false);
        node->children.push_back(createPath(level - 1, value));
        return node;
    }
    
    std::shared_ptr<Node> insertIntoPath(std::shared_ptr<Node> node, 
                                        int level, size_t index, int value) const {
        if (level == 0) {
            // Лист
            auto newNode = std::make_shared<Node>(true);
            newNode->values = node->values;
            newNode->values.push_back(value);
            return newNode;
        }
        
        auto newNode = std::make_shared<Node>(false);
        newNode->children = node->children;
        
        int childIndex = (index >> (level * SHIFT)) & (BRANCHING_FACTOR - 1);
        
        if (childIndex < newNode->children.size()) {
            newNode->children[childIndex] = 
                insertIntoPath(newNode->children[childIndex], 
                             level - 1, index, value);
        } else {
            newNode->children.push_back(createPath(level, value));
        }
        
        return newNode;
    }
};
```

### Применения Persistent структур:
- **Undo/Redo системы** в редакторах
- **Функциональное программирование** (Clojure, Haskell)
- **Базы данных** с версионированием
- **Concurrent программирование** (избежание блокировок)

------

## 5.4 Lock-free структуры

### ⚡ Compare-and-Swap (CAS) операции

**Атомарная операция:** Сравнить значение и заменить, если оно равно ожидаемому.

```cpp
// Псевдокод CAS
bool compare_and_swap(T* ptr, T expected, T new_value) {
    if (*ptr == expected) {
        *ptr = new_value;
        return true;
    }
    return false;
}
```

#### Lock-free Stack:

```cpp
template<typename T>
class LockFreeStack {
private:
    struct Node {
        T data;
        std::atomic<Node*> next;
        
        Node(const T& item) : data(item), next(nullptr) {}
    };
    
    std::atomic<Node*> head;
    
public:
    LockFreeStack() : head(nullptr) {}
    
    void push(const T& item) {
        Node* newNode = new Node(item);
        Node* currentHead;
        
        do {
            currentHead = head.load();
            newNode->next.store(currentHead);
        } while (!head.compare_exchange_weak(currentHead, newNode));
    }
    
    bool pop(T& result) {
        Node* currentHead;
        
        do {
            currentHead = head.load();
            if (currentHead == nullptr) {
                return false; // Стек пуст
            }
            
            result = currentHead->data;
        } while (!head.compare_exchange_weak(currentHead, 
                                           currentHead->next.load()));
        
        // Осторожно с удалением - может быть проблема ABA
        // В реальной реализации нужен hazard pointer или RCU
        delete currentHead;
        return true;
    }
    
    bool empty() const {
        return head.load() == nullptr;
    }
};
```

#### Lock-free Queue (Michael & Scott):

```cpp
template<typename T>
class LockFreeQueue {
private:
    struct Node {
        std::atomic<T*> data;
        std::atomic<Node*> next;
        
        Node() : data(nullptr), next(nullptr) {}
    };
    
    std::atomic<Node*> head;
    std::atomic<Node*> tail;
    
public:
    LockFreeQueue() {
        Node* dummy = new Node();
        head.store(dummy);
        tail.store(dummy);
    }
    
    void enqueue(const T& item) {
        Node* newNode = new Node();
        T* data = new T(std::move(item));
        newNode->data.store(data);
        
        while (true) {
            Node* last = tail.load();
            Node* next = last->next.load();
            
            if (last == tail.load()) { // Проверяем консистентность
                if (next == nullptr) {
                    // Попытка связать узел в конец списка
                    if (last->next.compare_exchange_weak(next, newNode)) {
                        break; // Enqueue выполнен
                    }
                } else {
                    // Помогаем продвинуть tail
                    tail.compare_exchange_weak(last, next);
                }
            }
        }
        
        // Продвигаем tail к вставленному узлу
        tail.compare_exchange_weak(tail.load(), newNode);
    }
    
    bool dequeue(T& result) {
        while (true) {
            Node* first = head.load();
            Node* last = tail.load();
            Node* next = first->next.load();
            
            if (first == head.load()) { // Проверяем консистентность
                if (first == last) {
                    if (next == nullptr) {
                        return false; // Очередь пуста
                    }
                    // Помогаем продвинуть tail
                    tail.compare_exchange_weak(last, next);
                } else {
                    // Читаем данные перед CAS
                    if (next == nullptr) {
                        continue; // Другой поток помог
                    }
                    
                    T* data = next->data.load();
                    if (data == nullptr) {
                        continue;
                    }
                    
                    // Попытка продвинуть head к следующему узлу
                    if (head.compare_exchange_weak(first, next)) {
                        result = *data;
                        delete data;
                        delete first;
                        return true;
                    }
                }
            }
        }
    }
};
```

### 🚧 Memory Ordering и барьеры

```cpp
// Различные типы memory ordering:

std::atomic<int> x{0}, y{0};

// Sequential consistency (по умолчанию)
x.store(1, std::memory_order_seq_cst);
int a = y.load(std::memory_order_seq_cst);

// Acquire-Release semantics
x.store(1, std::memory_order_release);    // Все предыдущие операции видны
int b = y.load(std::memory_order_acquire); // Все последующие операции после этого

// Relaxed ordering (только атомарность)
x.store(1, std::memory_order_relaxed);
int c = y.load(std::memory_order_relaxed);
```

------

## 🔬 Практические задания

### Задание 1: Поисковая система с автодополнением
**Цель:** Создать систему, которая индексирует текстовые документы и предоставляет быстрое автодополнение.

```cpp
class SearchEngine {
private:
    Trie autocompleteIndex;
    std::unordered_map<std::string, std::vector<int>> invertedIndex;
    std::vector<std::string> documents;
    
public:
    void addDocument(int id, const std::string& content);
    std::vector<std::string> autocomplete(const std::string& prefix);
    std::vector<int> search(const std::string& query);
};
```

### Задание 2: Аналитическая система для больших данных
**Цель:** Реализовать систему для анализа потока событий в реальном времени.

```cpp
class RealTimeAnalytics {
private:
    CountMinSketch frequency;
    HyperLogLog uniqueUsers;
    BloomFilter seenEvents;
    
public:
    void processEvent(const std::string& userId, const std::string& event);
    int getEventFrequency(const std::string& event);
    double getUniqueUserCount();
    bool hasSeenEvent(const std::string& event);
};
```

### Задание 3: Многопоточный веб-сервер
**Цель:** Создать высокопроизводительный сервер с lock-free структурами.

```cpp
class HighPerformanceServer {
private:
    LockFreeQueue<Request> requestQueue;
    LockFreeStack<Response> responsePool;
    std::vector<std::thread> workers;
    
public:
    void start(int numWorkers);
    void handleRequest(const Request& req);
    void workerLoop();
};
```

------

## 📊 Сравнительная таблица структур

| Структура | Память | Поиск | Вставка | Особенности |
|-----------|--------|-------|---------|-------------|
| Trie | O(ALPHABET_SIZE × N) | O(m) | O(m) | Префиксные запросы |
| Suffix Array | O(n) | O(m log n) | - | Поиск подстрок |
| Bloom Filter | O(m) | O(k) | O(k) | Ложные срабатывания |
| Count-Min Sketch | O(d × w) | O(d) | O(d) | Приближенные частоты |
| HyperLogLog | O(m) | - | O(1) | Подсчет уникальных |
| Skip List | O(n) | O(log n) | O(log n) | Простота реализации |
| Persistent Vector | O(n) | O(log n) | O(log n) | Версионирование |
| Lock-free Stack | O(n) | - | O(1) | Многопоточность |

*где m - длина паттерна, n - размер данных, k - количество хеш-функций*

------

## 🎯 Ключевые выводы

1. **Специализированные структуры** решают конкретные проблемы эффективнее универсальных
2. **Вероятностные структуры** обменивают точность на эффективность памяти
3. **Persistent структуры** обеспечивают безопасность и версионирование
4. **Lock-free структуры** критичны для высокопроизводительных многопоточных приложений
5. **Выбор структуры** зависит от специфики задачи и требований производительности

------

## 📚 Дополнительные ресурсы

- **Статьи:** "The Art of Multiprocessor Programming" (Herlihy & Shavit)
- **Исследования:** Google's Bigtable, Amazon's Dynamo papers
- **Инструменты:** Intel Threading Building Blocks, Folly library
- **Бенчмарки:** Google Benchmark, Catch2 для тестирования

------

**Следующий блок:** Практическое применение в реальных системах 🚀