# 🌐 Блок 4: Web-разработка и фреймворки

---

**⏱ Длительность:** 8-10 недель  
**🎯 Цель:** Освоить создание веб-приложений и понять архитектуру современных веб-сервисов  
**📊 Уровень сложности:** ⭐⭐⭐⭐☆

---

## 📋 Содержание блока

```
┌─────────────────────────────────────────────────────────┐
│  4.1 Основы веб-технологий                             │
│  4.2 Flask - микрофреймворк                            │
│  4.3 Django - полнофункциональный фреймворк            │
│  4.4 Работа с базами данных в веб                      │
│  4.5 Формы и валидация                                 │
│  4.6 Аутентификация и авторизация                      │
│  4.7 REST API разработка                               │
│  4.8 Тестирование веб-приложений                       │
│  4.9 Деплой и продакшн                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🌍 4.1 Основы веб-технологий

### 📖 Теоретическая часть

#### HTTP протокол и методы

```
┌─────────────────────────────────────────────────────────┐
│                    HTTP REQUEST/RESPONSE                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CLIENT                    SERVER                       │
│    │                        │                          │
│    │ ──── HTTP REQUEST ───→ │                          │
│    │                        │                          │
│    │ ←─── HTTP RESPONSE ──── │                          │
│    │                        │                          │
└─────────────────────────────────────────────────────────┘
```

**Основные HTTP методы:**

| Метод  | Назначение | Пример использования |
|--------|------------|---------------------|
| `GET`  | Получение данных | Загрузка страницы |
| `POST` | Отправка данных | Отправка формы |
| `PUT`  | Полное обновление | Обновление профиля |
| `PATCH`| Частичное обновление | Изменение email |
| `DELETE`| Удаление | Удаление записи |

#### Архитектура клиент-сервер

```
┌─────────────────────────────────────────────────────────┐
│                     WEB АРХИТЕКТУРА                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   КЛИЕНТ    │    │   СЕРВЕР    │    │  БАЗА ДАННЫХ│  │
│  │             │    │             │    │             │  │
│  │ - Browser   │◄──►│ - Python    │◄──►│ - PostgreSQL│  │
│  │ - Mobile    │    │ - Flask/    │    │ - MySQL     │  │
│  │ - Desktop   │    │   Django    │    │ - SQLite    │  │
│  │             │    │             │    │             │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 🛠 Практическое задание

**Создание простого HTTP сервера на Python:**

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Hello, Web World!</h1>')
        
        elif self.path == '/api/users':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
            self.wfile.write(json.dumps(users).encode())

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), SimpleHandler)
    print("Сервер запущен на http://localhost:8000")
    server.serve_forever()
```

---

## 🧪 4.2 Flask - микрофреймворк

### 📖 Теоретическая часть

Flask - это минималистичный веб-фреймворк, который предоставляет основные инструменты для создания веб-приложений.

#### Архитектура Flask

```
┌─────────────────────────────────────────────────────────┐
│                   FLASK АРХИТЕКТУРА                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │                  REQUEST                        │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    │                                    │
│  ┌─────────────────▼───────────────────────────────┐    │
│  │              ROUTING                            │    │
│  │            @app.route()                         │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    │                                    │
│  ┌─────────────────▼───────────────────────────────┐    │
│  │            VIEW FUNCTION                        │    │
│  │           def index():                          │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    │                                    │
│  ┌─────────────────▼───────────────────────────────┐    │
│  │              TEMPLATE                           │    │
│  │            (Jinja2)                             │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    │                                    │
│  ┌─────────────────▼───────────────────────────────┐    │
│  │              RESPONSE                           │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 🛠 Практические примеры

#### Создание первого Flask приложения

