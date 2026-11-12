from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Country(Base):
    __tablename__ = "paises"

    country_id: Mapped[int] = mapped_column("id_pais", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("nombre", String(100), nullable=False)
    active: Mapped[bool] = mapped_column("activo", Boolean, default=True, nullable=False)

    departments: Mapped[list["Department"]] = relationship(back_populates="country")


class Department(Base):
    __tablename__ = "departamentos"

    department_id: Mapped[int] = mapped_column("id_departamento", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("nombre", String(100), nullable=False)
    country_id: Mapped[int] = mapped_column("id_pais", ForeignKey("paises.id_pais"), nullable=False)
    active: Mapped[bool] = mapped_column("activo", Boolean, default=True, nullable=False)

    country: Mapped["Country"] = relationship(back_populates="departments")
    municipalities: Mapped[list["Municipality"]] = relationship(back_populates="department")


class Municipality(Base):
    __tablename__ = "municipios"

    municipality_id: Mapped[int] = mapped_column("id_municipio", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("nombre", String(100), nullable=False)
    department_id: Mapped[int] = mapped_column(
        "id_departamento",
        ForeignKey("departamentos.id_departamento"), nullable=False
    )
    active: Mapped[bool] = mapped_column("activo", Boolean, default=True, nullable=False)

    department: Mapped["Department"] = relationship(back_populates="municipalities")
