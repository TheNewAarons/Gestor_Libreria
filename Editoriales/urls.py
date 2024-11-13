from django.urls import path
from Editoriales import views
from Editoriales.views import EditorialListView, EditorialCreateView, EditorialDeleteView, EditorialUpdateView
urlpatterns = [
    path('listEditorial/', EditorialListView.as_view(), name = 'editorialList'),
    path('CreateEditorial/', EditorialCreateView.as_view(), name = 'editorialCreate'),
    path('DeleteEditorial/<int:pk>', EditorialDeleteView.as_view(), name = 'editorialDelete'),
    path('UpdateEditorial/<int:pk>', EditorialUpdateView.as_view(), name='editorialUpdate')
]