#Models is used for the SQL alchemy data models
#this is for the db structure and mapping

from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    role: str

class Statement(BaseModel):
    id: int
    user_id: int
    filename: str
    upload_date: datetime

class DownloadToken(BaseModel):
    token: str
    statement_id: int
    expiration: datetime
