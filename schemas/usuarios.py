from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    data_aniversario: date


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    data_aniversario: Optional[date] = None


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_aniversario: date

    class Config:
        from_attributes = True