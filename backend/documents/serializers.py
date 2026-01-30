from rest_framework import serializers
from .models import UploadedDocument

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = [ "file"]
        read_only_fields = ["status", "created_at"]

class SearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    top_k = serializers.IntegerField(required = False, default = 5)
    