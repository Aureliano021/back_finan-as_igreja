import pandas as pd
from connection import get_engine

engine = get_engine()

df_main = pd.read_excel('exel.xlsx')
df_nomes = pd.read_excel('exel.xlsx', sheet_name='Nomes Membros', header=1)


#formatação da lista de membros.
df_membros = pd.melt(df_nomes,
        value_vars=['NOMES DOS MEMBROS', 'CONGREGADOS BATIZADOS C/ UNIÃO ESTÁVEL',
                 'CONGREGADOS NÃO BATIZADOS', 'CRIANÇAS'],
        var_name='categoria',
        value_name='nome',
        )

df_membros = df_membros.dropna(subset=['nome'])

#aqui é corrigido os 3 booleans que estão presentes na tabela
df_membros['membro'] = df_membros['categoria'] == 'NOMES DOS MEMBROS'
df_membros['batizado'] = df_membros['categoria'].isin(['NOMES DOS MEMBROS','CONGREGADOS BATIZADOS C/ UNIÃO ESTÁVEL'])
df_membros['uniao_estavel'] = df_membros['categoria'] == 'CONGREGADOS BATIZADOS C/ UNIÃO ESTÁVEL'

df_membros = df_membros.reset_index(drop=True)
df_membros = df_membros.drop(columns=['categoria'])

#Adição das colunas que faltam.
#OBS: todas nulas, na planilha original esses dados não estão presentes
df_membros['cpf'] = None
df_membros['cep'] = None
df_membros['email'] = None
df_membros['data_nascimento'] = None
df_membros['endereco'] = None
df_membros['celular'] = None

#df_membros.to_excel('teste.xlsx')

#Formatação da planilha main.
df_main.dropna(how='all', inplace=True)
df_main = df_main.reset_index(drop=True)

#tira os espaços indesejados
df_main['3. Descrição da Movimentação ou Nome do Contribuinte (se aplicável)'] =\
    df_main['3. Descrição da Movimentação ou Nome do Contribuinte (se aplicável)'].str.strip()

df_dizimos = df_main[df_main['2. Tipo de Movimentação'] == 'Dízimo']
df_dizimos = df_dizimos.drop(columns=['Carimbo de data/hora'])

df_membros_sql = pd.read_sql('membros', con=engine)

mapa_nomes = {
    'Marlene':  'Marlene Oliveira da Costa',
    'Voldionor':'Valdionor de Jesus Silva',
    'Ary':      'Ary dos Santos Peixoto',
    'Maria':    'Maria Cruz Neres',
    'Marília':  'Marilha Lopes',
    'Valdionor':'Valdionor de Jesus Silva',
    'Marilia' : 'Marilha Lopes',
    'Edna':     'Edna Maria Francosviak',
    'Mateus':   'Matheus Francosviak Lima'
}
df_dizimos = df_dizimos.replace(mapa_nomes)
df_dizimos = df_dizimos.merge(
    df_membros_sql,
    left_on='3. Descrição da Movimentação ou Nome do Contribuinte (se aplicável)',
    right_on='nome',
    how='left'
)

mapa_columns = {
    '1. Data da Movimentação': 'data',
    '2. Tipo de Movimentação': 'fora',
    '3. Descrição da Movimentação ou Nome do Contribuinte (se aplicável)':'fora1',
    '4. Valor (R$)': 'valor',
    'id': 'membro_id'
}

df_dizimos = df_dizimos.rename(columns = mapa_columns)
df_dizimos = df_dizimos.drop(
    columns=[
             'fora',
             'fora1',
             'nome',
             'data_nascimento',
             'cpf',
             'cep',
             'endereco',
             'email',
             'celular',
             'membro',
             'batizado',
             'uniao_estavel'
    ])

#Já foi e com sucesso df_dizimos.to_sql('dizimos', con=engine, if_exists='append', index=False)

#ofertas
df_oferta = df_main[df_main['2. Tipo de Movimentação'] == 'Oferta']
df_oferta = df_oferta.drop(columns=['Carimbo de data/hora'])

mapa_columns_oferta = {
    '1. Data da Movimentação': 'data',
    '2. Tipo de Movimentação': 'fora',
    '3. Descrição da Movimentação ou Nome do Contribuinte (se aplicável)':'nome',
    '4. Valor (R$)': 'valor',
}

df_oferta = df_oferta.rename(columns = mapa_columns_oferta)

df_oferta = df_oferta.drop(
    columns=[
       'fora',
        'nome',
    ])
#sucesso df_oferta.to_sql('ofertas', con=engine, if_exists='append', index=False)

df_despesas = df_main[df_main['2. Tipo de Movimentação'] == 'Saída (Despesa)']
df_despesas = df_despesas.drop(columns=['Carimbo de data/hora'])

df_despesas = df_despesas.rename(columns = mapa_columns_oferta)
df_despesas = df_despesas[['nome', 'valor', 'data']]

df_despesas.to_sql('despesas', con=engine, if_exists='append', index=False)