from app.domain.models.admin_model import Administrador
from app.api.schemas.admin_schema import AdminCreate
from app.repositories.repositories.admin_repository import admin_repository

class AdminService:
    def __init__(self):
        self.repository = admin_repository

    def crear_admin(self, datos: AdminCreate, rol_usuario_token: str) -> Administrador:
        # Validación HU: Permisos (Lanza error 403 luego en el router)
        if rol_usuario_token != "Gerente":
            raise PermissionError("No cuenta con los permisos necesarios para realizar esta acción")
        
        # Validación HU: Existencia del rol (Lanza error 400 luego en el router)
        nombre_rol = self.repository.find_rol_by_id(datos.id_rol)
        if not nombre_rol:
            raise ValueError("Rol no válido")
        
        nuevo_admin = Administrador(
            id_admin=0,
            nombre=datos.nombre,
            email=datos.email,
            password_hash=f"hashed_{datos.password}_2026",
            id_rol=datos.id_rol,
            rol_nombre=nombre_rol
        )
        
        return self.repository.save(nuevo_admin)

admin_service = AdminService()