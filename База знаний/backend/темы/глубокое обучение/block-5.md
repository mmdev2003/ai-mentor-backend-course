# 🚀 Блок 5: Генеративные модели и продвинутые техники

---

**⏱ Длительность:** 7-9 недель  
**🎯 Цель:** Освоить современные генеративные модели и продвинутые методы  
**📊 Уровень сложности:** ★★★★☆

---

## 📋 Обзор блока

```
Блок 5: Генеративные модели
├── 📖 Глава 5.1: Автоэнкодеры (1 неделя)
├── 🎨 Глава 5.2: Вариационные автоэнкодеры (VAE) (1-2 недели)  
├── ⚔️ Глава 5.3: Генеративно-состязательные сети (GAN) (2 недели)
├── 🌊 Глава 5.4: Диффузионные модели (1-2 недели)
├── 🎮 Глава 5.5: Reinforcement Learning основы (1 неделя)
├── 🧠 Глава 5.6: Meta-learning и Few-shot learning (1 неделя)
└── 🔗 Глава 5.7: Multimodal модели (1 неделя)
```

---

## 📖 Глава 5.1: Автоэнкодеры
**⏱ Длительность:** 1 неделя

### 🎯 Цели главы
- Понять принципы работы автоэнкодеров
- Изучить различные типы автоэнкодеров
- Реализовать автоэнкодер для сжатия данных

### 📚 Теоретическая часть

#### Что такое автоэнкодер?

```
Входные данные (X) → [Энкодер] → Латентное пространство (Z) → [Декодер] → Восстановленные данные (X')
```

**Автоэнкодер** - это нейронная сеть, которая учится эффективно кодировать входные данные в сжатое представление (латентное пространство), а затем декодировать их обратно.

#### Архитектура автоэнкодера

```
─────────────────────────────────────────────────────────────
│                    АВТОЭНКОДЕР                            │
├─────────────────────────┬─────────────────────────────────┤
│        ЭНКОДЕР          │          ДЕКОДЕР                │
├─────────────────────────┼─────────────────────────────────┤
│                         │                                 │
│  Input (784)            │              Output (784)       │
│     ↓                   │                 ↑               │
│  Hidden (512)           │              Hidden (512)       │
│     ↓                   │                 ↑               │
│  Hidden (256)           │              Hidden (256)       │
│     ↓                   │                 ↑               │
│  Latent (32) ──────────────────────────→ Latent (32)     │
│                         │                                 │
─────────────────────────────────────────────────────────────
```

#### Типы автоэнкодеров

##### 1. **Классический автоэнкодер**
```python
# Архитектура
Input → Dense(512) → Dense(256) → Dense(32) → Dense(256) → Dense(512) → Output
```

##### 2. **Denoising автоэнкодер**
```
Чистое изображение → [Добавление шума] → Зашумленное изображение → [Автоэнкодер] → Чистое изображение
```

##### 3. **Sparse автоэнкодер**
```
Обычная функция потерь + L1 регуляризация латентного пространства
Loss = Reconstruction_Loss + λ * ||z||₁
```

### 💻 Практическая часть

#### Задание 1: Реализация классического автоэнкодера

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

class Autoencoder(nn.Module):
    def __init__(self, input_dim=784, hidden_dims=[512, 256], latent_dim=32):
        super(Autoencoder, self).__init__()
        
        # Энкодер
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dims[0]),
            nn.ReLU(),
            nn.Linear(hidden_dims[0], hidden_dims[1]),
            nn.ReLU(),
            nn.Linear(hidden_dims[1], latent_dim)
        )
        
        # Декодер
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dims[1]),
            nn.ReLU(),
            nn.Linear(hidden_dims[1], hidden_dims[0]),
            nn.ReLU(),
            nn.Linear(hidden_dims[0], input_dim),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
```

#### Задание 2: Denoising автоэнкодер

```python
def add_noise(data, noise_factor=0.3):
    """Добавляет гауссовский шум к данным"""
    noise = torch.randn_like(data) * noise_factor
    noisy_data = data + noise
    return torch.clamp(noisy_data, 0., 1.)

# Тренировка с зашумленными данными
for epoch in range(num_epochs):
    for batch_idx, (data, _) in enumerate(train_loader):
        # Добавляем шум
        noisy_data = add_noise(data.view(-1, 784))
        clean_data = data.view(-1, 784)
        
        # Обучение
        optimizer.zero_grad()
        reconstructed = model(noisy_data)
        loss = criterion(reconstructed, clean_data)  # Сравниваем с чистыми данными!
        loss.backward()
        optimizer.step()
```

### 📊 Визуализация результатов

```
Оригинальные изображения:
┌─────┬─────┬─────┬─────┬─────┐
│  🔢  │  🔢  │  🔢  │  🔢  │  🔢  │
│  3   │  7   │  2   │  1   │  0   │
└─────┴─────┴─────┴─────┴─────┘

Восстановленные изображения:
┌─────┬─────┬─────┬─────┬─────┐
│  🔢  │  🔢  │  🔢  │  🔢  │  🔢  │
│  3   │  7   │  2   │  1   │  0   │
└─────┴─────┴─────┴─────┴─────┘

Качество восстановления: 95.2%
```

### 🏆 Практические результаты
- ✅ Реализация автоэнкодера с нуля
- ✅ Сжатие изображений MNIST с потерями <5%
- ✅ Создание denoising автоэнкодера
- ✅ Визуализация латентного пространства

---

## 🎨 Глава 5.2: Вариационные автоэнкодеры (VAE)
**⏱ Длительность:** 1-2 недели

### 🎯 Цели главы
- Понять математические основы VAE
- Изучить reparameterization trick
- Реализовать VAE для генерации новых данных

### 📚 Теоретическая часть

#### Основные отличия VAE от обычного автоэнкодера

```
Обычный автоэнкодер:
Input → Encoder → z (детерминированный) → Decoder → Output

VAE:
Input → Encoder → μ, σ → z ~ N(μ, σ) → Decoder → Output
                     ↑
              (стохастический)
```

#### Математические основы

**Функция потерь VAE:**
```
L = E[log p(x|z)] - KL(q(z|x) || p(z))
    └─────────────┘   └─────────────────┘
  Reconstruction Loss    Regularization
```

**KL-дивергенция для нормального распределения:**
```
KL(N(μ,σ) || N(0,1)) = ½ * Σ(μ² + σ² - log(σ²) - 1)
```

#### Reparameterization trick

```
Проблема: z ~ N(μ, σ) - не дифференцируемо
                 ↓
Решение: z = μ + σ * ε, где ε ~ N(0,1)
```

### 💻 Практическая часть

#### Реализация VAE

```python
class VAE(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=512, latent_dim=32):
        super(VAE, self).__init__()
        
        # Энкодер
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # Параметры распределения
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)
        
        # Декодер
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid()
        )
    
    def encode(self, x):
        h = self.encoder(x)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar
    
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        z = mu + eps * std
        return z
    
    def decode(self, z):
        return self.decoder(z)
    
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        recon_x = self.decode(z)
        return recon_x, mu, logvar

