import os
import json
import re
import nltk
from PyPDF2 import PdfReader
from transformers import BertTokenizer

# Carregar o tokenizer BERT treinado (ou usar o tokenizer padrão)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Definições de categorias com padrões relacionados
CATEGORIAS_VALIDAS = {
    'RH': ['recursos humanos', 'contratação', 'benefícios', 'folha de pagamento', 'RH', 'Pessoal', 'cadastro'],
    'ALMOXARIFADO': ['estoque', 'almoxarifado', 'material', 'suprimentos'],
    'MARKETING': ['campanha', 'publicidade', 'propaganda', 'branding', 'marketing', 'publicação'],
    'INFORMATICA': ['tecnologia', 'sistema', 'rede', 'hardware', 'software', 'informatica', 'computadores'],
    'CONTAS': ['pagamento', 'fatura', 'contabilidade', 'finanças']
}

def processar_pdf(caminho_pdf):
    """Extrai o texto de um PDF usando PyPDF2."""
    texto = ""
    try:
        with open(caminho_pdf, 'rb') as f:
            leitor = PdfReader(f)
            for pagina in leitor.pages:
                texto += pagina.extract_text() or ""
    except Exception as e:
        print(f"Erro ao processar {caminho_pdf}: {e}")
    return texto

def identificar_categoria_por_conteudo(texto):
    """Identifica a categoria do documento com base no conteúdo textual."""
    texto = texto.lower()
    for categoria, padroes in CATEGORIAS_VALIDAS.items():
        for padrao in padroes:
            if re.search(r'\b' + re.escape(padrao) + r'\b', texto):
                return categoria
    return "INDEFINIDO"

def processar_e_salvar_pdfs(caminho_pasta, caminho_saida):
    """Processa os PDFs com limpeza básica para BERT e salva os resultados em um arquivo JSON."""
    documentos = []
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))  # Usando as stopwords do NLTK como exemplo

    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith(".pdf"):
            caminho_completo = os.path.join(caminho_pasta, arquivo)
            texto = processar_pdf(caminho_completo)

            # Limpeza básica do texto (opcional: você pode adaptar conforme necessário)
            texto = texto.lower()  # Converter para minúsculas
            palavras = re.findall(r'\b\w+\b', texto)  # Separar palavras simples

            # Remover stopwords e palavras de junção (básico)
            palavras_limpa = [palavra for palavra in palavras if palavra not in stopwords]

            # Reconstruir o texto processado para o modelo
            texto_processado = ' '.join(palavras_limpa)

            # Identificar a categoria com base no conteúdo original
            categoria = identificar_categoria_por_conteudo(texto)

            # Adicionar os documentos à lista
            documentos.append({
                'nome_arquivo': arquivo,
                'texto_processado': texto_processado,
                'categoria': categoria,
                'conteudo': texto[:200]  # Inclui uma prévia do conteúdo original (opcional)
            })
    
    # Salvar documentos processados em JSON
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(documentos, f, ensure_ascii=False, indent=4)

    # Salvar os documentos processados em JSON
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(documentos, f, ensure_ascii=False, indent=4)

# Defina os caminhos
caminho_pasta = r'C:\Users\BApR2\Desktop\SEAD\3. ARQUIVOS_PDF'
caminho_saida = 'documentos_processados.json'

# Executar o pré-processamento
processar_e_salvar_pdfs(caminho_pasta, caminho_saida)