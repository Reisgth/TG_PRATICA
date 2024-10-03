import os
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

nltk.download('punkt')
nltk.download('stopwords')

# Definir stopwords
stop_words = set(stopwords.words('portuguese'))

# Função para limpar e tokenizar texto
def limpar_tokenizar_texto(texto):
    # Tokenizar o texto
    tokens = word_tokenize(texto.lower())
    # Remover stopwords
    tokens_limpos = [t for t in tokens if t.isalnum() and t not in stop_words]
    return tokens_limpos

# Função para processar um arquivo PDF
def processar_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ''
        for pagina in range(len(leitor.pages)):
            texto += leitor.pages[pagina].extract_text()
        return limpar_tokenizar_texto(texto)

# Função para processar todos os PDFs em uma pasta
def processar_pdfs_pasta(caminho_pasta):
    dados = []
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith('.pdf'):
            caminho_pdf = os.path.join(caminho_pasta, arquivo)
            texto_limpo = processar_pdf(caminho_pdf)
            dados.append({
                'nome_arquivo': arquivo,
                'texto_limpo': ' '.join(texto_limpo)  # Salvamos o texto limpo como string
            })
    return dados

# Processar os PDFs
caminho_pasta = r'C:\Users\vagner reis\Desktop\TG_PRATICA\ARQUIVOS_PDF'  # Substituir pelo caminho real dos PDFs
dados_processados = processar_pdfs_pasta(caminho_pasta)

# Salvar os dados pré-processados em um arquivo JSON
caminho_saida_json = 'dados_processados.json'
with open(caminho_saida_json, 'w', encoding='utf-8') as f:
    json.dump(dados_processados, f, ensure_ascii=False, indent=4)

print(f"Dados pré-processados salvos em {caminho_saida_json}")


import random
import json

# Carregar os dados processados
caminho_dados = 'dados_processados.json'
with open(caminho_dados, 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Embaralhar os dados para garantir aleatoriedade
random.shuffle(dados)

# Dividir em 80% treino e 20% teste
tamanho_treino = int(0.8 * len(dados))
dados_treino = dados[:tamanho_treino]
dados_teste = dados[tamanho_treino:]

# Salvar os arquivos de treino e teste
with open('dados_treino.json', 'w', encoding='utf-8') as f:
    json.dump(dados_treino, f, ensure_ascii=False, indent=4)

with open('dados_teste.json', 'w', encoding='utf-8') as f:
    json.dump(dados_teste, f, ensure_ascii=False, indent=4)

print("Conjuntos de treino e teste salvos com sucesso!")
