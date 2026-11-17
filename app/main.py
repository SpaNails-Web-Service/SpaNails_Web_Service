from fastapi import FastAPI
from database import engine
from app.domain.models.direccion_model import Direccion
from app.domain.models.reserva_model import Reserva

from app.api.routers import cliente_router
from app.api.routers import admin_router
from app.api.routers import auth_router
from app.api.routers import catalogo_router
from app.api.routers import zona_router
from app.api.routers import logistica_router
from app.api.routers import citas_router
from app.api.routers import agenda_router
from app.api.routers import reservas_router
from app.api.routers import confirmacion_router
from app.api.routers import cancelacion_router
from app.api.routers import citas_futuras_router
from app.api.routers import direccion_router
from app.api.routers import empleado_citas_router
from app.api.router import router as products_router
from app.api.parametrics_router import router as parametrics_router

app = FastAPI(
    title="SpaNails API",
    description="API REST de SpaNails con arquitectura de capas",
    version="1.0.0",
)

# Registro de Routers
app.include_router(cliente_router.router)
app.include_router(admin_router.router)
app.include_router(auth_router.router)
app.include_router(catalogo_router.router)
app.include_router(zona_router.router)
app.include_router(logistica_router.router)
app.include_router(citas_router.router)
app.include_router(agenda_router.router)
app.include_router(reservas_router.router)
app.include_router(confirmacion_router.router)
app.include_router(cancelacion_router.router)
app.include_router(citas_futuras_router.router)
app.include_router(direccion_router.router)
app.include_router(empleado_citas_router.router)
app.include_router(products_router)
app.include_router(parametrics_router)