```python
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Простой маршрут
@app.route('/')
def home():
    return '<h1>Добро пожаловать в Flask!</h1>'

# Маршрут с параметром
@app.route('/user/<name>')
def user_profile(name):
    return f'<h1>Привет, {name}!</h1>'

# Обработка GET и POST запросов
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return f'Спасибо, {name}! Ваш email: {email}'
    
    return '''
    <form method="POST">
        <input type="text" name="name" placeholder="Имя" required>
        <input type="email" name="email" placeholder="Email" required>
        <button type="submit">Отправить</button>
    </form>
    '''

# API endpoint
@app.route('/api/data')
def api_data():
    return jsonify({
        'status': 'success',
        'data': ['item1', 'item2', 'item3']
    })

if __name__ == '__main__':
    app.run(debug=True)
```

#### Шаблоны Jinja2

**templates/base.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Мой сайт{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #007bff; color: white; padding: 20px; }
        .content { padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{% block header %}Добро пожаловать{% endblock %}</h1>
    </div>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**templates/index.html:**
```html
{% extends "base.html" %}

{% block title %}Главная страница{% endblock %}

{% block content %}
    <h2>Список пользователей:</h2>
    <ul>
    {% for user in users %}
        <li>{{ user.name }} ({{ user.email }})</li>
    {% endfor %}
    </ul>
{% endblock %}
```

### 📊 Структура Flask проекта

```
my_flask_app/
├── app.py                 # Главный файл приложения
├── config.py             # Конфигурация
├── requirements.txt      # Зависимости
├── templates/           # HTML шаблоны
│   ├── base.html
│   ├── index.html
│   └── forms.html
├── static/              # Статические файлы
│   ├── css/
│   ├── js/
│   └── images/
└── instance/            # Конфиденциальные настройки
    └── config.py
```

---

## 🎯 4.3 Django - полнофункциональный фреймворк

### 📖 Теоретическая часть

Django следует принципу "batteries included" и предоставляет множество встроенных функций.

#### Архитектура MVT (Model-View-Template)

```
┌─────────────────────────────────────────────────────────┐
│                   DJANGO MVT PATTERN                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │                 REQUEST                         │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    │                                    │
│  ┌─────────────────▼───────────────────────────────┐    │
│  │              URL DISPATCHER                     │    │
│  │            urls.py                              │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    │                                    │
│  ┌─────────────────▼───────────────────────────────┐    │
│  │               VIEW                              │    │
│  │            views.py                             │    │
│  └─────────┬───────────────────────┬─────────────────    │
│            │                       │                    │
│  ┌─────────▼─────────┐   ┌─────────▼─────────┐          │
│  │      MODEL        │   │     TEMPLATE      │          │
│  │    models.py      │   │   template.html   │          │
│  │   (Database)      │   │     (HTML)        │          │
│  └───────────────────┘   └───────────────────┘          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 🛠 Практические примеры

#### Создание Django проекта

```bash
# Создание проекта
django-admin startproject mysite
cd mysite

# Создание приложения
python manage.py startapp blog

# Миграция базы данных
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
```

#### Модели Django

```python
# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])
```

#### Представления Django

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Category

def post_list(request):
    posts = Post.objects.filter(status='published')
    
    # Пагинация
    paginator = Paginator(posts, 5)  # 5 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj
    })

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                           status='published',
                           slug=slug,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)
    
    return render(request, 'blog/post_detail.html', {'post': post})

def posts_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, status='published')
    
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts
    })

# API view
def api_posts(request):
    posts = Post.objects.filter(status='published').values(
        'title', 'slug', 'author__username', 'publish'
    )[:10]
    
    return JsonResponse(list(posts), safe=False)
```

### 📊 Структура Django проекта

```
mysite/
├── manage.py
├── mysite/                    # Настройки проекта
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blog/                      # Приложение
│   ├── __init__.py
│   ├── admin.py              # Административная панель
│   ├── apps.py
│   ├── models.py             # Модели данных
│   ├── views.py              # Представления
│   ├── urls.py               # URL маршруты
│   ├── forms.py              # Формы
│   ├── migrations/           # Миграции БД
│   ├── templates/            # Шаблоны
│   │   └── blog/
│   │       ├── base.html
│   │       ├── post_list.html
│   │       └── post_detail.html
│   └── static/               # Статические файлы
│       └── blog/
│           ├── css/
│           └── js/
└── requirements.txt
```

---

## 💾 4.4 Работа с базами данных в веб

### 📖 Django ORM примеры

```python
# Создание записей
post = Post.objects.create(
    title="Мой первый пост",
    content="Содержание поста",
    author=request.user,
    status='published'
)

# Запросы
all_posts = Post.objects.all()
published_posts = Post.objects.filter(status='published')
recent_posts = Post.objects.filter(
    publish__gte=timezone.now() - timedelta(days=7)
)

# Сложные запросы
from django.db.models import Q, Count

# OR условие
posts = Post.objects.filter(
    Q(title__icontains='Python') | Q(content__icontains='Django')
)

# Подсчет связанных объектов
categories_with_count = Category.objects.annotate(
    post_count=Count('post')
).filter(post_count__gt=0)

# Оптимизация запросов
posts_with_authors = Post.objects.select_related('author', 'category')
```

### 📊 Диаграмма связей в базе данных

```
┌─────────────────────────────────────────────────────────┐
│                  DATABASE RELATIONSHIPS                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │    USER     │    │    POST     │    │  CATEGORY   │  │
│  │             │    │             │    │             │  │
│  │ • id        │◄──┐│ • id        │┌──►│ • id        │  │
│  │ • username  │   ││ • title     ││   │ • name      │  │
│  │ • email     │   ││ • content   ││   │ • slug      │  │
│  │ • password  │   ││ • author_id ││   │             │  │
│  │             │   ││ • category  ││   │             │  │
│  └─────────────┘   │└─────────────┘│   └─────────────┘  │
│                    │               │                    │
│                    │ ForeignKey    │ ForeignKey         │
│                    │               │                    │
│                    └───────────────┘                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 4.5 Формы и валидация

### Django Forms

```python
# blog/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Содержание поста'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError('Заголовок должен содержать минимум 5 символов')
        return title

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('.com'):
            raise ValidationError('Используйте email с доменом .com')
        return email
```

### Обработка форм в представлениях

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm, ContactForm

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост успешно создан!')
            return redirect('blog:post_detail', 
                          year=post.publish.year,
                          month=post.publish.month,
                          day=post.publish.day,
                          slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Отправка email или сохранение в БД
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            # ... логика обработки
            messages.success(request, 'Сообщение отправлено!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
```

---

## 🔐 4.6 Аутентификация и авторизация

### Django Authentication

```python
# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверные данные для входа')
    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'posts': user_posts})

def logout_view(request):
    logout(request)
    return redirect('home')
```

### Разграничение доступа

```python
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

# Функциональные представления
@login_required
@permission_required('blog.add_post')
def create_post(request):
    # Только авторизованные пользователи с правом создания постов
    pass

def is_author(user):
    return user.groups.filter(name='Authors').exists()

@user_passes_test(is_author)
def author_dashboard(request):
    # Только для пользователей из группы "Authors"
    pass

# Классовые представления
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_list.html'
    login_url = '/login/'
    
class CreatePostView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    permission_required = 'blog.add_post'
```

---

## 🔗 4.7 REST API разработка

### Django REST Framework

```python
# serializers.py
from rest_framework import serializers
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'post_count']
    
    def get_post_count(self, obj):
        return obj.post_set.filter(status='published').count()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 
                 'category', 'category_id', 'publish', 'status']
        read_only_fields = ['slug', 'publish']
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Заголовок должен содержать минимум 5 символов"
            )
        return value

# views.py (API)
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_stats(request):
    stats = {
        'total_posts': Post.objects.filter(status='published').count(),
        'total_categories': Category.objects.count(),
        'recent_posts': Post.objects.filter(
            publish__gte=timezone.now() - timedelta(days=7)
        ).count()
    }
    return Response(stats)
```

### API URLs

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API URLs
api_urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('stats/', views.api_stats, name='api-stats'),
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),
    # ... остальные URL
]
```

---

## 🧪 4.8 Тестирование веб-приложений

### Unit тесты для Django

```python
# tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Category

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
    
    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            category=self.category,
            status='published'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.slug)  # Автоматически генерируется
    
    def test_post_str_representation(self):
        post = Post(title='Test Post')
        self.assertEqual(str(post), 'Test Post')

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            category=self.category,
            status='published'
        )
    
    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_post_detail_view(self):
        url = self.post.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
    
    def test_create_post_requires_login(self):
        response = self.client.get(reverse('blog:create_post'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_create_post_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('blog:create_post'), {
            'title': 'New Post',
            'content': 'New content',
            'category': self.category.id,
            'status': 'published'
        })
        self.assertEqual(response.status_code, 302)  # Редирект после создания
        self.assertTrue(Post.objects.filter(title='New Post').exists())

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='API Test Post',
            content='API test content',
            author=self.user,
            status='published'
        )
    
    def test_api_post_list(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['title'], 'API Test Post')
    
    def test_api_post_create_requires_auth(self):
        response = self.client.post('/api/posts/', {
            'title': 'New API Post',
            'content': 'New API content'
        })
        self.assertEqual(response.status_code, 401)  # Unauthorized
