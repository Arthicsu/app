from django.urls import path
from .views import upload_document, document_list, review_document

urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path('documents/', document_list, name='document_list'),
    path('review/<int:doc_id>/', review_document, name='review_document'),
    path('admin/documents/', document_list, name='admin_document_list'),  # <-- добавлено
]
