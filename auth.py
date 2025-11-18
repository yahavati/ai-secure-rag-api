from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from models import Users
from database import SessionLocal

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str
   


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if password !=user.hashed_password:
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta,role:str):
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": username, "id": user_id, "exp": expire,'role':role}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user"
            )

        return {"username": username, "id": user_id,"user_role": user_role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: CreateUserRequest):
    new_user = Users(
        username=user.username,
        hashed_password=user.password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}


@router.post("/token", response_model=Token)
async def login(
    from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(from_data.username, from_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(
        user.username,
        user.id,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        user.role
    )

    return {"access_token": token, "token_type": "bearer"}
