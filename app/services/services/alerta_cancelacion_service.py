from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.repositories.repositories.alerta_cancelacion_repository import (
    AlertaCancelacionRepository,
)


class AlertaCancelacionService:
    @staticmethod
    def _plantilla_cliente(id_cita: int) -> str:
        return (
            f"Hola, te informamos que tu cita #{id_cita} en SpaNails ha sido cancelada "
            f"y el espacio en agenda ha sido liberado."
        )

    @staticmethod
    def _plantilla_empleada(id_cita: int) -> str:
        return (
            f"Hola, la cita #{id_cita} asignada ha sido cancelada y el espacio en tu "
            f"agenda quedó disponible."
        )

    @staticmethod
    def _extraer_contacto(actor, canal: str) -> str | None:
        if not actor:
            return None
        if canal == "PUSH":
            return getattr(actor, "device_token", None) or getattr(actor, "email", None)
        return getattr(actor, "email", None) or getattr(actor, "correo", None)

    @staticmethod
    def alertar_cancelacion(db: Session, id_cita: int, canal: str = "EMAIL"):
        cita, cliente, empleada = AlertaCancelacionRepository.obtener_cita_y_actores(
            db, id_cita
        )

        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada para alertar cancelación.",
            )

        correo_cliente = AlertaCancelacionService._extraer_contacto(cliente, canal)
        correo_empleada = AlertaCancelacionService._extraer_contacto(empleada, canal)

        if not correo_cliente or not correo_empleada:
            return JSONResponse(
                status_code=status.HTTP_206_PARTIAL_CONTENT,
                content={
                    "mensaje": "Alerta procesada parcialmente por falta de datos de contacto",
                    "data": None,
                    "success": False,
                },
            )

        _mensaje_cliente = AlertaCancelacionService._plantilla_cliente(id_cita)
        _mensaje_empleada = AlertaCancelacionService._plantilla_empleada(id_cita)

        destinos = [correo_cliente, correo_empleada]

        return {
            "message": "Alertas de cancelación transmitidas",
            "data": {
                "alertas_generadas": len(destinos),
                "destinos": destinos,
            },
            "success": True,
        }