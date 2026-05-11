from fastapi import FastAPI
from app.routes.chat import router as chat_router

app = FastAPI(title="SHL Assessment Agent")

app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "SHL Assessment Agent Running"}

@app.get("/health")
def health():
    return {"status": "ok"}