from fastapi import FastAPI

from app.api.routers import cliente_router
from app.api.routers import admin_router  # <-- AGREGADO: Importación del router de administrador (HU-011)
from app.api.router import router as products_router
from app.api.parametrics_router import router as parametrics_router

app = FastAPI(
    title="SpaNails API",
    description="API REST de SpaNails con arquitectura de capas",
    version="1.0.0",
)

# Registro de rutas (Endpoints)
app.include_router(cliente_router.router)
app.include_router(admin_router.router)   # <-- AGREGADO: Registro del router de administrador (HU-011)
app.include_router(products_router)
app.include_router(parametrics_router)


@app.get("/")
def root():
    return {"message": "SpaNails API funcionando"}


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}