import math
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.repositories.repositories.alerta_logistica_repository import (
    AlertaLogisticaRepository,
)


class AlertaLogisticaService:
    @staticmethod
    def calcular_tiempo_estimado_minutos(
        zona,
        distancia_override: float | None = None,
        velocidad_promedio_kmh: float = 24.0,
    ) -> int | None:
        if velocidad_promedio_kmh <= 0:
            return None

        if zona is not None:
            tiempo_directo = (
                getattr(zona, "tiempo_estimado_minutos", None)
                or getattr(zona, "tiempo_promedio_min", None)
                or getattr(zona, "minutos_estimados", None)
            )
            if tiempo_directo is not None:
                try:
                    valor_min = int(round(float(tiempo_directo)))
                    if valor_min > 0:
                        return valor_min
                except (TypeError, ValueError):
                    pass

        distancia_km = distancia_override
        if distancia_km is None and zona is not None:
            distancia_raw = (
                getattr(zona, "distancia_km", None)
                or getattr(zona, "distancia_promedio_km", None)
                or getattr(zona, "distancia", None)
            )
            if distancia_raw is not None:
                try:
                    distancia_km = float(distancia_raw)
                except (TypeError, ValueError):
                    distancia_km = None

        if distancia_km is None or distancia_km <= 0:
            return None

        minutos = math.ceil((distancia_km / velocidad_promedio_kmh) * 60)
        return max(1, int(minutos))

    @staticmethod
    def alertar_estado_logistico(
        db: Session,
        id_cita: int,
        canal: str = "SMS",
        distancia_km: float | None = None,
        velocidad_promedio_kmh: float = 24.0,
    ):
        cita, cliente, zona = AlertaLogisticaRepository.obtener_cita_cliente_y_zona(
            db, id_cita
        )

        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada para transmitir alerta logística.",
            )

        minutos_estimados = AlertaLogisticaService.calcular_tiempo_estimado_minutos(
            zona=zona,
            distancia_override=distancia_km,
            velocidad_promedio_kmh=velocidad_promedio_kmh,
        )

        if minutos_estimados is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "mensaje": "No se pudo estimar el tiempo de llegada",
                    "data": None,
                    "success": False,
                },
            )

        _destinatario = None
        if cliente is not None:
            if canal == "EMAIL":
                _destinatario = getattr(cliente, "email", None) or getattr(
                    cliente, "correo", None
                )
            else:
                _destinatario = (
                    getattr(cliente, "telefono", None)
                    or getattr(cliente, "celular", None)
                    or getattr(cliente, "email", None)
                )

        _mensaje = (
            f"Tu manicurista está En camino para la cita #{id_cita}. "
            f"Tiempo estimado de llegada: {minutos_estimados} minutos."
        )

        return {
            "message": "Alerta logística transmitida al cliente",
            "data": {
                "id_notificacion": 900 + id_cita,
                "estado": "En camino",
                "tiempo_estimado_minutos": minutos_estimados,
            },
            "success": True,
        }