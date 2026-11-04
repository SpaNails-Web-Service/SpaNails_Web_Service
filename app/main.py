from fastapi import FastAPI

app = FastAPI(
    title="SpaNails API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "SpaNails API funcionando"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": "development"
    }
