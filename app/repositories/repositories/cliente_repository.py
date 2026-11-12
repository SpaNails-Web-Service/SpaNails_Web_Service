from app.domain.models.cliente_model import Cliente
from typing import Optional, List

class ClienteRepository:
    _instance = None
    _db: List[Cliente] = []
    _current_id: int = 100

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClienteRepository, cls).__new__(cls)
        return cls._instance

    def find_by_email(self, email: str) -> Optional[Cliente]:
        """Busca un cliente por su correo electrónico."""
        for cliente in self._db:
            if cliente.email == email:
                return cliente
        return None

    def save(self, cliente: Cliente) -> Cliente:
        """Guarda un nuevo cliente simulando un autoincremental."""
        self._current_id += 1
        cliente.id_cliente = self._current_id
        self._db.append(cliente)
        return cliente

# Instancia Singleton
cliente_repository = ClienteRepository()