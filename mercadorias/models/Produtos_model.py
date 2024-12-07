from shared.database import Base

from sqlalchemy import Column, Integer, String, Double, Boolean
from sqlalchemy.sql import func



class Produtos(Base):
    __tablename__ = "Produtos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(250), nullable=False)
    preco = Column(Double, nullable=False)
    disponivel = Column(Boolean, nullable=False)
    fornecedor = Column(String(100), nullable=False)


class Config:
    orm_mode = True

