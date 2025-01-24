from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Borrow, User
from app import schemas, auth
from app.models import Book


router = APIRouter(
    prefix="/borrows"
)

#BORROW
@router.post("/",response_model=schemas.BorrowResponse)
def borrow_book(borrow_request : schemas.BorrowBase,db: Session = Depends(get_db), current_user : User = Depends(auth.get_current_user)):
    book = db.query(Book).filter(Book.id ==borrow_request.book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail="book not found"
        )
    if book.quantity < 1:
        raise HTTPException (
            status_code=400,
            detail="Book is not available for borrowing"
        )
    
    book.quantity -= 1

    borrow_entry = Borrow(
        book_id = book.id,
        user_id = current_user.id
    )
    db.add(borrow_entry)
    db.commit()

    db.refresh(borrow_entry)

    return borrow_entry

#RETURN BOOK

@router.post("/return", response_model=schemas.BorrowResponse)
def return_book(
    borrow_request: schemas.BorrowBase,
    db:Session = Depends(get_db),
    current_user : User = Depends(auth.get_current_user)
):
    borrowed_entry = db.query(Borrow).filter(Borrow.book_id==borrow_request.book_id,Borrow.returned_at ==None, Borrow.user_id == current_user.id).first()
    if not borrowed_entry:
        raise HTTPException(
            status_code=404,
            detail="no records of borrowed book found"
        )
    borrowed_entry.returned_at = datetime.now()

    book = db.query(Book).filter(Book.id == borrow_request.book_id).first()
    book.quantity+=1

    db.commit()
    db.refresh(borrowed_entry)

    return borrowed_entry

#VIEW ALL BORROWED BOOKS
@router.get("/", response_model=list[schemas.BorrowResponse])
def get_borrowed_books(
    db:Session = Depends(get_db), current_user : User = Depends(auth.get_current_user)
):
    borrowed_books = db.query(Borrow).filter(Borrow.user_id == current_user.id).all()
    return borrowed_books
