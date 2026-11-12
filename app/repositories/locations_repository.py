from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.domain.locations import Country, Department, Municipality


def list_active_locations(db: Session, filter_text: str | None = None) -> list[dict]:
    statement = (
        select(
            Municipality.municipality_id.label("id_municipio"),
            Municipality.name.label("nombre"),
            Department.name.label("departamento"),
        )
        .join(Department, Municipality.department_id == Department.department_id)
        .join(Country, Department.country_id == Country.country_id)
        .where(
            Municipality.active.is_(True),
            Department.active.is_(True),
            Country.active.is_(True),
        )
    )

    if filter_text:
        pattern = f"%{filter_text}%"
        statement = statement.where(
            or_(
                Municipality.name.ilike(pattern),
                Department.name.ilike(pattern),
                Country.name.ilike(pattern),
            )
        )

    rows = db.execute(statement.order_by(Department.name, Municipality.name)).all()

    return [
        {
            "id_municipio": row.id_municipio,
            "nombre": row.nombre,
            "departamento": row.departamento,
        }
        for row in rows
    ]
