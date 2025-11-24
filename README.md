# News Classification System

A Bengali news classification system that groups similar news articles using semantic similarity and LLM-based clustering.

## Features

- **Semantic Similarity Detection**: Uses sentence transformers to find similar news articles
- **Intelligent Grouping**: Groups articles with nearly identical meanings together
- **LLM-powered Classification**: Uses Ollama for structured JSON output
- **Automatic Fallback**: Shuffles articles when no similarities are found

## Project Structure

```
news_classification/
├── main.py                 # Main pipeline script
├── utils/
│   ├── helper.py          # Core utility functions
│   └── news_summary.py    # Database extraction utilities
├── prompts/
│   └── prompt_v1.py       # LLM prompt templates
├── models/                # Local sentence transformer models
├── db_data.json          # Input news data
├── grouped_news.json     # Output results
└── requirements files
```

## Setup

### Prerequisites

- Python 3.11+
- Ollama installed and running locally
- Required Python packages (see installation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd news_classification
   ```

2. **Install dependencies**
   ```bash
   pip install sentence-transformers numpy ollama faiss-cpu
   ```

3. **Setup Ollama**
   ```bash
   # Install and start Ollama
   ollama serve
   
   # Pull required model
   ollama pull qwen3:1.7b
   ```

4. **Prepare data**
   - Place your news data in `db_data.json` format:
   ```json
   [
     {
       "id": 1,
       "title": "News title in Bengali",
       "newspaper_name": "Source name",
       "link": "https://example.com",
       "published_time": "Time string",
       "scrape_id": 1
     }
   ]
   ```

## Usage

### Basic Usage

```bash
python main.py
```

### Pipeline Steps

1. **Data Loading**: Reads news articles from `db_data.json`
2. **Embedding Generation**: Creates semantic embeddings using sentence transformers
3. **Similarity Detection**: Finds articles with similarity > 0.8 threshold
4. **Grouping**: Groups similar articles together, shuffles if no similarities found
5. **LLM Classification**: Uses Ollama to create structured JSON output
6. **Output**: Saves results to `grouped_news.json`

### Output Format

```json
{
  "Similar": [
    {
      "items": [
        {"id": 4, "title": "Similar news 1"},
        {"id": 23, "title": "Similar news 2"}
      ]
    }
  ],
  "Unique": [
    {"id": 2, "title": "Unique news article"}
  ]
}
```

## Configuration

### Similarity Threshold
Adjust in `utils/helper.py`:
```python
similarity_threshold = 0.8  # Change as needed
```

### Model Selection
Change the sentence transformer model in `utils/helper.py`:
```python
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
```

### Ollama Model
Update the model in `utils/helper.py`:
```python
ollama.generate(model="qwen3:1.7b", prompt=full_prompt)
```

## Functions

### Core Functions

- `read_file(file_path)`: Load news data from JSON
- `get_embedding(titles)`: Generate semantic embeddings
- `find_similarity_pair(embeddings, news_data)`: Find and group similar articles
- `group_data(similarity, final_news)`: Use LLM for final classification

## Requirements

- `sentence-transformers`: For semantic embeddings
- `numpy`: For numerical operations
- `ollama`: For local LLM integration

## Troubleshooting

### Common Issues


1. **Model Download Issues**
   - Models are automatically downloaded to `./models/` directory
   - Ensure sufficient disk space (>500MB)

2. **Memory Issues**
   - Reduce batch size for large datasets
   - Use smaller sentence transformer models

### Performance Tips

- Use GPU-enabled sentence transformers for faster processing
- Adjust similarity threshold based on your data
- Consider using approximate similarity search for large datasets

