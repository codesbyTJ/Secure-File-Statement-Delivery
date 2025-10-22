#Models is used for the SQL alchemy data models
#this is for the db structure and mapping


from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db import Base



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255))
 

class Statement(Base):
    __tablename__ = "statements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)


class DownloadToken(Base):
    __tablename__ = "download_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, index=True, nullable=False)
    statement_id = Column(Integer, ForeignKey("statements.id"), nullable=False)
    expiration = Column(DateTime, nullable=False)
