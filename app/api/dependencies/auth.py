from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.services.auth_service import auth_service


bearer_scheme = HTTPBearer(auto_error=False)


def obtener_cliente_actual(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> int:
    usuario = obtener_usuario_actual(credentials)

    if usuario.rol != "Cliente":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un cliente puede realizar esta operación",
        )

    return usuario.id_usuario


def obtener_admin_actual(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> int:
    usuario = obtener_usuario_actual(credentials)
    if usuario.rol not in {"Administrador", "Gerente", "Sistema"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un administrador puede realizar esta operación",
        )
    return usuario.id_usuario


def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials | None,
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debe iniciar sesión para realizar esta operación",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        usuario = auth_service.validar_token_simulado(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o vencido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario
