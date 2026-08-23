from fastapi import FastAPI
from sqlalchemy import text
from database import engine

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