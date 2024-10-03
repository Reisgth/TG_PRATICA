import json
import pandas as pd
from sklearn.model_selection import train_test_split

# Caminho para o arquivo JSON com os tokens pré-processados
caminho_json = r"C:\Users\vagner reis\Desktop\TG_PRATICA\PRÉ_PROCESSAMENTO\ARQUIVOS_PRE_PROCESSADOS.json"

# Carregar os dados pré-processados
with open(caminho_json, 'r', encoding='utf-8') as f:
    documentos_preprocessados = json.load(f)

# Definir as categorias e mapear os documentos para suas categorias
# Supondo que os nomes dos arquivos contenham a categoria, por exemplo:
# "documento_rh_pessoal_1.pdf", "documento_marketing_1.pdf", etc.
# Caso contrário, você precisará de uma forma de mapear manualmente cada documento para sua categoria

categorias = ['RH/PESSOAL', 'INFORMATICA', 'MARKETING', 'CONTAS A PAGAR/TESOURARIA', 'ALMOXARIFADO']
dados = []

for nome_arquivo, tokens in documentos_preprocessados.items():
    # Extraia a categoria do nome do arquivo
    # Ajuste esta parte conforme a nomenclatura dos seus arquivos
    if 'rh_pessoal' in nome_arquivo.lower():
        categoria = 'RH/PESSOAL'
    elif 'informatica' in nome_arquivo.lower():
        categoria = 'INFORMATICA'
    elif 'marketing' in nome_arquivo.lower():
        categoria = 'MARKETING'
    elif 'contas_a_pagar' in nome_arquivo.lower() or 'tesouraria' in nome_arquivo.lower():
        categoria = 'CONTAS A PAGAR/TESOURARIA'
    elif 'almoxarifado' in nome_arquivo.lower():
        categoria = 'ALMOXARIFADO'
    else:
        categoria = 'OUTROS'  # Categoria para documentos que não se encaixam nas principais

    # Converter tokens de volta para texto
    texto = ' '.join(tokens)

    dados.append({'texto': texto, 'categoria': categoria})

# Criar um DataFrame
df = pd.DataFrame(dados)

# Remover documentos sem categoria principal (se houver)
df = df[df['categoria'].isin(categorias)]

# Dividir os dados em treino e teste
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42, stratify=df['categoria'])

# Salvar os conjuntos de dados em CSV
df_train.to_csv("dados_train.csv", index=False)
df_test.to_csv("dados_test.csv", index=False)

print("Dados preparados e salvos com sucesso!")
