from documents.models import UploadedDocument
import fitz
from documents.services.indexer import index_document
from documents.pipeline.chunker import chunk_text

def process_pdf(document_id: int) -> UploadedDocument:
    doc = UploadedDocument.objects.get(id = document_id)
    
    try:
        doc.status = "processing"
        doc.save(update_fields = ["status"])
        extracted_text = []

        with fitz.open(doc.file.path) as pdf:
            for page in pdf:
                extracted_text.append(page.get_text())

        full_text = "\n".join(extracted_text)
        chunks = chunk_text(full_text)
        index_document(doc, chunks)
        
        doc.status = "indexed"
        doc.save(update_fields = ["status"])
    
    except Exception as e:
        doc.status = "failed"
        doc.save(update_fields=["status"])
        raise e

    return doc


    
