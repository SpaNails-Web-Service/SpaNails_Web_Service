from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

# --- ESQUEMAS HU-026: Crear Servicio ---
class ServicioCreate(BaseModel):
    nombre: str = Field(..., min_length=2, example="Uñas Acrílicas Premium")
    precio: float = Field(..., example=50000.0)
    duracion_minutos: int = Field(..., example=60)

    @field_validator('precio')
    @classmethod
    def precio_mayor_cero(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser un valor mayor a cero.")
        return v
        
    @field_validator('duracion_minutos')
    @classmethod
    def duracion_mayor_cero(cls, v):
        if v <= 0:
            raise ValueError("La duración debe ser un valor mayor a cero.")
        return v

class ServicioDataResponse(BaseModel):
    id_servicio: int
    nombre: str
    estado: str

class ServicioResponse(BaseModel):
    message: Optional[str] = None
    mensaje: Optional[str] = None
    data: Optional[ServicioDataResponse]
    success: bool

# --- ESQUEMAS HU-029: Consultar Catálogo ---
class ServicioCatalogoItem(BaseModel):
    id_servicio: int
    nombre: str
    precio: float
    duracion_minutos: int
    aplica_domicilio: bool

class CatalogoResponse(BaseModel):
    message: Optional[str] = None
    mensaje: Optional[str] = None
    data: Optional[List[ServicioCatalogoItem]]
    success: bool

# --- ESQUEMAS HU-031: Habilitar Domicilio ---
class ModalidadUpdate(BaseModel):
    aplica_domicilio: bool = Field(..., example=True)

class ModalidadDataResponse(BaseModel):
    id_servicio: int
    aplica_domicilio: bool

class ModalidadResponse(BaseModel):
    message: Optional[str] = None
    mensaje: Optional[str] = None
    data: Optional[ModalidadDataResponse]
    success: bool
