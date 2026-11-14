from app.repositories.repositories.zona_repository import zona_repository
from app.api.schemas.zona_schema import ZonaCreate
from app.domain.models.zona_model import Zona

class ZonaService:
    def __init__(self):
        self.repository = zona_repository

    def crear_zona(self, datos: ZonaCreate, rol_usuario: str) -> Zona:
        # Validación de permisos (Caso 4 y RBAC)
        if rol_usuario not in ["Administrador", "Gerente"]:
            raise PermissionError("No cuenta con los permisos necesarios para realizar esta acción")

        # Validación de duplicidad (Caso 2)
        if self.repository.find_zona_by_nombre(datos.nombre_zona):
            raise FileExistsError("Ya existe una zona de cobertura con ese nombre")
            
        nueva_zona = Zona(
            id_zona=0,
            nombre_zona=datos.nombre_zona.strip(),
            estado="Activo"
        )
        
        return self.repository.save_zona(nueva_zona)

zona_service = ZonaService()
