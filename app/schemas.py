from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email :str
    role: Optional[str] = None

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    id : int

class BookBase(BaseModel):
    title : str
    author : str
    quantity : int

class BookCreate(BookBase):
    pass

class BookRespoonse(BookBase):
    id : int

class BorrowBase(BaseModel):
    book_id : int

class BorrowResponse(BorrowBase):
    id : int
    borrowed_at = datetime
    returned_at = Optional[datetime] = None