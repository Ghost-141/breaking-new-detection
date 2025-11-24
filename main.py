from utils.helper import read_file, get_embedding, find_similarity_pair, group_data
import json


def main():
    """
    Main function to run the news classification pipeline.

    Process:
    1. Read news data from JSON file
    2. Generate embeddings for news titles
    3. Find similar news pairs and group them
    4. Use Ollama LLM to create structured output with similar and unique articles
    """
    try:
        # Step 1: Read news data
        print("📰 Reading news data...")
        news_data, titles = read_file("db_data.json")
        print(f"✔ Loaded {len(news_data)} news articles")

        # Step 2: Generate embeddings
        print("🔤 Generating embeddings...")
        embeddings = get_embedding(titles)
        print(f"✔ Generated embeddings with shape: {embeddings.shape}")

        # Step 3: Find similar pairs and group articles
        print("🔍 Finding similar news pairs...")
        has_similarity, final_news = find_similarity_pair(embeddings, news_data)

        # Step 4: Group data using Ollama
        print("🤖 Grouping articles with Ollama...")
        grouped_result = group_data(has_similarity, final_news)

        # Step 5: Save results
        print("💾 Saving results...")
        with open("grouped_news.json", "w", encoding="utf8") as f:
            f.write(grouped_result)

        print("✅ News classification completed successfully!")
        print(f"📄 Results saved to: grouped_news.json")

    except FileNotFoundError:
        print("❌ Error: db_data.json file not found. Please ensure the file exists.")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")


if __name__ == "__main__":
    main()
