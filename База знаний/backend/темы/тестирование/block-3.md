# 🚀 Блок 3: Автоматизация тестирования
## От основ программирования до CI/CD

---

## 🎯 Цель блока
**Изучить принципы и инструменты автоматизации, научиться писать автотесты**

**Продолжительность**: 3-4 месяца  
**Уровень**: Intermediate → Advanced

---

## 📊 Прогресс обучения

```
Блок 1: Основы ████████████████████████████████████████ 100%
Блок 2: Практика ████████████████████████████████████████ 100%
Блок 3: Автоматизация ████████████████████████████████████████ [В ПРОЦЕССЕ]
Блок 4: Специализация ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%
```

---

## 🗓️ Глава 3.1: Основы программирования
### Временные рамки: 4 недели

#### 📋 Чек-лист изучения:
- [ ] Выбор языка программирования для автоматизации
- [ ] Изучение основ выбранного языка
- [ ] Понимание принципов ООП
- [ ] Работа с Git и системами контроля версий

---

### 🔧 Выбор языка программирования

```
┌─────────────────────────────────────────────────────┐
│                ПОПУЛЯРНЫЕ ЯЗЫКИ                     │
├─────────────────────────────────────────────────────┤
│  Python     │ ████████████████████████████ 85%     │
│  Java       │ ████████████████████████ 75%         │
│  JavaScript │ ████████████████████ 65%             │
│  C#         │ ████████████████ 55%                 │
│  Ruby       │ ████████ 25%                         │
└─────────────────────────────────────────────────────┘
```

#### 🐍 Python - Рекомендуемый выбор для новичков

**Преимущества:**
- Простой и читаемый синтаксис
- Огромное количество библиотек
- Активное сообщество
- Универсальность применения

**Недостатки:**
- Медленнее Java/C#
- Динамическая типизация может привести к ошибкам

---

### 📚 Основы Python для тестировщиков

#### Неделя 1: Базовый синтаксис
```python
# Переменные и типы данных
name = "QA Engineer"
age = 25
is_automation_expert = False

# Условия
if age >= 18:
    print("Можете работать тестировщиком!")
else:
    print("Учитесь дальше!")

# Циклы
test_cases = ["login", "logout", "search", "purchase"]
for test in test_cases:
    print(f"Выполняется тест: {test}")
```

#### Неделя 2: Структуры данных
```python
# Списки (для хранения тест-данных)
browsers = ["Chrome", "Firefox", "Safari", "Edge"]
test_results = [True, False, True, True]

# Словари (для конфигурации)
config = {
    "base_url": "https://example.com",
    "timeout": 30,
    "browser": "Chrome"
}

# Функции
def execute_test(test_name, expected_result):
    """Выполняет тест и возвращает результат"""
    print(f"Executing: {test_name}")
    return expected_result == True
```

#### Неделя 3: ООП для тестировщиков
```python
class TestCase:
    def __init__(self, name, priority="Medium"):
        self.name = name
        self.priority = priority
        self.status = "Not Run"
    
    def execute(self):
        """Выполняет тест-кейс"""
        self.status = "Running"
        # Логика выполнения теста
        self.status = "Passed"
        return True
    
    def get_result(self):
        return f"{self.name}: {self.status}"

# Использование
login_test = TestCase("User Login", "High")
login_test.execute()
print(login_test.get_result())
```

#### Неделя 4: Git и контроль версий
```bash
# Основные команды Git
git init                    # Инициализация репозитория
git add .                   # Добавление файлов в staging
git commit -m "Initial commit"  # Фиксация изменений
git push origin main        # Отправка на удаленный репозиторий

# Работа с ветками
git branch feature/new-tests    # Создание новой ветки
git checkout feature/new-tests  # Переключение на ветку
git merge feature/new-tests     # Слияние веток
```

---

### 🎯 Практическое задание Главы 3.1

**Создайте простой калькулятор с тестами:**

```python
# calculator.py
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Деление на ноль!")
        return a / b

# test_calculator.py
import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
```

---

## 🗓️ Глава 3.2: Введение в автоматизацию
### Временные рамки: 3 недели

---

### 🏗️ Пирамида тестирования

