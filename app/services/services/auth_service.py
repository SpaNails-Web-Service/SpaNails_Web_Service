from app.repositories.repositories.auth_repository import auth_repository
from app.api.schemas.auth_schema import LoginRequest, LoginDataResponse

class AuthService:
    def __init__(self):
        self.repository = auth_repository

    def _verificar_password(self, plain_password: str, hashed_password: str) -> bool:
        # Simulación de verificación de hash (Ej: bcrypt.checkpw)
        return f"hashed_{plain_password}_2026" == hashed_password

    def _generar_jwt(self, id_usuario: int, rol: str) -> str:
        # Simulación de generación de Token JWT
        return f"eyJhbGciOiJIUzI1NiIsInR.simulado.{id_usuario}.{rol}"

    def autenticar_usuario(self, credenciales: LoginRequest) -> LoginDataResponse:
        usuario = self.repository.find_user_by_email(credenciales.email)
        
        # Validación: Usuario no existe o contraseña incorrecta (No revelar cuál falló)
        if not usuario or not self._verificar_password(credenciales.password, usuario.password_hash):
            raise PermissionError("Correo electrónico o contraseña incorrectos")
            
        # Validación: Cuenta inactiva
        if not usuario.activo:
            raise PermissionError("Su cuenta se encuentra inactiva. Contacte al administrador.")
            
        # Generar token si todo es correcto
        token = self._generar_jwt(usuario.id_usuario, usuario.rol)
        
        return LoginDataResponse(
            token=token,
            id_usuario=usuario.id_usuario,
            rol=usuario.rol
        )

    def validar_token_simulado(self, token: str):
        """Valida el token de demostración emitido por este servicio."""
        partes = token.rsplit(".", 2)
        if len(partes) != 3:
            raise ValueError("Token inválido")

        try:
            user_id = int(partes[1])
        except ValueError as exc:
            raise ValueError("Token inválido") from exc

        usuario = self.repository.find_user_by_id(user_id)
        if (
            usuario is None
            or not usuario.activo
            or usuario.rol != partes[2]
            or token != self._generar_jwt(usuario.id_usuario, usuario.rol)
        ):
            raise ValueError("Token inválido o usuario inactivo")

        return usuario

auth_service = AuthService()
