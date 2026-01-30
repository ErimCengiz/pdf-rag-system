from django.urls import path
from .views import upload_document, search, ask, ask_page

urlpatterns = [
    path('upload/', upload_document),
    path("search/", search),
    path("ask/", ask),
    
    path("", ask_page, name = "home"),
    path("ask/", ask_page, name="ask.page"),
    ]
