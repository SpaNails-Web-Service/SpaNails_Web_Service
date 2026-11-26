from sqlalchemy.orm import Session
from app.domain.models.reserva_model import Reserva
from app.domain.models.cliente_model import Cliente

class NotificacionRepository:
    @staticmethod
    def obtener_reserva_y_cliente(db: Session, id_reserva: int):
        reserva = db.query(Reserva).filter(Reserva.id == id_reserva).first()
        if not reserva:
            return None, None
            
        cliente = None
        if hasattr(reserva, "cliente_id") and reserva.cliente_id is not None:
            cliente = db.query(Cliente).filter(Cliente.id == reserva.cliente_id).first()
            
        return reserva, cliente