from sqlalchemy.orm import Session
from app.domain.models.reserva_model import Reserva

try:
    from app.domain.models.cliente_model import Cliente
except ImportError:
    Cliente = None

try:
    from app.domain.models.zona_model import Zona
except ImportError:
    Zona = None


class AlertaLogisticaRepository:
    @staticmethod
    def obtener_cita_cliente_y_zona(db: Session, id_cita: int):
        cita = db.query(Reserva).filter(Reserva.id_reserva == id_cita).first()
        if not cita:
            return None, None, None

        cliente = None
        if Cliente is not None and getattr(cita, "cliente_id", None) is not None:
            cliente_pk = getattr(Cliente, "id_cliente", None) or getattr(Cliente, "id", None)
            if cliente_pk is not None:
                cliente = db.query(Cliente).filter(cliente_pk == cita.cliente_id).first()

        zona = None
        if Zona is not None:
            zona_id = getattr(cita, "zona_id", None) or getattr(cita, "id_zona", None)
            zona_pk = getattr(Zona, "id_zona", None) or getattr(Zona, "id", None)
            if zona_id is not None and zona_pk is not None:
                zona = db.query(Zona).filter(zona_pk == zona_id).first()
            elif zona_pk is not None:
                zona = db.query(Zona).first()

        return cita, cliente, zona