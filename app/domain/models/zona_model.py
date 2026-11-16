from dataclasses import dataclass
from typing import Optional

@dataclass
class Zona:
    id_zona: int
    nombre_zona: str
    estado: str
    tarifa_domicilio: Optional[int] = None
