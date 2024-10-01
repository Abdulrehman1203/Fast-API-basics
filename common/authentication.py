from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
from schemas.user_schema import TokenData
from passlib.context import CryptContext
import logging

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging.basicConfig(level=logging.INFO)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    logging.info(f"Verifying token: {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logging.info(f"Decoded payload: {payload}")
        username = payload.get("sub")
        if username is None:
            logging.warning("No subject found in token")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError as e:
        logging.error(f"Token verification error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=360)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


logger = logging.getLogger(__name__)


def verify_token(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded payload: {payload}")  # Log the payload
        username = payload.get("sub")
        if username is None:
            return None
        db_user = db.query(User).filter(User.username == username).first()
        return db_user
    except JWTError as e:
        logger.error(f"JWT Error: {e}")  # Log the error
        return None  # Token is invalid


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
