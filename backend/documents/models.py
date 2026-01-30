from django.db import models

class Document(models.Model):
    name = models.CharField(max_length = 255)
    file = models.FileField(upload_to = "documents/")
    status = models.CharField(
        max_length = 20,
        default = "uploaded",
    )
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    
class UploadedDocument(models.Model):
    title = models.CharField(max_length = 255)
    file = models.FileField(upload_to = "documents/")

    text = models.TextField(null = True, blank = True)

    status = models.CharField(
        max_length = 20,
        default = "pending",
        choices = [
                ("pending", "Pending"),
                ("processing", "Processing"),
                ("indexed", "Indexed"),
                ("failed", "Failed"),
                ]
    )
    created_at = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.title
    
    