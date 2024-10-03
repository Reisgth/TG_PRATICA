import os
import json
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Certifique-se de que as dependências estão baixadas
nltk.download('punkt')
nltk.download('stopwords')

# Função para extrair texto de um único PDF
def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        texto_completo = ""
        for page in reader.pages:
            if page.extract_text():
                texto_completo += page.extract_text()
        return texto_completo

# Função para limpar e tokenizar o texto
def limpar_e_tokenizar_texto(texto):
    texto = texto.lower()  # Transformar em minúsculas
    texto = re.sub(r'\d+', '', texto)  # Remover números
    texto = re.sub(r'[^\w\s]', '', texto)  # Remover pontuação
    tokens = word_tokenize(texto)  # Tokenizar o texto
    stop_words = set(stopwords.words('portuguese'))  # Carregar stopwords em português
    tokens_limpos = [token for token in tokens if token not in stop_words]  # Remover stopwords
    return tokens_limpos

# Função para processar todos os PDFs em uma pasta e salvar os tokens em JSON
def processar_e_salvar_pdfs_pasta(caminho_pasta, caminho_saida_json):
    resultados = {}

    # Iterar sobre todos os arquivos na pasta
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(caminho_pasta, arquivo)
            try:
                print(f"Processando {arquivo}...")
                texto_extraido = extrair_texto_pdf(caminho_pdf)  # Extrair texto do PDF
                tokens = limpar_e_tokenizar_texto(texto_extraido)  # Limpar e tokenizar
                resultados[arquivo] = tokens  # Armazenar os tokens
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")
    
    # Salvar os resultados em um arquivo JSON
    with open(caminho_saida_json, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

# Caminho da pasta onde os PDFs estão armazenados
caminho_pasta = r"C:\Users\BApR2\Desktop\SEAD\BASE_DE_DADOS\PESSOAL"  # Windows

# Caminho para salvar o arquivo JSON com os tokens
caminho_saida_json = r"C:\Users\BApR2\Desktop\SEAD\PRÉ_PROCESSAMENTO\ARQUIVOS_PRE_PROCESSADOS.json"

# Processar todos os PDFs na pasta e salvar os tokens no arquivo JSON
processar_e_salvar_pdfs_pasta(caminho_pasta, caminho_saida_json)