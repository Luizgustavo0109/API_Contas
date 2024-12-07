import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.database import Base
from shared.dependencies import get_db
from main import app

# Configuração da base de dados para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Configura e limpa o banco de dados antes de cada teste."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_criar_produto():
    produto = {
        "nome": "Reparador de pontas",
        "descricao": "Seu cacho de pontas reparadas",
        "preco": 10.50,
        "disponivel": True,
        "fornecedor": "Fornecedor X"
    }
    response = client.post("/produtos/", json=produto)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == produto["nome"]
    assert data["descricao"] == produto["descricao"]
    assert float(data["preco"]) == produto["preco"]
    assert data["disponivel"] == produto["disponivel"]
    assert data["fornecedor"] == produto["fornecedor"]


def test_listar_produtos():
    produtos = [
        {
            "nome": "Esmalte",
            "descricao": "Unhas belas",
            "preco": 5.50,
            "disponivel": True,
            "fornecedor": "Fornecedor X"
        },
        {
            "nome": "Cortador de unhas",
            "descricao": "Cortador de unhas",
            "preco": 150.00,
            "disponivel": False,
            "fornecedor": "Fornecedor Y"
        }
    ]

    for produto in produtos:
        client.post("/produtos/", json=produto)

    response = client.get("/produtos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_obter_produto_por_id():
    produto = {
        "nome": "Creme de Bebe",
        "descricao": " Creme para bebe",
        "preco": 50.00,
        "disponivel": True,
        "fornecedor": "Fornecedor Z"
    }
    response_post = client.post("/produtos/", json=produto)
    produto_id = response_post.json()["id"]

    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == produto["nome"]


def test_atualizar_produto():
    produto = {
        "nome": "Geleia",
        "descricao": "Geleia de cabelo",
        "preco": 70.00,
        "disponivel": True,
        "fornecedor": "Fornecedor A"
    }
    response_post = client.post("/produtos/", json=produto)
    produto_id = response_post.json()["id"]

    produto_atualizado = {
        "nome": "Escova",
        "descricao": "Escova de cabelo",
        "preco": 15.00,
        "disponivel": False,
        "fornecedor": "Fornecedor B"
    }
    response_put = client.put(f"/produtos/{produto_id}", json=produto_atualizado)
    assert response_put.status_code == 200
    data = response_put.json()
    assert data["nome"] == produto_atualizado["nome"]
    assert data["descricao"] == produto_atualizado["descricao"]


def test_deletar_produto():
    produto = {
        "nome": "Creme de pele",
        "descricao": "Para uma pele mais saudavel",
        "preco": 50.00,
        "disponivel": True,
        "fornecedor": "Fornecedor C"
    }
    response_post = client.post("/produtos/", json=produto)
    produto_id = response_post.json()["id"]

    response_delete = client.delete(f"/produtos/{produto_id}")
    assert response_delete.status_code == 204

    response_get = client.get(f"/produtos/{produto_id}")
    assert response_get.status_code == 404


def test_produto_nao_encontrado():
    response = client.get("/produtos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto com ID 999 não encontrado."


def test_validacao_campos():
    produto_invalido = {
        "nome": "Creme",
        "descricao": "Cachos tipo ABC",
        "preco": -50.00,
        "disponivel": True,
        "fornecedor": "F"
    }
    response = client.post("/produtos/", json=produto_invalido)
    assert response.status_code == 422