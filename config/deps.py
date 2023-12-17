from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Generator
from pydantic import ValidationError
from sqlalchemy.orm import Session, joinedload
from jose import jwt

from decouple import config

from crud import crud_user as crud
from models.User import User
from schemas.Token import TokenPayload
from schemas.User import User as UserSchema
from config import security

from config.db import SessionLocal


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, config("SECRET_KEY"), algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credenciales invalidas",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


def get_current_active_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserSchema:
    """
    Obtiene el usuario actualmente activo.

    Parámetros:
    - db: La sesión de la base de datos.
    - current_user: El usuario actual.

    Retorna:
    - UserResponse: Usuario con su rol y permisos.

    Excepciones:
    - HTTPException: Si el usuario no está activo.
    - HTTPException: Si no se encuentra el rol del usuario.
    """
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    # Consultar el usuario rol y los permisos
    user = db.query(User).\
        filter_by(id=current_user.id).\
        options(joinedload(User.roles)).\
        first()

    if not user:
        raise HTTPException(status_code=404, detail="Rol del usuario no encontrado")

    return user


def get_current_active_admin(
    current_user: User = Depends(get_current_user)
) -> UserSchema:
    """
    Obtén el usuario actualmente autenticado como administrador.

    Args:
        current_user (User): El usuario actualmente autenticado.

    Returns:
        User: El usuario actualmente autenticado como administrador.

    Raises:
        HTTPException: Si el usuario no tiene suficientes privilegios (no es administrador).

    Example:
        Para obtener el usuario actualmente autenticado como administrador:
        ```
        admin_user: User = Depends(get_current_active_admin())
        ```
    """

    # Verificar si el usuario es administrador o tiene los privilegios adecuados
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="El usuario no tiene suficientes privilegios"
        )

    return current_user
