# Благотворительный фонд помощи кошкам QRKOT

Благотворительный фонд помощи кошкам QRKOT, специализируется на том, чтобы помогать кошкам, создавая благотворительные сборы, где каждый желающий зарегистрированный пользователь, может пожертвовать свои деньги на помощь кошкам.

### Технологии
- Python
- Pydantic
- FastApi
- SQLAlchemy
- Аlembic
- SQLite
- aiogoogle

## Установка

1. Склонируйте репозиторий.
```bash
git clone https://github.com/daniltivodar/QRkot_spreadsheets.git
```

2. Создайте и активируйте виртуальное окружение, заполнив его зависимостями из файла **requirements.txt**.
```bash
cd QRKOT_SPREADSHEETS
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

3. Наполнить файл .env следующими командами:
```bash
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
DESCRIPTION=Сервис для поддержки котиков!
FIRST_SUPERUSER_EMAIL=admin@gmail.com
FIRST_SUPERUSER_PASSWORD=MY_SECRET_PASSWORD

# для google api
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

4. Запуск:
Создать базу данных и применить миграции можно командой:
```bash
alembic upgrade head
```
Запустить сервис можно командой:
```bash
uvicorn app.main:app --reload
```

## API documentation
**[Апи документация redoc](http://127.0.0.1:8000/redoc)**
**[Апи документация swagger](http://127.0.0.1:8000/docs)**

## Создатель
**[Данил Тиводар](https://github.com/daniltivodar)**
