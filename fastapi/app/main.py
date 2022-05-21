from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, crud, models, schemas, sendmail
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/register")
def register_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    # db_user = crud.get_users_by_username(db=db, username=user.username)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email existiert bereits im System")
    db_user = crud.create_user(db=db, user=user)
    token = auth.create_access_token(db_user)
    sendmail.send_mail(to=db_user.email, token=token, username=db_user.username)
    return db_user


@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = crud.get_users_by_username(db=db, username=form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Anmeldeinformationen nicht korrekt"
        )

    if auth.verify_password(form_data.password, db_user.hashed_password):
        token = auth.create_access_token(db_user)
        return {"access_token": token, "token_Type": "bearer"}
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