def vae_loss(recon_x, x, mu, logvar, beta=1.0):
    """VAE Loss = Reconstruction Loss + β * KL Divergence"""
    recon_loss = F.binary_cross_entropy(recon_x, x, reduction='sum')
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon_loss + beta * kl_loss
```

### 📊 Генерация новых данных

```python
def generate_samples(model, num_samples=16):
    """Генерируем новые образцы из VAE"""
    with torch.no_grad():
        # Сэмплируем из prior распределения
        z = torch.randn(num_samples, latent_dim)
        generated = model.decode(z)
        return generated
```

### 🔍 Анализ латентного пространства

```
Визуализация латентного пространства VAE:

        z₂
         ↑
    ┌────┼────┐
    │ 🔢 │ 🔢 │
    │ 1  │ 7  │
────┼────┼────┼──→ z₁
    │ 🔢 │ 🔢 │
    │ 0  │ 2  │
    └────┼────┘
         
Интерполяция между точками:
🔢 → 🔢 → 🔢 → 🔢 → 🔢
1   1.5   ?   8.5   8
```

### 🏆 Практические результаты
- ✅ Реализация VAE с нуля
- ✅ Генерация новых реалистичных изображений
- ✅ Интерполяция в латентном пространстве
- ✅ Понимание β-VAE для контроля disentanglement

---

## ⚔️ Глава 5.3: Генеративно-состязательные сети (GAN)
**⏱ Длительность:** 2 недели

### 🎯 Цели главы
- Понять принципы adversarial training
- Изучить различные архитектуры GAN
- Реализовать GAN для генерации реалистичных изображений

### 📚 Теоретическая часть

#### Принцип работы GAN

```
                    ГЕНЕРАТИВНО-СОСТЯЗАТЕЛЬНАЯ СЕТЬ
    
    ┌─────────────────┐                    ┌─────────────────┐
    │                 │                    │                 │
    │   ГЕНЕРАТОР     │                    │ ДИСКРИМИНАТОР   │
    │       G         │                    │       D         │
    │                 │                    │                 │
    └─────────────────┘                    └─────────────────┘
            ↑                                      ↑
            │                                      │
      Случайный шум                         Реальные + Фальшивые
         z ~ N(0,1)                              изображения
            │                                      │
            ↓                                      ↓
      Фальшивые                              Вероятность
      изображения                          "реальности"
        G(z)                                   D(x)
```

#### Игра с нулевой суммой

```
Генератор (G):  Максимизирует  log(D(G(z)))
Дискриминатор (D): Максимизирует  log(D(x)) + log(1 - D(G(z)))

Общая задача:  min max V(D,G) = E[log D(x)] + E[log(1 - D(G(z)))]
                G   D
```

#### Проблемы обучения GAN

```
🚨 ОСНОВНЫЕ ПРОБЛЕМЫ:

1. Mode Collapse
   ┌─────────────────┐
   │ Все генерируемые│
   │ образцы похожи  │ 
   │ 🔢 🔢 🔢 🔢     │
   │ 3  3  3  3      │
   └─────────────────┘

2. Training Instability
   Loss G ↗️↘️↗️↘️↗️
   Loss D ↘️↗️↘️↗️↘️

3. Vanishing Gradients
   D слишком хорош → G не может учиться
```

### 💻 Практическая часть

#### Реализация DCGAN

```python
class Generator(nn.Module):
    def __init__(self, latent_dim=100, img_channels=1, img_size=28):
        super(Generator, self).__init__()
        
        self.init_size = img_size // 4
        self.l1 = nn.Sequential(nn.Linear(latent_dim, 128 * self.init_size ** 2))
        
        self.conv_blocks = nn.Sequential(
            nn.BatchNorm2d(128),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 128, 3, stride=1, padding=1),
            nn.BatchNorm2d(128, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 64, 3, stride=1, padding=1),
            nn.BatchNorm2d(64, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, img_channels, 3, stride=1, padding=1),
            nn.Tanh()
        )
    
    def forward(self, z):
        out = self.l1(z)
        out = out.view(out.shape[0], 128, self.init_size, self.init_size)
        img = self.conv_blocks(out)
        return img

class Discriminator(nn.Module):
    def __init__(self, img_channels=1, img_size=28):
        super(Discriminator, self).__init__()
        
        def discriminator_block(in_filters, out_filters, bn=True):
            block = [nn.Conv2d(in_filters, out_filters, 3, 2, 1), nn.LeakyReLU(0.2, inplace=True), nn.Dropout2d(0.25)]
            if bn:
                block.append(nn.BatchNorm2d(out_filters, 0.8))
            return block
        
        self.model = nn.Sequential(
            *discriminator_block(img_channels, 16, bn=False),
            *discriminator_block(16, 32),
            *discriminator_block(32, 64),
            *discriminator_block(64, 128),
        )
        
        ds_size = img_size // 2 ** 4
        self.adv_layer = nn.Sequential(nn.Linear(128 * ds_size ** 2, 1), nn.Sigmoid())
    
    def forward(self, img):
        out = self.model(img)
        out = out.view(out.shape[0], -1)
        validity = self.adv_layer(out)
        return validity
```

#### Цикл обучения GAN

```python
def train_gan(generator, discriminator, dataloader, num_epochs=100):
    
    # Оптимизаторы
    opt_G = torch.optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
    opt_D = torch.optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))
    
    criterion = nn.BCELoss()
    
    for epoch in range(num_epochs):
        for i, (real_imgs, _) in enumerate(dataloader):
            
            # Метки
            valid = torch.ones(real_imgs.size(0), 1, requires_grad=False)
            fake = torch.zeros(real_imgs.size(0), 1, requires_grad=False)
            
            # -----------------
            #  Обучение Generator
            # -----------------
            
            opt_G.zero_grad()
            
            # Сэмплируем шум
            z = torch.randn(real_imgs.size(0), latent_dim)
            
            # Генерируем изображения
            gen_imgs = generator(z)
            
            # Потеря генератора
            g_loss = criterion(discriminator(gen_imgs), valid)
            
            g_loss.backward()
            opt_G.step()
            
            # ---------------------
            #  Обучение Discriminator
            # ---------------------
            
            opt_D.zero_grad()
            
            # Потеря на реальных изображениях
            real_loss = criterion(discriminator(real_imgs), valid)
            
            # Потеря на фальшивых изображениях
            fake_loss = criterion(discriminator(gen_imgs.detach()), fake)
            
            # Общая потеря дискриминатора
            d_loss = (real_loss + fake_loss) / 2
            
            d_loss.backward()
            opt_D.step()
            
            # Логирование
            if i % 100 == 0:
                print(f"Epoch {epoch}, Batch {i}, G_loss: {g_loss.item():.4f}, D_loss: {d_loss.item():.4f}")
```

### 📊 Улучшенные архитектуры GAN

#### StyleGAN концепция

```
    Традиционный GAN:
    z → Generator → Image
    
    StyleGAN:
    z → Mapping Network → w
    Noise → AdaIN(w) → Progressive Generation → High-Res Image
