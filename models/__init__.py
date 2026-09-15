from configs.get_db import Base, engine

from .usuarios import Usuario
__all__ = [
    'Usuario',
]

Base.metadata.create_all(bind=engine)
