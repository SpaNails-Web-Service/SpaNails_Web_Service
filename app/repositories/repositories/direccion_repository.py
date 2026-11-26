from sqlalchemy.orm import Session

from app.domain.models.direccion_model import Direccion


class DireccionRepository:
    def check_municipio_exists(self, db: Session, municipio_id: int) -> bool:
        # Validación temporal hasta integrar la tabla paramétrica de municipios.
        return municipio_id > 0

    def save(self, db: Session, direccion_data: dict) -> Direccion:
        nueva_direccion = Direccion(**direccion_data)
        db.add(nueva_direccion)
        db.commit()
        db.refresh(nueva_direccion)
        return nueva_direccion

    def find_owned_address(self, db: Session, address_id: int, user_id: int):
        # Buscar por ambos campos evita revelar si una dirección ajena existe.
        return (
            db.query(Direccion)
            .filter(
                Direccion.id == address_id,
                Direccion.usuario_id == user_id,
            )
            .first()
        )


direccion_repository = DireccionRepository()
