from app.repositories.repositories.catalogo_repository import catalogo_repository
from app.api.schemas.catalogo_schema import ServicioCreate
from app.domain.models.catalogo_model import Servicio
from typing import List

class CatalogoService:
    def __init__(self):
        self.repository = catalogo_repository

    # --- HU-026: Crear Servicio ---
    def crear_servicio(self, datos: ServicioCreate, rol_usuario: str) -> Servicio:
        if rol_usuario not in ["Administrador", "Gerente"]:
            raise PermissionError("No cuenta con los permisos necesarios para realizar esta acción")

        if self.repository.find_servicio_by_nombre(datos.nombre):
            raise FileExistsError("Ya existe un servicio registrado con este nombre")
            
        nuevo_servicio = Servicio(
            id_servicio=0,
            nombre=datos.nombre,
            precio=datos.precio,
            duracion_minutos=datos.duracion_minutos,
            estado="Activo",
            aplica_domicilio=False # Por defecto
        )
        
        return self.repository.save_servicio(nuevo_servicio)

    # --- HU-029: Consultar Catálogo ---
    def obtener_catalogo(self) -> List[Servicio]:
        return self.repository.get_servicios_activos()

catalogo_service = CatalogoService()
