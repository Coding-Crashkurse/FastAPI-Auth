from dotenv import find_dotenv, load_dotenv
from datetime import timedelta
load_dotenv(find_dotenv())

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import os

from fastapi_login import LoginManager

from . import auth, crud, models, schemas, sendmail
from .database import engine, get_db, DBContext

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES=60

# manager = LoginManager(SECRET_KEY, token_url="/login", use_cookie=True, use_header=False)
# manager.cookie_name = "auth"


# @manager.user_loader()
# def get_user(username: str, db: Session = None):
#     if db is None:
#         with DBContext() as db:
#             return crud.get_user_by_username(db=db,username=username)    
#     return crud.get_user_by_username(db=db, username=username)


@app.post("/register")
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email existiert bereits im System")
    db_user = crud.create_user(db=db, user=user)
    token = auth.create_access_token(db_user)
    sendmail.send_mail(to=db_user.email, token=token, username=db_user.username)
    return db_user


@app.post("/login")
def login_user(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_username(db=db, username=form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Anmeldeinformationen nicht korrekt"
        )

    if auth.verify_password(form_data.password, db_user.hashed_password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(db_user)
        # response = Response(status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True)
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Anmeldeinformationen nicht korrekt")


@app.get("/logout")
def logout(response: Response):
    response.set_cookie(response, None)
    return response


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


@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_users(db=db)
    return users

@app.get("/secured", dependencies=[Depends(auth.check_active)])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_users(db=db)
    return users


@app.get("/adminsonly", dependencies=[Depends(auth.check_admin)])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_users(db=db)
    return users
