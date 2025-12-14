# Капусти и Деплоймент

## Локальная Разработка

### 1. Настройка Backend

```bash
# Открыть терминал 1
cd backend

# активировать venv
source venv/bin/activate  # Linux/Mac
# или
venv\\Scripts\\activate  # Windows

# установить зависимости
pip install -r requirements.txt

# инициализировать БД с демо данными
python init_db.py

# запустить FastAPI сервер
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Сервер будет работать на:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Настройка Frontend

Опция 1: Открыть прямо в браузере:

```bash
Сна принеса до frontend/index.html в браузер
```

Опция 2: Открыть через локальный веб-сервер:

```bash
# Открыть новый терминал
cd frontend

# Питон
python -m http.server 3000

# или Node.js + http-server
npx http-server -p 3000

# При что браузере открыть http://localhost:3000
```

## Тестирование API

### Утилиты тестирования

1. **Swagger UI** (наиболее полезно)
   - Открыть: http://localhost:8000/docs

2. **ReDoc** (документация)
   - Открыть: http://localhost:8000/redoc

3. **curl**:

```bash
# Получить все проекты
curl -X GET "http://localhost:8000/api/projects" -H "accept: application/json"

# Поныть поиск
curl -X GET "http://localhost:8000/api/projects?search=эко" -H "accept: application/json"

# Крейт нового проекта
curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{"title": "Мой проект", "description": "Описание", "goal": 100000, "deadline": "2025-03-14T00:00:00", "category": "Экология", "creator_id": 1}'
```

## Production Деплоймент

### Основные Рекомендации

1. **Настройка Окружения**
   - Гервраоте PostgreSQL весто SQLite
   - Настройте оменные переменные в файле .env

2. **Веб-Сервер (Быстрые Данные)**
   - Использовать Gunicorn/Uvicorn для распределения
   - Конфигурировать Nginx как reverse proxy

3. **Цатя Невисимые**
   - Добавить JWT при необходимости
   - Ограничить количество запросов (rate limiting)
   - Настроить HTTPS

### Heroku/Railway Деплой

```bash
# Гервер - Проста связь
heroku login
heroku create <your-app-name>
git push heroku main

# Railway
railway init
railway up
```

## Омедодование Ооибок

### Обчные Проблемы

1. **CORS Ошибки**
   - Открыте все стороны в main.py (production: ограничить)

2. **Проблемы с Портами**
   - 8000 для API
   - 3000 для Frontend
   - Дубли порты экономные использовать

3. **Ошибки ФОрмы**
   - Проверьте JSON в Console
   - Получите статус в Network таб

## Логи

Для трассировки открыть Browser Console (F12) и Backend логи.

## Примерные Нагружки

```python
# Новый Проект
{
  "title": "Жывые Экологы",
  "description": "Красивая экологическая инициатива",
  "goal": 500000,
  "deadline": "2025-04-15T00:00:00",
  "category": "Экология",
  "creator_id": 1
}
```
