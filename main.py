from fastapi import FastAPI
from pydantic import BaseModel


class Horta(BaseModel):
    id: int
    nome: str
    localizacao: str
    responsavel: str
    area: float


app = FastAPI(
    title="Sistema de Gestão de Hortas Comunitárias",
    description="API REST para consulta de hortas comunitárias.",
    version="1.0.0",
)


hortas = [
    Horta(
        id=1,
        nome="Horta Comunitária Esperança",
        localizacao="Bairro Jardim das Flores",
        responsavel="Maria Silva",
        area=450.0,
    ),
    Horta(
        id=2,
        nome="Horta Verde Vida",
        localizacao="Praça Central",
        responsavel="João Santos",
        area=320.5,
    ),
    Horta(
        id=3,
        nome="Horta Raízes do Bairro",
        localizacao="Vila Nova",
        responsavel="Ana Oliveira",
        area=275.0,
    ),
]


@app.get("/api/hortas", response_model=list[Horta])
def listar_hortas() -> list[Horta]:
    """Retorna todas as hortas comunitárias cadastradas em memória."""
    return hortas


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
