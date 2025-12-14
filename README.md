# MDK Crowdfunding Platform

Платформа краудфандинга для поддержки инновационных проектов.

## Тех Нология

- **Backend:** FastAPI + SQLAlchemy + Alembic
- **Database:** SQLite (development) / PostgreSQL (production)
- **Frontend:** Vanilla JavaScript + HTML + CSS
- **Architecture:** RESTful API

## Настройка и Капусти

### Предварительные пометки

- Python 3.10+
- pip
- SQLite или PostgreSQL

### Настройка Backend

1. Клонировать репозиторий:
```bash
git clone https://github.com/danilazero2008-star/new-project-MDK.git
cd new-project-MDK
```

2. Создать виртуальное окружение:
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\\Scripts\\activate
```

3. Установить зависимости:
```bash
cd backend
pip install -r requirements.txt
```

4. Пустить FastAPI сервер:
```bash
python main.py
# или
python -m uvicorn main:app --reload
```

Сервер будет работать на `http://localhost:8000`

API документация: `http://localhost:8000/docs`

### Настройка Frontend

Открыть `frontend/index.html` в браузере или установить локальный веб-сервер.

## API Кончания

### Проекты
- `GET /api/projects` - Получить все проекты
- `GET /api/projects/{id}` - Получить проект по ID
- `POST /api/projects` - Создать проект
- `PUT /api/projects/{id}` - Обновить проект

### Инвестиции
- `POST /api/investments` - Поддержать проект
- `GET /api/investments/project/{id}` - Получить инвестиции

### Отзывы
- `POST /api/reviews` - Оставить отзыв
- `GET /api/reviews/project/{id}` - Получить отзывы

### Пользователи
- `POST /api/users` - Создать пользователя
- `GET /api/users/{id}` - Получить пользователя

### Поиск и Фильтрация
- `GET /api/projects?search=query` - Поиск проектов
- `GET /api/projects?sort_by=popular|new|ending` - Сортировка
- `GET /api/projects?category=...` - Фильтр по категории

### Другое
- `GET /api/statistics` - Генеральная статистика
- `GET /api/featured-projects` - Оставочные проекты
- `GET /health` - Проверка здоровья

## Понимание Работы JavaScript

Все кнопки и формы в приложении автоматически соединены с API ручками:

- Кнопка "Поддержать" → `POST /api/investments`
- Не поиск → `GET /api/projects?search=...`
- Проаккрая → `GET /api/projects?sort_by=...`

## Лицензия

MIT License