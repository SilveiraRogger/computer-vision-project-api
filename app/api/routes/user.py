from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.core.security import hash_password
from app.api.db.session import get_db
from app.api.models.user import User
from app.api.schemas.user import createUserRequest

router = APIRouter(tags=["user"])


@router.post("/user")
def create_user(data: createUserRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    else:
        encrypted_password = hash_password(data.password)
        new_user = User(name=data.name, email=data.email, password=encrypted_password)
        db.add(new_user)
        db.commit()
        return {"mensagem": "usuário cadastrado com sucesso"}
