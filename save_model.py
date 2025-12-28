from sentence_transformers import SentenceTransformer
import torch

EMBEDDING_MODEL_NAME = "models/multilingual-e5-small"
# Extract model name from full path for directory naming
MODEL_DIR_NAME = EMBEDDING_MODEL_NAME.split("/")[-1]

device = "cuda" if torch.cuda.is_available() else "cpu"

model = SentenceTransformer(
    "intfloat/multilingual-e5-small", device=device, trust_remote_code=True
)

# Save to local folder based on model name
save_path = f"models/{EMBEDDING_MODEL_NAME.split('/')[-1]}"
model.save(save_path)
print(f"Model saved to: {save_path}")
