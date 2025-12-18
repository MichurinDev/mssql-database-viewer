# MSSQL Database Viewer

## Backend

REST API для работы с сущностями проекта: `Project`, `Task`, `Comment`, `Attachment`

*Стек: Python, FastAPI, SQLAlchemy, pymssql; конфигурация через `.env`*

### Архитектура

- **API слой:** `app/backend/api.py` – FastAPI endpoints для CRUD, фильтрации, сортировки, агрегаций и отчётов.
- **Бизнес-логика / CRUD:** `app/backend/crud/crud.py` – функции создания/чтения/обновления/удаления через SQLAlchemy Session.
- **Модели:** `app/backend/models/models.py` – SQLAlchemy ORM-модели и отношения (relations & cascade).
- **Схемы:** `app/backend/schemas.py` – Pydantic-схемы для валидации и сериализации.
- **SQL-артефакты:** `schemas/sql/` – T-SQL скрипты (индексы, хранимые процедуры, триггеры).
- **Утилиты:** `scripts/apply_sql.py` – простая утилита для применения `.sql` файлов (разделитель `GO`).

### База данных

- **СУБД:** Microsoft SQL Server (MSSQL).
- **Подключение:** через `pymssql`; параметры берутся из `.env` (host, port, user, password, database).

### Файловая структура и ключевые файлы

- `main.py` – единая точка входа (запуск FastAPI/uvicorn).
- `app/backend/api.py` – маршруты и эндпоинты.
- `app/backend/models/models.py` – ORM-сущности.
- `app/backend/crud/crud.py` – операции с БД.
- `app/backend/schemas.py` – Pydantic-схемы.
- `schemas/sql/` – SQL-скрипты (create indexes, procedures, triggers).
- `scripts/apply_sql.py` – выполнение SQL-файлов на MSSQL.

### API возможности

- CRUD для `projects`, `tasks`, `comments`, `attachments`.
- Фильтрация/сортировка/пагинация через query params: `filter`, `sort`, `limit`, `offset`.
- Агрегаты и отчёты (count, sum, join-отчёты) доступны отдельными endpoints.

## Frontend