```
                    ┌─────────────────┐
                    │   UI Tests      │ ← Медленные, дорогие
                    │     (10%)       │   но важные
                    └─────────────────┘
                  ┌─────────────────────┐
                  │  Integration Tests  │ ← Средняя скорость
                  │      (20%)          │   и стоимость
                  └─────────────────────┘
            ┌─────────────────────────────────┐
            │        Unit Tests               │ ← Быстрые, дешевые
            │         (70%)                   │   много тестов
            └─────────────────────────────────┘
```

---

### 🤔 Что автоматизировать?

#### ✅ АВТОМАТИЗИРУЕМ:
- Регрессионные тесты
- Smoke тесты
- Повторяющиеся тесты
- Тесты с большим объемом данных
- Длительные тесты
- Тесты для нескольких браузеров/устройств

#### ❌ НЕ АВТОМАТИЗИРУЕМ:
- Исследовательские тесты
- Тесты юзабилити
- Одноразовые тесты
- Тесты с частыми изменениями UI
- Тесты, требующие человеческого восприятия

---

### 💰 ROI (Return on Investment) автоматизации

```
┌─────────────────────────────────────────────────────┐
│                 ФОРМУЛА ROI                         │
├─────────────────────────────────────────────────────┤
│  ROI = (Экономия - Затраты) / Затраты × 100%       │
│                                                     │
│  Экономия = Время_ручного_тестирования ×            │
│            Количество_запусков × Стоимость_часа     │
│                                                     │
│  Затраты = Время_написания_автотеста ×              │
│           Стоимость_часа + Поддержка                │
└─────────────────────────────────────────────────────┘
```

#### 📊 Пример расчета:
- **Ручной тест**: 2 часа × 50 запусков × $30/час = $3000
- **Автоматизация**: 8 часов × $30/час + $200 поддержка = $440
- **ROI**: ($3000 - $440) / $440 × 100% = **582%**

---

### 🏗️ Паттерны проектирования автотестов

#### 1. **Page Object Model (POM)**
```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-btn")
    
    def enter_username(self, username):
        element = self.driver.find_element(*self.username_field)
        element.clear()
        element.send_keys(username)
    
    def enter_password(self, password):
        element = self.driver.find_element(*self.password_field)
        element.clear()
        element.send_keys(password)
    
    def click_login(self):
        self.driver.find_element(*self.login_button).click()
```

#### 2. **Factory Pattern**
```python
class DriverFactory:
    @staticmethod
    def create_driver(browser_name):
        if browser_name.lower() == "chrome":
            return webdriver.Chrome()
        elif browser_name.lower() == "firefox":
            return webdriver.Firefox()
        elif browser_name.lower() == "safari":
            return webdriver.Safari()
        else:
            raise ValueError(f"Браузер {browser_name} не поддерживается")
```

---

## 🗓️ Глава 3.3: UI автоматизация
### Временные рамки: 5 недель

---

### 🌐 Selenium WebDriver: Основы

#### Архитектура Selenium
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Test Script   │◄──►│ Selenium WebDriver│◄──►│   Browser      │
│   (Python/Java) │    │                 │    │   (Chrome/FF)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Установка и настройка
```bash
# Установка Selenium
pip install selenium

# Установка драйвера (ChromeDriver)
pip install webdriver-manager
```

#### Первый автотест
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка драйвера
driver = webdriver.Chrome()

try:
    # Открытие страницы
    driver.get("https://example.com")
    
    # Поиск элемента и взаимодействие
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium testing")
    search_box.submit()
    
    # Ожидание результата
    wait = WebDriverWait(driver, 10)
    results = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
    )
    
    print("Тест пройден успешно!")
    
finally:
    driver.quit()
```

---

### 🎯 Локаторы: Стратегии поиска элементов

#### 1. **CSS Селекторы**
```python
# По ID
driver.find_element(By.CSS_SELECTOR, "#username")

# По классу
driver.find_element(By.CSS_SELECTOR, ".btn-primary")

# По атрибуту
driver.find_element(By.CSS_SELECTOR, "[data-testid='login-btn']")

# Комбинированные
driver.find_element(By.CSS_SELECTOR, "form.login-form input[type='email']")
```

#### 2. **XPath**
```python
# Простой XPath
driver.find_element(By.XPATH, "//input[@id='username']")

# XPath с текстом
driver.find_element(By.XPATH, "//button[text()='Login']")

