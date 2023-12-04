from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, NoteCreateView, NoteRetrieveUpdateDestroyView, NoteAuthorCreateView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-create-list'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('notes/', NoteCreateView.as_view(), name='note-create'),
    path('notes/<int:pk>/', NoteRetrieveUpdateDestroyView.as_view(), name='note-retrieve-update-delete'),
    path('notes-author/', NoteAuthorCreateView.as_view(), name='note-author')
]
