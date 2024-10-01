from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from common.authentication import create_access_token, verify_password, get_password_hash, verify_token, \
    get_current_user
from database.db import get_db
from schemas.user_schema import UserCreate, UserUpdate, UserLogin
from models.user import User
import logging

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully!"}


@router.post("/token")
def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):  # Use UserLogin schema
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/user/update")
def update_user(user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = get_password_hash(user.password)
        db.commit()
        return {"message": "User updated successfully!"}
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/user/delete")
async def delete_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == current_user.id).first()

    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully!"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
