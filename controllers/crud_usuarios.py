from models.usuarios import Usuario

async def get_usuarios(db):
    usuarios = db.query(Usuario).all()

    return usuarios
