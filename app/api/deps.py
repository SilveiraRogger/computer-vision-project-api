from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.api.db.session import get_db
from app.api.core.config import settings
from app.api.repositories import user_repository

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = UUID(payload.get("sub"))
    except (JWTError, TypeError):
        raise HTTPException(status_code=401, detail="Token inválido")

    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user
