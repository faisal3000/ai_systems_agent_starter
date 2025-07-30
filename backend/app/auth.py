# backend/app/auth.py

import os
import datetime
import jwt
from pathlib import Path
from typing import Generator

from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field, create_engine, Session, select

# 1) Project-root users.db
ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH  = ROOT_DIR / "users.db"
print(f">>> AUTH – using DB at: {DB_PATH}")

# 2) Engine & session factory
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=False,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3) Security utilities
pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
SECRET  = os.getenv("JWT_SECRET", "CHANGE_ME")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 12))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(raw: str) -> str:
    return pwd_ctx.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    return pwd_ctx.verify(raw, hashed)

# 4) SQLModel User table (now pointing at plural "users")
class User(SQLModel, table=True):
    __tablename__ = "users"

    id:         int  | None = Field(default=None, primary_key=True)
    email:      str        = Field(unique=True, index=True)
    password:   str
    is_active:  bool       = Field(default=True)
    is_admin:   bool       = Field(default=False)

SQLModel.metadata.create_all(engine)

# 5) Pydantic Token model
class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_access_token(user: User) -> str:
    payload = {
        "sub": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
        "adm": user.is_admin,
        "act": user.is_active,
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

# 6) Dependency for protected routes
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    user = db.exec(select(User).where(User.email == payload.get("sub"))).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# 7) Auth endpoints
@auth_router.post("/register", response_model=Token)
def register(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    if db.exec(select(User).where(User.email == form.username)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    user = User(
        email=form.username,
        password=hash_password(form.password),
        is_active=True,    # auto-approve in dev
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return Token(access_token=create_access_token(user))

@auth_router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.exec(select(User).where(User.email == form.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not verify_password(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not active")
    return Token(access_token=create_access_token(user))
