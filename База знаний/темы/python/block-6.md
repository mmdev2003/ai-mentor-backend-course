# 🚀 Блок 6: Специализированные области Python

---

## 📋 Обзор блока

**⏱ Продолжительность:** 8-12 недель  
**🎯 Цель:** Получить экспертные знания в выбранной области применения Python  
**📊 Формат:** Теория + практика + специализированные проекты

---

## 🎯 Выбор специализации

```
┌─────────────────────────────────────────────────────────────────┐
│                    ВЫБЕРИТЕ СВОЙ ТРЕК                          │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   📊 DATA       │   🛠 DEVOPS     │   🎮 GAMEDEV    │ 🖥 DESKTOP│
│   SCIENCE       │                 │                 │           │
│                 │                 │                 │           │
│ • ML/AI         │ • Автоматизация │ • Pygame        │ • GUI     │
│ • Анализ данных │ • Облака        │ • Архитектура   │ • Системы │
│ • Визуализация  │ • CI/CD         │ • AI для игр    │ • Кросс-  │
│ • BigData       │ • Мониторинг    │ • Мультиплеер   │ платформа │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

---

# 📊 DATA SCIENCE ТРЕК

---

## 📈 6.1 Продвинутый анализ данных

### 🔍 Pandas: Продвинутые техники

#### Многоуровневые индексы (MultiIndex)
```python
# Создание MultiIndex
import pandas as pd
import numpy as np

# Создаем данные с многоуровневым индексом
arrays = [
    ['Москва', 'Москва', 'СПб', 'СПб'],
    ['2023', '2024', '2023', '2024']
]
index = pd.MultiIndex.from_arrays(arrays, names=['Город', 'Год'])
df = pd.DataFrame({'Продажи': [100, 120, 80, 95]}, index=index)

# Операции с MultiIndex
df.loc['Москва']  # Выбор по первому уровню
df.xs('2023', level='Год')  # Выбор по второму уровню
```

#### Операции с группировкой
```python
# Продвинутая группировка
grouped = df.groupby(['region', 'product'])
result = grouped.agg({
    'sales': ['sum', 'mean', 'std'],
    'profit': 'max',
    'customers': 'count'
})

# Применение функций к группам
def custom_metric(group):
    return group['profit'].sum() / group['sales'].sum()

metrics = df.groupby('category').apply(custom_metric)
```

---

### 📅 Обработка временных рядов

#### Работа с датами
```python
# Создание временного индекса
dates = pd.date_range('2023-01-01', periods=365, freq='D')
ts = pd.Series(np.random.randn(365), index=dates)

# Ресемплинг данных
monthly = ts.resample('M').mean()  # По месяцам
weekly = ts.resample('W').sum()    # По неделям

# Скользящие окна
rolling_mean = ts.rolling(window=30).mean()
expanding_mean = ts.expanding().mean()
```

#### Анализ сезонности
```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Декомпозиция временного ряда
decomposition = seasonal_decompose(ts, model='additive', period=365)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid
```

---

### 📊 Статистический анализ с SciPy

#### Проверка гипотез
```python
from scipy import stats

# t-тест для двух выборок
group1 = np.random.normal(10, 2, 100)
group2 = np.random.normal(12, 2, 100)
t_stat, p_value = stats.ttest_ind(group1, group2)

# Критерий Шапиро-Уилка для нормальности
shapiro_stat, shapiro_p = stats.shapiro(group1)

# Корреляционный анализ
correlation, p_val = stats.pearsonr(x, y)
```

#### ANOVA и другие тесты
```python
# Однофакторный дисперсионный анализ
f_stat, p_value = stats.f_oneway(group1, group2, group3)

# Критерий Краскела-Уоллиса (непараметрический)
h_stat, p_value = stats.kruskal(group1, group2, group3)

# Критерий хи-квадрат
chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
```

---

### 🧪 A/B тестирование

#### Планирование эксперимента
```python
def calculate_sample_size(p1, p2, alpha=0.05, power=0.8):
    """Расчет размера выборки для A/B теста"""
    effect_size = abs(p1 - p2)
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    pooled_p = (p1 + p2) / 2
    variance = 2 * pooled_p * (1 - pooled_p)
    
    n = ((z_alpha + z_beta) ** 2 * variance) / (effect_size ** 2)
    return int(np.ceil(n))

