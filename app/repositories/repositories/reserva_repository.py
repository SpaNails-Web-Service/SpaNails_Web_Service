from sqlalchemy.orm import Session

from app.domain.models.reserva_model import Reserva


class ReservaRepository:
    def crear(self, db: Session, reserva: Reserva) -> Reserva:
        db.add(reserva)
        db.commit()
        db.refresh(reserva)
        return reserva


reserva_repository = ReservaRepository()
