from datetime import date
from app.domain.models.cliente_model import Cliente
from app.api.schemas.cliente_schema import ClienteCreate
from app.repositories.repositories.cliente_repository import cliente_repository

class ClienteService:
    def __init__(self):
        self.repository = cliente_repository

    def _hash_password(self, password: str) -> str:
        """Simula la encriptación de la contraseña."""
        return f"hashed_{password}_2026"

    def crear_cliente(self, datos: ClienteCreate) -> Cliente:
        """
        Regla de negocio: Validar que el correo no exista previamente.
        Lanza ValueError si hay duplicidad.
        """
        if self.repository.find_by_email(datos.email):
            raise ValueError("El correo electrónico ya se encuentra registrado")
        
        nuevo_cliente = Cliente(
            id_cliente=0, # Se asignará en el repositorio
            nombre=datos.nombre,
            documento=datos.documento,
            email=datos.email,
            password_hash=self._hash_password(datos.password),
            fecha_registro=date.today()
        )
        
        return self.repository.save(nuevo_cliente)

# Instancia del servicio
cliente_service = ClienteService()