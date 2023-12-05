from django.shortcuts import get_object_or_404
from rest_framework import permissions

from app.models import Note, NoteAuthor


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj == request.user


class IsNoteAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only authors of a note to create NoteAuthor instances.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        note_id = request.data.get('note')
        user_id = request.user.id
        return Note.objects.filter(pk=note_id, authors=user_id).exists()

class IsNoteAuthor(permissions.BasePermission):
    """
    Custom permission to allow only authors of a note to access Note instances.
    """
    def has_object_permission(self, request, view, obj):
        return obj.authors.filter(pk=request.user.id).exists()

