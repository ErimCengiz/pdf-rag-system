from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from documents.services.searcher import search_documents
from .serializers import SearchSerializer
from documents.services.qa_service import answer_question
from documents.services.processor import process_pdf
from .serializers import DocumentUploadSerializer
from django.shortcuts import render

@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_document(request):
    serializer = DocumentUploadSerializer(data = request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
 
    doc = serializer.save(status = "pending")   

    process_pdf(doc.id)
    

    return Response({
        "massage": "Upload succesful",
        "document_id": doc.id,
        "status": doc.status,
    },
    status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
def search(request):
    serializer = SearchSerializer(data = request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    query = serializer.validated_data["query"]
    top_k = serializer.validated_data["top_k"]

    results = search_documents(query, top_k = 3)

    return Response({
        "query": query,
        "results": results
    })

@api_view(["POST"])
def ask(request):
    question = request.data.get("question")

    if not question:
        return Response({"error": "question is required"}, status = 400)

    result = answer_question(question)

    return Response(result, status = 200)

def ask_page(request):

    return render(request, "ask.html")