# XPath с contains
driver.find_element(By.XPATH, "//div[contains(@class, 'error-message')]")

# Относительный XPath
driver.find_element(By.XPATH, "//form//input[@type='password']")
```

---

### ⏰ Ожидания и синхронизация

#### Типы ожиданий
```
┌─────────────────────────────────────────────────────┐
│              ТИПЫ ОЖИДАНИЙ                          │
├─────────────────────────────────────────────────────┤
│  Implicit Wait  │ Глобальное ожидание элементов     │
│  Explicit Wait  │ Ожидание конкретного условия      │
│  Fluent Wait    │ Гибкое ожидание с параметрами     │
└─────────────────────────────────────────────────────┘
```

#### Примеры использования
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Implicit Wait
driver.implicitly_wait(10)

# Explicit Wait
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, "submit-btn")))

# Fluent Wait
wait = WebDriverWait(driver, 10, poll_frequency=1)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result")))
```

---

### 🏗️ Page Object Model (POM) - Продвинутый уровень

#### Базовая структура проекта
```
tests/
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/
│   ├── __init__.py
│   ├── test_login.py
│   └── test_dashboard.py
├── utils/
│   ├── __init__.py
│   └── driver_factory.py
└── conftest.py
```

#### Базовая страница
```python
# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def wait_for_element_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def get_page_title(self):
        return self.driver.title
```

#### Страница логина
```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Локаторы
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-btn")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://example.com/login")
    
    def enter_username(self, username):
        element = self.wait_for_element_visible(self.USERNAME_INPUT)
        element.clear()
        element.send_keys(username)
        return self
    
    def enter_password(self, password):
        element = self.wait_for_element_visible(self.PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)
        return self
    
    def click_login(self):
        button = self.wait_for_element_clickable(self.LOGIN_BUTTON)
        button.click()
        return self
    
    def get_error_message(self):
        element = self.wait_for_element_visible(self.ERROR_MESSAGE)
        return element.text
    
    def login(self, username, password):
        """Метод для быстрого логина"""
        return (self.enter_username(username)
                   .enter_password(password)
                   .click_login())
```

---

### 🧪 Тестовые фреймворки

#### pytest - Рекомендуемый выбор
```python
# conftest.py
import pytest
from selenium import webdriver
from utils.driver_factory import DriverFactory

@pytest.fixture
def driver():
    driver = DriverFactory.create_driver("chrome")
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)
```

#### Тест с использованием pytest
```python
# tests/test_login.py
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLogin:
    def test_successful_login(self, driver):
        login_page = LoginPage(driver)
        login_page.login("valid_user", "valid_password")
        
        dashboard_page = DashboardPage(driver)
        assert dashboard_page.is_welcome_message_displayed()
    
    def test_invalid_credentials(self, driver):
        login_page = LoginPage(driver)
        login_page.login("invalid_user", "invalid_password")
        
        error_message = login_page.get_error_message()
        assert "Invalid credentials" in error_message
    
    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "password", "Username is required"),
        ("username", "", "Password is required"),
        ("", "", "Username is required")
    ])
    def test_validation_errors(self, driver, username, password, expected_error):
        login_page = LoginPage(driver)
        login_page.login(username, password)
        
        error_message = login_page.get_error_message()
        assert expected_error in error_message
```

---

## 🗓️ Глава 3.4: API тестирование
### Временные рамки: 4 недели

---

### 🌐 Основы HTTP протокола

#### HTTP методы
```
┌─────────────────────────────────────────────────────┐
│                 HTTP МЕТОДЫ                         │
├─────────────────────────────────────────────────────┤
│  GET     │ Получение данных                         │
│  POST    │ Создание новых данных                    │
│  PUT     │ Обновление данных (полное)               │
│  PATCH   │ Частичное обновление                     │
│  DELETE  │ Удаление данных                          │
└─────────────────────────────────────────────────────┘
```

#### Коды состояния HTTP
```
┌─────────────────────────────────────────────────────┐
│              КОДЫ СОСТОЯНИЯ                         │
├─────────────────────────────────────────────────────┤
│  200 OK           │ Успешный запрос                 │
│  201 Created      │ Ресурс создан                   │
│  400 Bad Request  │ Некорректный запрос             │
│  401 Unauthorized │ Нет авторизации                 │
│  404 Not Found    │ Ресурс не найден                │
│  500 Server Error │ Внутренняя ошибка сервера       │
└─────────────────────────────────────────────────────┘
```

