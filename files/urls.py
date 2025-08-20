from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('' , views.home),
    path('files/' , views.files_operations , name = "files_operations" ),
    path('files/<str:file_id>/progress/' , views.files_progress , name = "files_progress" ),
    path('files/<str:file_id>/' , views.files_CRUD , name = "files_CRUD" ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)