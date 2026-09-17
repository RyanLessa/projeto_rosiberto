from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from configs.get_db import get_db
from schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from controllers import crud_usuarios as usuario_controller

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_usuario_endpoint(dados: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário na base de dados.
    """
    return usuario_controller.criar_usuario(db=db, dados=dados)


@router.put("/{usuario_id}")
def editar_usuario_endpoint(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    """
    Edita os dados de um usuário existente pelo seu ID.
    """
    return usuario_controller.editar_usuario(usuario_id=usuario_id, db=db, dados=dados)


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def deletar_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    """
    Deleta um usuário pelo seu ID.
    """
    return usuario_controller.deletar_usuario(usuario_id=usuario_id, db=db)

@router.get("/aniversariantes")
def get_aniversariantes(
    db: Session = Depends(get_db)
):
    return usuario_controller.listar_aniversariantes(db=db)


@router.get("/aniversariantes/hoje")
def get_aniversariantes_do_dia(
    db: Session = Depends(get_db)
):
    return usuario_controller.listar_aniversariantes_do_dia(db=db)


@router.get("/aniversariantes/mes")
def get_aniversariantes_do_mes(
    mes: Optional[int] = Query(default=None),
    db: Session = Depends(get_db)
):
    return usuario_controller.listar_aniversariantes_do_mes(
        db=db,
        mes=mes
    )


@router.get("/aniversariantes/pesquisar")
def get_pesquisar_aniversariantes(
    termo: str,
    db: Session = Depends(get_db)
):
    return usuario_controller.pesquisar_aniversariantes(
        termo=termo,
        db=db
    )
