from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from EXPfileUploading.views import upload_document, document_list, review_document


urlpatterns = [
    path('', include('main.urls', namespace = 'main')),
    path('admin/', admin.site.urls),
    path('studentRating/', include('studentRating.urls')),
    path('upload/', upload_document, name='upload_document'),
    path('list/', document_list, name='document_list'),
    path('review/<int:doc_id>/', review_document, name='review_document'),
    path('admin/documents/', document_list, name='admin_document_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)