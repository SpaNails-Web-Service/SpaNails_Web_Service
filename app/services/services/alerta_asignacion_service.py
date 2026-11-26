from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.repositories.repositories.alerta_asignacion_repository import (
    AlertaAsignacionRepository,
)


class AlertaAsignacionService:
    @staticmethod
    def _resumen_servicio(cita) -> str:
        detalle = getattr(cita, "servicios_detalle", None)
        if isinstance(detalle, list) and detalle:
            nombres = [
                item.get("nombre") or item.get("servicio") or str(item)
                if isinstance(item, dict)
                else str(item)
                for item in detalle
            ]
            return ", ".join(nombres)
        if detalle:
            return str(detalle)
        return "Servicio de SpaNails"

    @staticmethod
    def alertar_asignacion(
        db: Session,
        id_cita: int,
        id_empleado: int,
        metodo: str = "PUSH",
        empleado_activo: bool | None = None,
    ):
        cita, empleado_info = AlertaAsignacionRepository.obtener_cita_y_empleado(
            db, id_cita, id_empleado
        )

        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada para alertar asignación.",
            )

        if id_empleado <= 0 or not empleado_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado.",
            )

        esta_activo = (
            empleado_activo
            if empleado_activo is not None
            else bool(empleado_info.get("activo", False))
        )

        if not esta_activo:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "mensaje": "El empleado destino no se encuentra activo",
                    "data": None,
                    "success": False,
                },
            )

        fecha = getattr(cita, "fecha", "por confirmar")
        hora = getattr(cita, "hora_inicio", "por confirmar")
        servicio = AlertaAsignacionService._resumen_servicio(cita)

        _mensaje_alerta = (
            f"Nueva cita #{id_cita} asignada: {servicio} el {fecha} a las {hora}."
        )

        return {
            "message": "Notificación de asignación enviada",
            "data": {
                "id_notificacion": 900 + id_cita,
                "id_empleado": id_empleado,
                "metodo": metodo,
            },
            "success": True,
        }