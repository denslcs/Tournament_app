# Tournament App

Учебное fullstack-приложение для организации киберспортивных турниров. Проект выполняется поэтапно в рамках лабораторных работ курса **Fullstack**.

## Назначение и сценарии

В приложении можно создавать турниры по выбранной игре (Dota 2, Counter-Strike 2, League of Legends, Valorant, Fortnite), указывать количество команд (8 или 16), призовой фонд в рублях и даты проведения. Команды занимают свободные места в турнире, после чего в состав каждой добавляют пять игроков и назначают капитана. Для полностью укомплектованных команд можно назначать матчи и фиксировать результаты.

Авторизация и управление пользователями пока не реализованы.

## Технологии

| Часть | Технологии |
| --- | --- |
| Frontend (ЛР №1) | React, TypeScript, Vite |
| Backend (ЛР №2) | Python, FastAPI, Pydantic |
| База данных и ORM | PostgreSQL, SQLAlchemy 2, psycopg |
| API-документация | Swagger UI (OpenAPI) |
| Контроль версий | Git, GitHub |

## Структура репозитория

```text
Tournament_app/
├── frontend/             # React + TypeScript, лабораторная №1 (ветка front)
│   └── src/
│       ├── pages/        # HomePage, TournamentsPage, MatchPage
│       └── data/         # Пока демонстрационные данные турниров
├── backend/              # FastAPI, лабораторная №2 (ветка backend)
│   ├── app/
│   │   ├── api/          # Маршруты и CRUD
│   │   ├── models/       # Таблицы и связи SQLAlchemy
│   │   ├── schemas/      # Проверка данных Pydantic
│   │   ├── config.py     # Настройки из окружения
│   │   ├── database.py   # Движок SQLAlchemy и сессии
│   │   └── main.py       # Создание приложения FastAPI
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md          # Подробная инструкция по API
├── docs/
│   └── screenshots/      # Скриншоты для отчёта
└── README.md
```

**Примечание о ветках:** исходный frontend расположен в ветке `front`, backend разрабатывается в ветке `backend`, основная ветка — `main`. До слияния веток соответствующие папки могут отсутствовать в текущей ветке.

## Как запустить backend (Windows)

**Требуется:** Python 3.11+ и запущенный PostgreSQL. В pgAdmin создайте базу данных `tournament_db`.

Из корня проекта:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

В `backend/.env` установите свои параметры подключения:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5433/tournament_db
```

Порт **5433** указан для локального PostgreSQL 17, использовавшегося при выполнении лабораторной. На другом компьютере порт может быть **5432** или иным; проверьте его в pgAdmin → Server → Properties → Connection. Если пароль содержит специальные символы URL, их необходимо закодировать.

Запуск из папки `backend`:

```powershell
python -m uvicorn app.main:app --reload
```

- Swagger UI: <http://127.0.0.1:8000/docs>
- OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>

При запуске SQLAlchemy создаёт отсутствующие таблицы через `Base.metadata.create_all()`. Это учебный способ и **не заменяет миграции** при изменении структуры существующих таблиц.

> Файл `.env` содержит секреты и не должен попадать в Git. В репозитории хранится только `.env.example`.

## Как запустить frontend

Если в текущей ветке доступна папка `frontend`:

```powershell
cd frontend
npm install
npm run dev
```

После запуска Vite открывается локальный адрес, обычно <http://localhost:5173/>. На этапе лабораторной №1 интерфейс использует данные из `src/data/tournaments.ts`; **подключение React к API ещё не выполнено**.

## Модель данных

В PostgreSQL созданы четыре связанные таблицы:

- **`tournaments`** — название, игра, вместимость, призовой фонд, даты начала/окончания, признак завершения/отмены.
- **`teams`** — название команды и внешний ключ `tournament_id`.
- **`players`** — никнейм, имя, фамилия, `is_captain` и внешний ключ `team_id`.
- **`matches`** — внешний ключ `tournament_id`, ссылки на две команды, время матча и счёт.

Связи: `tournament → teams → players` и `tournament → matches`; каждый матч содержит ссылки на две команды. Используются первичные и внешние ключи, ограничения уникальности и проверки целостности.

## REST API

Все приведённые маршруты относятся к текущей версии бэкенда. Базовый адрес: `http://127.0.0.1:8000`. Формат запросов и ответов — JSON.

