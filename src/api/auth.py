from fastapi import APIRouter, Depends, HTTPException, Depends, Request, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.repository.database.db import get_db
from src.repository import users
from src.schemas import UserCreate, UserBase, UserResponse  
from src.services.auth import create_access_token, decode_token, get_current_user, upload_avatar
from src.services.security import  verify_password
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.repository.database.models import User

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserBase, status_code=201)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if users.get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="User already exists")
    return users.create_user(db, user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = users.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/confirm")
def confirm_email(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = users.get_user_by_email(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.confirmed = True
    db.commit()
    return {"message": "Email confirmed"}

@router.get("/me", response_model=UserResponse)
@limiter.limit("5/minute")
def read_me(request: Request, current_user = Depends(get_current_user)):
    return current_user

@router.post("/avatar", response_model=dict)
def update_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG allowed.")

    avatar_url = upload_avatar(file)
    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)

    return {"avatar_url": avatar_url}