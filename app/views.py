from rest_framework import generics, permissions
from django.shortcuts import render
from app.models import User, Note, NoteAuthor
from .serializers import UserSerializer, NoteSerializer,NoteAuthorSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseNotFound
from django.views import View
from django.shortcuts import get_object_or_404
from django.db import transaction
import json
from rest_framework import generics, status
from rest_framework.response import Response


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Retrieve the count of related notes
        note_count = instance.noteauthor_set.count()

        # Add the note_count to the serialized data
        serialized_data = serializer.data
        serialized_data['note_count'] = note_count

        return Response(serialized_data)

class NoteCreateView(generics.CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NoteAuthorCreateView(generics.CreateAPIView):
    queryset = NoteAuthor.objects.all()
    serializer_class = NoteAuthorSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        note_id = request.data.get('note')
        permission = request.data.get('permission')

        # You may want to add additional validation for user, note, and permission data

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if the relationship already exists
            if NoteAuthor.objects.filter(user_id=user_id, note_id=note_id).exists():
                return Response({'detail': 'Relationship already exists'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



