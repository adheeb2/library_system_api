from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book
from app import schemas

router = APIRouter(
    prefix="books"
)

@router.post("")