"""
Esta versão mantém propositalmente várias linhas de código comentadas
para documentar meu processo de aprendizagem como engenheira de software. 
Mantive o registro do teste com spacy porque foi a primeira ideia que tive, 
servindo como um histórico do meu fluxo de pensamento. Depois de testar,
percebi que não era necessário e apenas com pandas conseguiria fazer o tratamento.
Talvez fosse necessário se o corpus fosse em português, mas considerando que 
as raízes do inglês são o lemma, não foi preciso. Eu percebi que estava aplicando 
a lógica do português ao inglês no início do raciocínio.
"""

import pandas as pd
#import spacy (não precisei usar)

## Carregar modelo do spacy para inglês
#nlp = spacy.load("en_core_web_sm")

## Testar o modelo: verificar nome, classes gramaticais e lematização
# print(f"Modelo carregado: {nlp.meta['name']} v{nlp.meta['version']}")
#doc = nlp("I am learning English in Brazil.")
#for token in doc:
#    print(f"{token.text:{10}} {token.pos_:{10}} {token.lemma_}")

# Ler a base de dados do corpus COCA
df_coca = pd.read_csv('data/raw/word-frequency-COCA.csv', sep=';')

# Primeira tentativa de filtro:
# Filtrar verbos, remover lemas duplicados, pegar os top 100
# df_coca_100 = df_coca[df_coca['PoS'] == 'v'].drop_duplicates(subset=['lemma']).head(100)

#print(df_coca_100.head())
#print(df_coca_100.tail())

# Observei que é necessário remover os modals, auxiliares e o be (conjugados errados)

# Segunda tentativa de filtro:
filtro_modal_aux_be = ['will', 'would', 'can', 'could', 'may', 'might', 'shall', 'should', 'must', 'ought', 'be']

# Deixar apenas os verbos que não contém os itens do filtro_modal_aux_be
modal_aux_be = ~df_coca['lemma'].isin(filtro_modal_aux_be)

# Filtrar os top 100 verbos (sem modals, auxiliares e be)
df_coca_100 = df_coca[(df_coca['PoS'] == 'v') & modal_aux_be].drop_duplicates(subset=['lemma']).head(100)

#print(df_coca_100.head())
#print(df_coca_100.tail())

# Criar df_dict com cabeçalho, para a base que contém as conjugações dos verbos
columns_dict = ['present', 'present_3rd', 'past_simple', 'past_participle', 'present_participle']
df_dict = pd.read_csv('data/raw/verbs-dictionaries.csv', sep='\t', names=columns_dict)

#print(df_dict.head())

# Remover compound verbs
df_dict = df_dict[~df_dict['present'].str.contains('-', na=False)]

# Cruzar os dados do corpus COCA
list_coca_100 = df_coca_100['lemma'].tolist()
df_final = df_dict[df_dict['present'].str.strip().isin(list_coca_100)].copy()

#print(df_final.head())
#print(df_final.tail())

# Remover verbos repetidos (variações de conjugação)
df_final = df_final.drop_duplicates(subset=['present'], keep='first')

# Verbo "do" está errado na base
# Corrigir o past participle para done
df_final.loc[df_final['present'] == 'do', 'past_participle'] = 'done'

# Ordenar meu df_final usando a ordem de frequência do COCA
df_final['rank'] = df_final['present'].str.strip().apply(list_coca_100.index)
df_final = df_final.sort_values('rank').drop(columns=['rank'])

# Considerando que removi o be, preciso:
# Criar dicionário para incluir o be conjugado corretamente
verbs_be = [
    {'present': 'am',  'present_3rd': None,  'past_simple': 'was',  'past_participle': 'been', 'present_participle': 'being'},
    {'present': None,   'present_3rd': 'is', 'past_simple': 'was',  'past_participle': 'been', 'present_participle': 'being'},
    {'present': 'are', 'present_3rd': None,  'past_simple': 'were', 'past_participle': 'been', 'present_participle': 'being'}
]

# Juntar as rows do verbs_be ao df_final
df_be = pd.DataFrame(verbs_be)
df_final = pd.concat([df_be, df_final], ignore_index=True)

# Salvar o df_final
df_final.to_csv('data/processed/top_100_verbs.csv', index=False)