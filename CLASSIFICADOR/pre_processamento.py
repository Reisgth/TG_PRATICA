import os
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PyPDF2 import PdfReader

# Baixar recursos necessários do NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Mapeamento de categorias
CATEGORIAS_VALIDAS = {
    'rh': 'RH',
    'almoxarifado': 'ALMOXARIFADO',
    'marketing': 'MARKETING',
    'informatica': 'INFORMATICA',
    'contas a pagar': 'CONTAS A PAGAR'  # Corrigindo "Financeiro"
}

def processar_pdf(caminho_pdf):
    """Extrai o texto de um arquivo PDF."""
    try:
        with open(caminho_pdf, 'rb') as f:
            reader = PdfReader(f)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text()
            return texto
    except Exception as e:
        print(f"Erro ao processar {caminho_pdf}: {e}")
        return ""

def limpar_e_tokenizar(texto):
    """Limpa e tokeniza o texto, removendo stopwords."""
    stop_words = set(stopwords.words('portuguese'))
    tokens = word_tokenize(texto.lower())
    tokens_limpos = [t for t in tokens if t.isalnum() and t not in stop_words]
    return tokens_limpos

def identificar_categoria(nome_arquivo):
    """Identifica a categoria do documento com base no nome do arquivo."""
    nome_arquivo = nome_arquivo.lower()
    for chave, categoria in CATEGORIAS_VALIDAS.items():
        if chave in nome_arquivo:
            return categoria
    return "INDEFINIDO"  # Caso nenhuma categoria seja encontrada

def processar_e_salvar_pdfs(caminho_pasta, caminho_saida):
    """Processa os PDFs e salva os resultados em um arquivo JSON."""
    documentos = []
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith(".pdf"):
            texto = processar_pdf(os.path.join(caminho_pasta, arquivo))
            tokens = limpar_e_tokenizar(texto)
            categoria = identificar_categoria(arquivo)
            
            documentos.append({
                'nome_arquivo': arquivo,
                'texto_limpo': " ".join(tokens),
                'categoria': categoria
            })

    # Salvar os documentos processados em JSON
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(documentos, f, ensure_ascii=False, indent=4)

# Defina os caminhos
caminho_pasta = r'C:\Users\BApR2\Desktop\SEAD\3. ARQUIVOS_PDF'
caminho_saida = 'documentos_processados.json'

# Executar o pré-processamento
processar_e_salvar_pdfs(caminho_pasta, caminho_saida)
