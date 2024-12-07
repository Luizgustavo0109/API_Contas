from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from mercadorias.models.Produtos_model import Produtos
from shared.dependencies import get_db
from shared.exceptions import NotFound

# Definindo o schema de resposta
class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: Decimal
    disponivel: bool
    fornecedor: str

    class Config:
        orm_mode = True


# Definindo o schema de criação/atualização
class ProdutoRequest(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    descricao: str = Field(..., min_length=10, max_length=250)
    preco: Decimal = Field(..., gt=0)
    disponivel: bool
    fornecedor: str = Field(..., min_length=3, max_length=100)


# Instanciando o roteador
router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
    responses={404: {"description": "Produto não encontrado"}},
)

# Endpoint para listar produtos com filtros opcionais
@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(
    disponivel: Optional[bool] = Query(None, description="Filtrar por disponibilidade"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros para retornar"),
    db: Session = Depends(get_db),
):
    query = db.query(Produtos)

    if disponivel is not None:
        query = query.filter(Produtos.disponivel == disponivel)

    produtos = query.offset(skip).limit(limit).all()
    return produtos

@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto_por_id(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produtos).get(produto_id)

    if not produto:
        raise NotFound(f"Produto com ID {produto_id} não encontrado.")
    return produto


# Endpoint para criar um produto
@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar_produto(produto_request: ProdutoRequest, db: Session = Depends(get_db)):
    produto = Produtos(**produto_request.dict())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


# Endpoint para atualizar um produto
@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, produto_request: ProdutoRequest, db: Session = Depends(get_db)):
    produto = db.query(Produtos).get(produto_id)

    if not produto:
        raise NotFound(f"Produto com ID {produto_id} não encontrado.")

    for key, value in produto_request.dict().items():
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)
    return produto


# Endpoint para deletar um produto
@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produtos).get(produto_id)

    if not produto:
        raise NotFound(f"Produto com ID {produto_id} não encontrado.")

    db.delete(produto)
    db.commit()





