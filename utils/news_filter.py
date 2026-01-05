import re
import logging
import unicodedata
import warnings
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, BertForSequenceClassification
from transformers import logging as trans_logger
from utils.filters import (
    COUNTRIES,
    CAPITALS,
    INTERNATIONAL_REGIONS,
    INTERNATIONAL_ORGS,
    INTERNATIONAL_ADJECTIVES,
    extras,
)

trans_logger.set_verbosity_error()
warnings.filterwarnings("ignore")

News_Filter_Model = "models/uncased_v2"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("models/uncased_v2/tokenizer")
model = BertForSequenceClassification.from_pretrained(News_Filter_Model)
model.to(device)

logging.info(f"Loaded News Filter model on {device}")


def build_international_pattern():
    all_locations = (
        COUNTRIES
        + CAPITALS
        + INTERNATIONAL_REGIONS
        + INTERNATIONAL_ORGS
        + INTERNATIONAL_ADJECTIVES
        + extras
    )

    suffixes = r"(য়|ে|ি|ী|তে|র|এর|কে|দের|সহ|ভিত্তিক)?"

    patterns = [re.escape(loc) + suffixes for loc in all_locations]

    return re.compile(r"(?<!\S)(" + "|".join(patterns) + r")(?!\S)", flags=re.UNICODE)


INTL_PATTERN = build_international_pattern()


def filter_international_news(text: str) -> bool:
    text = unicodedata.normalize("NFKC", text)
    return bool(INTL_PATTERN.search(text))


def news_type_predictor(
    text: str,
    max_length: int = 64,
    return_probs: bool = False,
):
    """
    Predict class label for a Bangla news title using a BERT-based classifier.

    Args:
        text: input title string
        max_length: 48/64 recommended for titles
        return_probs: return probability distribution

    Returns:
        dict with label, confidence, class_id, (optional) probs
    """
    model.eval()

    inputs = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=max_length,
        return_tensors="pt",
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    id2label = {0: "BD", 1: "FOREIGN", 2: "SPORTS", 3: "OTHER"}

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits  # shape: [1, num_classes]
    probs = F.softmax(logits, dim=-1)[0]  # shape: [num_classes]

    pred_id = int(torch.argmax(probs).item())
    pred_label = id2label[pred_id]
    confidence = float(probs[pred_id].item())

    result = {
        "label": pred_label,
        "confidence": confidence,
        "class_id": pred_id,
    }

    # if return_probs:
    #     result["probs"] = {
    #         id2label[i]: float(probs[i].item()) for i in range(len(probs))
    #     }

    return result