# Пример использования
sample_size = calculate_sample_size(0.10, 0.12)  # 10% vs 12% конверсия
```

#### Анализ результатов
```python
def ab_test_analysis(control, treatment):
    """Анализ A/B теста"""
    n_control = len(control)
    n_treatment = len(treatment)
    
    p_control = control.mean()
    p_treatment = treatment.mean()
    
    # Объединенная пропорция
    p_pooled = (control.sum() + treatment.sum()) / (n_control + n_treatment)
    
    # Стандартная ошибка
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_control + 1/n_treatment))
    
    # Z-статистика
    z = (p_treatment - p_control) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    return {
        'conversion_control': p_control,
        'conversion_treatment': p_treatment,
        'lift': (p_treatment - p_control) / p_control,
        'z_score': z,
        'p_value': p_value,
        'significant': p_value < 0.05
    }
```

---

### 💾 Работа с большими данными (Dask)

#### Основы Dask
```python
import dask.dataframe as dd

# Чтение больших файлов
df = dd.read_csv('large_file_*.csv')

# Ленивые вычисления
result = df.groupby('category').sales.sum()
computed_result = result.compute()  # Выполнение вычислений

# Параллельная обработка
df_processed = df.map_partitions(lambda x: x[x.sales > 1000])
```

---

## 🤖 6.2 Машинное обучение

### 🔧 Scikit-learn: Классификация и регрессия

#### Подготовка данных
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Нормализация
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Обработка пропусков
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train_scaled)
```

#### Модели классификации
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

# Создание пайплайна
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Обучение и предсказание
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
probabilities = pipeline.predict_proba(X_test)
```

---

### 📊 Оценка качества моделей

#### Метрики для классификации
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

# Основные метрики
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average='weighted')
recall = recall_score(y_test, predictions, average='weighted')
f1 = f1_score(y_test, predictions, average='weighted')

# ROC-AUC для бинарной классификации
if len(np.unique(y)) == 2:
    auc = roc_auc_score(y_test, probabilities[:, 1])

# Матрица ошибок
cm = confusion_matrix(y_test, predictions)
```

#### Визуализация результатов
```python
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve

# ROC кривая
fpr, tpr, _ = roc_curve(y_test, probabilities[:, 1])
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

---

### 🎛 Feature Engineering

#### Создание признаков
```python
# Полиномиальные признаки
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Биннинг непрерывных переменных
from sklearn.preprocessing import KBinsDiscretizer

discretizer = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='quantile')
X_binned = discretizer.fit_transform(X[['continuous_feature']])

# Кодирование категориальных переменных
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
X_encoded = encoder.fit_transform(X[['category']])
```

#### Отбор признаков
```python
from sklearn.feature_selection import (
    SelectKBest, f_classif, RFE, SelectFromModel
)

# Univariate Feature Selection
selector = SelectKBest(score_func=f_classif, k=10)
X_selected = selector.fit_transform(X, y)

# Recursive Feature Elimination
rfe = RFE(estimator=RandomForestClassifier(), n_features_to_select=10)
X_rfe = rfe.fit_transform(X, y)

# Feature importance от модели
sfm = SelectFromModel(RandomForestClassifier(), threshold='mean')
X_important = sfm.fit_transform(X, y)
```

---

### 🔄 Кросс-валидация и гиперпараметры

#### Стратегии валидации
```python
from sklearn.model_selection import (
    cross_val_score, StratifiedKFold, TimeSeriesSplit
)

# Обычная кросс-валидация
cv_scores = cross_val_score(
    pipeline, X, y, cv=5, scoring='accuracy'
)

# Стратифицированная для несбалансированных классов
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipeline, X, y, cv=skf)

# Для временных рядов
tscv = TimeSeriesSplit(n_splits=5)
cv_scores = cross_val_score(pipeline, X, y, cv=tscv)
```

#### Подбор гиперпараметров
```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

# Grid Search
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [3, 5, 7, None],
    'classifier__min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1
)
grid_search.fit(X_train, y_train)

# Random Search (более эффективный)
from scipy.stats import randint

param_dist = {
    'classifier__n_estimators': randint(50, 500),
    'classifier__max_depth': [3, 5, 7, 10, None],
    'classifier__min_samples_split': randint(2, 20)
}

