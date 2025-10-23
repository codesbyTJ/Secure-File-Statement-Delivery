from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import secrets

from db import get_db
import models
import utils
import auth_utils

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/onboard")
def onboard_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/onboard")
def onboard_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing = db.query(models.User).filter(models.User.email == username).first()
    if existing:
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": "Email already registered"}
        )
    hashed = utils.get_password_hash(password)
    user = models.User(email=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse("/login", status_code=303)


@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_post(
    request: Request,
    username: str = Form(...),  # OAuth2 form uses 'username' field
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user or not utils.verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid credentials"}
        )
    access_token = auth_utils.create_access_token(data={"sub": user.email})
    resp = RedirectResponse("/statements", status_code=303)
    resp.set_cookie("Authorization", f"Bearer {access_token}", httponly=True, samesite="lax")
    resp.set_cookie("user_email", user.email, httponly=False, samesite="lax")
    return resp


@router.get("/logout")
def logout():
    resp = RedirectResponse("/login", status_code=303)
    resp.delete_cookie("Authorization")
    return resp


@router.get("/statements")
def statements_get(request: Request):
    email = request.cookies.get("user_email")
    return templates.TemplateResponse("statements.html", {"request": request, "email": email})


@router.post("/statements/generate-download")
def statements_generate(
    request: Request,
    statement_id: int = Form(...),
    db: Session = Depends(get_db),
):
    statement = db.query(models.Statement).filter(models.Statement.id == statement_id).first()
    if not statement:
        return templates.TemplateResponse(
            "statements.html", {"request": request, "error": "Statement not found"}
        )

    token = secrets.token_urlsafe(16)
    expiration = datetime.now(timezone.utc) + timedelta(minutes=60)
    db_token = models.DownloadToken(token=token, statement_id=statement_id, expiration=expiration)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    # redirect to your existing download endpoint (downloads router)
    return RedirectResponse(f"/statements/download-statement/?token={token}", status_code=303)


@router.post("/statements/generate-download-json")
def generate_download_json(statement_id: int = Form(...), db: Session = Depends(get_db)):
    statement = db.query(models.Statement).filter(models.Statement.id == statement_id).first()
    if not statement:
        return JSONResponse({"error": "Statement not found"}, status_code=404)

    token = secrets.token_urlsafe(16)
    expiration = datetime.now(timezone.utc) + timedelta(minutes=60)
    db_token = models.DownloadToken(token=token, statement_id=statement_id, expiration=expiration)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return {"token": token, "expiration": expiration.isoformat()}