from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book, User
from app import auth, schemas

router = APIRouter(
    prefix="/books"
)

#NEW BOOK ADD

@router.post("/",response_model=schemas.BookResponse )
def add_books(book: schemas.BookBase, db:Session = Depends(get_db), current_user : User = Depends(auth.get_librarian_user)):
    db_book = db.query(Book).filter(Book.isbn==book.isbn).first()
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Book with this ISBN is already exist"
        )
    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

#GET ALL BOOKS
@router.get("/", response_model=list[schemas.BookResponse])
def get_all_books(db:Session = Depends(get_db)):
    return db.query(Book).all()
    
#UPDATE BOOKS
@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_books(book_id : int, book:schemas.BookBase, db:Session = Depends(get_db), current_user : User = Depends(auth.get_librarian_user)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

#DELETE A BOOK
@router.delete("/{book_id}")
def delete_book(book_id : int, db:Session = Depends(get_db), current_user : User = Depends(auth.get_admin_user)):
    db_book = db.query(Book).filter(Book.id ==book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    db.delete(db_book)
    db.commit
    return {"message:" "Book deleted succesfully"}