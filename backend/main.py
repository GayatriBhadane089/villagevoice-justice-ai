from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models.user import User
from schemas import UserRegister, UserLogin, TokenResponse
from auth import hash_password, verify_password, create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="VillageVoice Justice AI - Backend")


@app.get("/")
def read_root():
    return {
        "message": "VillageVoice Justice AI backend is running.",
        "status": "research prototype"
    }


@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database_connection": "success"}
    except Exception as e:
        return {"database_connection": "failed", "error": str(e)}


@app.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone_number == user_data.phone_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    new_user = User(
        full_name=user_data.full_name,
        phone_number=user_data.phone_number,
        preferred_language=user_data.preferred_language,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": str(new_user.id)}


@app.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == login_data.phone_number).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid phone number or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token)