# Backend — лабораторная работа №2

Серверная часть **Tournament App** на Python, FastAPI, SQLAlchemy 2, Pydantic и PostgreSQL.

Полное описание сущностей, REST-эндпоинтов, бизнес-правил и примеры JSON приведены в [главном README](../README.md).

## Быстрый запуск (Windows PowerShell)

1. Создайте в PostgreSQL базу `tournament_db` (в pgAdmin).
2. Из корня проекта выполните:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

3. Настройте `DATABASE_URL` в `.env`, указав фактический пароль и порт PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5433/tournament_db
```

В данном учебном окружении PostgreSQL 17 использует порт **5433**. У других установок может использоваться **5432**. Не публикуйте файл `.env`.

4. Запустите API:

```powershell
python -m uvicorn app.main:app --reload
```

Swagger UI: <http://127.0.0.1:8000/docs>.

На старте вызывается `Base.metadata.create_all()`, создающий отсутствующие таблицы `tournaments`, `teams`, `players`, `matches`. Для изменения уже существующих таблиц нужны миграции (например, Alembic).

## Структура

- `app/main.py` — экземпляр FastAPI, подключение роутеров и CORS.
- `app/config.py` — чтение переменных среды.
- `app/database.py` — подключение SQLAlchemy и сессия БД.
- `app/models/entities.py` — ORM-таблицы, ключи, связи и ограничения.
- `app/schemas/entities.py` — схемы Pydantic для JSON-запросов и ответов.
- `app/api/tournaments.py` — CRUD турниров.
- `app/api/teams.py` — CRUD команд.
- `app/api/players.py` — CRUD игроков.
- `app/api/matches.py` — CRUD матчей.
- `app/api/common.py` — общие проверки, сохранение и расчёт статусов.

Реализовано 20 маршрутов: POST/GET списка/GET одного/PUT/DELETE для каждого из четырёх ресурсов. `PATCH` и префикс `/api/v1` в этой версии **ещё не добавлены**.

## Проверка

Через Swagger создайте турнир `POST /tournaments`, затем получите его через `GET /tournaments`. После этого зарегистрируйте команду и добавьте пять игроков, включая капитана. Для матча потребуются две полностью укомплектованные команды.

Коды ответа: `201` при создании, `200` при чтении/обновлении, `204` при удалении, `404` для отсутствующих ресурсов, `409` для конфликтов бизнес-правил, `422` при ошибке входных данных.
