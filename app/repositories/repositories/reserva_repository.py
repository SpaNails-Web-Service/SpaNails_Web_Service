from sqlalchemy.orm import Session

from app.domain.models.reserva_model import Reserva


class ReservaRepository:
    def obtener_por_id(self, db: Session, id_reserva: int) -> Reserva | None:
        return db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()

    def crear(self, db: Session, reserva: Reserva) -> Reserva:
        db.add(reserva)
        db.commit()
        db.refresh(reserva)
        return reserva


reserva_repository = ReservaRepository()
