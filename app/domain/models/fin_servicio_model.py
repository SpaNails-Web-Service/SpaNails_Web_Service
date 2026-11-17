from sqlalchemy import Column, Integer, String, DateTime
from app.repositories.database import Base

class Viaje(Base):
    __tablename__ = "viajes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_reserva = Column(Integer, nullable=False)
    domiciliario_id = Column(Integer, nullable=False)
    estado = Column(String(50), default="Activo", nullable=False)
    resultado = Column(String(50), nullable=True)
    observaciones = Column(String(255), nullable=True)
    fecha_hora_fin = Column(DateTime(timezone=True), nullable=True)