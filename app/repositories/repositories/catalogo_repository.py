from app.domain.models.catalogo_model import Servicio
from typing import Optional, List

class CatalogoRepository:
    _instance = None
    
    _db: List[Servicio] = [
        Servicio(id_servicio=10, nombre="Manicura Semipermanente", precio=45000.0, duracion_minutos=60, estado="Activo", aplica_domicilio=False),
        Servicio(id_servicio=11, nombre="Pedicura Spa", precio=35000.0, duracion_minutos=45, estado="Inactivo", aplica_domicilio=False)
    ]
    _current_id: int = 40 

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

    def get_servicios_activos(self) -> List[Servicio]:
        return [s for s in self._db if s.estado == "Activo"]

    # --- HU-031: Habilitar Domicilio ---
    def find_servicio_by_id(self, id_servicio: int) -> Optional[Servicio]:
        """Busca un servicio por su ID."""
        for servicio in self._db:
            if servicio.id_servicio == id_servicio:
                return servicio
        return None

    def update_modalidad(self, id_servicio: int, aplica_domicilio: bool) -> Servicio:
        """Actualiza la bandera de domicilio del servicio."""
        servicio = self.find_servicio_by_id(id_servicio)
        if servicio:
            servicio.aplica_domicilio = aplica_domicilio
        return servicio

catalogo_repository = CatalogoRepository()
