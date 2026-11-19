from dataclasses import dataclass

@dataclass
class Administrador:
    id_admin: int
    nombre: str
    email: str
    password_hash: str
    id_rol: int
    rol_nombre: str