from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# --- User schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Token schema ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Post schemas ---
class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str
    content: str

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    is_public: bool

    model_config = ConfigDict(from_attributes=True)
