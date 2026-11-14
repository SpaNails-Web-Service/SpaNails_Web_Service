from dataclasses import dataclass

@dataclass
class Servicio:
    id_servicio: int
    nombre: str
    precio: float
    duracion_minutos: int
    estado: str
