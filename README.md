# Благотворительный фонд помощи кошкам cat_charity_fund

Благотворительный фонд помощи кошкам cat_charity_fund, специализируется на том, чтобы помогать кошкам, создавая благотворительные сборы, где каждый желающий зарегистрированный пользователь, может пожертвовать свои деньги на помощь кошкам.

### Технологии
- Python
- Pydantic
- FastApi
- SQLAlchemy
- Аlembic
- SQLite

## Установка

1. Склонируйте репозиторий.
```bash
git clone https://github.com/daniltivodar/cat_charity_fund.git
```

2. Создайте и активируйте виртуальное окружение, заполнив его зависимостями из файла **requirements.txt**.
```bash
cd cat_charity_fund
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
