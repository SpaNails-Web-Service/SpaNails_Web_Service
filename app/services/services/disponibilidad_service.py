from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy.orm import Session

from app.repositories.repositories.agenda_repository import agenda_repository
from app.repositories.repositories.direccion_repository import direccion_repository
from app.services.services.catalogo_service import catalogo_service
from app.services.services.cita_tiempo_service import TIEMPO_ADICIONAL_MINUTOS
from app.services.services.zona_service import zona_service


ZONA_HORARIA_NEGOCIO = timezone(timedelta(hours=-5))
INTERVALO_INICIOS_MINUTOS = 30

HORARIO_SEMANAL = {
    0: ((time(9, 0), time(13, 0)), (time(14, 0), time(18, 0))),
    1: ((time(9, 0), time(13, 0)), (time(14, 0), time(18, 0))),
    2: ((time(9, 0), time(13, 0)), (time(14, 0), time(18, 0))),
    3: ((time(9, 0), time(13, 0)), (time(14, 0), time(18, 0))),
    4: ((time(9, 0), time(13, 0)), (time(14, 0), time(18, 0))),
    5: ((time(9, 0), time(13, 0)),),
    6: (),
}


class ServicioNoEncontradoError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


class FechaNoValidaError(Exception):
    pass


class ModalidadNoDisponibleError(Exception):
    pass


class DireccionNoEncontradaError(Exception):
    pass


class FueraDeCoberturaError(Exception):
    pass


class DisponibilidadService:
    def _normalizar_modalidad(self, modalidad: str) -> str:
        valor = modalidad.strip().lower()
        if valor in {"spa", "en el spa"}:
            return "En el spa"
        if valor in {"domicilio", "a domicilio"}:
            return "A domicilio"
        raise ValueError("La modalidad debe ser 'En el spa' o 'A domicilio'")

    def consultar(
        self,
        db: Session,
        id_servicio: int,
        fecha: date,
        modalidad: str,
        id_direccion: int | None = None,
        user_id: int | None = None,
    ) -> dict:
        modalidad_normalizada = self._normalizar_modalidad(modalidad)
        hoy = datetime.now(ZONA_HORARIA_NEGOCIO).date()
        if fecha <= hoy:
            raise FechaNoValidaError("La fecha debe ser futura")

        servicio = catalogo_service.obtener_servicio(id_servicio)
        if servicio is None:
            raise ServicioNoEncontradoError(
                f"No existe el servicio con ID {id_servicio}"
            )
        if servicio.estado.strip().lower() != "activo":
            raise ServicioNoDisponibleError("El servicio no está activo")
        if not isinstance(servicio.duracion_minutos, int) or servicio.duracion_minutos <= 0:
            raise ServicioNoDisponibleError(
                "No fue posible calcular la duración del servicio"
            )

        if modalidad_normalizada == "A domicilio":
            if not servicio.aplica_domicilio:
                raise ModalidadNoDisponibleError(
                    "El servicio no está habilitado para domicilio"
                )
            if id_direccion is None or user_id is None:
                raise ValueError(
                    "Para domicilio debe iniciar sesión y enviar una dirección registrada"
                )
            direccion = direccion_repository.find_owned_address(
                db, id_direccion, user_id
            )
            if direccion is None:
                raise DireccionNoEncontradaError(
                    "La dirección no existe o no pertenece al cliente"
                )
            if zona_service.validar_cobertura(direccion.barrio) is None:
                raise FueraDeCoberturaError(
                    "La dirección se encuentra fuera de la zona de cobertura"
                )

        bloque_minutos = servicio.duracion_minutos + TIEMPO_ADICIONAL_MINUTOS
        ventanas = HORARIO_SEMANAL[fecha.weekday()]
        bloqueos = agenda_repository.obtener_bloques_ocupados(
            fecha, modalidad_normalizada
        )
        horarios = []
        intervalo = timedelta(minutes=INTERVALO_INICIOS_MINUTOS)
        duracion = timedelta(minutes=servicio.duracion_minutos)
        bloque = timedelta(minutes=bloque_minutos)

        for apertura, cierre in ventanas:
            inicio = datetime.combine(fecha, apertura)
            limite = datetime.combine(fecha, cierre)
            while inicio + bloque <= limite:
                fin_bloqueo = inicio + bloque
                ocupado = any(
                    inicio.time() < fin_ocupado and fin_bloqueo.time() > inicio_ocupado
                    for inicio_ocupado, fin_ocupado in bloqueos
                )
                if not ocupado:
                    horarios.append(
                        {
                            "hora_inicio": inicio.strftime("%H:%M"),
                            "hora_fin": (inicio + duracion).strftime("%H:%M"),
                        }
                    )
                inicio += intervalo

        mensaje = (
            "Disponibilidad consultada exitosamente"
            if horarios
            else "No hay horarios disponibles para los criterios seleccionados"
        )
        return {
            "mensaje": mensaje,
            "data": {
                "fecha": fecha,
                "id_servicio": id_servicio,
                "modalidad": modalidad_normalizada,
                "horarios_disponibles": horarios,
            },
            "success": True,
        }


disponibilidad_service = DisponibilidadService()
