from pydantic import BaseModel, Field

class PromedioData(BaseModel):
    promedio_global: float = Field(..., description="Calificación promedio redondeada a 1 decimal")
    total_resenas: int = Field(..., description="Número total de reseñas válidas")

class ResenaPromedioResponse(BaseModel):
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    data: PromedioData
    success: bool = True

    class Config:
        from_attributes = True