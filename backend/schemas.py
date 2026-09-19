from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    Active = "Active"
    Inactive = "Inactive"

# Jab naya student CREATE karna ho, yeh shape chahiye
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    course: str
    phone: Optional[str] = None
    address: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.Active

# Jab student ko UPDATE karna ho (sab fields optional, kyunki partial update ho sakta hai)
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    course: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: Optional[StatusEnum] = None

# Jab API se student data RESPONSE mein bhejna ho
class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    course: str
    phone: Optional[str] = None
    address: Optional[str] = None
    status: StatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True   # yeh SQLAlchemy object ko Pydantic mein convert karne deta hai