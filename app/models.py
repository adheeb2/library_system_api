from sqlalchemy import VARCHAR, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum
from datetime import datetime

class Role(PyEnum):
    ADMIN = "Admin"
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)   
    role = Column(VARCHAR, default=Role.MEMBER.value)
    borrows = relationship("Borrow", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    isbn = Column(String, unique=True, index=True)

    borrows = relationship("Borrow", back_populates="book")

class Borrow(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrowed_at = Column(DateTime(timezone=True), server_default=func.now())
    returned_at = Column(DateTime(timezone=True), nullable=True)

    book = relationship("Book", back_populates="borrows")
    user = relationship("User", back_populates="borrows")

