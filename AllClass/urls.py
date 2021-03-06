from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from board import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('board.urls')),
                  path('common/', include('common.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
