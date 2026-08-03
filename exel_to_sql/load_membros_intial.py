import pandas as pd


from connection import get_engine

engine = get_engine()


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

print(df_membros)
#df_membros.to_sql('membros', con=engine, if_exists='append', index=False)