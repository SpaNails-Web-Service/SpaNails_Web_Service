from fastapi import FastAPI

app = FastAPI(
    title="SpaNails Web Service",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "SpaNails API funcionando correctamente"
    }