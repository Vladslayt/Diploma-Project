# Веб-сервис по подбору совместных арендаторов жилья

Этот веб-сервис позволяет пользователям найти соседей для совместного съема жилья, используя REST API стороннего сервиса для получения информации о доступных квартирах. Веб-сервис предоставляет различные функциональные возможности, включая создание и управление лобби, поиск и оценку квартир, а также управление пользовательскими профилями.

## Основные возможности

- **Регистрация и аутентификация пользователей:** Пользователи могут зарегистрироваться и создать профиль, указав основную информацию о себе. Функционал аутентификации обеспечивает безопасный вход в систему и доступ ко всем функциям сервиса.
- **Создание и управление лобби:** Пользователи могут создавать собственные лобби, приглашать других участников и управлять ими. Лобби могут быть как публичными, так и приватными с паролем, что позволяет гибко организовывать группы совместных арендаторов по различным критериям.
- **Фильтры для поиска лобби:** Пользователи могут искать лобби, используя различные фильтры, такие как название, максимальное количество участников, приватность и тип лобби.
- **Поиск и добавление квартир:** Веб-сервис интегрирован с внешним REST API, что позволяет пользователям получать актуальную информацию о доступных квартирах. Поиск можно осуществлять по различным параметрам, таким как цена, количество комнат, район и станция метро.
- **Определение полей для отображения у квартир:** Пользователи могут выбирать, какие поля информации о квартирах будут отображаться в результатах поиска.
- **Оценка квартир:** Пользователи могут оценивать квартиры, добавленные в лобби, что позволяет другим участникам видеть средний рейтинг и принимать более обоснованные решения при выборе жилья.
- **Просмотр и управление профилем:** Пользователи могут редактировать свои профили и управлять персональной информацией.
- **Политика конфиденциальности:** Веб-сервис предоставляет пользователям информацию о политике конфиденциальности.

## Установка и запуск

### С использованием Docker Compose

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Vladslayt/Diploma-Project.git
    cd your-repo
    ```

2. Убедитесь, что Docker и Docker Compose установлены на вашем компьютере.

3. Создайте файл `.env` в корне проекта и добавьте необходимые переменные окружения (например, настройки базы данных, секретный ключ Django и другие параметры):
    ```
    SECRET_KEY=your_secret_key
    DEBUG=True
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=db
    DB_PORT=5432
    ```

4. Запустите Docker Compose:
    ```bash
    docker-compose up --build
    ```

5. Примените миграции и создайте суперпользователя:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

6. Перейдите в браузере по адресу `http://localhost:8000` для доступа к веб-сервису.

## Структура проекта

- **myapp/**: Основное приложение Django, содержащее модели, представления, формы и шаблоны.
- **templates/**: Директория, содержащая HTML-шаблоны для различных страниц веб-сервиса.
- **static/**: Директория, содержащая статические файлы, такие как CSS и JavaScript.
- **docker-compose.yaml**: Конфигурационный файл Docker Compose для развертывания проекта.
- **Dockerfile**: Файл для создания Docker-образа веб-приложения.

## Контейнеризация и развертывание

Проект использует Docker и Docker Compose для удобного развертывания и управления зависимостями. Docker Compose конфигурирует несколько сервисов, включая веб-сервер Django, базу данных PostgreSQL и другие необходимые компоненты. Этот подход позволяет легко развертывать и тестировать проект в контейнеризованной среде.
