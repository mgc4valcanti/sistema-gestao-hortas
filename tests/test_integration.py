import pytest
from fastapi.testclient import TestClient

import main
from main import app


@pytest.fixture
def client_com_hortas(monkeypatch):
    """Fixture que isola a lista em memória e provê um TestClient."""
    hortas_iniciais = [
        main.Horta(
            id=1,
            nome="Horta Um",
            localizacao="Local Um",
            responsavel="Responsável Um",
            area=100.0,
        ),
        main.Horta(
            id=2,
            nome="Horta Dois",
            localizacao="Local Dois",
            responsavel="Responsável Dois",
            area=200.0,
        ),
    ]
    monkeypatch.setattr(main, "hortas", hortas_iniciais)
    client = TestClient(app)
    return client, hortas_iniciais


def test_get_listar_hortas_retorna_200_com_lista_json(client_com_hortas):
    client, _ = client_com_hortas

    response = client.get("/api/hortas")

    assert response.status_code == 200
    dados = response.json()
    assert len(dados) == 2
    assert dados[0]["id"] == 1
    assert dados[0]["nome"] == "Horta Um"
    assert dados[1]["id"] == 2
    assert dados[1]["nome"] == "Horta Dois"


def test_get_listar_hortas_retorna_lista_vazia_quando_sem_registros(monkeypatch):
    monkeypatch.setattr(main, "hortas", [])
    client = TestClient(app)

    response = client.get("/api/hortas")

    assert response.status_code == 200
    assert response.json() == []


def test_post_cadastrar_horta_retorna_201_com_dados_e_id_gerado(client_com_hortas):
    client, hortas = client_com_hortas
    nova_horta_payload = {
        "nome": "Horta Comunitária Sol",
        "localizacao": "Bairro Esperança",
        "responsavel": "Carlos Lima",
        "area": 350.0,
    }

    response = client.post("/api/hortas", json=nova_horta_payload)

    assert response.status_code == 201
    dados = response.json()
    assert dados["id"] == 3
    assert dados["nome"] == "Horta Comunitária Sol"
    assert dados["localizacao"] == "Bairro Esperança"
    assert dados["responsavel"] == "Carlos Lima"
    assert dados["area"] == 350.0
    assert len(hortas) == 3


def test_post_cadastrar_horta_retorna_422_quando_faltam_campos_obrigatorios(
    client_com_hortas,
):
    client, hortas = client_com_hortas
    payload_incompleto = {
        "nome": "Horta Sem Area",
        "localizacao": "Local",
        # responsavel e area ausentes
    }

    response = client.post("/api/hortas", json=payload_incompleto)

    assert response.status_code == 422
    assert len(hortas) == 2


def test_post_cadastrar_horta_retorna_422_quando_tipo_incompativel(client_com_hortas):
    client, hortas = client_com_hortas
    payload_invalido = {
        "nome": "Horta Invalida",
        "localizacao": "Local",
        "responsavel": "Resp",
        "area": "nao-eh-numero",
    }

    response = client.post("/api/hortas", json=payload_invalido)

    assert response.status_code == 422
    assert len(hortas) == 2


def test_get_recuperar_horta_retorna_200_quando_existe(client_com_hortas):
    client, _ = client_com_hortas

    response = client.get("/api/hortas/1")

    assert response.status_code == 200
    dados = response.json()
    assert dados["id"] == 1
    assert dados["nome"] == "Horta Um"
    assert dados["area"] == 100.0


def test_get_recuperar_horta_retorna_404_quando_inexistente(client_com_hortas):
    client, _ = client_com_hortas

    response = client.get("/api/hortas/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Horta não encontrada"}


def test_get_recuperar_horta_retorna_422_para_id_invalido(client_com_hortas):
    client, _ = client_com_hortas

    response = client.get("/api/hortas/abc")

    assert response.status_code == 422


