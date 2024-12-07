import uvicorn
from fastapi import FastAPI

from mercadorias.routers import Produtos_routers
from shared.database import engine, Base
from mercadorias.models import Produtos_model


def init_db():
    """Função para inicializar o banco de dados."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="API de Produtos de Beleza",
    description="API para gerenciar produtos de beleza",
    version="1.0.0"
)


@app.get("/")
def welcome_message() -> str:
    """Endpoint de boas-vindas."""
    return "Seja bem-vindo(a) à maior revendedora de produtos de beleza!"


app.include_router(Produtos_routers.router)


@app.on_event("startup")
def startup_event():
    """Evento disparado ao iniciar o aplicativo."""
    init_db()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)