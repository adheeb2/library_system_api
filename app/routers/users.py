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

# GET CURRENT USER

@router.get("/me", response_model=schemas.UserResponse)
def get_user(
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    return current_user

#GET ALL USERS

@router.get("/", response_model=list[schemas.UserResponse])
def get_all_user(db:Session = Depends(get_db), current_user : User = Depends(auth.get_admin_user )):
    return db.query(User).all()

#UPDATE USER ROLE

@router.put("/{user_id}/role")
def update_user_role(user_id : int, role_update: schemas.RoleUpdate, db:Session = Depends(get_db), current_user : User = Depends(auth.get_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    role = role_update.role
    db.add(user)
    db.commit()
    return {"message":"User role updated successfully"}