from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from debug_toolbar.toolbar import debug_toolbar_urls

from where_to_go import views

urlpatterns = (
    [
        path('admin/', admin.site.urls),
        path('', views.index),
        path('places/<int:id>/', views.get_object_by_id, name='place_detail'),
        path('tinymce/', include('tinymce.urls')),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
)
