from django.contrib import admin
from django.urls import path, include, re_path
from Libreria import views
from Libreria.views import BaseView, SeccionInformesView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('test/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # API Routes
    path('api/v1/', include('Libros.urls')),
    path('api/v1/', include('Bodegas.urls')),
    path('api/v1/', include('Editoriales.urls')),
    path('api/v1/', include('Usuarios.urls')),
    path('api/v1/auth/', include('registration.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)