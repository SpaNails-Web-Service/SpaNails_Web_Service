from app.domain.models.zona_model import Zona
from typing import Optional, List

class ZonaRepository:
    _instance = None
    _db: List[Zona] = []
    _current_id: int = 4 # Inicia en 4 para simular el ID 5 de la HU

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ZonaRepository, cls).__new__(cls)
        return cls._instance

    def find_zona_by_nombre(self, nombre: str) -> Optional[Zona]:
        for zona in self._db:
            # Validación de duplicidad sin distinguir mayúsculas/minúsculas ni espacios
            if zona.nombre_zona.strip().lower() == nombre.strip().lower() and zona.estado == "Activo":
                return zona
        return None

    def save_zona(self, zona: Zona) -> Zona:
        self._current_id += 1
        zona.id_zona = self._current_id
        self._db.append(zona)
        return zona

zona_repository = ZonaRepository()
