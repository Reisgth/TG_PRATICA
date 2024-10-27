import os
import time
import json
import re
import torch
from PyPDF2 import PdfReader
from transformers import BertTokenizer, BertForSequenceClassification
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Carregar o modelo e tokenizer treinados
modelo = BertForSequenceClassification.from_pretrained('./modelo_treinado')
tokenizer = BertTokenizer.from_pretrained('./modelo_treinado')

# Mapeamento das categorias numéricas para nomes
mapeamento_categorias = {
    'RH': 0,
    'ALMOXARIFADO': 1,
    'MARKETING': 2,
    'INFORMATICA': 3,
    'CONTAS': 4 
}

def extrair_texto_pdf(caminho_pdf):
    """Extrai o texto de um PDF usando PyPDF2."""
    texto = ""
    with open(caminho_pdf, 'rb') as f:
        leitor_pdf = PdfReader(f)
        for pagina in range(len(leitor_pdf.pages)):
            texto += leitor_pdf.pages[pagina].extract_text() or ""
    return texto

def preprocessar_texto(texto):
    """Remove caracteres especiais e múltiplos espaços do texto."""
    texto_limpo = re.sub(r'\W+', ' ', texto)
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    return texto_limpo

def preparar_para_inferencia(texto):
    """Pré-processa e tokeniza o texto para o modelo BERT."""
    texto_limpo = preprocessar_texto(texto)
    inputs = tokenizer(texto_limpo, return_tensors="pt", padding=True, truncation=True)
    return inputs

def classificar_pdf(caminho_pdf):
    """Extrai o texto do PDF, processa e classifica."""
    try:
        texto_extraido = extrair_texto_pdf(caminho_pdf)
        if not texto_extraido:
            raise ValueError("Nenhum texto extraído do PDF.")

        inputs = preparar_para_inferencia(texto_extraido)

        # Fazer a inferência com o modelo treinado
        with torch.no_grad():
            outputs = modelo(**inputs)

        # Obter a categoria prevista
        logits = outputs.logits
        predicao = torch.argmax(logits, dim=-1).item()

        return [k for k, v in mapeamento_categorias.items() if v == predicao][0]
    except Exception as e:
        print(f"Erro ao classificar {caminho_pdf}: {e}")

class PDFHandler(FileSystemEventHandler):
    """Handler que processa arquivos PDF novos na pasta monitorada."""
    def on_created(self, event):
        if event.src_path.endswith(".pdf"):
            print(f"Novo PDF detectado: {event.src_path}")
            categoria = classificar_pdf(event.src_path)
            if categoria is not None:
                print(f"Categoria do documento: {categoria}")

def monitorar_pasta(pasta):
    """Inicia a observação da pasta para novos PDFs."""
    observador = Observer()
    handler = PDFHandler()
    observador.schedule(handler, pasta, recursive=False)
    observador.start()
    print(f"Monitorando a pasta: {pasta}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observador.stop()
    observador.join()

# Caminho da pasta a ser monitorada
pasta_monitorada = "./documentos_novos"

# Iniciar monitoramento da pasta
monitorar_pasta(pasta_monitorada)