| Метод | Маршрут | Назначение |
| --- | --- | --- |
| POST | `/tournaments` | Создать турнир |
| GET | `/tournaments` | Получить список турниров |
| GET | `/tournaments/{tournament_id}` | Получить турнир |
| PUT | `/tournaments/{tournament_id}` | Заменить изменяемые параметры турнира |
| DELETE | `/tournaments/{tournament_id}` | Удалить турнир |
| POST | `/tournaments/{tournament_id}/teams` | Создать команду и занять слот |
| GET | `/tournaments/{tournament_id}/teams` | Список команд |
| GET | `/tournaments/{tournament_id}/teams/{team_id}` | Команда с игроками |
| PUT | `/tournaments/{tournament_id}/teams/{team_id}` | Изменить название команды |
| DELETE | `/tournaments/{tournament_id}/teams/{team_id}` | Отменить регистрацию команды |
| POST | `/tournaments/{tournament_id}/teams/{team_id}/players` | Добавить игрока |
| GET | `/tournaments/{tournament_id}/teams/{team_id}/players` | Игроки команды |
| GET | `/tournaments/{tournament_id}/teams/{team_id}/players/{player_id}` | Получить игрока |
| PUT | `/tournaments/{tournament_id}/teams/{team_id}/players/{player_id}` | Изменить игрока |
| DELETE | `/tournaments/{tournament_id}/teams/{team_id}/players/{player_id}` | Удалить игрока |
| POST | `/tournaments/{tournament_id}/matches` | Назначить матч |
| GET | `/tournaments/{tournament_id}/matches` | Матчи турнира |
| GET | `/tournaments/{tournament_id}/matches/{match_id}` | Получить матч |
| PUT | `/tournaments/{tournament_id}/matches/{match_id}` | Изменить матч/записать результат |
| DELETE | `/tournaments/{tournament_id}/matches/{match_id}` | Удалить матч |

В текущем коде для обновлений используется `PUT` с обязательными полями схемы; `PATCH` и префикс `/api/v1` пока не реализованы. Планируются при дальнейшем развитии API.

### Пример: создать турнир

`POST /tournaments`

```json
{
  "name": "Dota 2 Championship",
  "game": "dota2",
  "capacity": 8,
  "prize_rub": 50000,
  "registration_closes_at": "2026-12-01T18:00:00+03:00",
  "starts_at": "2026-12-05T18:00:00+03:00",
  "ends_at": "2026-12-10T18:00:00+03:00"
}
```

### Пример: зарегистрировать команду

`POST /tournaments/1/teams`

```json
{"name": "Night Wolves"}
```

Команда сразу занимает одно место турнира, даже если в ней пока нет игроков.

### Пример: добавить игрока

`POST /tournaments/1/teams/1/players`

```json
{
  "nickname": "Shadow",
  "first_name": "Иван",
  "last_name": "Иванов",
  "is_captain": true
}
```

В составе максимум пять игроков. Капитан один; назначение нового капитана снимает этот статус с предыдущего. Для назначения матча у обеих команд должны быть пять игроков и капитан.

### Пример: назначить матч

`POST /tournaments/1/matches`

```json
{
  "home_team_id": 1,
  "away_team_id": 2,
  "scheduled_at": "2026-12-05T19:00:00+03:00"
}
```

Матч назначается между зарегистрированными командами одного турнира. ID команд в примере условные.

## Бизнес-правила и статусы

- В турнире может быть **8 или 16** команд; игры выбираются из `dota2`, `cs2`, `lol`, `valorant`, `fortnite`.
- Регистрация команды доступна, пока статус турнира — **«Регистрация»** и есть свободные места.
- Статусы турнира: **Регистрация → Скоро → Идёт → Завершён**; возможна **Отмена**. Вычисляются из дат и признаков `finished` / `canceled`.
- Матчи имеют статусы **Ожидается**, **Идёт**, **Завершён**. «Идёт» сейчас определяется по запланированному времени (учебное упрощение).
- Изменение состава команды допускается во время регистрации и до назначения ей матча.
- Назначить матч можно только полностью укомплектованным командам.

## Проверка лабораторной №2

Проверка проводится в Swagger UI: создать турнир (ожидается **201**), получить его через GET (**200**), создать команду, добавить игроков, назначить матч, выполнить обновление через PUT и удаление через DELETE (**204**). Отдельно проверяются ошибки: **404** — запись не найдена, **409** — конфликт бизнес-правил, **422** — неверные входные данные.

В pgAdmin результат можно проверить запросом:

```sql
SELECT * FROM public.tournaments ORDER BY id;
```

Для отчёта скриншоты Swagger и таблиц PostgreSQL сохраняются в `docs/screenshots/`. В рамках текущей работы подтверждены запуск Swagger, создание таблиц и успешный `POST /tournaments` (**201 Created**); остальные операции следует проверить перед сдачей.

## Лабораторные работы

- **№1 — Frontend:** страницы, маршрутизация, интерфейс React + TypeScript на демонстрационных данных (`front`).
- **№2 — Backend:** API FastAPI, связанные сущности SQLAlchemy, PostgreSQL, CRUD, валидация и обработка ошибок (`backend`).
- Следующие этапы — интеграция интерфейса с API и дальнейшее развитие приложения.

1 Работа:
Была сделана часть frontend. Добавлены файлы и папки:
Public/
    -icons
    -images
src/
    -data/
        -tournaments.ts
    -pages/
        -HomePage.tsx
        -MatchPage.tsx
        -TournamentsPage.tsx
    -App.tsx

В файлах icons и images я добавил логотипы игр и задний фон сайта

В файле -tournaments.ts я добавил константы для заполнения форм турниров, но пока это файл-мок

В файле -HomePage.tsx я реализовал внешний вид основной страницы
В файле -MatchPage.tsx я реализовал страницы матчей
В файле -TournamentsPage.tsx я реализовал страницу где показаны все турниры

-App.tsx основной файл реализации фронтенда (фоновое изображение, панель навигации, рабочая область и маршрутизации страниц)

запуск frontend:
cd frontend
npm run dev
