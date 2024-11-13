import json
import torch
from torch.utils.data import DataLoader, Dataset, random_split
from transformers import BertForSequenceClassification, AdamW, BertTokenizer
from tqdm import tqdm

# Caminho para o arquivo JSON gerado no pré-processamento
caminho_dados = 'documentos_processados.json'

# Carregar os dados processados
with open(caminho_dados, 'r', encoding='utf-8') as f:
    documentos = json.load(f)

# Mapeamento das categorias para índices
mapeamento_categorias = {
    'RH': 0,
    'ALMOXARIFADO': 1,
    'MARKETING': 2,
    'INFORMATICA': 3,
    'CONTAS A PAGAR': 4,
}

# Filtrar documentos com categorias definidas
documentos = [doc for doc in documentos if doc['categoria'] in mapeamento_categorias]

# Criar uma classe Dataset personalizada
class DocumentDataset(Dataset):
    def __init__(self, documentos, tokenizer, max_length=512):
        self.documentos = documentos
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.documentos)

    def __getitem__(self, idx):
        texto = self.documentos[idx]['texto_processado']
        label = mapeamento_categorias[self.documentos[idx]['categoria']]

        # Tokenizar o texto
        inputs = self.tokenizer.encode_plus(
            texto,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        input_ids = inputs['input_ids'].squeeze()  # Remover dimensões extras
        attention_mask = inputs['attention_mask'].squeeze()  # Remover dimensões extras

        return input_ids, attention_mask, torch.tensor(label)

# Tokenizer usado anteriormente
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Criar o DataLoader
dataset = DocumentDataset(documentos, tokenizer)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8)

# Configurar o modelo
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(mapeamento_categorias))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Configurar o otimizador
optimizer = AdamW(model.parameters(), lr=2e-5)

# Treinamento do modelo
epochs = 3
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for input_ids, attention_mask, labels in tqdm(train_loader):
        input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(train_loader)}")

    # Validação
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for input_ids, attention_mask, labels in val_loader:
            input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            predictions = torch.argmax(outputs.logits, dim=-1)
            correct += (predictions == labels).sum().item()
            total += labels.size(0)
    print(f"Validation Accuracy: {correct / total:.2f}")

# Salvar o modelo treinado
model.save_pretrained('modelo_treinado')
tokenizer.save_pretrained('modelo_treinado')
