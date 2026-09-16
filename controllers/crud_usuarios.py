from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import extract, or_, date, Optional


from models.usuarios import Usuario
from schemas.usuarios import UsuarioCreate, UsuarioUpdate


def criar_usuario(db: Session, dados: UsuarioCreate):
    try:
        novo_usuario = Usuario(
            nome=dados.nome,
            email=dados.email,
            data_aniversario=dados.data_aniversario
        )
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return novo_usuario

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o usuário no banco de dados."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro inesperado no processamento da requisição: {str(e)}"
        )


def editar_usuario(usuario_id: int, db: Session, dados: UsuarioUpdate):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {usuario_id} não encontrado."
            )

        # Filtra apenas os campos enviados (não nulos)
        dados_dict = dados.model_dump(exclude_unset=True)
        for chave, valor in dados_dict.items():
            setattr(usuario, chave, valor)

        db.commit()
        db.refresh(usuario)
        return usuario

    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar os dados do usuário no banco."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro inesperado no processamento da requisição: {str(e)}"
        )


def deletar_usuario(usuario_id: int, db: Session):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {usuario_id} não encontrado."
            )

        db.delete(usuario)
        db.commit()
        return {"mensagem": f"Usuário {usuario_id} deletado com sucesso."}

    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar o usuário no banco de dados."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro inesperado no processamento da requisição: {str(e)}"
        )

def listar_aniversariantes(db: Session):
    try:
        aniversariantes = (
            db.query(Usuario)
            .order_by(
                extract("month", Usuario.data_aniversario),
                extract("day", Usuario.data_aniversario),
                Usuario.nome
            )
            .all()
        )

        return aniversariantes

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar os aniversariantes."
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro inesperado no processamento da requisição: {str(e)}"
        )


def listar_aniversariantes_do_dia(db: Session):
    try:
        hoje = date.today()

        aniversariantes = (
            db.query(Usuario)
            .filter(
                Usuario.data_aniversario.isnot(None),
                extract("month", Usuario.data_aniversario) == hoje.month,
                extract("day", Usuario.data_aniversario) == hoje.day
            )
            .order_by(Usuario.nome)
            .all()
        )

        return aniversariantes

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar os aniversariantes do dia."
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro inesperado no processamento da requisição: {str(e)}"
        )

def listar_aniversariantes_do_mes(
    db: Session,
    mes: Optional[int] = None
):
    try:
        mes_consultado = mes or date.today().month

        if mes_consultado < 1 or mes_consultado > 12:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O mês deve estar entre 1 e 12."
            )

        aniversariantes = (
            db.query(Usuario)
            .filter(
                Usuario.data_aniversario.isnot(None),
                extract("month", Usuario.data_aniversario) == mes_consultado
            )
            .order_by(
                extract("day", Usuario.data_aniversario),
                Usuario.nome
            )
            .all()
        )

        return aniversariantes

    except HTTPException as http_exc:
        raise http_exc

    except SQLAlchemyError:
        db.rollback( )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar os aniversariantes do mês."
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro inesperado no processamento da requisição: {str(e)}"
        )

def pesquisar_aniversariantes(
    termo: str,
    db: Session
):
    try:
        if not termo or not termo.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O termo da pesquisa deve ser informado."
            )

        termo_pesquisa = f"%{termo.strip()}%"

        aniversariantes = (
            db.query(Usuario)
            .filter(
                Usuario.data_aniversario.isnot(None),
                or_(
                    Usuario.nome.ilike(termo_pesquisa),
                    Usuario.email.ilike(termo_pesquisa)
                )
            )
            .order_by(Usuario.nome)
            .all()
        )

        return aniversariantes

    except HTTPException as http_exc:
        raise http_exc

    except SQLAlchemyError:
        db.rollback( )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao pesquisar os aniversariantes."
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro inesperado no processamento da requisição: {str(e)}"
        )
