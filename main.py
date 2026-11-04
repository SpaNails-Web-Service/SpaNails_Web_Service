from fastapi import FastAPI

app = FastAPI(
    title="SpaNails Web Service",
    description="API RESTful para gestión de citas y servicios de SpaNails",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "SpaNails Web Service",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": "development"
    }