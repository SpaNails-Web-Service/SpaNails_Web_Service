from sqlalchemy.orm import Session
from app.domain.models.cliente_model import Cliente
from app.domain.models.reserva_model import Reserva


class AlertaCancelacionRepository:
    @staticmethod
    def obtener_cita_y_actores(db: Session, id_cita: int):
        cita = db.query(Reserva).filter(Reserva.id_reserva == id_cita).first()
        if not cita:
            return None, None, None

        cliente = None
        if getattr(cita, "cliente_id", None) is not None:
            cliente_pk = getattr(Cliente, "id_cliente", None) or getattr(Cliente, "id", None)
            if cliente_pk is not None:
                cliente = db.query(Cliente).filter(cliente_pk == cita.cliente_id).first()

        # No hay modelo de empleado en app/domain/models ni FK en Reserva
        empleada = None

        return cita, cliente, empleada