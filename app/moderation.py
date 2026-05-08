import re
import torch

from app.config import (
    SPAM_KEYWORDS,
    APPROVE_THRESHOLD,
    PENDING_THRESHOLD,
    MAX_LENGTH
)

from app.model_loader import load_model

# ==========================================
# CLEAN TEXT
# ==========================================
def clean_text(text: str):

    text = text.lower()

    # remove links
    text = re.sub(r"http\S+", "", text)

    # remove special chars
    text = re.sub(r"[^a-z0-9 ]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ==========================================
# RULE-BASED FILTER
# ==========================================
def rule_based_check(text: str):

    text = text.lower()

    # spam keywords
    for keyword in SPAM_KEYWORDS:

        if keyword in text:

            return False, f"Spam keyword detected: {keyword}"

    # external links
    if "http://" in text or "https://" in text:

        return False, "External links detected"

    # too short
    if len(text.split()) < 3:

        return False, "Content too short"

    return True, None


# ==========================================
# AI PREDICTION
# ==========================================
def predict_score(text: str):

    # lazy load model
    tokenizer, model, device = load_model()

    # tokenize
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    ).to(device)

    # inference
    with torch.no_grad():

        outputs = model(**inputs)

    # softmax probability
    probs = torch.softmax(outputs.logits, dim=1)

    # positive class score
    score = probs[0][1].item()

    return score


# ==========================================
# MAIN MODERATION FUNCTION
# ==========================================
def moderate_campaign(
    title: str,
    description: str
):

    # combine text
    full_text = f"{title} {description}"

    # clean text
    text = clean_text(full_text)

    # ======================================
    # RULE-BASED CHECK
    # ======================================
    passed, reason = rule_based_check(text)

    if not passed:

        return {
            "status": "rejected",
            "reason": reason,
            "trust_score": 0
        }

    # ======================================
    # AI SCORE
    # ======================================
    try:

        score = predict_score(text)

    except Exception as e:

        return {
            "status": "pending",
            "reason": f"Model inference error: {str(e)}",
            "trust_score": 0
        }

    # ======================================
    # DECISION LOGIC
    # ======================================
    if score >= APPROVE_THRESHOLD:

        status = "approved"

    elif score >= PENDING_THRESHOLD:

        status = "pending"

    else:

        status = "rejected"

    # ======================================
    # RESPONSE
    # ======================================
    return {
        "status": status,
        "trust_score": round(score, 4)
    }