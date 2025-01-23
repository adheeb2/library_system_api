from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
from app.database import get_db
from app.models import User
from app import schemas
from app import env

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def hash_password(password: str) -> str:
      return pwd_context.hash(password)

def verify_password(plain_password : str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(user : User) -> str:
    to_encode = {"sub" : str(user.id)}
    expire = datetime.now() + timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm= env.JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.UserResponse:
    try:
        payload = jwt.decode(token ,env.SECRET_KEY,algorithms=[env.JWT_ALGORITHM])
        user_id : str = payload.get('sub')
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail = "Could not validate credentials"
            )
        user = db.query(User).filter(User.id == user_id).first()
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail = "Could not validate credentials"
            )
        return user
    except JWTError as err:
        print(err)
        raise HTTPException(
            status_code=401,
            detail='Token is invalid or expired'
        )

