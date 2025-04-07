from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date
from typing import Optional

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    avatar: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    username: str
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    username: str
    is_active: bool
    avatar_url: str | None = None

    model_config = ConfigDict(from_attributes=True)