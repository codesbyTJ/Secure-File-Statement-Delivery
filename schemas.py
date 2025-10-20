#Schemas is utilised for the Pydantic data models
#This is for the API validation

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str

class StatementCreate(BaseModel):
    user_id: int
    filename: str

class StatementRead(BaseModel):
    id: int
    user_id: int
    filename: str
    upload_date: datetime

class DownloadToken(BaseModel):
    token: str
    statement_id: int
    expiration: datetime