def test_put_atualizar_horta_retorna_200_quando_sucesso(client_com_hortas):
    client, hortas = client_com_hortas
    dados_atualizacao = {
        "nome": "Horta Um Atualizada",
        "localizacao": "Local Um Novo",
        "responsavel": "Novo Responsável",
        "area": 120.0,
    }

    response = client.put("/api/hortas/1", json=dados_atualizacao)

    assert response.status_code == 200
    dados = response.json()
    assert dados["id"] == 1
    assert dados["nome"] == "Horta Um Atualizada"
    assert dados["area"] == 120.0
    assert hortas[0].nome == "Horta Um Atualizada"


def test_put_atualizar_horta_retorna_404_quando_inexistente(client_com_hortas):
    client, _ = client_com_hortas
    dados_atualizacao = {
        "nome": "Horta Fantasma",
        "localizacao": "Local",
        "responsavel": "Resp",
        "area": 50.0,
    }

    response = client.put("/api/hortas/999", json=dados_atualizacao)

    assert response.status_code == 404
    assert response.json() == {"detail": "Horta não encontrada"}


def test_put_atualizar_horta_retorna_422_para_payload_invalido(client_com_hortas):
    client, _ = client_com_hortas
    payload_invalido = {
        "nome": "Horta Invalida",
        "area": "invalido",
    }

    response = client.put("/api/hortas/1", json=payload_invalido)

    assert response.status_code == 422


def test_put_atualizar_horta_retorna_422_para_id_invalido(client_com_hortas):
    client, _ = client_com_hortas
    dados_atualizacao = {
        "nome": "Horta",
        "localizacao": "Local",
        "responsavel": "Resp",
        "area": 50.0,
    }

    response = client.put("/api/hortas/invalido", json=dados_atualizacao)

    assert response.status_code == 422


def test_fluxo_integrado_completo_api(monkeypatch):
    """Testa o ciclo de vida completo de uma horta via chamadas HTTP sequenciais."""
    monkeypatch.setattr(main, "hortas", [])
    client = TestClient(app)

    # 1. Base vazia
    res_list = client.get("/api/hortas")
    assert res_list.status_code == 200
    assert res_list.json() == []

    # 2. Cadastro de horta
    payload_criacao = {
        "nome": "Horta Ciclo Completo",
        "localizacao": "Zona Norte",
        "responsavel": "Marina Santos",
        "area": 250.0,
    }
    res_post = client.post("/api/hortas", json=payload_criacao)
    assert res_post.status_code == 201
    horta_criada = res_post.json()
    novo_id = horta_criada["id"]
    assert novo_id == 1

    # 3. Consulta da horta recém-criada
    res_get = client.get(f"/api/hortas/{novo_id}")
    assert res_get.status_code == 200
    assert res_get.json()["nome"] == "Horta Ciclo Completo"

    # 4. Atualização da horta
    payload_atualizacao = {
        "nome": "Horta Ciclo Completo Expandida",
        "localizacao": "Zona Norte - Setor 2",
        "responsavel": "Marina Santos",
        "area": 400.0,
    }
    res_put = client.put(f"/api/hortas/{novo_id}", json=payload_atualizacao)
    assert res_put.status_code == 200
    assert res_put.json()["area"] == 400.0
    assert res_put.json()["nome"] == "Horta Ciclo Completo Expandida"

    # 5. Verificação após atualização
    res_get_atualizada = client.get(f"/api/hortas/{novo_id}")
    assert res_get_atualizada.status_code == 200
    assert res_get_atualizada.json()["nome"] == "Horta Ciclo Completo Expandida"
    assert res_get_atualizada.json()["area"] == 400.0

    # 6. Listagem final confirmando quantidade
    res_list_final = client.get("/api/hortas")
    assert res_list_final.status_code == 200
    lista_final = res_list_final.json()
    assert len(lista_final) == 1
    assert lista_final[0]["id"] == novo_id


def test_rotas_documentacao_openapi():
    client = TestClient(app)

    res_docs = client.get("/docs")
    assert res_docs.status_code == 200

    res_openapi = client.get("/openapi.json")
    assert res_openapi.status_code == 200
    openapi_json = res_openapi.json()
    assert openapi_json["info"]["title"] == "Sistema de Gestão de Hortas Comunitárias"
    assert "/api/hortas" in openapi_json["paths"]
    assert "/api/hortas/{horta_id}" in openapi_json["paths"]
