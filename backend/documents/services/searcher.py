from documents.services.embeddings import embed_text
from documents.services.qdrant_client import client, COLLECTION_NAME
import hashlib
import re

SCORE_THRESHOLD = 0.35

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

def text_hash(text:str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def search_documents(query: str, top_k: int = 5):
    query_vector = embed_text(query)

    results = client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_vector,
        limit = top_k * 5,
        with_payload = True,
    )
    
    

    best_per_doc = {}
    for point in results.points:
        score = point.score

        if score < SCORE_THRESHOLD:
            continue

        text = point.payload["text"]
        h = text_hash(normalize_text(text))

        if h not in best_per_doc or score > best_per_doc[h]["score"]:
            best_per_doc[h] = {
                "id": point.id,
                "score": score,
                "text": text,
                "document_id": point.payload["document_id"],
                "chunk_id": point.payload["chunk_id"],
            }

    return sorted(
        best_per_doc.values(),
        key = lambda x: x["score"],
        reverse = True
    )[:top_k]