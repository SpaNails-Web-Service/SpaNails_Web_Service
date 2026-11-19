from datetime import datetime, timedelta, timezone

from app.api.schemas.cita_tiempo_schema import CalcularTiempoFinRequest
from app.services.services.catalogo_service import catalogo_service


TIEMPO_ADICIONAL_MINUTOS = 20
# Colombia mantiene UTC-5 y no aplica cambio estacional de hora.
ZONA_HORARIA_NEGOCIO = timezone(timedelta(hours=-5))


class ServicioNoEncontradoError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


class DuracionNoConfiguradaError(Exception):
    pass


class InicioEnElPasadoError(Exception):
    pass


class ModalidadNoDisponibleError(Exception):
    pass


class CitaTiempoService:
    def calcular(self, solicitud: CalcularTiempoFinRequest) -> dict:
        inicio = datetime.combine(
            solicitud.fecha,
            solicitud.hora_inicio,
            tzinfo=ZONA_HORARIA_NEGOCIO,
        )
        if inicio <= datetime.now(ZONA_HORARIA_NEGOCIO):
            raise InicioEnElPasadoError("La fecha y hora de inicio no pueden estar en el pasado")

        duracion_total = 0
        for item in solicitud.servicios:
            servicio = catalogo_service.obtener_servicio(item.id_servicio)
            if servicio is None:
                raise ServicioNoEncontradoError(
                    f"No existe el servicio con ID {item.id_servicio}"
                )
            if servicio.estado.strip().lower() != "activo":
                raise ServicioNoDisponibleError(
                    f"El servicio con ID {item.id_servicio} no está activo"
                )
            if not isinstance(servicio.duracion_minutos, int) or servicio.duracion_minutos <= 0:
                raise DuracionNoConfiguradaError(
                    "No fue posible calcular la duración de uno o más servicios"
                )
            if solicitud.modalidad == "A domicilio" and not servicio.aplica_domicilio:
                raise ModalidadNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está habilitado para domicilio"
                )
            duracion_total += servicio.duracion_minutos

        fin_servicio = inicio + timedelta(minutes=duracion_total)
        fin_bloqueo = fin_servicio + timedelta(minutes=TIEMPO_ADICIONAL_MINUTOS)

        return {
            "hora_inicio": inicio.strftime("%H:%M"),
            "duracion_total_servicios_minutos": duracion_total,
            "hora_fin_servicio": fin_servicio.strftime("%H:%M"),
            "tiempo_adicional_minutos": TIEMPO_ADICIONAL_MINUTOS,
            "hora_fin_bloqueo_agenda": fin_bloqueo.strftime("%H:%M"),
        }


cita_tiempo_service = CitaTiempoService()
