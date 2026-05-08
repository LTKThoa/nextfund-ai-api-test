import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

MODEL_NAME = "LTKThoa/nextfund-campaign-moderation"

device = torch.device("cpu")

tokenizer = None
model = None


def load_model():

    global tokenizer, model

    if tokenizer is None or model is None:

        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME
        )

        model.to(device)
        model.eval()

    return tokenizer, model, device