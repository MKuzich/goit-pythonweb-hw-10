from sqlalchemy.orm import Session
from src.repository.database.models import User
from src.schemas import UserCreate
from src.services.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = User(username = user.username, email=user.email, hashed_password=hashed_pw, confirmed=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user