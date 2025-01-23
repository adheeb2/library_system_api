from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app import schemas, auth

router = APIRouter(
    prefix="/users"
)

#REGISTER
@router.post("/register", response_model=schemas.UserResponse)
def register_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email ==data.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    hashed_password = auth.hash_password(data.password)

    user_data = data.model_dump(exclude_none=True)
    user_data.pop("password")
    user_data.update({"hashed_password": hashed_password})
        
    new_user = User(**user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#LOGIN
@router.post("/login")
def login_user(data: schemas.UserLogin, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not auth.verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="invalid email or password"
        )
    access_token = auth.create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}