random_search = RandomizedSearchCV(
    pipeline, param_dist, n_iter=100, cv=5, n_jobs=-1
)
random_search.fit(X_train, y_train)
```

---

### 🎯 Ансамблевые методы

#### Voting и Stacking
```python
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import StackingClassifier

# Voting Classifier
clf1 = LogisticRegression()
clf2 = RandomForestClassifier()
clf3 = SVC(probability=True)

voting_clf = VotingClassifier(
    estimators=[('lr', clf1), ('rf', clf2), ('svc', clf3)],
    voting='soft'  # 'hard' для мажоритарного голосования
)

# Stacking Classifier
stacking_clf = StackingClassifier(
    estimators=[('lr', clf1), ('rf', clf2), ('svc', clf3)],
    final_estimator=LogisticRegression(),
    cv=5
)
```

#### Blending
```python
def create_blend_predictions(models, X_blend, X_test):
    """Создание blend предсказаний"""
    blend_train = np.zeros((X_blend.shape[0], len(models)))
    blend_test = np.zeros((X_test.shape[0], len(models)))
    
    for i, model in enumerate(models):
        blend_train[:, i] = model.predict_proba(X_blend)[:, 1]
        blend_test[:, i] = model.predict_proba(X_test)[:, 1]
    
    return blend_train, blend_test

# Использование
blend_train, blend_test = create_blend_predictions(
    [clf1, clf2, clf3], X_blend, X_test
)

# Мета-модель
meta_model = LogisticRegression()
meta_model.fit(blend_train, y_blend)
final_predictions = meta_model.predict(blend_test)
```

---

## 🧠 6.3 Глубокое обучение

### 🔥 TensorFlow и Keras

#### Создание нейронной сети
```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization

# Простая полносвязная сеть
model = Sequential([
    Dense(128, activation='relu', input_shape=(input_dim,)),
    BatchNormalization(),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(num_classes, activation='softmax')
])

# Компиляция модели
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Обучение
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=100,
    batch_size=32,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(patience=10),
        tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
    ]
)
```

#### Кастомные слои и функции потерь
```python
class CustomLayer(tf.keras.layers.Layer):
    def __init__(self, units=32):
        super(CustomLayer, self).__init__()
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer='random_normal',
            trainable=True
        )
        self.b = self.add_weight(
            shape=(self.units,),
            initializer='zeros',
            trainable=True
        )

    def call(self, inputs):
        return tf.matmul(inputs, self.w) + self.b

# Кастомная функция потерь
def custom_loss(y_true, y_pred):
    """Focal Loss для несбалансированных данных"""
    alpha = 0.25
    gamma = 2.0
    
    ce_loss = tf.keras.losses.categorical_crossentropy(y_true, y_pred)
    p_t = tf.exp(-ce_loss)
    focal_loss = alpha * (1 - p_t) ** gamma * ce_loss
    
    return focal_loss
```

---

### 🖼 CNN для компьютерного зрения

#### Архитектура CNN
```python
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten

# CNN для классификации изображений
cnn_model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

# Data Augmentation
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2
)

# Обучение с аугментацией
model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    validation_data=(X_val, y_val),
    epochs=50
)
```

#### Transfer Learning
```python
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import GlobalAveragePooling2D

