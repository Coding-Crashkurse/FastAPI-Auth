from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional

from . import auth, crud, models, schemas, sendmail
from .database import get_db, DBContext


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse(url='/docs')


@app.post("/register")
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email existiert bereits im System")
    db_user = crud.create_user(db=db, user=user)
    token = auth.create_access_token(db_user)
    sendmail.send_mail(to=db_user.email, token=token, username=db_user.username)
    return


@app.post('/login', response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_username(db=db, username=form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Anmeldeinformationen nicht korrekt"
        )

    if auth.verify_password(form_data.password, db_user.hashed_password):
        access_token = auth.create_access_token(db_user)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Anmeldeinformationen nicht korrekt")


@app.get("/verify/{token}", response_class=HTMLResponse)
def login_user(token: str, db: Session = Depends(get_db)):
    payload = auth.verify_token(token)
    username = payload.get("sub")
    db_user = crud.get_users_by_username(db, username)
    db_user.is_active = True
    db.commit()
    return f"""
    <html>
        <head>
            <title>Bestätigung der Registrierung</title>
        </head>
        <body>
            <h2>Aktivierung von {username} erfolgreich!</h2>
            <a href="https://google.com">
                Zurück
            </a>
        </body>
    </html>
    """


@app.get("/user/me", response_model=schemas.UserPlain)
def get_current_user(db: Session = Depends(get_db), username: str = Depends(auth.get_current_user)):
    db_user = crud.get_user_by_username(db=db, username=username)
    return db_user

@app.get("/users", dependencies=[Depends(auth.check_active)], response_model=List[schemas.UserPlain])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", dependencies=[Depends(auth.check_active)], response_model=schemas.UserPlain)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/adminsonly", dependencies=[Depends(auth.check_admin)], response_model=List[schemas.UserDB])
def get_all_users_admin(db: Session = Depends(get_db)):
    users = crud.get_users(db=db)
    return users
