from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.core.security import create_access_token, verify_password
from app.api.db.session import get_db
from app.api.repositories import user_repository
from app.api.schemas.auth import LoginRequest, TokenOut

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = user_repository.get_user_by_email(db, credentials.email)

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}
