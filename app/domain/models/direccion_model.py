from sqlalchemy import Column, Integer, String
from app.repositories.database import Base 

class Direccion(Base):
    __tablename__ = "direcciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, nullable=False)
    municipio_id = Column(Integer, nullable=False)
    direccion = Column(String(255), nullable=False)
    barrio = Column(String(100), nullable=False)
    observaciones = Column(String(255), nullable=True)