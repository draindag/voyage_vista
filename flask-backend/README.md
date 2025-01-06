## Включение конфигурационного файла в проект

Перед запуском сервера обязательно добавьте в папку flask-backend переданный вам `.env` файл

## Создание виртуального окружения

Чтобы создать виртуальное окружение, можно воспользоваться модулем venv в одной из команд:
```bash
python -m venv venv
python3 -m venv venv
py -m venv venv
```
Также можно установить библиотеку virtualvenv:
```bash
pip install virtualenv
```
и прописать команду 
```bash
python3 -m virtualenv venv
```
Либо использовать библиотеку pipenv(**приоритетный способ**):
```bash
pip install pipenv
```
Для создания окружения:
```bash
pipenv install
```
Для запуска окружения в первых двух способах:
```bash
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Unix
```
А используя pipenv:
```bash
pipenv shell
```

## Установка зависимостей

При работе на Linux системах возможна ошибка при установке библиотеки psycopg2

Необходимо установить дополнительные библиотеки. Для примера, на Ubuntu:
```bash
sudo apt install python3-dev libpq-dev
```
Все зависимости содержатся в requirements.txt или Pipfile в папке flask-backend

Находясь в данной папке, после создания и активации виртуального окружения:

- Если вы использовали venv или virtualvenv:
    ```bash
    pip install -r ./requirements.txt
    ```
    Для фикисрования новых зависимостей:
    ```bash
    pip freeze > ./requirements.txt
    ```
- А при использовании pipenv все зависмости установились при создании окружения

    Для фикисрования новых зависимостей:
    ```bash
    pipenv install название_библиотеки
    ```
    pipenv сам зафиксирует зависимость в Pipfile и Pipfile.lock

## Работа с контейнером БД проекта

Для данного проекта создан репозиторий на Docker Hub с настроенной базой данных и сервером Postgre

Для загрузки образа из хаба необходимо прописать:
```bash
sudo docker pull nordraven/voyage-vista:latest
```
Создание и запуск контейнера:
```bash
sudo docker run --name voyage-vista-db --network host -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 nordraven/voyage-vista:latest # Linux
docker run --name voyage-vista-db -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 nordraven/voyage-vista:latest # Windows
```
Для последующих запусков контейнера:
```bash
sudo docker start voyage-vista-db
```
Подключение к консоли Postgresql сервера:
```bash
sudo docker exec -it voyage-vista-db psql -U postgres
```

## Применение миграций

Для работы с миграциями базы данных в проекте используется Alembic, а точнее её обертка Flask-Migrate. В проект уже включен репозиторий миграций -
в каталоге flask-backend папка migrations.

Для применения миграций к базе данных в контейнере необходимо выполнить:
```bash
flask --app run.py db upgrade
```

Для отката на одну миграцию назад можно прописать:
```bash
flask --app run.py db downgrade
```

## Запуск проекта

Файлом для запуска проекта является run.py
```bash
python run.py
```


## Документация по backend части проекта

Интерактивная ERD диаграмма базы данных с комментариями:
- https://drawsql.app/teams/voyage-vista/diagrams/voyage-vista-database

Swagger-документация по API-путям проекта доступна после запуска сервера по адресу:
- http://127.0.0.1:8000/apidocs

## Особенности тестовых данных

В тестовых данных, которые добавляются с выполнением последней миграции:
- Пароль для пользователя user - 1111
- Пароль для пользователя moderator - 2222
- Пароль для пользователя admin - admin

Так как картинки, в отличие от данных в БД, не могут добавляться и удаляться с каждым воспроизведением миграции, 
необходимо самостоятельно очистить папку `/react-frontend/public/cover_images`, когда тестовые обложки перестанут быть нужны

## Проверка работоспособности бота в Telegram / работа с ngrok
Для обеспечения работы вебхука телеграм бота используется сервис ngrok. После регистрации и установки
идет настройка конфигурации приложения
```bash
ngrok config add-authtoken <ваш ngrok токен>
```
После этого в приложении ngrok необходимо выполнить команду 
```bash
ngrok http --url=adequately-internal-bullfrog.ngrok-free.app 8000
```
трафик локального приложения теперь станет доступен глобально
