import re

from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.repositories.locations_repository import list_active_locations

VALID_FILTER = re.compile(r"[A-Za-zÁÉÍÓÚáéíóúÑñ\s'-]*")


def get_locations(db: Session, filter_text: str | None):
    filter_text = (filter_text or "").strip()

    if filter_text and not VALID_FILTER.fullmatch(filter_text):
        return JSONResponse(
            status_code=400,
            content={
                "mensaje": "Los parámetros de búsqueda contienen caracteres no válidos.",
                "data": [],
                "success": False,
            },
        )

    try:
        locations = list_active_locations(db, filter_text or None)
    except SQLAlchemyError:
        return JSONResponse(
            status_code=503,
            content={
                "mensaje": "No fue posible consultar las ubicaciones geográficas.",
                "data": [],
                "success": False,
            },
        )

    if not locations:
        return {
            "mensaje": "No se encontraron ubicaciones geográficas configuradas",
            "data": [],
            "success": False,
        }

    return {
        "message": "Ubicaciones consultadas exitosamente",
        "data": locations,
        "success": True,
    }
