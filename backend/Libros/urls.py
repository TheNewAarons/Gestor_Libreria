from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import LibroViewSet

router = SimpleRouter()
router.register(r'libros', LibroViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
