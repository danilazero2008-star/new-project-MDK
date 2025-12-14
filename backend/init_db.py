"""Инициализация базы данных с демо данными"""

from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
from models import User, Category, Project

# Создание таблиц
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Создание категорий
    categories_data = [
        "Экология",
        "Образование",
        "Искусство",
        "Технологии",
        "Социальные проекты",
        "Культура",
        "Здравоохранение",
        "Бизнес",
        "Дизайн",
        "Транспорт"
    ]
    
    categories = []
    for cat_name in categories_data:
        existing = db.query(Category).filter(Category.name == cat_name).first()
        if not existing:
            category = Category(name=cat_name)
            db.add(category)
            categories.append(category)
    db.commit()
    print(f"✓ Создано {len(categories)} категорий")

    # Создание тестовых пользователей
    users_data = [
        {"username": "creator1", "email": "creator1@example.com", "full_name": "Иван Петров"},
        {"username": "creator2", "email": "creator2@example.com", "full_name": "Мария Сидорова"},
        {"username": "investor1", "email": "investor1@example.com", "full_name": "Алексей Волков"},
    ]
    
    users = []
    for user_data in users_data:
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing:
            user = User(**user_data)
            db.add(user)
            users.append(user)
    db.commit()
    print(f"✓ Создано {len(users)} пользователей")

    # Создание тестовых проектов
    projects_data = [
        {
            "title": "Экологичная упаковка для еды",
            "description": "Разработка биоразлагаемой упаковки из растительных материалов для ресторанов и кафе",
            "image_url": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800&h=600&fit=crop",
            "goal": 500000,
            "raised_amount": 387500,
            "backers_count": 142,
            "deadline": datetime.utcnow() + timedelta(days=30),
            "category": "Экология",
            "creator_id": 1
        },
        {
            "title": "Мобильное приложение для изучения языков",
            "description": "Инновационная платформа с AI-ассистентом для персонализированного обучения иностранным языкам",
            "image_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&h=600&fit=crop",
            "goal": 1000000,
            "raised_amount": 756000,
            "backers_count": 328,
            "deadline": datetime.utcnow() + timedelta(days=40),
            "category": "Образование",
            "creator_id": 2
        },
        {
            "title": "Арт-пространство для молодых художников",
            "description": "Создание креативного пространства с мастерскими и галереей для поддержки начинающих художников",
            "image_url": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800&h=600&fit=crop",
            "goal": 750000,
            "raised_amount": 512000,
            "backers_count": 89,
            "deadline": datetime.utcnow() + timedelta(days=20),
            "category": "Искусство",
            "creator_id": 1
        },
        {
            "title": "Умные теплицы для городских жителей",
            "description": "Компактные автоматизированные теплицы для выращивания свежих овощей дома",
            "image_url": "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=800&h=600&fit=crop",
            "goal": 2000000,
            "raised_amount": 1850000,
            "backers_count": 456,
            "deadline": datetime.utcnow() + timedelta(days=50),
            "category": "Технологии",
            "creator_id": 2
        },
        {
            "title": "Центр реабилитации животных",
            "description": "Открытие центра для лечения и реабилитации диких животных, пострадавших от деятельности человека",
            "image_url": "https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=800&h=600&fit=crop",
            "goal": 1500000,
            "raised_amount": 923000,
            "backers_count": 267,
            "deadline": datetime.utcnow() + timedelta(days=35),
            "category": "Социальные проекты",
            "creator_id": 1
        },
    ]
    
    projects_created = 0
    for proj_data in projects_data:
        category_name = proj_data.pop("category")
        category = db.query(Category).filter(Category.name == category_name).first()
        
        existing = db.query(Project).filter(Project.title == proj_data["title"]).first()
        if not existing and category:
            project = Project(**proj_data, category_id=category.id)
            db.add(project)
            projects_created += 1
    
    db.commit()
    print(f"✓ Создано {projects_created} проектов")

    print("\n✅ База данных успешно инициализирована!")
    print("\nТестовые данные:")
    print("- Пользователь-создатель 1: creator1@example.com")
    print("- Пользователь-создатель 2: creator2@example.com")
    print("- Инвестор: investor1@example.com")
    print(f"- Всего проектов: {projects_created}")

except Exception as e:
    print(f"❌ Ошибка при инициализации БД: {e}")
    db.rollback()

finally:
    db.close()
