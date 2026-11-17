from sqlalchemy.orm import Session
from app.domain.models.viaje_model import Viaje

class ViajeRepository:
    def find_by_id(self, db: Session, id_viaje: int) -> Viaje | None:
        return db.query(Viaje).filter(Viaje.id == id_viaje).first()

    def update_and_save(self, db: Session, viaje: Viaje) -> Viaje:
        db.commit()
        db.refresh(viaje)
        return viaje
