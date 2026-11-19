from app.repositories.repositories.zona_repository import zona_repository
from app.api.schemas.zona_schema import ZonaCreate
from app.domain.models.zona_model import Zona
from typing import Optional

class ZonaService:
    def __init__(self):
        self.repository = zona_repository

    # --- HU-036: Crear Zona ---
    def crear_zona(self, datos: ZonaCreate, rol_usuario: str) -> Zona:
        if rol_usuario not in ["Administrador", "Gerente"]:
            raise PermissionError("No cuenta con los permisos necesarios para realizar esta acción")

        if self.repository.find_zona_by_nombre(datos.nombre_zona):
            raise FileExistsError("Ya existe una zona de cobertura con ese nombre")
            
        nueva_zona = Zona(
            id_zona=0,
            nombre_zona=datos.nombre_zona.strip(),
            estado="Activo",
            tarifa_domicilio=datos.tarifa_domicilio,
        )
        
        return self.repository.save_zona(nueva_zona)

    # --- HU-038: Comprobar Cobertura ---
    def validar_cobertura(self, ubicacion: str) -> Optional[Zona]:
        """
        Retorna la Zona si hay cobertura (Caso 1), o None si no hay (Caso 2).
        Lanza ValueError si falta el parámetro (Caso 4).
        """
        if not ubicacion or not ubicacion.strip():
            raise ValueError("Parámetros de ubicación incompletos")
            
        return self.repository.find_zona_by_barrio(ubicacion)

zona_service = ZonaService()
