from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import EditorialViewSet

router = SimpleRouter()
router.register(r'editoriales', EditorialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]