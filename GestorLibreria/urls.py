from django.contrib import admin
from django.urls import path, include, re_path
from Libreria import views
from Libreria.views import BaseView
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('base/', BaseView.as_view(), name='base'),
    path('contacto/', views.contacto, name='contacto'),
    path('Libros/', include('Libros.urls')),
    path('Bodegas/', include('Bodegas.urls')),
    path('Editoriales/', include('Editoriales.urls')),
    path('ImportarProductos/', include('ImportarProductos.urls')),
    path('accounts', include('django.contrib.auth.urls')),
    path('users/', include('Usuarios.urls')),
    re_path(r'^.*$', views.page_not_found_view, name='page_not_found')
]
#aqui vamos a redirigir cuando se introduzca una url invalida y no muestre datos de las demas urls
handler404 = 'Libreria.views.page_not_found_view'
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)