def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]: 
    if not text:
        return []
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks