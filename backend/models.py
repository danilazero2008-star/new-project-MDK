from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    investments = relationship("Investment", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    projects = relationship("Project", back_populates="creator")


class Category(Base):
    """Модель категории проекта"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    
    # Relationships
    projects = relationship("Project", back_populates="category")


class Project(Base):
    """Модель проекта"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    image_url = Column(String(500))
    goal = Column(Float, nullable=False)  # Целевая сумма
    raised_amount = Column(Float, default=0)  # Собрано денег
    backers_count = Column(Integer, default=0)  # Количество поддерживающих
    deadline = Column(DateTime, nullable=False)  # Срок окончания проекта
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    category = relationship("Category", back_populates="projects")
    creator = relationship("User", back_populates="projects")
    investments = relationship("Investment", back_populates="project", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="project", cascade="all, delete-orphan")


class Investment(Base):
    """Модель инвестиции (поддержки проекта)"""
    __tablename__ = "investments"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)  # Сумма инвестиции
    message = Column(Text)  # Сообщение от инвестора
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="investments")
    user = relationship("User", back_populates="investments")


class Review(Base):
    """Модель отзыва о проекте"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    rating = Column(Integer, default=5)  # Рейтинг от 1 до 5
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
