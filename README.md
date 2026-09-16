### Тестовое задание, REST API для бронирования столиков


## Стек

- Python 3.11+
- FastAPI + Pydantic
- SQLAlchemy
- SQLite
- Alembic
- pytest


## Локальный запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/lwyruup/mise_booking_api.git
cd mise_booking_api
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Для Windows:

```bash
.venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Применить миграции
```bash
alembic upgrade head
```

### 5. Запустить приложение

```bash
uvicorn main:app --reload
```

## Запуск через Docker

Для запуска приложения через Docker Compose:

```bash
docker compose up
```

После запуска API будет доступно на:

```text
http://localhost:8000
```


Swagger:

```text
http://localhost:8000/docs
```

Миграции Alembic при запуске контейнера применяются автоматически.


## Тесты

Для запуска тестов:

```bash
pytest
```

Для запуска тестов с отчётом о покрытии:

```bash
pytest --cov=app
```
Покрытие тестами - 84%

## Принятые решения

Для хранения данных выбрана SQLite с асинхронным SQLAlchemy, поскольку для задачи не требуется внешняя БД, при этом такой вариант позволяет сохранить полноценный слой работы с базой данных.  Для управления схемой базы используется Alembic. Отмена брони реализована как soft delete через изменение статуса на `cancelled`, поэтому история бронирований сохраняется. Реализована также проверка конфликта активных броней.

## Что можно было бы добавить

При наличии доп. времени я бы  расширил набор тестов для граничных случаев, добавил бы пагинация. Также для production-сценария можно было перейти на PostgreSQL, добавить авторизацию.
