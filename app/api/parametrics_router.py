from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from app.services.parametrics_service import get_locations

router = APIRouter(prefix="/api/v1/parametricas", tags=["Paramétricas"])


@router.get(
    "/ubicaciones",
    summary="Consultar ubicaciones geográficas",
    description=(
        "Lista municipios activos cuyo departamento y país también están activos. "
        "Permite filtrar por nombre de municipio, departamento o país."
    ),
    responses={
        400: {"description": "El filtro contiene caracteres no válidos"},
        503: {"description": "No fue posible consultar la base de datos"},
    },
)
def get_locations_endpoint(
    filter_text: str | None = Query(default=None, alias="filtro"),
    db: Session = Depends(get_db),
):
    return get_locations(db, filter_text)
