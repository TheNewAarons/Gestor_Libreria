from django.urls import path
from Editoriales import views
from Editoriales.views import EditorialListView, EditorialCreateView, EditorialDeleteView, EditorialUpdateView, EditorialEditListView, EditorialDeleteListView
urlpatterns = [
    path('listEditorial/', EditorialListView.as_view(), name = 'editorialList'),
    path('CreateEditorial/', EditorialCreateView.as_view(), name = 'editorialCreate'),
    path('DeleteEditorial/<int:pk>', EditorialDeleteView.as_view(), name = 'editorialDelete'),
    path('UpdateEditorial/<int:pk>', EditorialUpdateView.as_view(), name='editorialUpdate'),
    path('edit-list/', EditorialEditListView.as_view(), name='editorial_edit_list'),
    path('delete-list/', EditorialDeleteListView.as_view(), name='editorial_delete_list'),
]