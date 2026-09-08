def test_cria_membro_com_sucesso(active_user, client_test, token_admin):
    response = client_test.post(
        "/membro",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={
            "nome": "Maria Souza",
            "data_nascimento": "1990-05-20",
            "membro": True,
            "batizado": True,
            "uniao_estavel": False,
        },
    )

    print(response.json())
    assert response.status_code == 201

def test_lista_membros(active_user, client_test, token_admin):

    client_test.post(
        "/membro",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={
            "nome": "Maria Souza",
            "data_nascimento": "1990-05-20",
            "membro": True,
            "batizado": True,
            "uniao_estavel": False,
        },
    )

    response = client_test.get(
        "/membro",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    print(response.json())
    assert response.json()[0] == {
        'membro': True,
        'nome': 'Maria Souza',
        'batizado': True,
        'id': 1,
        'data_nascimento': '1990-05-20',
        'uniao_estavel': False
    }

def test_deleta_membro(active_user, client_test, token_admin):

    client_test.post(
        "/membro",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={
            "nome": "Maria Souza",
            "data_nascimento": "1990-05-20",
            "membro": True,
            "batizado": True,
            "uniao_estavel": False,
        },
    )

    response = client_test.delete(
        "/membro/1",
        headers={"Authorization": f"Bearer {token_admin}"},
    )

    assert response.status_code == 204

def test_patch_membro(active_user, client_test, token_admin):
    response1 = client_test.post(
        "/membro",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={
            "nome": "Maria Souza",
            "data_nascimento": "1990-05-20",
            "membro": True,
            "batizado": True,
            "uniao_estavel": True,
        },
    )


    response2 = client_test.patch(
        "/membro/1",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={
            "nome": "Maria Souza",
            "data_nascimento": "1990-05-15",
            "membro": False,
            "batizado": False
        }
    )

    response = client_test.get(
        "/membro",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.json()[0] == {
        'membro': False,
        'nome': 'Maria Souza',
        'batizado': False,
        'id': 1,
        'data_nascimento': '1990-05-15',
        'uniao_estavel': True
    }

