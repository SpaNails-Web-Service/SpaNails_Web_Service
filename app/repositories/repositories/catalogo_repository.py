from app.domain.models.catalogo_model import Servicio
from typing import Optional, List

class CatalogoRepository:
    _instance = None
    _db: List[Servicio] = []
    _current_id: int = 40 # Inicia en 40 para simular el ID 45 de la HU

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CatalogoRepository, cls).__new__(cls)
        return cls._instance

    def find_servicio_by_nombre(self, nombre: str) -> Optional[Servicio]:
        for servicio in self._db:
            if servicio.nombre.strip().lower() == nombre.strip().lower():
                return servicio
        return None

    def save_servicio(self, servicio: Servicio) -> Servicio:
        self._current_id += 1
        servicio.id_servicio = self._current_id
        self._db.append(servicio)
        return servicio

catalogo_repository = CatalogoRepository()
