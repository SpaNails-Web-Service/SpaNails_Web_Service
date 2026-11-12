from fastapi import FastAPI
# 1. Importas el router de la capa api
from app.api.routers import cliente_router 

app = FastAPI(
    title="SpaNails API",
    version="1.0.0"
)

# 2. Registras el router en la aplicación de FastAPI
app.include_router(cliente_router.router)

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