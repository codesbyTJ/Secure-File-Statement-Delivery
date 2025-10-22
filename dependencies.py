from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from .db import get_db
from . import models, auth

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload=auth.verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_email=payload.get("sub")
    user=db.query(models.User).filter(models.User.email==user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user