# Загрузка предобученной модели
base_model = VGG16(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Заморозка базовых слоев
base_model.trainable = False

# Добавление классификатора
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

# Fine-tuning
base_model.trainable = True
for layer in base_model.layers[:-4]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(lr=0.0001/10),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

---

### 📝 RNN и LSTM для текста

#### Обработка текстовых данных
```python
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Токенизация
tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')
tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=100, padding='post')

# Создание word embeddings
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 100

embedding_matrix = np.zeros((vocab_size, embedding_dim))
# Загрузка предобученных embeddings (Word2Vec, GloVe)
```

#### LSTM для классификации текста
```python
from tensorflow.keras.layers import LSTM, Embedding, Bidirectional

# Модель для анализа тональности
text_model = Sequential([
    Embedding(vocab_size, embedding_dim, input_length=max_length),
    Bidirectional(LSTM(64, dropout=0.3, recurrent_dropout=0.3)),
    Dense(32, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

# Attention механизм
from tensorflow.keras.layers import Attention

class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self):
        super(AttentionLayer, self).__init__()

    def call(self, inputs):
        # inputs: (batch_size, time_steps, features)
        attention_weights = tf.nn.softmax(
            tf.reduce_sum(inputs, axis=-1, keepdims=True), axis=1
        )
        context_vector = tf.reduce_sum(
            inputs * attention_weights, axis=1
        )
        return context_vector
```

---

## 🔧 6.4 MLOps и продакшн ML

### 📦 Версионирование данных и моделей

#### DVC (Data Version Control)
```bash
# Инициализация DVC
dvc init

# Добавление данных под версионный контроль
dvc add data/raw_data.csv
git add data/raw_data.csv.dvc .gitignore
git commit -m "Add raw data"

# Создание пайплайна
dvc run -f prepare.dvc \
    -d data/raw_data.csv \
    -o data/processed_data.csv \
    python src/prepare.py

# Воспроизведение пайплайна
dvc repro
```

#### MLflow для экспериментов
```python
import mlflow
import mlflow.sklearn

# Логирование эксперимента
with mlflow.start_run():
    # Логирование параметров
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    
    # Обучение модели
    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)
    
    # Логирование метрик
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    
    # Сохранение модели
    mlflow.sklearn.log_model(model, "model")
```

---

### 🐳 Docker для ML проектов

#### Dockerfile для ML
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY src/ ./src/
COPY models/ ./models/

# Создание пользователя
RUN useradd -m mluser
USER mluser

EXPOSE 8000

CMD ["python", "src/api.py"]
```

#### Docker Compose для ML стека
```yaml
version: '3.8'

services:
  ml-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/models/model.pkl
    volumes:
      - ./models:/app/models
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: mldb
      POSTGRES_USER: mluser
      POSTGRES_PASSWORD: mlpass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

### 🚀 API для ML моделей

#### FastAPI для ML сервиса
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="ML Model API", version="1.0.0")

