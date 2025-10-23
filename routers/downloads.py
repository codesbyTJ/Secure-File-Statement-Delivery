#implemet andpoint to create download tokens.
#Generate unique token for each download request.
#Store the download tokens in the database with expiration time.
#return the token reponse

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone 
import secrets
import os
import starlette.responses as FileResponse

from db import get_db
from models import DownloadToken as DBDownloadToken, Statement
import schemas

router=APIRouter()

@router.post("/generate-download-token", response_model=schemas.DownloadToken)
def generrate_download_token(statement_id: int, db: Session = Depends(get_db)):
    token=secrets.token_urlsafe(16)
    #first check if statement exists
    statement=db.query(Statement).filter(Statement.id==statement_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement could not be found")
    
    #create enique token with expiry time

    token=secrets.token_urlsafe(16)
    expiration=datetime.now(timezone.utc)+ timedelta(minutes=60) #token valid for 60 minutes

    #now save this ot the db

    db_token=DBDownloadToken(token=token, statement_id=statement_id, expiration=expiration)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token

@router.get("/download-statement/")
def download_statement(token: str = Query(...), db: Session = Depends(get_db)):
    db_token=db.query(DBDownloadToken).filter(DBDownloadToken.token==token).first()
    if not db_token or db_token.expiration < datetime.now(timezone.utc):
        raise HTTPException(status_code=404, detail="Invalid or expired download token")
    
    statement=db.query(Statement).filter(Statement.id==db_token.statement_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")

    file_path=os.path.join("statements_files", statement.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    return FileResponse(path=file_path, filename=statement.filename, media_type='application/octet-stream')

