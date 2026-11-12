from dataclasses import dataclass
from datetime import date

@dataclass
class Cliente:
    id_cliente: int
    nombre: str
    documento: str
    email: str
    password_hash: str
    fecha_registro: date