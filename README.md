## технологии

- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **SQLite**
- **uv**(я использую uv, поэтому тут и появлися pyprojet.toml)

### Есть json с API в формате [openapi.json](https://github.com/An4nasik/ucartesttask/blob/master/openapi.json) если не хочеться запускать сам проект

## Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/An4nasik/ucartesttask.git
    cd ucartesttask
    ```

2.  **Установите зависимости:** <br>
    Я на винде сижу, поэтуму тут все под windows, если используете linux/macos верю, что сами разберетесь, но если что - пишите
    ```bash
    # Создание и активация виртуального окружения
    python -m venv venv
    source venv/bin/activate  # для Windows: venv\Scripts\activate

    # Установка зависимостей
    pip install fastapi "uvicorn[standard]" sqlalchemy pydantic
    ```

4.  **Запустите сервис:**
    Сервер будет запущен, и при первом запуске автоматически создастся файл базы данных `db/reviews.db` с нужной таблицей.

    ```bash
    uvicorn main:app --reload
    ```
    Сервис будет доступен по адресу `http://127.0.0.1:8000`.

## API

Вы можете взаимодействовать с сервисом через HTTP-запросы, но я бы рекомендовал перейти на `http://127.0.0.1:8000/docs` или `http://127.0.0.1:8000/redoc`

### 1. Отправить отзыв на анализ

- **Эндпоинт:** `POST /reviews`
- **Описание:** Принимает JSON с текстом отзыва, анализирует его тональность, сохраняет в БД и возвращает созданную запись.
- **Тело запроса:**
  ```json
  {
    "text": "отзыв"
  }
  ```

**Пример `curl` запроса:**
```bash
curl -X POST "http://127.0.0.1:8000/reviews" \
-H "Content-Type: application/json" \
-d '{"text": "Отличный сервис, мне все очень понравилось, спасибо!"}'
```

**Пример ответа (positive):**
```json
{
  "id": 1,
  "text": "Отличный сервис, мне все очень понравилось, спасибо!",
  "sentiment": "positive",
  "created_at": "2023-10-27T10:30:00.123456"
}
```

---

**Пример `curl` запроса (negative):**
```bash
curl -X POST "http://127.0.0.1:8000/reviews" \
-H "Content-Type: application/json" \
-d '{"text": "Ужасное обслуживание, возникла проблема, которую не решили."}'
```

**Пример ответа (negative):**
```json
{
  "id": 2,
  "text": "Ужасное обслуживание, возникла проблема, которую не решили.",
  "sentiment": "negative",
  "created_at": "2023-10-27T10:31:00.123456"
}
```

### 2. Получить отзывы по тональности

- **Эндпоинт:** `GET /reviews`
- **Описание:** Возвращает список всех отзывов с указанной тональностью (`positive`, `negative` или `neutral`).
- **Query параметр:** `sentiment`

**Пример `curl` запроса:**
```bash
curl -X GET "http://127.0.0.1:8000/reviews?sentiment=negative"
```

**Пример ответа:**
```json
[
  {
    "id": 2,
    "text": "Ужасное обслуживание, возникла проблема, которую не решили.",
    "sentiment": "negative",
    "created_at": "2023-10-27T10:31:00.123456"
  }
]
```
