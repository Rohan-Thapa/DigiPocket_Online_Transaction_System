from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from .config import settings
from repositories.user_repo import UserRepository
from models.user import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
user_repo = UserRepository()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    to_encode = {"sub": subject}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_access_token_expires_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

async def authenticate_user(email: str, password: str) -> UserInDB | None:
    user_dict = await user_repo.get_by_email(email)
    if not user_dict:
        return None
    # Convert ObjectId to string for Pydantic
    user_dict['_id'] = str(user_dict['_id'])
    user = UserInDB(**user_dict)
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_dict = await user_repo.get_by_email(email)
    if not user_dict:
        raise credentials_exception
    # Convert ObjectId to string
    user_dict['_id'] = str(user_dict['_id'])
    return UserInDB(**user_dict)