```

#### CycleGAN для перевода изображений

```
    Домен A ←→ Домен B
    
    🐴 ────→ 🦓
    │  G_AB  │
    │        │
    │  G_BA  │
    🦓 ←──── 🐴
    
    Cycle Consistency: G_BA(G_AB(x)) ≈ x
```

### 🏆 Практические результаты
- ✅ Реализация DCGAN с нуля
- ✅ Генерация реалистичных лиц
- ✅ Понимание проблем обучения GAN
- ✅ Эксперименты с различными архитектурами

---

## 🌊 Глава 5.4: Диффузионные модели
**⏱ Длительность:** 1-2 недели

### 🎯 Цели главы
- Понять принципы диффузионных процессов
- Изучить DDPM (Denoising Diffusion Probabilistic Models)
- Реализовать простую диффузионную модель

### 📚 Теоретическая часть

#### Принцип диффузии

```
ПРЯМОЙ ПРОЦЕСС (добавление шума):
x₀ → x₁ → x₂ → x₃ → ... → xₜ → ... → xₜ₋₁ → xₜ (чистый шум)
🖼️   📸   📷   📹         🌫️         ⚪    ⚫

ОБРАТНЫЙ ПРОЦЕСС (удаление шума):
xₜ → xₜ₋₁ → xₜ₋₂ → ... → x₁ → x₀
⚫    ⚪    🌫️       📷  🖼️

Модель учится обратному процессу!
```

#### Математические основы

**Прямой процесс:**
```
q(xₜ|xₜ₋₁) = N(xₜ; √(1-βₜ)xₜ₋₁, βₜI)

где βₜ - schedule шума
```

**Обратный процесс:**
```
pθ(xₜ₋₁|xₜ) = N(xₜ₋₁; μθ(xₜ,t), Σθ(xₜ,t))
```

#### U-Net архитектура для диффузии

```
                    U-NET ДЛЯ ДИФФУЗИИ
    
    Вход: xₜ (зашумленное изображение) + t (временной шаг)
    
    ┌─────────────────────────────────────────────────────────┐
    │                    ЭНКОДЕР                              │
    │  32x32 → 16x16 → 8x8 → 4x4 → 2x2                      │
    │   ↓       ↓      ↓     ↓     ↓                         │
    │  Conv   Conv   Conv  Conv   Conv                       │
    │   ↓       ↓      ↓     ↓     ↓                         │
    │  [Skip connections]   ↓                                │
    │                       ↓                                │
    │              ┌─────────────────┐                       │
    │              │  BOTTLENECK     │                       │
    │              │  + Time Embed   │                       │
    │              └─────────────────┘                       │
    │                       ↓                                │
    │                    ДЕКОДЕР                             │
    │  2x2 → 4x4 → 8x8 → 16x16 → 32x32                      │
    │   ↑     ↑     ↑      ↑       ↑                         │
    │  Conv Conv  Conv   Conv    Conv                        │
    │   ↑     ↑     ↑      ↑       ↑                         │
    │  [Skip connections from encoder]                       │
    └─────────────────────────────────────────────────────────┘
    
    Выход: ε̂θ(xₜ,t) (предсказанный шум)
```

### 💻 Практическая часть

#### Реализация простой диффузионной модели

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class SimpleDiffusion:
    def __init__(self, num_timesteps=1000):
        self.num_timesteps = num_timesteps
        
        # Создаем schedule для шума
        self.betas = self.linear_beta_schedule(num_timesteps)
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)
        
    def linear_beta_schedule(self, timesteps, start=0.0001, end=0.02):
        """Линейный schedule для шума"""
        return torch.linspace(start, end, timesteps)
    
    def q_sample(self, x_start, t, noise=None):
        """Добавляем шум к изображению на шаге t"""
        if noise is None:
            noise = torch.randn_like(x_start)
        
        sqrt_alphas_cumprod_t = self.alphas_cumprod[t].sqrt()
        sqrt_one_minus_alphas_cumprod_t = (1 - self.alphas_cumprod[t]).sqrt()
        
        return sqrt_alphas_cumprod_t * x_start + sqrt_one_minus_alphas_cumprod_t * noise
    
    def p_losses(self, denoise_model, x_start, t, noise=None):
        """Вычисляем потери для обучения"""
        if noise is None:
            noise = torch.randn_like(x_start)
        
        # Добавляем шум
        x_noisy = self.q_sample(x_start, t, noise)
        
        # Предсказываем шум
        predicted_noise = denoise_model(x_noisy, t)
        
        # Вычисляем потери
        loss = F.mse_loss(noise, predicted_noise)
        return loss

class TimeEmbedding(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        
    def forward(self, time):
        device = time.device
        half_dim = self.dim // 2
        embeddings = np.log(10000) / (half_dim - 1)
        embeddings = torch.exp(torch.arange(half_dim, device=device) * -embeddings)
        embeddings = time[:, None] * embeddings[None, :]
        embeddings = torch.cat((embeddings.sin(), embeddings.cos()), dim=-1)
        return embeddings

class SimpleUNet(nn.Module):
    def __init__(self, channels=1, time_emb_dim=128):
        super().__init__()
        
        self.time_embedding = TimeEmbedding(time_emb_dim)
        
        # Энкодер
        self.conv1 = nn.Conv2d(channels, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, 3, padding=1)
        
        # Bottleneck
        self.bottleneck = nn.Conv2d(256, 512, 3, padding=1)
        self.time_proj = nn.Linear(time_emb_dim, 512)
        
        # Декодер
        self.upconv3 = nn.ConvTranspose2d(512, 256, 3, padding=1)
        self.upconv2 = nn.ConvTranspose2d(256 + 256, 128, 3, padding=1)  # +256 для skip connection
        self.upconv1 = nn.ConvTranspose2d(128 + 128, 64, 3, padding=1)   # +128 для skip connection
        self.final_conv = nn.Conv2d(64 + 64, channels, 3, padding=1)     # +64 для skip connection
        
    def forward(self, x, time):
        # Time embedding
        time_emb = self.time_embedding(time)
        
        # Энкодер с сохранением skip connections
        skip1 = F.relu(self.conv1(x))
        skip2 = F.relu(self.conv2(F.max_pool2d(skip1, 2)))
        skip3 = F.relu(self.conv3(F.max_pool2d(skip2, 2)))
        
        # Bottleneck с time embedding
        bottleneck = F.relu(self.bottleneck(F.max_pool2d(skip3, 2)))
        time_proj = self.time_proj(time_emb)
        bottleneck = bottleneck + time_proj.view(-1, 512, 1, 1)
        
        # Декодер с skip connections
        x = F.relu(self.upconv3(F.interpolate(bottleneck, scale_factor=2)))
        x = torch.cat([x, skip3], dim=1)
        
        x = F.relu(self.upconv2(F.interpolate(x, scale_factor=2)))
        x = torch.cat([x, skip2], dim=1)
        
        x = F.relu(self.upconv1(F.interpolate(x, scale_factor=2)))
        x = torch.cat([x, skip1], dim=1)
        
        x = self.final_conv(x)
        return x
```

#### Процесс обучения

