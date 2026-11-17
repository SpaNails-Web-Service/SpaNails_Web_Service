from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.api.schemas.fin_servicio_schemea import ViajeFinalizarCreate
from app.repositories.repositories.fin_servicio_repository import ViajeRepository

class ViajeService:
    def __init__(self, repository: ViajeRepository):
        self.repository = repository

    def finalizar_viaje(self, db: Session, id_viaje: int, datos: ViajeFinalizarCreate, usuario_actual: dict):
        viaje = self.repository.find_by_id(db, id_viaje)
        if not viaje:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El viaje especificado no existe"
            )

        if viaje.estado == "Finalizado":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "mensaje": "El viaje ya se encuentra finalizado",
                    "data": None,
                    "success": False
                }
            )

        es_admin = "Administrador" in usuario_actual.get("roles", [])
        es_asignado = viaje.domiciliario_id == usuario_actual.get("id")
        
        if not es_admin and not es_asignado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No cuenta con los permisos para finalizar este viaje"
            )

        colombia_tz = timezone(timedelta(hours=-5))
        fecha_actual = datetime.now(colombia_tz)

        viaje.estado = "Finalizado"
        viaje.resultado = datos.resultado
        viaje.observaciones = datos.observaciones
        viaje.fecha_hora_fin = fecha_actual

        viaje_actualizado = self.repository.update_and_save(db, viaje)

        return {
            "mensaje": "Servicio logístico finalizado exitosamente",
            "data": {
                "id_viaje": viaje_actualizado.id,
                "id_reserva": viaje_actualizado.id_reserva,
                "estado": viaje_actualizado.estado,
                "resultado": viaje_actualizado.resultado,
                "fecha_hora_fin": viaje_actualizado.fecha_hora_fin.isoformat()
            },
            "success": True
        }