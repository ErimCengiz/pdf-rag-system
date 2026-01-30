from documents.services.searcher import search_documents
from documents.services.llm.model import generate_answer
from tqdm import tqdm


MAX_CONTEXT_CHARS = 1200
PRIMARY_THRESHOLD = 0.35
SECONDARY_THRESHOLD = 0.0

def answer_question(question: str):
    tqdm.disable = True
    
    results = search_documents(question)

    if not results or results[0]["score"] < PRIMARY_THRESHOLD:
        return {
            "answer": "The answer is not available in the provided documents ",
            "citations": [],
            "context_chars": 0,
        }
    
    context_parts = []
    citations = []
    total_chars = 0
    used_documents = set()

    
    for i, hit in enumerate(results):
        if hit["score"] < SECONDARY_THRESHOLD:
            continue

        if hit["document_id"] in used_documents:
            continue

        
        text = hit["text"]
        if not text:
            continue

        text_len = len(text)

        if total_chars + text_len > MAX_CONTEXT_CHARS:
            break
        
        used_documents.add(hit["document_id"])
        tag = f"[{len(context_parts) + 1}]"
        context_parts.append(f"{tag}{hit['text']}")

        citations.append({
            "tag":tag,
            "document_id": hit["document_id"],
            "chunk_id": hit["chunk_id"],
            "page": hit.get("page"),
            "score": round(hit["score"], 3),
        })
        total_chars += text_len


    context = "\n---\n".join(context_parts)

    
    confidence = compute_confidence(
        results = results,
        used_documents_count = len(used_documents),
        context_chars = total_chars,
    )
    
    answer = generate_answer(context = context, question = question)

    return {
        "answer": answer,
        "confidence": confidence,
        "citations": citations,
        "context_tokens": total_chars,
        
    }

def compute_confidence(results, used_documents_count, context_chars):

    top_score = results[0]["score"]
    semantic_conf = min(top_score / 0.6, 1.0)

    if used_documents_count >= 3:
        doc_conf = 1.0
    elif used_documents_count == 2:
        doc_conf = 0.7
    else:
        doc_conf = 0.4

    if context_chars >= 800:
        context_conf = 1.0
    elif context_chars >=400:
        context_conf = 0.7
    else:
        context_conf = 0.4

    confidence = (
        semantic_conf * 0.5 +
        doc_conf * 0.3 +
        context_conf * 0.2
    )
    
    return round(confidence * 100, 1)