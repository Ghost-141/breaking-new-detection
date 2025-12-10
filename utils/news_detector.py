import logging
import numpy as np
import ollama


# Generate embeddings using Ollama
def get_ollama_embeddings(text_list: list, model_name: str):
    embeddings = []
    for text in text_list:
        response = ollama.embeddings(model=model_name, prompt=text)
        embeddings.append(response["embedding"])
    return np.array(embeddings, dtype="float32")


# Predefined breaking news keywords
BREAKING_KEYWORDS = [
    "হত্যা",
    "দুর্ঘটনা",
    "প্রাণ",
    "মৃত্যু",
    "মৃতদেহ",
    "ধর্ষণ",
    "আগুন",
    "বিস্ফোরণ",
    "ভূমিকম্প",
    "রাজনৈতিক সহিংসতা",
    "নির্বাচন",
    "গ্রেফতার",
    "মোতায়েন",
    "অবরোধ",
    "বিক্ষোভ",
    "ধাওয়া–পাল্টাধাওয়া",
    "নিরাপত্তা",
    "রিমান্ড",
    "প্রদর্শন",
    "ঘোষণা",
    "বন্যা",
    "ঝড়",
    "জরুরি",
    "বিল পাস",
    "রায়",
    "গুরুতর আহত",
    "খুন",
    "অপহরণ",
    "সংঘর্ষ",
    "মৃত",
    "মহাসড়ক",
]


def is_breaking_news(title, subtitle="", publish_time=""):
    """Detect if news is breaking based on similarity with breaking keywords.

    Returns:
        int: 1 if breaking news (similarity > 0.50), 0 otherwise
    """
    try:
        # Combine title and subtitle for analysis
        text = f"{title} {subtitle}".strip()
        if not text:
            return 0

        # Generate embeddings
        text_embeddings = get_ollama_embeddings(
            [text], model_name="embeddinggemma:300m"
        )
        keyword_embeddings = get_ollama_embeddings(
            BREAKING_KEYWORDS, model_name="embeddinggemma:300m"
        )

        # Normalize embeddings for cosine similarity
        text_norm = text_embeddings / np.linalg.norm(
            text_embeddings, axis=1, keepdims=True
        )
        keyword_norm = keyword_embeddings / np.linalg.norm(
            keyword_embeddings, axis=1, keepdims=True
        )

        # Compute similarity
        similarities = np.dot(keyword_norm, text_norm[0])
        max_similarity = np.max(similarities)

        return 1 if max_similarity > 0.50 else 0

    except Exception as e:
        logging.error(f"Error in breaking news detection: {e}")
        return 0
