from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.api.schemas.Direccion_schema import DireccionCreate 
from app.repositories.repositories.direccion_repository import direccion_repository

class DireccionService:
    def __init__(self):
        self.repository = direccion_repository

    def crear_direccion(self, db: Session, usuario_id: int, direccion_in: DireccionCreate):

        if not self.repository.check_municipio_exists(db, direccion_in.municipio_id):
            raise HTTPException(
                status_code=400,
                detail={
                    "mensaje": "La ubicación seleccionada no es válida",
                    "data": None,
                    "success": False
                }
            )

        try:
            datos_insercion = direccion_in.model_dump()
            datos_insercion["usuario_id"] = usuario_id
            
            direccion_db = self.repository.save(db, datos_insercion)
            direccion_completa = f"{direccion_db.direccion}, {direccion_db.barrio}"
            
            return {
                "message": "Dirección añadida exitosamente",
                "data": {
                    "id_direccion": direccion_db.id,
                    "direccion_completa": direccion_completa
                },
                "success": True
            }
            
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=503,
                detail="Service Unavailable: Falla en la conexión a la base de datos"
            )

# Instancia del servicio
direccion_service = DireccionService()