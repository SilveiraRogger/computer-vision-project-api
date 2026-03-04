from pydantic import BaseModel, EmailStr, field_validator


class createUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("A senha deve ter no mínimo 8 caracteres")
        if not any(c.isupper() for c in value):
            raise ValueError("A senha deve ter pelo menos uma letra maiúscula")
        if not any(c.isdigit() for c in value):
            raise ValueError("A senha deve ter pelo menos um número")
        return value
