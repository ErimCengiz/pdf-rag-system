from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import os
COLLECTION_NAME = "documents"
VECTOR_SIZE = 384
client = QdrantClient(
    host = os.getenv("QDRANT_HOST", "qdrant"),
    port = 6333
    
)

def ensure_collection():
    collections = client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        client.create_collection(
            collection_name = COLLECTION_NAME,
            vectors_config = VectorParams(
                size = VECTOR_SIZE,
                distance = Distance.COSINE,
            ),
        )
