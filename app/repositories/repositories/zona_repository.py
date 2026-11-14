from app.domain.models.zona_model import Zona
from typing import Optional, List

class ZonaRepository:
    _instance = None
    
    # Base de datos pre-cargada para probar la HU-038
    _db: List[Zona] = [
        Zona(id_zona=5, nombre_zona="Cabecera", estado="Activo"),
        Zona(id_zona=6, nombre_zona="Provenza", estado="Inactivo")
    ]
    _current_id: int = 6

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ZonaRepository, cls).__new__(cls)
        return cls._instance

    # --- HU-036: Crear Zona ---
    def find_zona_by_nombre(self, nombre: str) -> Optional[Zona]:
        for zona in self._db:
            if zona.nombre_zona.strip().lower() == nombre.strip().lower() and zona.estado == "Activo":
                return zona
        return None

    def save_zona(self, zona: Zona) -> Zona:
        self._current_id += 1
        zona.id_zona = self._current_id
        self._db.append(zona)
        return zona

    # --- HU-038: Comprobar Cobertura ---
    def find_zona_by_barrio(self, barrio_o_ubicacion: str) -> Optional[Zona]:
        """
        Simulador de motor geo-espacial para el MVP.
        Busca si el barrio ingresado coincide con una zona ACTIVA.
        """
        for zona in self._db:
            # Validamos que coincida el nombre y que esté activa
            if zona.nombre_zona.strip().lower() == barrio_o_ubicacion.strip().lower():
                if zona.estado == "Activo":
                    return zona
        return None

zona_repository = ZonaRepository()
