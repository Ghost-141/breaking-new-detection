import json
import logging
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "models/."
model = SentenceTransformer(
    model_name, local_files_only=True, trust_remote_code=True
).to(device=device)
# model.save("./models")


# Embedding Generation Using Hugging Face Model
def get_hf_embeddings(text_list: list):
    model.to(device=device)
    embeddings = model.encode(
        text_list,
        show_progress_bar=True,
        prompt="task: sentence similarity | document: ",
    )
    return np.array(embeddings, dtype="float32")


def main():

    # Read news data from a JSON file
    input_path = "news_2025-12-26_21:21:18.json"
    logger.info(f"Reading news data from {input_path}...")
    with open(input_path, "r", encoding="utf8") as f:
        news_data = json.load(f)

    if not news_data:
        logger.info("⚠️ No news data found. Exiting.")
        return

    titles = [item["title"] for item in news_data]
    logger.info(f"✔ Loaded {len(news_data)} titles")

    # Load model and compute embeddings
    logger.info("🔤 Generating embeddings using Hugging Face model...")
    embeddings = get_hf_embeddings(titles)
    logger.info("✔ Generated embeddings")

    # Compute Cosine Similarity from embedding
    logger.info("🔍 Computing similarities...")
    norm_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    similarities = np.dot(norm_embeddings, norm_embeddings.T)

    # Grouping Logic
    grouped = []
    used = set()

    for i in range(len(news_data)):
        if i in used:
            continue
        group = [news_data[i]]
        used.add(i)

        for j in range(i + 1, len(news_data)):
            if j not in used and similarities[i][j] > 0.90:
                group.append(news_data[j])
                used.add(j)

        grouped.append(group)

    # Pairing Similar & Unique Titles
    result = {
        "Similar": [
            {"items": [{"id": item["id"], "title": item["title"]} for item in group]}
            for group in grouped
            if len(group) > 1
        ],
        "Unique": [
            {"id": group[0]["id"], "title": group[0]["title"]}
            for group in grouped
            if len(group) == 1
        ],
    }

    # Save results into JSON
    logger.info("💾 Saving results...")
    with open("grouped_news.json", "w", encoding="utf8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logger.info("✅ Completed successfully!")


if __name__ == "__main__":

    main()
