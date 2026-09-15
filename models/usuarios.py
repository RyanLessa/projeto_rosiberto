from configs.get_db import Base
from sqlalchemy import Column, Integer, String, Date


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    data_aniversario = Column(Date, nullable=False)