```

---

## 🚀 4.9 Деплой и продакшн

### Подготовка к деплою

```python
# settings/production.py
import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# База данных для продакшна
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Безопасность
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Docker настройка

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=0
      - DB_NAME=postgres
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_HOST=db
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  redis:
    image: redis:6-alpine

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

---

## 🎯 Итоговые проекты блока

### 1. 📝 Блог с административной панелью
- **Функционал:** CRUD операции для постов, категории, комментарии
- **Технологии:** Django, PostgreSQL, Bootstrap
- **Особенности:** Административная панель, пагинация, поиск

### 2. 🔗 API для мобильного приложения
- **Функционал:** REST API с аутентификацией
- **Технологии:** Django REST Framework, JWT токены
- **Особенности:** Документация API, версионирование

### 3. 🛒 Интернет-магазин с корзиной и оплатой
- **Функционал:** Каталог товаров, корзина, оформление заказов
- **Технологии:** Django, Stripe API, Redis для сессий
- **Особенности:** Интеграция платежей, email уведомления

### 4. 👥 Социальная сеть (упрощенная версия)
- **Функционал:** Профили пользователей, публикации, подписки
- **Технологии:** Django, WebSockets для чата, PostgreSQL
- **Особенности:** Real-time уведомления, система подписок

---

## 📊 Чек-лист прогресса

### ✅ Базовые навыки
- [ ] Понимание HTTP протокола
- [ ] Создание простых Flask приложений
- [ ] Работа с Django моделями
- [ ] Создание и обработка HTML форм
- [ ] Базовая аутентификация

### ✅ Продвинутые навыки
- [ ] Создание REST API
- [ ] Написание тестов для веб-приложений
- [ ] Оптимизация запросов к БД
- [ ] Настройка деплоя
- [ ] Работа с Docker

### ✅ Экспертный уровень
- [ ] Архитектурное проектирование
- [ ] Масштабирование приложений
- [ ] Безопасность веб-приложений
- [ ] CI/CD настройка
- [ ] Мониторинг и логирование

---

## 📚 Дополнительные ресурсы

- **Документация Django:** https://docs.djangoproject.com/
- **Flask документация:** https://flask.palletsprojects.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **Книга "Two Scoops of Django"**
- **Real Python:** https://realpython.com/

---

**🎯 Следующий блок:** Продвинутые темы и оптимизация