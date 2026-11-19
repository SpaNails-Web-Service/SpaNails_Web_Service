from datetime import date

from sqlalchemy.orm import Session

from app.domain.models.reserva_model import Reserva


class ReservaRepository:
    def listar_futuras_cliente(
        self, db: Session, cliente_id: int, desde: date
    ) -> list[Reserva]:
        return (
            db.query(Reserva)
            .filter(
                Reserva.cliente_id == cliente_id,
                Reserva.fecha >= desde,
                Reserva.estado.in_(("Pendiente", "Confirmada")),
            )
            .order_by(Reserva.fecha.asc(), Reserva.hora_inicio.asc())
            .all()
        )

    def obtener_por_id(self, db: Session, id_reserva: int) -> Reserva | None:
        return db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()

    def crear(self, db: Session, reserva: Reserva) -> Reserva:
        db.add(reserva)
        db.commit()
        db.refresh(reserva)
        return reserva


reserva_repository = ReservaRepository()
