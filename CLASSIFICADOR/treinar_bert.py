from datasets import load_dataset
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch

# 1. Carregar os arquivos de treino e teste
train_dataset = load_dataset('json', data_files='dados_treino.json')['train']
test_dataset = load_dataset('json', data_files='dados_teste.json')['train']

# 2. Carregar o tokenizer do BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 3. Função para tokenizar os dados
def tokenize_data(examples):
    return tokenizer(examples['texto_limpo'], padding='max_length', truncation=True)

# 4. Tokenizar os dados
train_dataset = train_dataset.map(tokenize_data, batched=True)
test_dataset = test_dataset.map(tokenize_data, batched=True)

# 5. Carregar o modelo BERT para classificação de sequência com 5 categorias
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=5)

# 6. Definir os argumentos de treinamento
training_args = TrainingArguments(
    output_dir='./resultados',          # Pasta para salvar os resultados
    eval_strategy="epoch",        # Avaliação a cada época
    num_train_epochs=3,                 # Número de épocas
    weight_decay=0.01,                  # Decaimento de peso (regularização)
    logging_dir='./logs',               # Pasta para salvar logs
    per_device_train_batch_size=16,   # Tamanho do batch para treino
    per_device_eval_batch_size=64,    # Tamanho do batch para avaliação
    warmup_steps=500,                 # Número de passos de aquecimento
    logging_steps=10,
)

# 7. Inicializar o Trainer
trainer = Trainer(
    model=model,                        # Modelo BERT
    args=training_args,                 # Argumentos de treinamento
    train_dataset=train_dataset,        # Conjunto de treino
    eval_dataset=test_dataset           # Conjunto de teste
)

# 8. Treinar o modelo
trainer.train()

# 9. Avaliar o modelo nos dados de teste
trainer.evaluate()