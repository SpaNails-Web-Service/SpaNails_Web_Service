from dataclasses import dataclass

@dataclass
class UsuarioAuth:
    id_usuario: int
    email: str
    password_hash: str
    rol: str
    activo: bool
