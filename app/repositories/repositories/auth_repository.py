from app.domain.models.auth_model import UsuarioAuth
from typing import Optional

class AuthRepository:
    _instance = None
    
    # Base de datos simulada para validación de Login
    _db = [
        UsuarioAuth(id_usuario=105, email="cliente@correo.com", password_hash="hashed_secreta123_2026", rol="Cliente", activo=True),
        UsuarioAuth(id_usuario=3, email="admin@spa.com", password_hash="hashed_admin123_2026", rol="Recepcionista", activo=False),
        UsuarioAuth(id_usuario=4, email="administrador@spa.com", password_hash="hashed_admin123_2026", rol="Administrador", activo=True),
    ]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthRepository, cls).__new__(cls)
        return cls._instance

    def find_user_by_email(self, email: str) -> Optional[UsuarioAuth]:
        for user in self._db:
            if user.email == email:
                return user
        return None

    def find_user_by_id(self, user_id: int) -> Optional[UsuarioAuth]:
        for user in self._db:
            if user.id_usuario == user_id:
                return user
        return None

auth_repository = AuthRepository()
