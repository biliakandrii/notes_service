from django.urls import path
from .views import UserView, NoteView

urlpatterns = [
    path('users/', UserView.as_view(), name='user-list-create'),
    path('users/<int:user_id>/', UserView.as_view(), name='user-retrieve-update-destroy'),
    path('notes/', NoteView.as_view(), name='note-create'),
    path('notes/<int:note_id>', NoteView.as_view(), name='note-retrieve-update-delete'),
]
