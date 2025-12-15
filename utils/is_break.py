import logging
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
import os
from utils.filters import BREAKING_KEYWORDS


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Lightweight multilingual embedding model for small GPUs
EMBEDDING_MODEL_NAME = "models/e5-small"
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model once
model = SentenceTransformer(EMBEDDING_MODEL_NAME, device=device, trust_remote_code=True, local_files_only=True)
logging.info(f"Loaded embedding model on {device}")

# Precompute keyword embeddings (batch)
keyword_embeddings = model.encode(
    BREAKING_KEYWORDS, convert_to_numpy=True, batch_size=32, device=device
)
keyword_embeddings /= np.linalg.norm(
    keyword_embeddings, axis=1, keepdims=True
)  # Normalize


def is_breaking_news(title:str, threshold:float):
    """
    Detect if news is breaking based on semantic similarity to predefined keywords.

    Args:
        title (str): News headline or text
        threshold (float): Cosine similarity threshold to classify as breaking

    Returns:
        int: 1 if breaking news, 0 otherwise
    """
    if not title or not title.strip():
        return 0

    try:
        # Generate embedding for the title
        text_emb = model.encode([title.strip()], convert_to_numpy=True, device=device)
        text_emb /= np.linalg.norm(text_emb, axis=1, keepdims=True)

        # Compute cosine similarity with all keywords
        # sims = np.dot(keyword_embeddings, text_emb[0])
        sims = keyword_embeddings @ text_emb[0]
        max_sim = np.max(sims)

        return 1 if max_sim > threshold else 0

    except Exception as e:
        logging.error(f"Error in breaking news detection: {e}")
        return 0
