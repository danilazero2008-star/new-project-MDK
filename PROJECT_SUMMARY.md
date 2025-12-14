# Обзор Проекта MDK Crowdfunding

## чем сделано

### В Баченд

✅ **Полноценные FastAPI API** с всеми ручками:
- Проекты (CRUD)
- Инвестиции / Поддержка проектов
- Отзывы
- Пользователи
- Категории
- Поиск и фильтрация
- Статистика

✅ **SQLAlchemy Модели**:
- `User` - Пользователи
- `Project` - Проекты
- `Category` - Категории
- `Investment` - Инвестиции
- `Review` - Отзывы

✅ **Pydantic Схемы** для валидации данных

✅ **CORS миддлверка** для работы с frontend

✅ **Alembic** миграции готовы к использованию

✅ **Демо данные** в init_db.py

### В Фронтенде

✅ **Переделанный script.js** с полной интеграцией с API:
- Функции для генерации данных ис API
- Обработки форм для сохранения инвестиций
- Открытие модаля с деталями проекта
- Поиск и сортировка всем научне элементам

✅ **HTML дизайн** состают от васи - дезайн не изменен

✅ **CSS стили** сохранены как и было

## Архитектура Проекта

```
new-project-MDK/
├── backend/
│   ├── main.py           # FastAPI аппликация
│   ├── models.py        # SQLAlchemy модели
│   ├── schemas.py       # Pydantic схемы
│   ├── database.py      # Настройка БД
│   ├── init_db.py       # Инициализация демо данных
│   ├── requirements.txt # Пакеты
│   └── .env.example     # Пример омедодования
├── frontend/
│   ├── index.html       # Основная страница
│   ├── script.js        # Обновленный JavaScript с API
│   ├── styles.css       # Основные стили
│   └── index.css        # Дополнительные стили
├── README.md        # Основная документация
├── DEPLOYMENT.md    # гайд разворачивания
├── .env.example     # Пример .env
└── PROJECT_SUMMARY.md  # этот файл
```

## Как все работает

### 1. Регистрация / Логин

```
User вводит однозначные данные
    → script.js собрает объект Пользователя
    → POST /api/users до FastAPI
    → Сохраняется в таблице users
    → localStorage для пострайя
```

### 2. Поддержка Проекта (Инвестиция)

```
Кнопка "Поддержать проект"
    → Открывается модаль с формой
    → Пользователь вводит сумму и ник
    → submitInvestment() сохраняет в АПИ
    → POST /api/investments до FastAPI
    → Обновляется raised_amount и backers_count в Проекте
    → Восянавливается страница
```

### 3. Поиск и Фильтрация

```
Набирает текст в поиске
    → performSearch() генерирует квери
    → GET /api/projects?search=query&sort_by=...
    → Получает отфильтрованные результаты
    → renderProjects() отображает результаты
```

## API Направление Минут

### гет

**Проекты:**
- `GET /api/projects` - Все проекты
- `GET /api/projects?search=eco` - Поиск
- `GET /api/projects?sort_by=popular|new|ending` - сортировка
- `GET /api/projects/{id}` - Один проект

**Инвестиции:**
- `POST /api/investments` - Новая инвестиция
- `GET /api/investments/project/{id}` - Эвестиции проекта

**Аутентификация:**
- `POST /api/users` - Новый пользователь
- `GET /api/users/{id}` - Один пользователь

**Отзывы:**
- `POST /api/reviews` - Новый отзыв
- `GET /api/reviews/project/{id}` - Отзывы проекта

## Как Начать

```bash
# 1. Клонировать
git clone https://github.com/danilazero2008-star/new-project-MDK.git
cd new-project-MDK

# 2. Настроить Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python init_db.py  # Наполнить демо данными
python main.py  # Запустить API

# 3. Открыть Frontend
# Открыть frontend/index.html в браузере

# API тестирование
# Арио документация: http://localhost:8000/docs
```

## Вичислили, Которые Устроюются С API

Каждая кнопка и форма в приложении выполняют реальные API-запросы:

- Кнопки для навигации
- Навигация по страницам
- Поиск и фильтрация
- Зависимости данных (статистика, проекты, инвестиции)

## Реализация

Так что плотные файлы останутся неиспользуемыми. Это внедряется диспатчер и может организовать картину данных.

При всем этом, архитектура достаточно пластична и готова к новым расчетам.

---

Проект готов к использованию и развитию! ✅
