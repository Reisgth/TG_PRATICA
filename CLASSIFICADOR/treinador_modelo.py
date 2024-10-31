import json
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset

# Carregar os dados do JSON gerado anteriormente
with open('documentos_processados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Preparação dos textos e rótulos
textos = [doc['texto_limpo'] for doc in dados]
categorias = [doc['categoria'] for doc in dados]

# Mapeamento das categorias para valores numéricos
mapeamento_categorias = {
    'RH': 0, 'ALMOXARIFADO': 1, 'MARKETING': 2, 
    'INFORMATICA': 3, 'CONTAS A PAGAR': 4
}
labels = [mapeamento_categorias[categoria] for categoria in categorias]

# Dividir em dados de treino e teste (80% treino, 20% teste)
textos_treino, textos_teste, labels_treino, labels_teste = train_test_split(
    textos, labels, test_size=0.2, random_state=42
)

# Carregar o tokenizer do BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenizar os textos
def tokenizar(textos):
    return tokenizer(textos, padding=True, truncation=True, return_tensors="pt")

treino_enc = tokenizar(textos_treino)
teste_enc = tokenizar(textos_teste)

# Criar um dataset personalizado
class CustomDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Instanciar os datasets de treino e teste
train_dataset = CustomDataset(treino_enc, labels_treino)
test_dataset = CustomDataset(teste_enc, labels_teste)

# Carregar o modelo BERT para classificação
modelo = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased', num_labels=len(mapeamento_categorias)
)

# Definir os argumentos de treinamento
args_treinamento = TrainingArguments(
    output_dir='./resultados',
    eval_strategy="epoch",  # Mudado de evaluation_strategy para eval_strategy
    save_strategy="epoch",  # Adicionado para corresponder à estratégia de avaliação
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy"
)

# Função de avaliação
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = torch.argmax(torch.tensor(logits), dim=-1)
    accuracy = (preds == torch.tensor(labels)).float().mean().item()
    return {"accuracy": accuracy}

# Inicializar o Trainer
trainer = Trainer(
    model=modelo,
    args=args_treinamento,
    train_dataset=train_dataset,  # Alterado para usar o dataset CustomDataset
    eval_dataset=test_dataset,     # Alterado para usar o dataset CustomDataset
    compute_metrics=compute_metrics
)

# Treinar o modelo
trainer.train()

# Avaliar o modelo
resultados = trainer.evaluate()
print(f"Acurácia no conjunto de teste: {resultados['eval_accuracy']}")
