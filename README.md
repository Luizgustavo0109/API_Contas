# API Produtos - Gerenciamento de Mercadorias

Bem-vindo ao repositório da Produtos API, uma aplicação desenvolvida em FastAPI para gerenciar produtos. Este projeto é uma demonstração de um sistema CRUD (Create, Read, Update, Delete) que permite realizar operações em uma base de dados de mercadorias.

## 📋 Funcionalidades
* Listar produtos com filtros opcionais (ex.: disponibilidade).
* Criar novos produtos.
* Atualizar informações de produtos existentes.
* Excluir produtos da base de dados.
* Obter detalhes de um produto específico.

## 🚀 Tecnologias Utilizadas
* Linguagem: Python
* Framework: FastAPI
* ORM: SQLAlchemy
* Banco de Dados: SQLite (Para testes) Postgres (em produção)
* Testes: Pytest e FastAPI TestClient
* Validação de Dados: Pydantic

## 📚 Instalação
Siga as etapas abaixo para configurar e executar a aplicação:

1️⃣ Clone o repositório

2️⃣ Crie e ative um ambiente virtual

~~~~
python -m venv venv
venv\Scripts\activate    
~~~~

3️⃣ Instale as dependências

~~~~
pip install -r requirements.txt
~~~~

4️⃣ Execute a aplicação

~~~~
fastapi dev main.py
~~~~

## 🔍 Endpoints
### Produtos

**GET** /produtos/
Lista produtos com filtros opcionais.

**GET** /produtos/{produto_id}
Retorna os detalhes de um produto específico.

**POST** /produtos/
Cria um novo produto.

**PUT** /produtos/{produto_id}
Atualiza os dados de um produto existente.

**DELETE** /produtos/{produto_id}
Exclui um produto pelo ID.

## 🧪 Executando os Testes

1. Certifique-se de que o banco de dados de testes está configurado em test.db.
2. Execute os testes com o comando:
~~~~
pytest
~~~~

## 📜 Licença
Este projeto está licenciado sob os termos da MIT License. Consulte o arquivo LICENSE para mais informações.

💻 Desenvolvido por Luiz Gustavo

