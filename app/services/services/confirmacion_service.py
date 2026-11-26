import time
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.repositories.confirmacion_repository import (
    ConfirmacionRepository,
)


class ConfirmacionService:
    @staticmethod
    def _enviar_con_reintentos(
        destinatario: str,
        canal: str,
        mensaje_renderizado: str,
        simular_fallo: bool = False,
        max_reintentos: int = 2,
    ) -> bool:
        if simular_fallo or not destinatario:
            return False

        for intento in range(max_reintentos):
            if destinatario and mensaje_renderizado:
                return True
            if intento < max_reintentos - 1:
                time.sleep(0.1)

        return False

    @staticmethod
    def transmitir_confirmacion(
        db: Session,
        id_reserva: int,
        canal: str = "EMAIL",
        simular_fallo_proveedor: bool = False,
    ):
        reserva, cliente = ConfirmacionRepository.obtener_reserva_y_cliente(
            db, id_reserva
        )

        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada para notificar.",
            )

        estado_reserva = getattr(reserva, "estado", None)
        if estado_reserva and str(estado_reserva).lower() in {"cancelada", "anulada"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La reserva no se encuentra en un estado válido para confirmación.",
            )

        destinatario = None
        if cliente:
            if canal == "SMS":
                destinatario = getattr(cliente, "telefono", None) or getattr(
                    cliente, "celular", None
                )
            else:
                destinatario = getattr(cliente, "email", None) or getattr(
                    cliente, "correo", None
                )

        destinatario = destinatario or "cliente@correo.com"

        plantilla_mensaje = (
            f"Hola! Tu reserva #{id_reserva} en SpaNails ha sido confirmada."
        )

        enviado = ConfirmacionService._enviar_con_reintentos(
            destinatario=destinatario,
            canal=canal,
            mensaje_renderizado=plantilla_mensaje,
            simular_fallo=simular_fallo_proveedor,
        )

        if not enviado:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "mensaje": "No se pudo transmitir la notificación de confirmación",
                    "data": None,
                    "success": False,
                },
            )

        return {
            "message": "Notificación de confirmación procesada",
            "data": {
                "id_notificacion": 900 + id_reserva,
                "tipo": canal,
                "estado": "Enviado",
                "destinatario": destinatario,
            },
            "success": True,
        }