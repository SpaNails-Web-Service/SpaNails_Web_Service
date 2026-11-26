from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.repositories.empleado_citas_repository import EmpleadoCitasRepository

class EmpleadoCitasService:
    def __init__(self, repository: EmpleadoCitasRepository):
        self.repository = repository

    def obtener_agenda_manicurista(self, db: Session, usuario_actual: dict):
        # 1. Validar restricción de rol (RBAC)
        roles = usuario_actual.get("roles", [])
        if "Manicurista" not in roles and "Administrador" not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Permisos insuficientes."
            )

        empleado_id = usuario_actual.get("id")

        # 2. Consultar citas asignadas exclusivamente al empleado logueado
        citas = self.repository.obtener_citas_por_empleado(db, empleado_id)

        # 3. Retornar estructura acorde a si tiene o no asignaciones
        if not citas:
            return {
                "mensaje": "No tienes citas asignadas para hoy",
                "data": [],
                "success": True
            }

        return {
            "message": "Agenda consultada exitosamente",
            "data": citas,
            "success": True
        }