```python
def train_diffusion_model(model, dataloader, diffusion, num_epochs=100):
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    
    for epoch in range(num_epochs):
        total_loss = 0
        for batch_idx, (data, _) in enumerate(dataloader):
            optimizer.zero_grad()
            
            # Случайные временные шаги
            batch_size = data.shape[0]
            t = torch.randint(0, diffusion.num_timesteps, (batch_size,))
            
            # Вычисляем потери
            loss = diffusion.p_losses(model, data, t)
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        print(f'Epoch {epoch}, Average Loss: {total_loss/len(dataloader):.4f}')
```

#### Сэмплирование (генерация)

```python
@torch.no_grad()
def sample_from_model(model, diffusion, image_size=(28, 28), num_samples=16):
    """Генерируем изображения из чистого шума"""
    
    # Начинаем с чистого шума
    img = torch.randn(num_samples, 1, *image_size)
    
    # Последовательно удаляем шум
    for i in reversed(range(diffusion.num_timesteps)):
        t = torch.full((num_samples,), i, dtype=torch.long)
        
        # Предсказываем шум
        predicted_noise = model(img, t)
        
        # Удаляем предсказанный шум
        alpha = diffusion.alphas[i]
        alpha_cumprod = diffusion.alphas_cumprod[i]
        beta = diffusion.betas[i]
        
        # Формула для удаления шума
        img = (1 / alpha.sqrt()) * (img - beta * predicted_noise / (1 - alpha_cumprod).sqrt())
        
        # Добавляем немного шума (кроме последнего шага)
        if i > 0:
            noise = torch.randn_like(img)
            img = img + (beta.sqrt() * noise)
    
    return img
```

### 📊 Сравнение с GAN

```
                    GAN vs ДИФФУЗИЯ
    
    ┌─────────────────┬─────────────────┐
    │      GAN        │   ДИФФУЗИЯ      │
    ├─────────────────┼─────────────────┤
    │ Быстрая         │ Медленная       │
    │ генерация       │ генерация       │
    │ (1 проход)      │ (1000 шагов)    │
    ├─────────────────┼─────────────────┤
    │ Нестабильное    │ Стабильное      │
    │ обучение        │ обучение        │
    ├─────────────────┼─────────────────┤
    │ Mode collapse   │ Покрывает все   │
    │                 │ распределение   │
    ├─────────────────┼─────────────────┤
    │ Высокое         │ Исключительное  │
    │ качество        │ качество        │
    └─────────────────┴─────────────────┘
```

### 🏆 Практические результаты
- ✅ Реализация DDPM с нуля
- ✅ Генерация высококачественных изображений
- ✅ Понимание процесса диффузии
- ✅ Сравнение с другими генеративными моделями

---

## 🎮 Глава 5.5: Reinforcement Learning основы
**⏱ Длительность:** 1 неделя

### 🎯 Цели главы
- Понять основы обучения с подкреплением
- Изучить Q-learning и Deep Q-Networks
- Реализовать агента для простой игры

### 📚 Теоретическая часть

#### Основные концепции RL

```
               СРЕДА (Environment)
                     │
                   state s
                     │
                     ↓
    ┌─────────────────────────────────────┐
    │            АГЕНТ                    │
    │                                     │
    │  Policy π(a|s) → action a           │
    │                                     │
    │  Value V(s) / Q(s,a)                │
    └─────────────────────────────────────┘
                     │
                  action a
                     │
                     ↓
               СРЕДА (Environment)
                     │
                  reward r
                     │
                     ↓
                АГЕНТ получает
               reward и new state
```

#### Основные компоненты

```
🎯 ЦЕЛЬ: Максимизировать кумулятивную награду

📊 ОСНОВНЫЕ ЭЛЕМЕНТЫ:
   • State (s): текущее состояние
   • Action (a): действие агента  
   • Reward (r): награда за действие
   • Policy (π): стратегия выбора действий
   • Value (V): ожидаемая награда из состояния
```

#### Q-Learning алгоритм

```
Q-функция: Q(s,a) = ожидаемая награда за действие a в состоянии s

Обновление Q-функции:
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
                    a'
где:
α - learning rate
γ - discount factor
```

### 💻 Практическая часть

#### Реализация Deep Q-Network (DQN)

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(DQN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )
    
    def forward(self, x):
        return self.network(x)

class DQNAgent:
    def __init__(self, state_size, action_size, lr=0.001):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = lr
        
        # Нейронные сети
        self.q_network = DQN(state_size, 128, action_size)
        self.target_network = DQN(state_size, 128, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        
        # Копируем веса в target network
        self.target_network.load_state_dict(self.q_network.state_dict())
    
    def remember(self, state, action, reward, next_state, done):
        """Сохраняем опыт в replay buffer"""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """Выбираем действие с epsilon-greedy стратегией"""
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        q_values = self.q_network(state_tensor)
        return np.argmax(q_values.cpu().data.numpy())
    
    def replay(self, batch_size=32):
        """Обучаем сеть на батче из replay buffer"""
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        states = torch.FloatTensor([e[0] for e in batch])
        actions = torch.LongTensor([e[1] for e in batch])
        rewards = torch.FloatTensor([e[2] for e in batch])
        next_states = torch.FloatTensor([e[3] for e in batch])
        dones = torch.BoolTensor([e[4] for e in batch])
        
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.target_network(next_states).max(1)[0].detach()
        target_q_values = rewards + (0.99 * next_q_values * ~dones)
        
        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def update_target_network(self):
        """Обновляем target network"""
        self.target_network.load_state_dict(self.q_network.state_dict())
```

#### Простая игровая среда (CartPole)

```python
import gym

def train_dqn_agent():
    env = gym.make('CartPole-v1')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    
    agent = DQNAgent(state_size, action_size)
    
    scores = []
    episodes = 1000
    
    for episode in range(episodes):
        state = env.reset()
        if isinstance(state, tuple):
            state = state[0]  # для новых версий gym
        
        total_reward = 0
        
        for time in range(500):  # максимум 500 шагов
            action = agent.act(state)
            next_state, reward, done, truncated, info = env.step(action)
            
            # Модифицируем награду для лучшего обучения
            if done and time < 499:
                reward = -10  # штраф за падение
            
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            
            if done:
                break
        
        scores.append(total_reward)
        
        # Обучаем агента
        if len(agent.memory) > 32:
            agent.replay(32)
        
        # Обновляем target network каждые 100 эпизодов
        if episode % 100 == 0:
            agent.update_target_network()
        
        # Логирование
        if episode % 100 == 0:
            avg_score = np.mean(scores[-100:])
            print(f'Episode {episode}, Average Score: {avg_score:.2f}, Epsilon: {agent.epsilon:.3f}')
    
    return agent, scores
```

### 📊 Анализ обучения

```python
def plot_training_progress(scores):
    """Визуализируем прогресс обучения"""
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(scores)
    plt.title('Score per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Score')
    
    plt.subplot(1, 2, 2)
    rolling_avg = [np.mean(scores[max(0, i-100):i+1]) for i in range(len(scores))]
    plt.plot(rolling_avg)
    plt.title('Rolling Average (100 episodes)')
    plt.xlabel('Episode')
    plt.ylabel('Average Score')
    
    plt.tight_layout()
    plt.show()
```

### 🎯 Продвинутые методы

#### Policy Gradient (REINFORCE)

```python
class PolicyNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(PolicyNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.Softmax(dim=-1)
        )
    
    def forward(self, x):
        return self.network(x)

def reinforce_update(policy_net, optimizer, states, actions, rewards, gamma=0.99):
    """REINFORCE алгоритм обновления"""
    
    # Вычисляем дисконтированные награды
    discounted_rewards = []
    cumulative_reward = 0
    for reward in reversed(rewards):
        cumulative_reward = reward + gamma * cumulative_reward
        discounted_rewards.insert(0, cumulative_reward)
    
    # Нормализуем награды
    discounted_rewards = torch.tensor(discounted_rewards)
    discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-8)
    
    # Вычисляем потери
    policy_loss = []
    for log_prob, reward in zip(log_probs, discounted_rewards):
        policy_loss.append(-log_prob * reward)
    
    # Обновляем веса
    optimizer.zero_grad()
    policy_loss = torch.stack(policy_loss).sum()
    policy_loss.backward()
    optimizer.step()
