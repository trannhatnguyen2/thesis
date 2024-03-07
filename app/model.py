import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import get_linear_schedule_with_warmup, AutoTokenizer, AutoModel, logging

tokenizer = AutoTokenizer.from_pretrained("./model_storage/phobert-base-v2", use_fast=True)

model_bert = AutoModel.from_pretrained("./model_storage/phobert-base-v2")

# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')

class_names = ['Tiêu cực', 'Tích cực']

class SentimentClassifier(nn.Module):
  def __init__(self, n_classes):
    super(SentimentClassifier, self).__init__()
    # self.bert = AutoModel.from_pretrained('vinai/phobert-base-v2')
    self.bert = model_bert
    self.drop = nn.Dropout(p=0.3)
    self.fc = nn.Linear(self.bert.config.hidden_size, n_classes)
    nn.init.normal_(self.fc.weight, std=0.02)
    nn.init.normal_(self.fc.bias,0)

  def forward(self, input_ids, attention_mask):
    last_hidden_state, output = self.bert(
        input_ids = input_ids,
        attention_mask = attention_mask,
        return_dict=False
    )
    x = self.drop(output)
    x= self.fc(x)

    return x


# Load model first
model = SentimentClassifier(n_classes=2).to(device)
model.load_state_dict(torch.load('./model_storage/phobert_fold5.pth', map_location=torch.device('cpu')))
model.eval()

def predict_pipeline(text, max_len=120):
    # model = SentimentClassifier(n_classes=2).to(device)
    # model.to(device)
    # model.load_state_dict(torch.load('./model_storage/phobert_fold5.pth'))
    # model.eval()
    encoded_review = tokenizer.encode_plus(
        text,
        max_length=max_len,
        truncation=True,
        add_special_tokens=True,
        padding='max_length',
        return_attention_mask=True,
        return_token_type_ids=False,
        return_tensors='pt',
    )

    input_ids = encoded_review['input_ids'].to(device)
    attention_mask = encoded_review['attention_mask'].to(device)

    output = model(input_ids, attention_mask)
    _, y_pred = torch.max(output, dim=1)

    return str(class_names[y_pred])


