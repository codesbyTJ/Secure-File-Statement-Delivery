from datetime import datetime, timedelta, timezone 
from jose import jwt, JWTError

SECRET_KEY="12345"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

def create_access_token(data: dict, expires_delta: timedelta =None):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})    
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload.get("sub") else None
    except JWTError:
        return None

