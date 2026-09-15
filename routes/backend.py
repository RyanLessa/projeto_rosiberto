from typing import Annotated

from fastapi import APIRouter, Request
from fastapi import Depends

from configs.get_db import get_db
from controllers import crud_usuarios


router = APIRouter()

@router.get("/backend/usuarios")
async def read_user(request: Request, db: Annotated[str, Depends(get_db)]):
    await crud_usuarios.get_usuarios(db)

    return {"status": "feito"}
