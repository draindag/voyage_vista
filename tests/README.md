# Тесты проекта

В этой папке находятся тесты для проверки работы бэкенда. Все тесты написаны с использованием `pytest`.

## Структура папки
- **`models/`** — тесты для моделей базы данных.
- **`routes/`** — тесты для роутов API.
- **`schemas/`** — тесты для схем сериализации и валидации данных.
- **`conftest.py`** — общие фикстуры и настройки для тестов.
- **`test_app.py`** — базовые тесты для приложения.

---

## Требования
Для запуска тестов убедитесь, что выполнены следующие условия:
1. Установлена необходимая версия Python.
2. Установлены зависимости, указанные в проекте (об установке см. flask-backend\README.md).

## Запуск тестов
- Базовый запуск
Для выполнения всех тестов в проекте выполните: 
    ```bash
    pytest
    ```

- Запуск тестов из конкретной директории
Чтобы запустить тесты только из определённой папки, например, routes, выполните:
    ```bash
    pytest tests/routes/
    ```

## Проверка покрытия кода
Для проверки покрытия кода выполните следующую команду:
```bash
pytest --cov=flask-backend
 ```
## Генерация html-отчета о покрытии
Для создания отчёта в формате HTML используйте:
```bash
pytest --cov=flask-backend --cov-report=html
 ```
После выполнения команды, отчёт будет сохранён в директории htmlcov/. Для просмотра откройте файл htmlcov/index.html в вашем браузере.

## Полезные параметры
- -s: Вывод отладочной информации (например, print внутри тестов):
```bash
pytest -s
 ```

- -v: Подробный вывод выполнения тестов:
```bash
pytest -v
```

- -k: Запуск тестов с определённым именем (например, содержащих login):
```bash
pytest -k "login"
```