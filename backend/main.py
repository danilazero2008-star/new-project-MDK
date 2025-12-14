from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_, func
from datetime import datetime
from typing import List, Optional

from database import engine, get_db, Base
from models import (
    Project, User, Investment, Review, Category
)
from schemas import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    InvestmentCreate, InvestmentResponse,
    ReviewCreate, ReviewResponse,
    UserCreate, UserResponse,
    CategoryResponse, SearchResponse
)

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MDK Crowdfunding Platform",
    description="Платформа для краудфандинга проектов",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== PROJECTS ====================

@app.get("/api/projects", response_model=List[ProjectResponse])
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = Query("popular", regex="^(popular|new|ending)$"),
    db: Session = Depends(get_db)
):
    """Получить список всех проектов с фильтрацией и сортировкой"""
    query = db.query(Project)
    
    # Фильтр по категории
    if category:
        query = query.join(Category).filter(Category.name == category)
    
    # Поиск по названию и описанию
    if search:
        search_term = f"%{search}%"
        query = query.filter(or_(
            Project.title.ilike(search_term),
            Project.description.ilike(search_term)
        ))
    
    # Сортировка
    if sort_by == "popular":
        query = query.order_by(desc(Project.backers_count))
    elif sort_by == "new":
        query = query.order_by(desc(Project.created_at))
    elif sort_by == "ending":
        query = query.order_by(Project.deadline)
    
    return query.offset(skip).limit(limit).all()


@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Получить детали проекта по ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project


@app.post("/api/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Создать новый проект"""
    # Проверка категории
    category = db.query(Category).filter(Category.name == project.category).first()
    if not category:
        category = Category(name=project.category)
        db.add(category)
        db.commit()
        db.refresh(category)
    
    db_project = Project(
        title=project.title,
        description=project.description,
        image_url=project.image_url,
        goal=project.goal,
        deadline=project.deadline,
        category_id=category.id,
        creator_id=project.creator_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.put("/api/projects/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Обновить проект"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    update_data = project.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "category" and value:
            category = db.query(Category).filter(Category.name == value).first()
            if not category:
                category = Category(name=value)
                db.add(category)
                db.commit()
            db_project.category_id = category.id
        else:
            setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


# ==================== INVESTMENTS ====================

@app.post("/api/investments", response_model=InvestmentResponse)
def create_investment(
    investment: InvestmentCreate,
    db: Session = Depends(get_db)
):
    """Создать инвестицию (поддержать проект)"""
    # Проверка проекта
    project = db.query(Project).filter(Project.id == investment.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Проверка срока проекта
    if project.deadline < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Проект завершён")
    
    # Проверка пользователя
    user = db.query(User).filter(User.id == investment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db_investment = Investment(
        amount=investment.amount,
        project_id=investment.project_id,
        user_id=investment.user_id,
        message=investment.message
    )
    
    # Обновление статистики проекта
    project.raised_amount += investment.amount
    project.backers_count += 1
    
    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)
    return db_investment


@app.get("/api/investments/project/{project_id}", response_model=List[InvestmentResponse])
def get_project_investments(
    project_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Получить инвестиции проекта"""
    return db.query(Investment).filter(
        Investment.project_id == project_id
    ).offset(skip).limit(limit).all()


# ==================== REVIEWS ====================

@app.post("/api/reviews", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """Создать отзыв о проекте"""
    # Проверка проекта
    project = db.query(Project).filter(Project.id == review.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Проверка пользователя
    user = db.query(User).filter(User.id == review.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db_review = Review(
        text=review.text,
        rating=review.rating,
        project_id=review.project_id,
        user_id=review.user_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@app.get("/api/reviews/project/{project_id}", response_model=List[ReviewResponse])
def get_project_reviews(
    project_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Получить отзывы проекта"""
    return db.query(Review).filter(
        Review.project_id == project_id
    ).order_by(desc(Review.created_at)).offset(skip).limit(limit).all()


# ==================== USERS ====================

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя"""
    # Проверка на уникальность email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


# ==================== CATEGORIES ====================

@app.get("/api/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Получить все категории"""
    return db.query(Category).all()


@app.post("/api/categories", response_model=CategoryResponse)
def create_category(name: str, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Категория уже существует")
    
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# ==================== SEARCH & STATISTICS ====================

@app.get("/api/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Поиск проектов"""
    search_term = f"%{q}%"
    projects = db.query(Project).filter(or_(
        Project.title.ilike(search_term),
        Project.description.ilike(search_term)
    )).limit(20).all()
    
    return SearchResponse(
        query=q,
        results=projects,
        total=len(projects)
    )


@app.get("/api/statistics")
def get_statistics(db: Session = Depends(get_db)):
    """Получить статистику платформы"""
    total_projects = db.query(func.count(Project.id)).scalar()
    total_raised = db.query(func.sum(Project.raised_amount)).scalar() or 0
    total_backers = db.query(func.sum(Project.backers_count)).scalar() or 0
    total_users = db.query(func.count(User.id)).scalar()
    
    return {
        "total_projects": total_projects,
        "total_raised": total_raised,
        "total_backers": total_backers,
        "total_users": total_users
    }


@app.get("/api/featured-projects", response_model=List[ProjectResponse])
def get_featured_projects(
    limit: int = Query(6, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Получить избранные проекты"""
    return db.query(Project).order_by(
        desc(Project.raised_amount)
    ).limit(limit).all()


# ==================== HEALTH CHECK ====================

@app.get("/health")
def health_check():
    """Проверка здоровья"""
    return {"status": "ok", "message": "MDK Crowdfunding is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
