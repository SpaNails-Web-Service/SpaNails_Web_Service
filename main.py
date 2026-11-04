import os

from fastapi import FastAPI

app = FastAPI(
    title="SpaNails Web Service",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "SpaNails API funcionando correctamente"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": os.getenv("APP_ENV", "development"),
    }
