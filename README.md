# 🛒 **ElectroEmporium** 

**Проект "Магазин электроники"** - это веб-приложение, предназначенное для предоставления пользователям возможности покупать и искать электронные товары онлайн. Здесь представлен широкий выбор электроники: от компьютеров и смартфонов до телевизоров и фотоаппаратов.

## 🚀 **Начало работы:**

1. **📦 Клонирование репозитория:**
    ```bash
    git clone https://github.com/sntx10/ElectroEmporium.git
    ```

2. **🛠 Создание виртуальной среды:**
    ```bash
    python3 -m venv <name of your environment>
    ```

3. **🌀 Активация виртуальной среды:**
    ```bash
    source <name of your environment>/bin/activate
    ```

4. **⚙ Установка зависимостей:**
    ```bash
    pip install -r requirements.txt
    ```

5. **🔑 Настройка конфигурации:**
    ```bash
    Переименуйте файл env_example в .env.
    Обновите значения в файле .env соответствующим образом.
    ```

6. **🗄 Применение миграций:**
    ```bash
    ./manage.py migrate
    ```

7. **🌍 Запуск проекта:** Вы можете использовать любой из следующих способов:
    ```
    ./manage.py runserver
    ```
    или
    ```
    python3 manage.py runserver
    ```
    или
    ```
    make run
    ```

## 🛠 **Возможности Makefile:**

- **👤 Создание суперпользователя:**
    ```
    make user
    ```

- **🔧 Применение миграций:**
    ```
    make migrate
    ```

- **📡 Запуск Celery:**
    ```
    make celery
    ```

- **⏰ Запуск Celery Beat:**
    ```
    make beat
    ```

- **🌐 Запуск ngrok (для предоставления API фронтенду):**
    ```
    make ngrok
    ```

## 🖋 **Заключение:**

Проект "Магазин электроники" был разработан с целью обеспечения удобного и надежного интерфейса для покупки электроники онлайн. Мы надеемся, что это руководство поможет вам легко настроить и начать работу с нашим проектом. 🤝
