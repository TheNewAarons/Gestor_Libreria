from django.contrib import admin
from django.urls import path, include
from Libros.views import LibroListView
from Libreria import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('Libros/', include('Libros.urls')),
    path('Editoriales/', include('Editoriales.urls')),
    path('accounts', include('django.contrib.auth.urls'))
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)