from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TaskOut(BaseModel):
    id: int
    task_description: str
    task_category: Optional[str]
    due_date: Optional[datetime]
    priority: Optional[str]
    tags: Optional[List[str]]
    is_recurring: Optional[bool]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True 

class TaskCreate(BaseModel):
    task_description: str
    task_category: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    is_recurring: Optional[bool] = False

class TaskFilter(BaseModel):
    task_description: Optional[str] = None
    task_category: Optional[str] = None
    due_date: Optional[str] = None
    due_date_before: Optional[datetime] = None
    due_date_after: Optional[datetime] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    is_recurring: Optional[bool] = None