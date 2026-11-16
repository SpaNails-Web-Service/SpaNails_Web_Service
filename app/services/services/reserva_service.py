from datetime import datetime, timedelta, timezone
from threading import RLock

from sqlalchemy.orm import Session

from app.api.schemas.reserva_schema import ReservaCreate
from app.domain.models.reserva_model import Reserva
from app.repositories.repositories.reserva_repository import reserva_repository
from app.services.services.catalogo_service import catalogo_service
from app.services.services.cita_tiempo_service import TIEMPO_ADICIONAL_MINUTOS
from app.services.services.domicilio_service import (
    DireccionNoEncontradaError,
    FueraDeCoberturaError,
    TarifaNoConfiguradaError,
    domicilio_service,
)
from app.services.services.disponibilidad_service import (
    disponibilidad_service,
)


ZONA_HORARIA_NEGOCIO = timezone(timedelta(hours=-5))


class ServicioReservaNoEncontradoError(Exception):
    pass


class ServicioReservaNoDisponibleError(Exception):
    pass


class ModalidadReservaNoDisponibleError(Exception):
    pass


class FechaReservaInvalidaError(Exception):
    pass


class HorarioNoDisponibleError(Exception):
    pass


class ReservaService:
    def __init__(self):
        # Serializa el check + insert dentro de este proceso para evitar carreras locales.
        self._lock = RLock()

    def crear(self, db: Session, cliente_id: int, solicitud: ReservaCreate) -> Reserva:
        inicio = datetime.combine(
            solicitud.fecha,
            solicitud.hora_inicio,
            tzinfo=ZONA_HORARIA_NEGOCIO,
        )
        if solicitud.fecha <= datetime.now(ZONA_HORARIA_NEGOCIO).date() or inicio <= datetime.now(ZONA_HORARIA_NEGOCIO):
            raise FechaReservaInvalidaError("La fecha y hora de la reserva deben ser futuras")

        servicios = []
        subtotal = 0.0
        duracion_total = 0
        for seleccionado in solicitud.servicios:
            servicio = catalogo_service.obtener_servicio(seleccionado.id_servicio)
            if servicio is None:
                raise ServicioReservaNoEncontradoError(
                    f"No existe el servicio con ID {seleccionado.id_servicio}"
                )
            if servicio.estado.strip().lower() != "activo":
                raise ServicioReservaNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está activo"
                )
            if (
                not isinstance(servicio.duracion_minutos, int)
                or servicio.duracion_minutos <= 0
                or servicio.precio is None
                or servicio.precio < 0
            ):
                raise ServicioReservaNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no tiene precio o duración válida"
                )
            if solicitud.modalidad == "A domicilio" and not servicio.aplica_domicilio:
                raise ModalidadReservaNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está habilitado para domicilio"
                )

            precio = round(float(servicio.precio), 2)
            subtotal += precio
            duracion_total += servicio.duracion_minutos
            servicios.append(
                {
                    "id_servicio": servicio.id_servicio,
                    "nombre": servicio.nombre,
                    "precio": precio,
                    "duracion_minutos": servicio.duracion_minutos,
                }
            )

        costo_domicilio = 0
        if solicitud.modalidad == "A domicilio":
            if solicitud.id_direccion is None:
                raise ValueError("Debe seleccionar una dirección para la atención a domicilio")
            costo_domicilio = domicilio_service.calcular_costo(
                db, cliente_id, solicitud.id_direccion
            )["costo_domicilio"]
        elif solicitud.id_direccion is not None:
            raise ValueError("No envíe una dirección cuando la modalidad es en el spa")

        with self._lock:
            if not disponibilidad_service.esta_disponible(
                db,
                solicitud.fecha,
                solicitud.hora_inicio,
                duracion_total,
                solicitud.modalidad,
            ):
                raise HorarioNoDisponibleError(
                    "El horario seleccionado ya no está disponible"
                )

            fin_servicio = inicio + timedelta(minutes=duracion_total)
            fin_bloqueo = fin_servicio + timedelta(
                minutes=TIEMPO_ADICIONAL_MINUTOS
            )
            subtotal = round(subtotal, 2)
            reserva = Reserva(
                cliente_id=cliente_id,
                fecha=solicitud.fecha,
                hora_inicio=solicitud.hora_inicio.strftime("%H:%M"),
                hora_fin_servicio=fin_servicio.strftime("%H:%M"),
                hora_fin_bloqueo=fin_bloqueo.strftime("%H:%M"),
                modalidad=solicitud.modalidad,
                id_direccion=solicitud.id_direccion,
                servicios_detalle=servicios,
                subtotal=subtotal,
                costo_domicilio=costo_domicilio,
                total=round(subtotal + costo_domicilio, 2),
                moneda="COP",
                estado="Pendiente",
            )
            return reserva_repository.crear(db, reserva)


reserva_service = ReservaService()
