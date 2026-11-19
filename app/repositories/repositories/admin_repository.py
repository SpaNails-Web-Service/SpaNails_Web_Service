from app.domain.models.admin_model import Administrador
from typing import List, Optional

class AdminRepository:
    _instance = None
    _db: List[Administrador] = []
    _current_id: int = 0
    
    # Simulación de la base de datos de roles paramétricos
    _roles_parametricos = {
        1: "Gerente",
        2: "Recepcionista"
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AdminRepository, cls).__new__(cls)
        return cls._instance

    def find_rol_by_id(self, id_rol: int) -> Optional[str]:
        """Verifica si el rol existe en el sistema."""
        return self._roles_parametricos.get(id_rol)

    def save(self, admin: Administrador) -> Administrador:
        """Guarda al administrador en memoria."""
        self._current_id += 1
        admin.id_admin = self._current_id
        self._db.append(admin)
        return admin

admin_repository = AdminRepository()