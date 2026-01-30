from documents.services.embeddings import embed_text
from documents.services.qdrant_client import COLLECTION_NAME, client, ensure_collection
from documents.models import UploadedDocument
from qdrant_client.http.models import VectorParams, Distance, PointStruct

def make_point_id(document_id: int, chunk_id:int) -> int:
    return document_id * 1_000_000 + chunk_id


def index_document(doc: UploadedDocument, chunks: list[str]):
    ensure_collection()
    points = []
    for idx, chunk in enumerate(chunks):
        vector  = embed_text(chunk)
        point_id = make_point_id(doc.id, idx)
        points.append(
           PointStruct(
               id = point_id,
               vector = vector,
               payload = {
                   "document_id": doc.id,
                   "chunk_id": idx,
                   "text": chunk,
               }
           )
       )
    client.upsert(
        collection_name = COLLECTION_NAME,
        points = points,
    )