from datetime import date, time
from sqlalchemy.orm import Session

from app.domain.models.reserva_model import Reserva


class AgendaRepository:
    """Consulta los bloques ocupados registrados en la tabla de reservas."""

    def obtener_bloques_ocupados(
        self, db: Session, fecha: date, modalidad: str
    ) -> list[tuple[time, time]]:
        filas = (
            db.query(Reserva.hora_inicio, Reserva.hora_fin_bloqueo)
            .filter(
                Reserva.fecha == fecha,
                Reserva.modalidad == modalidad,
                Reserva.estado != "Cancelada",
            )
            .all()
        )
        return [
            (time.fromisoformat(hora_inicio), time.fromisoformat(hora_fin))
            for hora_inicio, hora_fin in filas
        ]


agenda_repository = AgendaRepository()