# Загрузка модели при старте
model = joblib.load("models/trained_model.pkl")
scaler = joblib.load("models/scaler.pkl")

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    probability: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # Предобработка
        features = np.array(request.features).reshape(1, -1)
        features_scaled = scaler.transform(features)
        
        # Предсказание
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0].max()
        
        return PredictionResponse(
            prediction=float(prediction),
            probability=float(probability)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/model/info")
async def model_info():
    return {
        "model_type": type(model).__name__,
        "features": model.n_features_in_
    }
```

---

### 📊 Мониторинг моделей

#### Мониторинг дрифта данных
```python
import numpy as np
from scipy import stats
from typing import Dict, Any

class DataDriftDetector:
    def __init__(self, reference_data: np.ndarray):
        self.reference_data = reference_data
        self.reference_stats = self._calculate_stats(reference_data)
    
    def _calculate_stats(self, data: np.ndarray) -> Dict[str, Any]:
        return {
            'mean': np.mean(data, axis=0),
            'std': np.std(data, axis=0),
            'min': np.min(data, axis=0),
            'max': np.max(data, axis=0)
        }
    
    def detect_drift(self, new_data: np.ndarray, threshold: float = 0.05) -> Dict[str, bool]:
        """Обнаружение дрифта с помощью KS-теста"""
        drift_detected = {}
        
        for i in range(new_data.shape[1]):
            ks_statistic, p_value = stats.ks_2samp(
                self.reference_data[:, i], 
                new_data[:, i]
            )
            drift_detected[f'feature_{i}'] = p_value < threshold
            
        return drift_detected
    
    def performance_degradation(self, predictions: np.ndarray, 
                              actuals: np.ndarray) -> float:
        """Мониторинг деградации производительности"""
        from sklearn.metrics import accuracy_score
        return accuracy_score(actuals, predictions)

# Использование
detector = DataDriftDetector(X_train)
drift_results = detector.detect_drift(X_new)
```

---

### 🔄 A/B тестирование моделей

#### Система A/B тестирования
```python
import hashlib
import random
from typing import Optional

class ModelABTester:
    def __init__(self, model_a, model_b, traffic_split: float = 0.5):
        self.model_a = model_a
        self.model_b = model_b
        self.traffic_split = traffic_split
        self.results = {'a': [], 'b': []}
    
    def get_model_assignment(self, user_id: str) -> str:
        """Детерминированное разделение пользователей"""
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        return 'a' if (hash_value % 100) < (self.traffic_split * 100) else 'b'
    
    def predict(self, user_id: str, features: np.ndarray):
        """Предсказание с учетом A/B теста"""
        assignment = self.get_model_assignment(user_id)
        
        if assignment == 'a':
            prediction = self.model_a.predict(features)
            self.results['a'].append({
                'user_id': user_id,
                'prediction': prediction,
                'timestamp': pd.Timestamp.now()
            })
        else:
            prediction = self.model_b.predict(features)
            self.results['b'].append({
                'user_id': user_id,
                'prediction': prediction,
                'timestamp': pd.Timestamp.now()
            })
        
        return prediction, assignment
    
    def analyze_results(self):
        """Анализ результатов A/B теста"""
        metrics_a = self._calculate_metrics(self.results['a'])
        metrics_b = self._calculate_metrics(self.results['b'])
        
        return {
            'model_a': metrics_a,
            'model_b': metrics_b,
            'statistical_significance': self._statistical_test(
                self.results['a'], self.results['b']
            )
        }
```

---

## 🎯 Итоговые проекты Data Science трека

### 1. 🏭 Полный ML пайплайн: Прогнозирование оттока клиентов

```
┌─────────────────────────────────────────────────────────────────┐
│                    АРХИТЕКТУРА ПРОЕКТА                         │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   📊 DATA       │   🤖 MODEL      │   🚀 DEPLOY     │ 📈 MONITOR│
│   PIPELINE      │   TRAINING      │                 │           │
│                 │                 │                 │           │
│ • ETL процессы  │ • Feature Eng   │ • FastAPI       │ • Drift   │
│ • Валидация     │ • AutoML        │ • Docker        │ • A/B     │
│ • Версионир.    │ • Гиперпарам.   │ • Kubernetes    │ • Alerts  │
│ • Качество      │ • Ансамбли     │ • CI/CD         │ • Дашборд │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

#### Структура проекта
```
churn_prediction/
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── src/
│   ├── data/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── validate.py
│   ├── models/
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── evaluate.py
│   ├── api/
│   │   ├── main.py
│   │   └── schemas.py
│   └── monitoring/
│       ├── drift.py
│       └── performance.py
├── tests/
├── configs/
├── notebooks/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── dvc.yaml
```

---

# 🎯 Заключение блока

## 📊 Критерии оценки экспертного уровня

```
┌─────────────────────────────────────────────────────────────────┐
│                    НАВЫКИ ЭКСПЕРТА                             │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   🧠 TECHNICAL  │   🏗 ARCHITECTURE│   👥 SOFT      │ 🚀 BUSINESS│
│                 │                 │                 │           │
│ • Алгоритмы     │ • Системный     │ • Коммуникация │ • ROI     │
│ • Математика    │   дизайн        │ • Менторство    │ • Продукт │
│ • Программир.   │ • Масштабир.    │ • Презентации  │ • Стратегия│
│ • Инструменты   │ • Надежность    │ • Тимворк       │ • Метрики │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

---

## 📚 Рекомендуемые ресурсы

### Книги
- **"Hands-On Machine Learning"** - Aurélien Géron
- **"The Elements of Statistical Learning"** - Hastie, Tibshirani, Friedman
- **"Deep Learning"** - Ian Goodfellow
- **"Building Machine Learning Pipelines"** - Hannes Hapke

### Курсы и платформы
- **Kaggle Learn** - бесплатные микрокурсы
- **Fast.ai** - практическое глубокое обучение
- **Coursera ML Specializations** - Andrew Ng
- **Papers With Code** - последние исследования

### Инструменты и библиотеки
- **MLflow** - управление экспериментами
- **DVC** - версионирование данных
- **Weights & Biases** - трекинг экспериментов
- **Optuna** - оптимизация гиперпараметров

---

## 🎯 Roadmap карьерного роста

```
Junior DS (0-2 года)     →  Middle DS (2-4 года)     →  Senior DS (4+ лет)
├─ Основы ML             ├─ Продвинутые алгоритмы   ├─ Архитектура систем
├─ Python/SQL            ├─ Feature Engineering     ├─ Техническое лидерство
├─ Pandas/Scikit-learn   ├─ Deep Learning          ├─ Бизнес-стратегия
└─ Jupyter notebooks     ├─ MLOps                  ├─ Исследования
                        └─ Продуктовое мышление    └─ Менторство команды
```

---

*Следующий материал: другие треки специализации (DevOps, GameDev, Desktop) 🚀*