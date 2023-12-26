# Foodgram

**Foodgram** — это веб-приложение, которое позволяет пользователям создавать, просматривать и обмениваться рецептами. Оно также предоставляет возможность подписываться на понравившихся авторов, добавлять рецепты в избранное и генерировать списки покупок в .txt на основе выбранных рецептов. Это полностью рабочий проект, который состоит из бэкенд-приложения на Django и фронтенд-приложения на React.

## Функции

- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление рецептов
- Поиск рецептов по различным тегам
- Подписка на авторов
- Добавление рецептов в избранное
- Генерация списка покупок на основе выбранных рецептов

## Структура проекта

```
├── backend/             # Файлы бэкенда (Django)
├── docs/                # Файлы документации
├── frontend/            # Файлы фронтенда (React)
├── infra/               # Файлы для настройки Docker-контейнеров
├── postman-collection/  # Файлы для проверки работы API
├── .env.example         # Файл-пример переменных окружения
├── .gitignore           # Файл для игнорирования файлов
├── README.md            # Файл с инструкциями (этот документ)
└── setup.cfg            # Файл конфигурации
```

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:andrew12022/foodgram-project-react.git
```

```
cd foodgram-project-react/backend
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать файл `.env` в исходной папке проекта:

```.env
POSTGRES_USER=foodram_user
POSTGRES_PASSWORD=foodram_password
POSTGRES_DB=foodgram
DB_HOST=db
DB_PORT=5432
SECRET_KEY='указать секретный ключ'
DEBUG=указать режим работы(False или True)
ALLOWED_HOSTS=указать внешний IP сервера, 127.0.0.1, localhost, домен(через запятые, без пробелов)
```

Выполнить миграции:

```
python manage.py migrate
```

### Контейнеризация

Перейти в папку /infra в командной строке:
```
cd infra
```

Из папки infra/ развернуть контейнеры при помощи docker-compose.production.yml:
```
docker compose -f docker-compose.production.yml up
```

Выполнить миграции:
```
docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

Собрать статику:
```
docker compose -f docker-compose.production.yml exec backend python manage.py collecstatic
```

Создать суперпользователя:
```
docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

Наполнить базу данных ингредиентами и тегами:
```
docker compose -f docker-compose.production.yml exec backend python manage.py import_json
```

## Технологии и необходимые инструменты
- Python 3.9
- Django 3.2.16
- PostgreSQL
- Docker
- Node.js 9.x.x
- Nginx
- Gunicorn 20.x.x
- React 
- python-dotenv
- DRF
- Djoser

## Ссылка на проект
- [Адрес веб-приложения](https://andrew12022.hopto.org/)
- [Адрес документации](https://andrew12022.hopto.org/api/docs/)

## Автор
- [Андрей Елистратов](https://github.com/andrew12022)
