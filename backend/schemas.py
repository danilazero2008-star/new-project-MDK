from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


# ==================== USER SCHEMAS ====================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== CATEGORY SCHEMAS ====================

class CategoryResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True


# ==================== PROJECT SCHEMAS ====================

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20)
    image_url: Optional[str] = None
    goal: float = Field(..., gt=0)
    deadline: datetime
    category: str
    creator_id: int


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=20)
    image_url: Optional[str] = None
    goal: Optional[float] = Field(None, gt=0)
    deadline: Optional[datetime] = None
    category: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: Optional[str]
    goal: float
    raised_amount: float
    backers_count: int
    deadline: datetime
    created_at: datetime
    updated_at: datetime
    category_id: int
    creator_id: int
    
    @property
    def progress_percent(self) -> float:
        if self.goal == 0:
            return 0
        return (self.raised_amount / self.goal) * 100
    
    @property
    def days_left(self) -> int:
        delta = self.deadline - datetime.utcnow()
        return max(0, delta.days)
    
    class Config:
        from_attributes = True


# ==================== INVESTMENT SCHEMAS ====================

class InvestmentCreate(BaseModel):
    amount: float = Field(..., gt=0)
    project_id: int
    user_id: int
    message: Optional[str] = Field(None, max_length=500)


class InvestmentResponse(BaseModel):
    id: int
    amount: float
    message: Optional[str]
    created_at: datetime
    project_id: int
    user_id: int
    
    class Config:
        from_attributes = True


# ==================== REVIEW SCHEMAS ====================

class ReviewCreate(BaseModel):
    text: str = Field(..., min_length=10, max_length=1000)
    rating: int = Field(..., ge=1, le=5)
    project_id: int
    user_id: int


class ReviewResponse(BaseModel):
    id: int
    text: str
    rating: int
    created_at: datetime
    project_id: int
    user_id: int
    
    class Config:
        from_attributes = True


# ==================== SEARCH SCHEMAS ====================

class SearchResponse(BaseModel):
    query: str
    results: List[ProjectResponse]
    total: int
