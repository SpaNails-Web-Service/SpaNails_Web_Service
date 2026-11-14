from app.repositories.repositories.catalogo_repository import catalogo_repository
from app.api.schemas.catalogo_schema import ServicioCreate
from app.domain.models.catalogo_model import Servicio

class CatalogoService:
    def __init__(self):
        self.repository = catalogo_repository

    def crear_servicio(self, datos: ServicioCreate, rol_usuario: str) -> Servicio:
        # Validación de permisos (Caso de Prueba 3 - Implícito en roles)
        if rol_usuario not in ["Administrador", "Gerente"]:
            raise PermissionError("No cuenta con los permisos necesarios para realizar esta acción")

        # Validación de duplicidad (Caso de Prueba 2)
        if self.repository.find_servicio_by_nombre(datos.nombre):
            raise FileExistsError("Ya existe un servicio registrado con este nombre")
            
        nuevo_servicio = Servicio(
            id_servicio=0,
            nombre=datos.nombre,
            precio=datos.precio,
            duracion_minutos=datos.duracion_minutos,
            estado="Activo"
        )
        
        return self.repository.save_servicio(nuevo_servicio)

catalogo_service = CatalogoService()
