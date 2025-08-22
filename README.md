# Благотворительный фонд помощи кошкам QRKOT

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4+-red.svg)](https://www.sqlalchemy.org/)

Благотворительный фонд помощи кошкам QRKOT специализируется на организации сбора пожертвований для помощи кошкам. Зарегистрированные пользователи могут создавать благотворительные сборы и делать пожертвования.

## Возможности

### Основной функционал
- Создание и управление благотворительными сборами
- Система пожертвований для зарегистрированных пользователей
- Полная документация API (Swagger/ReDoc)

### Интеграции
- Работа с Google Sheets через API
- Автоматическое обновление отчетов в таблицах
- Синхронизация данных с внешними сервисами

### Безопасность
- Аутентификация и авторизация пользователей
- Валидация данных через Pydantic
- Защищенные соединения и обработка данных

## Технологический стек

- Python 3.9+ - Основной язык программирования
- FastAPI - Современный асинхронный фреймворк
- SQLAlchemy - ORM для работы с базой данных
- Alembic - Управление миграциями базы данных
- Pydantic - Валидация и сериализация данных
- SQLite - База данных (может быть заменена на PostgreSQL)
- aiogoogle - Асинхронный клиент для Google API

## Быстрый старт

### Предварительные требования
- Python 3.9 или новее
- Виртуальное окружение
- Аккаунт Google для работы с API (опционально)

### Установка и настройка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/daniltivodar/QRkot_spreadsheets.git
cd QRkot_spreadsheets
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте окружение:
Создайте файл .env и заполните его по примеру:
```bash
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
DESCRIPTION=Сервис для поддержки котиков!
FIRST_SUPERUSER_EMAIL=admin@gmail.com
FIRST_SUPERUSER_PASSWORD=MY_SECRET_PASSWORD

# для Google API
API_TYPE=service_account
API_PROJECT_ID=idid
API_PRIVATE_KEY_ID="1337qwerty"
API_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n1337qwerty\n-----END PRIVATE KEY-----\n"
API_CLIENT_EMAIL=project@qwerty11.iam.gserviceaccount.com
API_CLIENT_ID=1234567890
API_AUTH_URI=https://accounts.google.com/o/oauth2/auth
API_TOKEN_URI=https://oauth2.googleapis.com/token
API_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
API_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/project@qwerty11.iam.gserviceaccount.com
API_UNIVERSE_DOMAIN=googleapis.com
API_EMAIL=you_email@gmail.com
```

5. Примените миграции базы данных:
```bash
alembic upgrade head
```

6. Запустите сервис:
```bash
uvicorn app.main:app --reload
```

## Документация API

После запуска сервиса документация доступна по адресам:
- ReDoc: http://127.0.0.1:8000/redoc
- Swagger UI: http://127.0.0.1:8000/docs

## Разработчик

**Данил Тиводар**  
[GitHub Профиль](https://github.com/daniltivodar)
