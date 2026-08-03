import pandas as pd
from connection import get_engine

engine = get_engine()

membros_avulsos = pd.DataFrame([
    {'nome': 'Maiquele', 'membro': False, 'batizado': False, 'uniao_estavel': False,
     'cpf': None, 'cep': None, 'email': None, 'data_nascimento': None,
     'endereco': None, 'celular': None},
    {'nome': 'Evelin', 'membro': False, 'batizado': False, 'uniao_estavel': False,
     'cpf': None, 'cep': None, 'email': None, 'data_nascimento': None,
     'endereco': None, 'celular': None},
])

membros_avulsos.to_sql('membros', con=engine, if_exists='append', index=False)