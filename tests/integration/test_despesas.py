def test_cria_despesa_com_sucesso(active_user, client_test, token_admin):
    response = client_test.post(
        "/despesas",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={
            "nome": "Maria Souza",
            "data": "2026-12-20",
            "valor": 125
        }
    )

    print(response.json())
    assert response.status_code == 201