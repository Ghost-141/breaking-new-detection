import logging
import numpy as np
import ollama
from utils.db import cursor, conn
from is_break import is_breaking_news

logging.basicConfig(level=logging.INFO)

# Generate embeddings using Ollama
def get_ollama_embeddings(text_list: list, model_name: str):
    embeddings = []
    for text in text_list:
        response = ollama.embeddings(model=model_name, prompt=text)
        embeddings.append(response["embedding"])
    return np.array(embeddings, dtype="float32")


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
    "ভোট",
    "রাষ্ট্রপতি",
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


# def is_breaking_news(title):
#     """Detect if news is breaking based on similarity with breaking keywords.

#     Returns:
#         int: 1 if breaking news (similarity > 0.50), 0 otherwise
#     """
#     try:
#         # Combine title and subtitle for analysis
#         text = title.strip()
#         if not text:
#             return 0

#         # Generate embeddings
#         text_embeddings = get_ollama_embeddings(
#             [text], model_name="embeddinggemma:300m"
#         )
#         keyword_embeddings = get_ollama_embeddings(
#             BREAKING_KEYWORDS, model_name="embeddinggemma:300m"
#         )

#         # Normalize embeddings for cosine similarity
#         text_norm = text_embeddings / np.linalg.norm(
#             text_embeddings, axis=1, keepdims=True
#         )
#         keyword_norm = keyword_embeddings / np.linalg.norm(
#             keyword_embeddings, axis=1, keepdims=True
#         )

#         # Compute similarity
#         similarities = np.dot(keyword_norm, text_norm[0])
#         max_similarity = np.max(similarities)

#         return 1 if max_similarity > 0.50 else 0

#     except Exception as e:
#         logging.error(f"Error in breaking news detection: {e}")
#         return 0



def process_pending_news():
    """Query pending news, check breaking status, and update database"""
    
    try:
        print("\n🔍 Fetching pending news...")
        sql = "SELECT id, title FROM news WHERE pending = 0"
        cursor.execute(sql)
        pending_news = cursor.fetchall()
        print(f"📊 Found {len(pending_news)} pending news items") # type: ignore
        
        breaking_count = 0
        for i, news in enumerate(pending_news, 1): # type: ignore
            print(f"\n[{i}/{len(pending_news)}] Processing: {news['title'][:50]}...") # type: ignore
            
            breaking_status = is_breaking_news(news['title'], threshold=0.83)
            if breaking_status:
                breaking_count += 1
                print(f"🚨 BREAKING NEWS detected!")
            else:
                print(f"📰 Regular news")
            
            update_sql = "UPDATE news SET is_breaking = %s, pending = 1 WHERE id = %s"
            cursor.execute(update_sql, (breaking_status, news['id']))
            
        conn.commit()
        print(f"\n✅ Processing complete: {breaking_count} breaking news out of {len(pending_news)} total") # type: ignore
        
    except Exception as e:
        logging.error(f"Error processing pending news: {e}")
        conn.rollback()
        print(f"❌ Error occurred: {e}")