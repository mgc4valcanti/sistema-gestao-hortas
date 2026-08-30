# Sistema de Gestão de Hortas Comunitárias

API REST em Python e FastAPI para consultar hortas comunitárias. Os dados são
armazenados em memória e reiniciados sempre que a aplicação é encerrada.

## Requisitos

- Python 3.10 ou superior

## Instalação e execução

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

A aplicação fica disponível em `http://localhost:8080` e a documentação
interativa do FastAPI em `http://localhost:8080/docs`.

## Endpoint

### `GET /api/hortas`

Retorna a lista de hortas comunitárias:

```bash
curl http://localhost:8080/api/hortas
```

Exemplo de resposta:

```json
[
  {
    "id": 1,
    "nome": "Horta Comunitária Esperança",
    "localizacao": "Bairro Jardim das Flores",
    "responsavel": "Maria Silva",
    "area": 450.0
  }
]
```

Também é possível iniciar diretamente com o Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```