```

### 🏆 Практические результаты
- ✅ Реализация DQN агента
- ✅ Обучение агента играть в CartPole
- ✅ Понимание exploration vs exploitation
- ✅ Знакомство с Policy Gradient методами

---

## 🧠 Глава 5.6: Meta-learning и Few-shot learning
**⏱ Длительность:** 1 неделя

### 🎯 Цели главы
- Понять концепцию "обучения обучению"
- Изучить MAML (Model-Agnostic Meta-Learning)
- Реализовать few-shot классификатор

### 📚 Теоретическая часть

#### Что такое Meta-learning?

```
                ОБЫЧНОЕ ОБУЧЕНИЕ
    
    Данные → Модель → Предсказания
    
    ────────────────────────────────────────────
    
                META-LEARNING
    
    Задача 1: Классификация кошек/собак
    Задача 2: Классификация птиц/рыб  
    Задача 3: Классификация машин/самолетов
                        │
                        ↓
                Meta-модель учится
               "как быстро учиться"
                        │
                        ↓
                Новая задача: Классификация цветов
                → Быстрая адаптация за несколько примеров
```

#### Few-shot learning задача

```
ПОДДЕРЖКА (Support Set):
┌─────┬─────┬─────┬─────┐
│ 🌹  │ 🌹  │ 🌻  │ 🌻  │  ← Мало примеров каждого класса
│Rose │Rose │Sun- │Sun- │    (обычно 1-5 примеров)
│     │     │flower│flower│
└─────┴─────┴─────┴─────┘

ЗАПРОС (Query Set):
┌─────┐
│ 🌹? │  ← Нужно классифицировать
│  ?  │
└─────┘

ЦЕЛЬ: Научиться быстро адаптироваться к новым задачам
```

#### MAML алгоритм

```
MAML (Model-Agnostic Meta-Learning):

