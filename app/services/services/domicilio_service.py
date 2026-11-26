from sqlalchemy.orm import Session

from app.repositories.repositories.direccion_repository import direccion_repository
from app.services.services.zona_service import zona_service


class DireccionNoEncontradaError(Exception):
    pass


class FueraDeCoberturaError(Exception):
    pass


class TarifaNoConfiguradaError(Exception):
    pass


class DomicilioService:
    def calcular_costo(self, db: Session, user_id: int, address_id: int) -> dict:
        direccion = direccion_repository.find_owned_address(db, address_id, user_id)
        if direccion is None:
            # Mismo resultado para una dirección inexistente o de otra persona.
            raise DireccionNoEncontradaError("La dirección no existe o no pertenece al cliente")

        zona = zona_service.validar_cobertura(direccion.barrio)
        if zona is None:
            raise FueraDeCoberturaError(
                "La dirección se encuentra fuera de la zona de cobertura"
            )

        tarifa = zona.tarifa_domicilio
        if tarifa is None or tarifa < 0:
            raise TarifaNoConfiguradaError(
                "No se puede calcular el costo: la zona no tiene una tarifa válida configurada"
            )

        return {
            "id_zona": zona.id_zona,
            "nombre_zona": zona.nombre_zona,
            "costo_domicilio": tarifa,
            "moneda": "COP",
        }


domicilio_service = DomicilioService()
