from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('main.urls', namespace = 'main')),
    # path('user/', include('users.urls', namespace = 'user')),
    path('studentRating/', include('studentRating.urls')),
]