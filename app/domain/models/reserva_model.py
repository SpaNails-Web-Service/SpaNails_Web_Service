from sqlalchemy import Column, Date, Float, Integer, JSON, String

from database import Base


class Reserva(Base):
    __tablename__ = "reservas"

    id_reserva = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    hora_inicio = Column(String(5), nullable=False)
    hora_fin_servicio = Column(String(5), nullable=False)
    hora_fin_bloqueo = Column(String(5), nullable=False)
    modalidad = Column(String(30), nullable=False, index=True)
    id_direccion = Column(Integer, nullable=True)
    servicios_detalle = Column(JSON, nullable=False)
    subtotal = Column(Float, nullable=False)
    costo_domicilio = Column(Integer, nullable=False, default=0)
    total = Column(Float, nullable=False)
    moneda = Column(String(3), nullable=False, default="COP")
    estado = Column(String(30), nullable=False, default="Pendiente", index=True)
