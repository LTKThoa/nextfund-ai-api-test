import re
import torch

from app.config import (
    SPAM_KEYWORDS,
    APPROVE_THRESHOLD,
    PENDING_THRESHOLD,
    MAX_LENGTH
)

from app.model_loader import (
    tokenizer,
    model,
    device
)

# ================================
# CLEAN TEXT
# ================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return text

# ================================
# RULE CHECK
# ================================
def rule_based_check(text):
    text = text.lower()

    for keyword in SPAM_KEYWORDS:
        if keyword in text:
            return False, f"Spam keyword: {keyword}"

    if "http://" in text or "https://" in text:
        return False, "External links detected"

    return True, None

# ================================
# PREDICT
# ================================
def predict_score(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)

    return probs[0][1].item()

# ================================
# MODERATION LOGIC
# ================================
def moderate_campaign(title, description):

    text = clean_text(f"{title} {description}")

    # rule-based
    passed, reason = rule_based_check(text)

    if not passed:
        return {
            "status": "rejected",
            "reason": reason,
            "trust_score": 0
        }

    # AI score
    score = predict_score(text)

    # decision
    if score > APPROVE_THRESHOLD:
        status = "approved"

    elif score > PENDING_THRESHOLD:
        status = "pending"

    else:
        status = "rejected"

    return {
        "status": status,
        "trust_score": round(score, 4)
    }