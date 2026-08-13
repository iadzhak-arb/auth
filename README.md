# Auth service
[![CI/CD Pipline](https://github.com/iadzhak-arb/auth/actions/workflows/main.yml/badge.svg)](https://github.com/iadzhak-arb/auth/actions)
> Является частью платформы [Arb Scanner](https://github.com/iadzhak-arb)

Сервис аутентификации и авторизации на **FastAPI** с поддержкой JWT-токенов в httpOnly cookie и асинхронной работой с базой данных.

## CI/CD

При каждом `push` в ветку `main` GitHub Actions запускает пайплайн:
- **Линтинг и проверка типов:** flake8
- **Сборка и публикация Docker-образа:** успешный пайплайн публикует образ в Docker Hub [iadzhak/arb-auth](https://hub.docker.com/repository/docker/iadzhak/arb-auth)


## Навигация
- [Стек технологий](#стек-технологий)
- [Возможности](#возможности)
- [Структура проекта](#структура-проекта)
- [Настройка](#настройка)
- [Быстрый старт](#быстрый-старт)
- [API Endpoints](#api-endpoints)

## Стек технологий

- **FastAPI** — фреймворк для создания API
- **SQLAlchemy** — ORM с асинхронной поддержкой
- **AuthX** — библиотека для работы с JWT-токенами
- **pwdlib + argon2** — хеширование паролей
- **Alembic** — миграции базы данных



## Возможности
- **Регистрация пользователей** — создание аккаунта с валидацией email и пароля
- **Аутентификация** — вход/выход с сохранением JWT-токенов в httpOnly cookie
- **JWT-авторизация** — access + refresh токены с поддержкой `remember me`
- **Обновление токенов** — автоматический refresh access-токена через refresh-токен
- **Управление профилем** — просмотр и обновление данных пользователя (имя, email)
- **Смена пароля** — безопасная смена с верификацией старого пароля
- **Валидация паролей** — проверка сложности через `pwdlib` + `argon2`
- **Alembic миграции** — автоматическое управление схемой БД
- **CORS поддержка** — настройка разрешённых origins


## Структура проекта

```
auth/
├── src/
│   ├── routes/           # API endpoints
│   │   ├── auth.py       # Логин, регистрация, logout, refresh
│   │   └── user.py       # Профиль, обновление данных, смена пароля
│   ├── models/           # SQLAlchemy модели
│   │   ├── user.py       # Модель пользователя
│   │   └── base.py       # Базовая модель
│   ├── schemas/          # Pydantic схемы
│   │   └── user.py       # Сериализация данных пользователя
│   ├── services/         # Бизнес-логика
│   │   ├── user.py       # Сервис работы с пользователями
│   │   ├── security.py   # Хеширование паролей
│   │   └── password_validators.py  # Валидация паролей
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


## Настройка

Конфигурация находится в `src/settings.py`.
Переменные окружения:

| Параметр                          | Описание                      | Значение по умолчанию                                                                                                     |
|-----------------------------------|-------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| `ALLOWED_HOSTS`                   | Разрешённые CORS-origins      | `["http://localhost:5173", "http://127.0.0.1:8001", "http://localhost:8001", "http://localhost", "http://192.168.0.100"]` |
| `SECRET_KEY`                      | Ключ для подписи JWT          | `secret_key`                                                                                                              |
| `ALGORITHM`                       | Алгоритм JWT                  | `HS256`                                                                                                                   |
| `ACCESS_TOKEN_EXPIRE_MINUTES`     | Время жизни access-токена     | `15` (минут)                                                                                                              |
| `REFRESH_TOKEN_EXPIRE_MINUTES`    | Время жизни refresh-токена    | `10080` (минут = 7 дней)                                                                                                  |
| `JWT_COOKIE_SECURE`               | Secure-флаг для cookie        | `False`                                                                                                                   |
| `AUTH_DB_TYPE`                         | Тип базы данных               | `sqlite` (`sqlite` / `postgres`)                                                                                          |
| `AUTH_SQLITE_PATH`                     | Путь к SQLite БД              | `database.db`                                                                                                             |
| `AUTH_DB_USER`                         | Имя пользователя PostgreSQL   | `postgres`                                                                                                                |
| `AUTH_DB_PASS`                         | Пароль PostgreSQL             | `postgres`                                                                                                                |
| `AUTH_DB_HOST`                         | Хост PostgreSQL               | `postgres`                                                                                                                |
| `AUTH_DB_PORT`                         | Порт PostgreSQL               | `5432`                                                                                                                    |
| `AUTH_DB_NAME`                         | Имя БД PostgreSQL             | `postgres`                                                                                                                |



## Быстрый старт

### 1. Установка

Настроить окружение
```bash
# Создайте виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Установите зависимости
pip install -r requirements.txt
```

Выполнить миграции
```bash
alembic upgrade head
```


### 2. Запуск
> Перед запуском необходимо настроить переменные окружения.

REST API
```bash
fastapi dev
```



## API Endpoints

Документация API (Swagger): `/api/auth/docs`

### Auth

| Метод    | Endpoint       | Описание                  | Тело запроса              |
|----------|----------------|---------------------------|---------------------------|
| `POST`   | `/api/auth/login`       | Вход в систему            | `{email, password, remember?}` |
| `POST`   | `/api/auth/registration`| Регистрация нового пользователя | `{email, password, first_name?, last_name?}` |
| `POST`   | `/api/auth/logout`      | Выход из системы          | —                         |
| `GET`    | `/api/auth/refresh`     | Обновление токенов        | —                         |

### User

| Метод    | Endpoint                | Описание                              | Тело запроса                      |
|----------|-------------------------|---------------------------------------|-----------------------------------|
| `GET`    | `/api/auth/user/me`              | Получить данные текущего пользователя | —                                 |
| `PUT`    | `/api/auth/user/me`              | Обновить данные пользователя          | `{first_name?, last_name?}`       |
| `PUT`    | `/api/auth/user/change-password` | Сменить пароль                        | `{password}`                      |

