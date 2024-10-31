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

Для данного проекта создан архив "voyage-vista-database.tar" с пустой базой данных Postgre

Для загрузки образа из архива необходимо прописать:
```bash
docker load -i voyage-vista-database.tar
```
Перед выполнением следующей команды необходимо узнать выданное образу имя

Замените my-postgres-image на фактическое имя образа, которое будет указано в выводе команды "docker load".
Если данная команда ничего не вывела, воспользуйтесь "docker images"

Запуск контейнера:
```bash
docker run --name <задайте имя контейнера сами> -e POSTGRES_PASSWORD=<задайте пароль для пользователя> -d my-postgres-image
```
Подключение к консоли Postgresql сервера:
```bash
docker exec -it <заданное вами имя контейнера> psql -U postgres
```

## Применение миграций

Для работы с миграциями базы данных в проекте используется Alembic, а точнее её обертка Flask-Migrate. В проект уже включен репозиторий миграций -
в каталоге flask-backend папка migrations.

Для применения миграций к базе данных в контейнере необходимо выполнить:
```bash
flask --app run.py db upgrade
```

## Запуск проекта

Файлом для запуска проекта является run.py


