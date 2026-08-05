# Auth Service

Сервис аутентификации и авторизации на **FastAPI** с поддержкой JWT-токенов, хранящихся в cookie, и асинхронной работой с базой данных.

## 🚀 Технологии

- **FastAPI** — быстрый фреймворк для создания API
- **SQLAlchemy 2.0** — ORM с асинхронной поддержкой
- **AuthX** — библиотека для работы с JWT-токенами
- **pwdlib + argon2** — хеширование паролей
- **Alembic** — миграции базы данных
- **SQLite** (aiosqlite) — база данных по умолчанию

## 📦 Установка

### Локальная разработка

```bash
# Создайте виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Установите зависимости
pip install -r requirements.txt
```

### Docker

```bash
docker build -t auth-service .
```

## ⚙️ Настройка

Конфигурация находится в `settings.py`. Основные параметры:

| Параметр                          | Описание                      | Значение по умолчанию              |
|-----------------------------------|-------------------------------|------------------------------------|
| `SECRET_KEY`                      | Ключ для подписи JWT          | `secret_key` (замените на-production!) |
| `ALGORITHM`                       | Алгоритм JWT                  | `HS256`                            |
| `ACCESS_TOKEN_EXPIRE_MINUTES`     | Время жизни access-токена     | `15` минут                         |
| `REFRESH_TOKEN_EXPIRE_MINUTES`    | Время жизни refresh-токена    | `10080` минут (7 дней)             |
| `DB_URL`                          | URL подключения к БД          | `sqlite+aiosqlite:///database.db`  |
| `ALLOWED_HOSTS`                   | Разрешённые CORS- origins     | `["http://localhost:5173", ...]`   |

### Генерация SECRET_KEY

```bash
openssl rand -hex 32
```

## 🏃 Запуск

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🗄️ Миграции

```bash
# Создание новой миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

## 📡 API Endpoints

Все endpoints находятся по пути `/api/auth`.

### Auth

| Метод    | Endpoint       | Описание                  | Тело запроса              |
|----------|----------------|---------------------------|---------------------------|
| `POST`   | `/login`       | Вход в систему            | `{email, password, remember?}` |
| `POST`   | `/registration`| Регистрация нового пользователя | `{email, password, first_name?, last_name?}` |
| `POST`   | `/logout`      | Выход из системы          | —                         |
| `GET`    | `/refresh`     | Обновление токенов        | —                         |

### User

| Метод    | Endpoint       | Описание                  |
|----------|----------------|---------------------------|
| `GET`    | `/user/me`     | Получить данные текущего пользователя |

### Примеры запросов

**Регистрация:**

```bash
curl -X POST http://localhost:8000/api/auth/registration \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "first_name": "Ivan",
    "last_name": "Petrov"
  }'
```

**Вход:**

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "remember": true
  }'
```

**Получить данные пользователя:**

```bash
curl http://localhost:8000/api/auth/user/me \
  -H "Cookie: access_token=...; refresh_token=..."
```

## 📁 Структура проекта

```
auth/
├── src/
│   ├── routes/           # API endpoints
│   │   ├── auth.py       # Логин, регистрация, logout, refresh
│   │   └── user.py       # Профиль пользователя
│   ├── models/           # SQLAlchemy модели
│   │   ├── user.py       # Модель пользователя
│   │   └── base.py       # Базовая модель
│   ├── schemas/          # Pydantic схемы
│   │   └── user.py       # Сериализация данных пользователя
│   ├── services/         # Бизнес-логика
│   │   ├── user.py       # Сервис работы с пользователями
│   │   ├── security.py   # Хеширование паролей
│   │   └── password_validators.py # Валидация паролей
│   ├── auth.py           # JWT-аутентификация (AuthX)
│   ├── database.py       # Асинхронный движок SQLAlchemy
│   ├── dependencies.py   # FastAPI зависимости
│   ├── error_handlers.py # Обработка ошибок
│   └── main.py           # Точка входа (FastAPI app)
├── src/migrations/        # Alembic миграции
├── settings.py            # Конфигурация приложения
├── requirements.txt       # Зависимости
├── Dockerfile             # Сборка Docker
└── alembic.ini            # Конфигурация Alembic
```

## 🔒 Безопасность

- Пароли хешируются с помощью **Argon2** через `pwdlib`
- JWT-токены хранятся в **httpOnly cookie**
- Поддержка `remember me` для длительного сеанса
- Валидация паролей с проверкой сложности

## 📝 Лицензия

MIT