---

### 🔧 Инструменты для API тестирования

#### Postman - Ручное тестирование
```javascript
// Pre-request Script
pm.globals.set("base_url", "https://api.example.com");
pm.globals.set("token", "your_auth_token");

// Test Script
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains user data", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('user');
    pm.expect(jsonData.user).to.have.property('id');
});
```

#### Python requests - Автоматизация
```python
import requests
import pytest

class TestUserAPI:
    BASE_URL = "https://api.example.com"
    
    @pytest.fixture
    def auth_headers(self):
        return {
            "Authorization": "Bearer your_token_here",
            "Content-Type": "application/json"
        }
    
    def test_get_user_success(self, auth_headers):
        response = requests.get(
            f"{self.BASE_URL}/users/123",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        user_data = response.json()
        assert "id" in user_data
        assert "name" in user_data
        assert user_data["id"] == 123
    
    def test_create_user_success(self, auth_headers):
        new_user = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        
        response = requests.post(
            f"{self.BASE_URL}/users",
            headers=auth_headers,
            json=new_user
        )
        
        assert response.status_code == 201
        created_user = response.json()
        assert created_user["name"] == new_user["name"]
        assert created_user["email"] == new_user["email"]
    
    def test_get_nonexistent_user(self, auth_headers):
        response = requests.get(
            f"{self.BASE_URL}/users/99999",
            headers=auth_headers
        )
        
        assert response.status_code == 404
```

---

### 🔐 Тестирование авторизации и безопасности

#### JWT Token тестирование
```python
import jwt
import time
import requests

class TestAuthentication:
    def test_valid_token_access(self):
        token = self.get_valid_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get("/protected-endpoint", headers=headers)
        assert response.status_code == 200
    
    def test_expired_token_rejection(self):
        expired_token = self.get_expired_token()
        headers = {"Authorization": f"Bearer {expired_token}"}
        
        response = requests.get("/protected-endpoint", headers=headers)
        assert response.status_code == 401
    
    def test_malformed_token_rejection(self):
        malformed_token = "invalid.token.here"
        headers = {"Authorization": f"Bearer {malformed_token}"}
        
        response = requests.get("/protected-endpoint", headers=headers)
        assert response.status_code == 401
    
    def test_sql_injection_protection(self):
        malicious_payload = "1' OR '1'='1"
        response = requests.get(f"/users/{malicious_payload}")
        
        # Должен вернуть 400 или 404, но не 200 с данными
        assert response.status_code in [400, 404]
```

---

## 🗓️ Глава 3.5: CI/CD для тестировщиков
### Временные рамки: 2 недели

---

### 🔄 Основы непрерывной интеграции

#### Схема CI/CD процесса
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Commit    │─►│   Build     │─►│    Test     │─►│   Deploy    │
│   Code      │  │   Code      │  │   Code      │  │   Code      │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
       ▲                                                     │
       │                                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Обратная связь                               │
│              (Уведомления, отчеты, логи)                       │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🛠️ GitHub Actions для автотестов

#### Конфигурация workflow
```yaml
# .github/workflows/tests.yml
name: Automated Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
        browser: [chrome, firefox]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --junitxml=unit-test-results.xml
    
    - name: Run API tests
      run: |
        pytest tests/api/ -v --junitxml=api-test-results.xml
    
    - name: Run UI tests
      run: |
        pytest tests/ui/ -v --junitxml=ui-test-results.xml --browser=${{ matrix.browser }}
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results-${{ matrix.python-version }}-${{ matrix.browser }}
        path: |
          unit-test-results.xml
          api-test-results.xml
          ui-test-results.xml
    
    - name: Generate Allure Report
      run: |
        allure generate allure-results --clean -o allure-report
    
    - name: Publish Allure Report
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: allure-report
```

---

### 📊 Отчетность: Allure Reports

#### Установка и настройка
```bash
# Установка Allure
pip install allure-pytest

# Запуск тестов с генерацией отчета
pytest --alluredir=allure-results

# Генерация HTML отчета
allure serve allure-results
```

