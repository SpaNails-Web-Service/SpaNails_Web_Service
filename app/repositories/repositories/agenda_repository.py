from datetime import date, time


class AgendaRepository:
    """Punto de integración para reservas y bloqueos de agenda.

    HU-051 aún no aporta almacenamiento de reservas; por ahora no hay bloques
    ocupados que consultar. Cuando exista ese módulo, este método debe leerlos.
    """

    def obtener_bloques_ocupados(
        self, fecha: date, modalidad: str
    ) -> list[tuple[time, time]]:
        return []


agenda_repository = AgendaRepository()
