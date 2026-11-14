from app.domain.models.catalogo_model import Servicio
from typing import Optional, List

class CatalogoRepository:
    _instance = None
    
    # Pre-cargamos servicios para probar el GET (HU-029)
    _db: List[Servicio] = [
        Servicio(id_servicio=10, nombre="Manicura Semipermanente", precio=45000.0, duracion_minutos=60, estado="Activo", aplica_domicilio=True),
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
        # HU-029: Retorna únicamente los servicios con estado Activo
        return [s for s in self._db if s.estado == "Activo"]

catalogo_repository = CatalogoRepository()