#### Использование в тестах
```python
import allure
import pytest

@allure.feature("User Management")
@allure.story("User Login")
class TestUserLogin:
    
    @allure.title("Successful login with valid credentials")
    @allure.description("This test verifies that user can login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver):
        with allure.step("Open login page"):
            login_page = LoginPage(driver)
        
        with allure.step("Enter valid credentials"):
            login_page.enter_username("valid_user")
            login_page.enter_password("valid_password")
        
        with allure.step("Click login button"):
            login_page.click_login()
        
        with allure.step("Verify successful login"):
            dashboard_page = DashboardPage(driver)
            assert dashboard_page.is_welcome_message_displayed()
    
    @allure.title("Login failure with invalid credentials")
    @pytest.mark.parametrize("username,password", [
        ("invalid_user", "valid_password"),
        ("valid_user", "invalid_password"),
        ("", "")
    ])
    def test_login_failure(self, driver, username, password):
        with allure.step(f"Attempt login with {username}/{password}"):
            login_page = LoginPage(driver)
            login_page.login(username, password)
        
        with allure.step("Verify error message appears"):
            error_message = login_page.get_error_message()
            assert error_message is not None
            
        # Прикрепление скриншота при неудаче
        allure.attach(
            driver.get_screenshot_as_png(),
            name="login_failure_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
```

---

## 🏆 Итоговый результат Блока 3

### ✅ Полученные знания:
- [ ] Основы программирования на Python
- [ ] Принципы автоматизации тестирования
- [ ] Selenium WebDriver для UI тестирования
- [ ] API тестирование с использованием requests
- [ ] CI/CD процессы и GitHub Actions
- [ ] Создание отчетов с Allure

### 🛠️ Освоенные навыки:
- [ ] Написание UI автотестов
- [ ] Создание API тестов
- [ ] Применение паттерна Page Object Model
- [ ] Настройка CI/CD pipeline
- [ ] Работа с Git и системами контроля версий

### 📁 Практические результаты:
- [ ] **Автоматизированный тест-фреймворк** для веб-приложения
- [ ] **Набор UI тестов** покрывающий основные сценарии
- [ ] **API тесты** для backend сервисов
- [ ] **CI/CD pipeline** с автоматическим запуском тестов
- [ ] **Отчеты** с детальной информацией о результатах

### 🔧 Освоенные инструменты:
- [ ] **Selenium WebDriver** - UI автоматизация
- [ ] **Pytest** - тестовый фреймворк
- [ ] **Requests** - API тестирование
- [ ] **Allure** - отчетность
- [ ] **GitHub Actions** - CI/CD
- [ ] **Git** - контроль версий

---

## 🎯 Финальный проект Блока 3

### Задание: Создание полноценного тест-фреймворка

**Требования:**
1. **UI тесты**: Автоматизация интернет-магазина (регистрация, авторизация, покупка)
2. **API тесты**: Тестирование REST API (CRUD операции)
3. **Структура проекта**: Использование POM паттерна
4. **CI/CD**: Автоматический запуск тестов на GitHub Actions
5. **Отчетность**: Генерация Allure отчетов

**Критерии оценки:**
- Читаемость и структура кода
- Покрытие тестами основных сценариев
- Правильное использование паттернов
- Настройка CI/CD pipeline
- Качество отчетов

---

## 🚀 Переход к следующему блоку

После успешного завершения Блока 3 вы будете готовы к изучению:

**Блок 4: Специализированные виды тестирования**
- Тестирование производительности
- Тестирование безопасности
- Мобильное тестирование
- Тестирование микросервисов

**Ваш текущий уровень**: Middle QA Automation Engineer 🎉

---

## 📚 Дополнительные ресурсы

### Книги:
- "Selenium WebDriver 3 Practical Guide" - Unmesh Gundecha
- "Python Testing with pytest" - Brian Okken
- "Continuous Delivery" - Jez Humble, David Farley

### Онлайн курсы:
- Test Automation University (Applitools)
- Selenium WebDriver tutorials
- Python для тестировщиков

### Практика:
- [The Internet](https://the-internet.herokuapp.com/) - сайт для практики автоматизации
- [JSON Placeholder](https://jsonplaceholder.typicode.com/) - API для тестирования
- [Automation Practice](http://automationpractice.com/) - интернет-магазин для тестов

---

*Удачи в изучении автоматизации тестирования! 🚀*