1. Инициализируем параметры θ
2. Для каждой задачи τᵢ:
   • Берем few-shot support set
   • Делаем несколько gradient steps: θ'ᵢ = θ - α∇θLτᵢ(θ)
   • Тестируем на query set: Lτᵢ(θ'ᵢ)
3. Обновляем мета-параметры: θ = θ - β∇θ Σᵢ Lτᵢ(θ'ᵢ)
```

### 💻 Практическая часть

#### Реализация MAML

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import OrderedDict

class MAMLModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MAMLModel, self).__init__()
        self.layers = nn.Sequential(
            OrderedDict([
                ('conv1', nn.Conv2d(3, 32, 3, padding=1)),
                ('bn1', nn.BatchNorm2d(32)),
                ('relu1', nn.ReLU()),
                ('pool1', nn.MaxPool2d(2)),
                
                ('conv2', nn.Conv2d(32, 64, 3, padding=1)),
                ('bn2', nn.BatchNorm2d(64)),
                ('relu2', nn.ReLU()),
                ('pool2', nn.MaxPool2d(2)),
                
                ('flatten', nn.Flatten()),
                ('fc1', nn.Linear(64 * 8 * 8, hidden_size)),
                ('relu3', nn.ReLU()),
                ('fc2', nn.Linear(hidden_size, output_size))
            ])
        )
    
    def forward(self, x, params=None):
        if params is None:
            return self.layers(x)
        
        # Используем переданные параметры
        x = self.functional_forward(x, params)
        return x
    
    def functional_forward(self, x, params):
        """Forward pass с заданными параметрами"""
        # Реализация функционального forward
        # (упрощенная версия для демонстрации)
        for name, layer in self.layers.named_children():
            if name in params:
                if isinstance(layer, nn.Conv2d):
                    x = F.conv2d(x, params[name + '.weight'], params[name + '.bias'], 
                               layer.stride, layer.padding)
                elif isinstance(layer, nn.Linear):
                    x = F.linear(x, params[name + '.weight'], params[name + '.bias'])
            else:
                x = layer(x)
        return x

class MAML:
    def __init__(self, model, inner_lr=0.01, outer_lr=0.001, inner_steps=5):
        self.model = model
        self.inner_lr = inner_lr
        self.outer_lr = outer_lr
        self.inner_steps = inner_steps
        self.optimizer = optim.Adam(model.parameters(), lr=outer_lr)
        self.loss_fn = nn.CrossEntropyLoss()
    
    def inner_update(self, support_x, support_y, params=None):
        """Внутренний цикл обучения на support set"""
        if params is None:
            params = {name: param.clone() for name, param in self.model.named_parameters()}
        
        for _ in range(self.inner_steps):
            # Forward pass
            logits = self.model(support_x, params)
            loss = self.loss_fn(logits, support_y)
            
            # Вычисляем градиенты
            grads = torch.autograd.grad(loss, params.values(), create_graph=True)
            
            # Обновляем параметры
            params = {name: param - self.inner_lr * grad 
                     for (name, param), grad in zip(params.items(), grads)}
        
        return params
    
    def meta_update(self, tasks):
        """Мета-обновление на батче задач"""
        self.optimizer.zero_grad()
        
        meta_loss = 0
        for task in tasks:
            support_x, support_y, query_x, query_y = task
            
            # Внутренний цикл
            adapted_params = self.inner_update(support_x, support_y)
            
            # Вычисляем потери на query set
            query_logits = self.model(query_x, adapted_params)
            query_loss = self.loss_fn(query_logits, query_y)
            
            meta_loss += query_loss
        
        meta_loss /= len(tasks)
        meta_loss.backward()
        self.optimizer.step()
        
        return meta_loss.item()
```

#### Prototypical Networks

```python
class PrototypicalNetwork(nn.Module):
    def __init__(self, encoder_dim=64):
        super(PrototypicalNetwork, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(64, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(64, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Flatten(),
            nn.Linear(64 * 4 * 4, encoder_dim)
        )
    
    def forward(self, support_set, query_set):
        """
        support_set: (n_way * n_shot, C, H, W)
        query_set: (n_query, C, H, W)
        """
        # Кодируем support set
        support_embeddings = self.encoder(support_set)
        
        # Кодируем query set
        query_embeddings = self.encoder(query_set)
        
        # Вычисляем прототипы (центроиды классов)
        n_way = len(torch.unique(support_labels))
        n_shot = support_set.size(0) // n_way
        
        prototypes = support_embeddings.view(n_way, n_shot, -1).mean(dim=1)
        
        # Вычисляем расстояния
        distances = self.euclidean_distance(query_embeddings, prototypes)
        
        # Конвертируем в логиты
        logits = -distances
        
        return logits
    
    def euclidean_distance(self, x, y):
        """Вычисляем евклидово расстояние"""
        n = x.size(0)
        m = y.size(0)
        d = x.size(1)
        
        x = x.unsqueeze(1).expand(n, m, d)
        y = y.unsqueeze(0).expand(n, m, d)
        
        return torch.pow(x - y, 2).sum(2)
```

#### Создание few-shot датасета

```python
class FewShotDataset:
    def __init__(self, data, labels, n_way=5, n_shot=1, n_query=15):
        self.data = data
        self.labels = labels
        self.n_way = n_way
        self.n_shot = n_shot
        self.n_query = n_query
        self.classes = np.unique(labels)
    
    def sample_episode(self):
        """Сэмплируем эпизод для few-shot обучения"""
        # Выбираем случайные классы
        selected_classes = np.random.choice(self.classes, self.n_way, replace=False)
        
        support_x, support_y = [], []
        query_x, query_y = [], []
        
        for i, cls in enumerate(selected_classes):
            # Находим все примеры этого класса
            class_indices = np.where(self.labels == cls)[0]
            
            # Выбираем примеры для support и query
            selected_indices = np.random.choice(class_indices, 
                                              self.n_shot + self.n_query, 
                                              replace=False)
            
            support_indices = selected_indices[:self.n_shot]
            query_indices = selected_indices[self.n_shot:]
            
            # Добавляем в support set
            support_x.append(self.data[support_indices])
            support_y.extend([i] * self.n_shot)
            
            # Добавляем в query set
            query_x.append(self.data[query_indices])
            query_y.extend([i] * self.n_query)
        
        support_x = np.concatenate(support_x)
        query_x = np.concatenate(query_x)
        
        return (torch.tensor(support_x), torch.tensor(support_y),
                torch.tensor(query_x), torch.tensor(query_y))
```

### 📊 Эксперименты и результаты

```python
def train_few_shot_model(model, dataset, num_episodes=10000):
    """Обучаем модель на few-shot задачах"""
    
    accuracies = []
    
    for episode in range(num_episodes):
        # Сэмплируем эпизод
        support_x, support_y, query_x, query_y = dataset.sample_episode()
        
        # Обучаем модель
        if isinstance(model, MAML):
            loss = model.meta_update([(support_x, support_y, query_x, query_y)])
        else:
            # Для Prototypical Networks
            logits = model(support_x, query_x)
            loss = F.cross_entropy(logits, query_y)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        # Вычисляем точность
        if episode % 100 == 0:
            with torch.no_grad():
                logits = model(support_x, query_x)
                pred = logits.argmax(dim=1)
                acc = (pred == query_y).float().mean()
                accuracies.append(acc.item())
                print(f'Episode {episode}, Accuracy: {acc:.3f}')
    
    return accuracies
```

### 🏆 Практические результаты
- ✅ Реализация MAML алгоритма
- ✅ Создание Prototypical Networks
- ✅ Few-shot классификация с точностью 80%+
- ✅ Понимание принципов meta-learning

---

## 🔗 Глава 5.7: Multimodal модели
**⏱ Длительность:** 1 неделя

### 🎯 Цели главы
- Понять принципы мультимодального обучения
- Изучить CLIP архитектуру
- Создать поисковик по изображениям с текстовыми запросами

### 📚 Теоретическая часть

#### Что такое мультимодальные модели?

```
                МУЛЬТИМОДАЛЬНЫЕ МОДЕЛИ
    
    Текст: "Красивый закат над океаном"
      ↓
    [Text Encoder] ──────────────┐
                                 │
                                 ↓
                         Общее пространство
                         представлений
                                 ↑
                                 │
    [Image Encoder] ─────────────┘
      ↑
    Изображение: 🌅
    
    ЦЕЛЬ: Связать разные модальности в едином пространстве
```

#### CLIP архитектура

```
                        CLIP МОДЕЛЬ
    
    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │  Text: "A cat sitting on a table"                      │
    │    ↓                                                    │
    │  [Text Encoder] ──────────────┐                        │
    │  (Transformer)                │                        │
    │                               │                        │
    │                               ↓                        │
    │                       [Contrastive Loss]               │
    │                               ↑                        │
    │                               │                        │
    │  [Image Encoder] ─────────────┘                        │
    │  (Vision Transformer)                                  │
    │    ↑                                                   │
    │  Image: 🐱                                            │
    │                                                        │
    └─────────────────────────────────────────────────────────┘
    
    Обучение: Положительные пары (изображение + описание) притягиваются,
              отрицательные пары отталкиваются
```

#### Contrastive Learning

```
Батч изображений: [🐱, 🐶, 🚗, 🌳]
Батч описаний:   ["cat", "dog", "car", "tree"]

Матрица схожести:
        "cat" "dog" "car" "tree"
🐱      [0.9   0.1   0.2   0.1 ]
🐶      [0.1   0.8   0.1   0.2 ]
🚗      [0.2   0.1   0.9   0.1 ]
🌳      [0.1   0.2   0.1   0.8 ]

Цель: Максимизировать диагональные элементы,
      минимизировать остальные
```

### 💻 Практическая часть

#### Реализация простого CLIP

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import clip
from PIL import Image
import requests
from transformers import AutoTokenizer, AutoModel

class SimpleTextEncoder(nn.Module):
    def __init__(self, vocab_size, embed_dim=512, max_len=77):
        super(SimpleTextEncoder, self).__init__()
        self.embed_dim = embed_dim
        self.token_embedding = nn.Embedding(vocab_size, embed_dim)
        self.position_embedding = nn.Embedding(max_len, embed_dim)
        
        # Transformer блоки
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(embed_dim, nhead=8, dim_feedforward=2048),
            num_layers=12
        )
        
        self.ln_final = nn.LayerNorm(embed_dim)
        
    def forward(self, text_tokens):
        seq_len = text_tokens.size(1)
        positions = torch.arange(seq_len, device=text_tokens.device)
        
        # Embeddings
        x = self.token_embedding(text_tokens) + self.position_embedding(positions)
        
        # Transformer
        x = x.permute(1, 0, 2)  # (seq_len, batch_size, embed_dim)
        x = self.transformer(x)
        x = x.permute(1, 0, 2)  # (batch_size, seq_len, embed_dim)
        
        # Pooling (берем последний токен)
        x = self.ln_final(x[:, -1, :])
        
        return x

class SimpleImageEncoder(nn.Module):
    def __init__(self, embed_dim=512):
        super(SimpleImageEncoder, self).__init__()
        
        # Используем ResNet backbone
        self.backbone = nn.Sequential(
            # Conv Block 1
            nn.Conv2d(3, 64, 7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2, padding=1),
            
            # Conv Block 2
            nn.Conv2d(64, 128, 3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            
            # Conv Block 3
            nn.Conv2d(128, 256, 3, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            
            # Conv Block 4
            nn.Conv2d(256, 512, 3, stride=2, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            
            # Global Average Pooling
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten()
        )
        
        self.projection = nn.Linear(512, embed_dim)
        
    def forward(self, images):
        features = self.backbone(images)
        embeddings = self.projection(features)
        return embeddings

class SimpleCLIP(nn.Module):
    def __init__(self, vocab_size=50000, embed_dim=512, temperature=0.07):
        super(SimpleCLIP, self).__init__()
        
        self.text_encoder = SimpleTextEncoder(vocab_size, embed_dim)
        self.image_encoder = SimpleImageEncoder(embed_dim)
        self.temperature = nn.Parameter(torch.tensor(temperature))
        
    def forward(self, images, text_tokens):
        # Получаем embeddings
        image_features = self.image_encoder(images)
        text_features = self.text_encoder(text_tokens)
        
        # Нормализуем features
        image_features = F.normalize(image_features, dim=-1)
        text_features = F.normalize(text_features, dim=-1)
        
        # Вычисляем similarity matrix
        logits = torch.matmul(image_features, text_features.T) / self.temperature
        
        return logits, image_features, text_features

def clip_loss(logits):
    """Contrastive loss для CLIP"""
    batch_size = logits.size(0)
    labels = torch.arange(batch_size, device=logits.device)
    
    # Loss в обе стороны
    loss_i2t = F.cross_entropy(logits, labels)
    loss_t2i = F.cross_entropy(logits.T, labels)
    
    return (loss_i2t + loss_t2i) / 2
```

#### Обучение CLIP модели

```python
def train_clip_model(model, dataloader, num_epochs=10):
    """Обучаем CLIP модель"""
    
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    model.train()
    
    for epoch in range(num_epochs):
        total_loss = 0
        
        for batch_idx, (images, text_tokens) in enumerate(dataloader):
            optimizer.zero_grad()
            
            # Forward pass
            logits, image_features, text_features = model(images, text_tokens)
            
            # Вычисляем loss
            loss = clip_loss(logits)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 100 == 0:
                print(f'Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item():.4f}')
        
        print(f'Epoch {epoch}, Average Loss: {total_loss/len(dataloader):.4f}')
```

#### Использование предобученного CLIP

```python
import clip
import torch
from PIL import Image

# Загружаем предобученную модель
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def image_search(query_text, image_paths):
    """Поиск изображений по текстовому запросу"""
    
    # Токенизируем текст
    text_tokens = clip.tokenize([query_text]).to(device)
    
    # Обрабатываем изображения
    images = []
    for path in image_paths:
        image = preprocess(Image.open(path)).unsqueeze(0).to(device)
        images.append(image)
    
    images = torch.cat(images)
    
    # Получаем embeddings
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)
        image_features = model.encode_image(images)
        
        # Нормализуем
        text_features = F.normalize(text_features, dim=-1)
        image_features = F.normalize(image_features, dim=-1)
        
        # Вычисляем схожесть
        similarities = torch.matmul(text_features, image_features.T)
    
    # Ранжируем результаты
    similarities = similarities.squeeze().cpu().numpy()
    ranked_indices = similarities.argsort()[::-1]
    
    results = []
    for idx in ranked_indices:
        results.append({
            'image_path': image_paths[idx],
            'similarity': similarities[idx]
        })
    
    return results

# Пример использования
query = "a cat sitting on a table"
image_paths = ["cat1.jpg", "dog1.jpg", "table1.jpg", "cat2.jpg"]
results = image_search(query, image_paths)

for result in results[:3]:  # Топ-3 результата
    print(f"Image: {result['image_path']}, Similarity: {result['similarity']:.3f}")
```

#### Создание веб-приложения для поиска

```python
import streamlit as st
import torch
import clip
from PIL import Image
import os
import numpy as np

class ImageSearchApp:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.image_features = None
        self.image_paths = []
    
    def index_images(self, image_folder):
        """Индексируем изображения в папке"""
        image_paths = []
        for filename in os.listdir(image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(image_folder, filename))
        
        # Вычисляем embeddings для всех изображений
        image_features = []
        for path in image_paths:
            image = self.preprocess(Image.open(path)).unsqueeze(0).to(self.device)
            with torch.no_grad():
                features = self.model.encode_image(image)
                features = F.normalize(features, dim=-1)
                image_features.append(features)
        
        self.image_features = torch.cat(image_features)
        self.image_paths = image_paths
        
        print(f"Проиндексировано {len(image_paths)} изображений")
    
    def search(self, query_text, top_k=5):
        """Поиск изображений по текстовому запросу"""
        if self.image_features is None:
            return []
        
        # Кодируем текстовый запрос
        text_tokens = clip.tokenize([query_text]).to(self.device)
        
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            text_features = F.normalize(text_features, dim=-1)
            
            # Вычисляем схожесть
            similarities = torch.matmul(text_features, self.image_features.T)
            similarities = similarities.squeeze().cpu().numpy()
        
        # Ранжируем результаты
        top_indices = similarities.argsort()[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                'image_path': self.image_paths[idx],
                'similarity': similarities[idx]
            })
        
        return results

# Streamlit веб-приложение
def main():
    st.title("🔍 CLIP Image Search")
    st.write("Поиск изображений по текстовому описанию")
    
    # Инициализация приложения
    if 'search_app' not in st.session_state:
        st.session_state.search_app = ImageSearchApp()
    
    # Загрузка изображений
    st.header("📁 Индексация изображений")
    image_folder = st.text_input("Путь к папке с изображениями:", "images/")
    
    if st.button("Индексировать изображения"):
        if os.path.exists(image_folder):
            st.session_state.search_app.index_images(image_folder)
            st.success(f"Проиндексировано изображений: {len(st.session_state.search_app.image_paths)}")
        else:
            st.error("Папка не найдена!")
    
    # Поиск
    st.header("🔍 Поиск")
    query = st.text_input("Введите описание изображения:", "a cat sitting on a table")
    top_k = st.slider("Количество результатов:", 1, 10, 5)
    
    if st.button("Найти"):
        if st.session_state.search_app.image_features is not None:
            results = st.session_state.search_app.search(query, top_k)
            
            st.header("📊 Результаты")
            for i, result in enumerate(results):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    try:
                        image = Image.open(result['image_path'])
                        st.image(image, caption=f"Similarity: {result['similarity']:.3f}")
                    except Exception as e:
                        st.error(f"Ошибка загрузки изображения: {e}")
                
                with col2:
                    st.write(f"**Путь:** {result['image_path']}")
                    st.write(f"**Схожесть:** {result['similarity']:.3f}")
                    st.write("---")
        else:
            st.warning("Сначала проиндексируйте изображения!")

if __name__ == "__main__":
    main()
```

### 🎨 Генерация изображений по тексту (DALL-E концепция)

```python
class SimpleTextToImage(nn.Module):
    def __init__(self, text_encoder, image_decoder):
        super(SimpleTextToImage, self).__init__()
        self.text_encoder = text_encoder
        self.image_decoder = image_decoder
        
    def forward(self, text_tokens):
        # Кодируем текст
        text_features = self.text_encoder(text_tokens)
        
        # Генерируем изображение
        generated_image = self.image_decoder(text_features)
        
        return generated_image

class ImageDecoder(nn.Module):
    def __init__(self, text_dim=512, image_size=64):
        super(ImageDecoder, self).__init__()
        
        self.text_projection = nn.Linear(text_dim, 1024)
        
        # Генератор изображений
        self.generator = nn.Sequential(
            # Входной слой
            nn.Linear(1024, 8 * 8 * 512),
            nn.ReLU(),
            
            # Reshape
            nn.Unflatten(1, (512, 8, 8)),
            
            # Upsampling блоки
            nn.ConvTranspose2d(512, 256, 4, 2, 1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            
            nn.ConvTranspose2d(256, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            
            nn.ConvTranspose2d(128, 64, 4, 2, 1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            
            nn.ConvTranspose2d(64, 3, 3, 1, 1),
            nn.Tanh()
        )
    
    def forward(self, text_features):
        # Проецируем текстовые features
        x = self.text_projection(text_features)
        
        # Генерируем изображение
        image = self.generator(x)
        
        return image
```

### 📊 Оценка качества мультимодальных моделей

```python
def evaluate_clip_model(model, test_dataloader):
    """Оценка качества CLIP модели"""
    model.eval()
    
    total_accuracy = 0
    total_samples = 0
    
    with torch.no_grad():
        for images, text_tokens in test_dataloader:
            batch_size = images.size(0)
            
            # Forward pass
            logits, _, _ = model(images, text_tokens)
            
            # Вычисляем accuracy
            # Для каждого изображения правильный текст должен иметь максимальную схожесть
            predicted_texts = logits.argmax(dim=1)
            true_labels = torch.arange(batch_size)
            
            accuracy = (predicted_texts == true_labels).float().mean()
            total_accuracy += accuracy.item() * batch_size
            total_samples += batch_size
    
    return total_accuracy / total_samples

def zero_shot_classification(model, image, class_names):
    """Zero-shot классификация с помощью CLIP"""
    
    # Создаем текстовые промпты для каждого класса
    text_prompts = [f"a photo of a {class_name}" for class_name in class_names]
    text_tokens = clip.tokenize(text_prompts).to(device)
    
    # Обрабатываем изображение
    image_tensor = preprocess(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        # Получаем embeddings
        text_features = model.encode_text(text_tokens)
        image_features = model.encode_image(image_tensor)
        
        # Нормализуем
        text_features = F.normalize(text_features, dim=-1)
        image_features = F.normalize(image_features, dim=-1)
        
        # Вычисляем схожесть
        similarities = torch.matmul(image_features, text_features.T)
        probabilities = F.softmax(similarities * 100, dim=-1)
    
    # Возвращаем результаты
    results = []
    for i, class_name in enumerate(class_names):
        results.append({
            'class': class_name,
            'probability': probabilities[0, i].item()
        })
    
    # Сортируем по убыванию вероятности
    results.sort(key=lambda x: x['probability'], reverse=True)
    
    return results

# Пример использования
image = Image.open("test_image.jpg")
classes = ["cat", "dog", "bird", "car", "airplane"]
results = zero_shot_classification(model, image, classes)

for result in results[:3]:
    print(f"{result['class']}: {result['probability']:.3f}")
```

### 🏆 Практические результаты
- ✅ Реализация простой CLIP модели
- ✅ Создание поисковика изображений по тексту
- ✅ Zero-shot классификация
- ✅ Веб-приложение для демонстрации

---

## 🎯 Итоговый проект блока

### Задание: Создание мультимодальной генеративной системы

**Цель:** Объединить знания всех глав в один проект

**Компоненты системы:**
1. **VAE** для генерации изображений
2. **CLIP** для связи текста и изображений
3. **GAN** для улучшения качества
4. **Веб-интерфейс** для взаимодействия

### Архитектура проекта

```
                    МУЛЬТИМОДАЛЬНАЯ СИСТЕМА
    
    Текстовый запрос: "Красивый закат над океаном"
                                │
                                ↓
                        [CLIP Text Encoder]
                                │
                                ↓
                        Текстовые embeddings
                                │
                                ↓
                        [VAE Decoder]
                                │
                                ↓
                        Базовое изображение
                                │
                                ↓
                        [GAN Generator]
                                │
                                ↓
                        Финальное изображение 🌅
```

### Критерии оценки

```
📊 ОЦЕНКА ПРОЕКТА (100 баллов):

✅ Техническая реализация (40 баллов):
   • Корректность архитектуры
   • Качество кода
   • Производительность

✅ Качество результатов (30 баллов):
   • Реалистичность генерации
   • Соответствие текстовому описанию
   • Разнообразие результатов

✅ Пользовательский интерфейс (20 баллов):
   • Удобство использования
   • Визуальное оформление
   • Функциональность

✅ Документация (10 баллов):
   • Описание архитектуры
   • Инструкции по использованию
   • Примеры результатов
```

---

## 🎓 Заключение блока

### Чему вы научились:

```
🧠 ТЕОРЕТИЧЕСКИЕ ЗНАНИЯ:
├── Математические основы генеративных моделей
├── Принципы adversarial training
├── Диффузионные процессы
├── Meta-learning концепции
└── Мультимодальное обучение

💻 ПРАКТИЧЕСКИЕ НАВЫКИ:
├── Реализация 6 типов генеративных моделей
├── Создание веб-приложений с ML
├── Оценка качества генерации
├── Работа с мультимодальными данными
└── Оптимизация сложных архитектур

🚀 ГОТОВНОСТЬ К ПРИМЕНЕНИЮ:
├── Создание генеративных приложений
├── Исследование новых архитектур
├── Работа с SOTA моделями
└── Решение реальных задач
```

### Следующие шаги:

1. **Изучите новые архитектуры:** Stable Diffusion, DALL-E 2, Midjourney
2. **Экспериментируйте с параметрами:** Различные loss functions, архитектуры
3. **Создайте портфолио:** Демонстрируйте различные генеративные проекты
4. **Следите за исследованиями:** Новые статьи и методы в области генеративных моделей

### Полезные ресурсы:

```
📚 ДОПОЛНИТЕЛЬНОЕ ИЗУЧЕНИЕ:
├── Papers With Code (Generative Models)
├── Hugging Face Transformers
├── OpenAI API Documentation
├── Stability AI Research
└── Google Research Blog

🛠️ ИНСТРУМЕНТЫ:
├── PyTorch / TensorFlow
├── Hugging Face Diffusers
├── OpenAI CLIP
├── Streamlit / Gradio
└── Weights & Biases
```

**🎉 Поздравляем с завершением блока "Генеративные модели и продвинутые техники"!**

Вы теперь владеете одной из самых захватывающих областей глубокого обучения. Генеративные модели открывают безграничные возможности для творчества и инноваций. Используйте полученные знания для создания удивительных приложений и продолжайте исследовать эту быстро развивающуюся область!