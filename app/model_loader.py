import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from app.config import MODEL_PATH

# device
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# model
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)
model.eval()