from fastapi import FastAPI

app = FastAPI(title="VillageVoice Justice AI - Backend")

@app.get("/")
def read_root():
    return {
        "message": "VillageVoice Justice AI backend is running.",
        "status": "research prototype"
    }