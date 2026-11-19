from sqlalchemy.orm import Session
from app.domain.models.reserva_model import Reserva


class AlertaAsignacionRepository:
    @staticmethod
    def obtener_cita_y_empleado(db: Session, id_cita: int, id_empleado: int):
        cita = db.query(Reserva).filter(Reserva.id_reserva == id_cita).first()
        if not cita:
            return None, None

        empleado_id_en_cita = (
            getattr(cita, "empleado_id", None)
            or getattr(cita, "manicurista_id", None)
            or getattr(cita, "id_empleado", None)
        )

        # Si la cita tiene un empleado asignado distinto al solicitado, lo reflejamos
        empleado_objetivo_id = empleado_id_en_cita or id_empleado

        empleado_info = {
            "id_empleado": empleado_objetivo_id,
            "activo": True,
            "contacto": None,
        }

        return cita, empleado_info