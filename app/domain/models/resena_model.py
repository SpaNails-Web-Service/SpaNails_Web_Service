from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Resena(Base):
    __tablename__ = "resenas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_reserva = Column(Integer, nullable=False)
    calificacion = Column(Integer, nullable=False)
    comentario = Column(String(500), nullable=True)
    estado = Column(String(50), default="Activa", nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)