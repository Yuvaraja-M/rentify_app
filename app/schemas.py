from pydantic import BaseModel, EmailStr
from typing import List,Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    is_seller: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id:int
    class Config:
        orm_mode = True

class PropertyBase(BaseModel):
    title:str
    description:str
    place:str
    area:str
    bedrooms: int
    bathrooms:int
    hospitalnearby: int
    schoolnearby : int
    price : float
class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    email:Optional[str] = None

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    place: Optional[str] = None
    area: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    hospitalnearby: Optional[int] = None
    schoolnearby: Optional[int] = None
    price: Optional[float] = None

class FilterCriteria(BaseModel):
    place: Optional[str] = None
    area: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    hospitalnearby: Optional[int] = None
    schoolnearby: Optional[int] = None
    price: Optional[float] = None