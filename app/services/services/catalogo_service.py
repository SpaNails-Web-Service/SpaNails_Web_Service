from app.repositories.repositories.catalogo_repository import catalogo_repository
from app.api.schemas.catalogo_schema import ServicioCreate, ModalidadUpdate
from app.domain.models.catalogo_model import Servicio
from typing import List

class CatalogoService:
    def __init__(self):
        self.repository = catalogo_repository

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
            aplica_domicilio=False
        )
        
        return self.repository.save_servicio(nuevo_servicio)

    def obtener_catalogo(self) -> List[Servicio]:
        return self.repository.get_servicios_activos()

    # --- HU-031: Habilitar Domicilio ---
    def actualizar_modalidad(self, id_servicio: int, datos: ModalidadUpdate, rol_usuario: str) -> Servicio:
        # Validación de permisos (Caso 4)
        if rol_usuario not in ["Administrador", "Gerente"]:
            raise PermissionError("No tiene permisos para modificar el catálogo.")
            
        # Validación de existencia (Caso 2)
        servicio = self.repository.find_servicio_by_id(id_servicio)
        if not servicio:
            raise KeyError("El servicio especificado no fue encontrado")
            
        # Actualización
        return self.repository.update_modalidad(id_servicio, datos.aplica_domicilio)

catalogo_service = CatalogoService()
