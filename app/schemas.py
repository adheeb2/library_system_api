from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models import Role


#USER
class UserBase(BaseModel):
    username : str
    email :str
    role: Optional[Role] = None

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    id : int


#BOOKS
class BookBase(BaseModel):
    title : str
    author : str
    quantity : int

class BookCreate(BookBase):
    pass

class BookRespoonse(BookBase):
    id : int


#BORROW
class BorrowBase(BaseModel):
    book_id : int

class BorrowResponse(BorrowBase):
    id : int
    borrowed_at = datetime
    returned_at = Optional[datetime] = None