from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
from datetime import datetime, timedelta,timezone

SECRET_KEY  = "7d13a26f5e0c4b93b68f2fd7e9a51c12dbaf09b8a7c88411c93d8c482739652a"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30

TOKEN_BLACKLIST = set()

def add_to_blacklist(token: str):
    TOKEN_BLACKLIST.add(token)

def is_blacklisted(token: str) -> bool:
    return token in TOKEN_BLACKLIST

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        SECRET_KEY, 
        algorithm=ALGORITHM 
    )
    return encoded_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session
                      = Depends(get_db)):

    if is_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token revoked")

    credentials_exception =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate" : "Bearer" },
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
