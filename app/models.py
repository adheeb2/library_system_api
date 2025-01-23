from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum

class Role(PyEnum):
    ADMIN = "Admin"
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(PyEnum(Role), default=Role.MEMBER)

    borrows = relationship("Borrow", back_populates="users")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    quantity = Column(Integer, default=0)

    borrows = relationship("Borrow", back_populates="books")

class Borrow(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrowed_at = Column(DateTime, nullable=False)
    returned_at = Column(DateTime, nullable=False)

    book = relationship("Book", back_populates="borrows")
    user = relationship("User", back_populates="borrows")