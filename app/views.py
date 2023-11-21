from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from app.models import User, Note
from .serializers import UserSerializer, NoteSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def get(self, request, user_id=None):
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data,  status=201, safe=False)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return JsonResponse(serializer.data,  status=201, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    def delete(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class NoteView(View):
    def get(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        serializer = NoteSerializer(note)
        return JsonResponse(serializer.data,  status=201,  safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = NoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    def put(self, request, note_id):
        try:
            note = get_object_or_404(Note, pk=note_id)
            data = json.loads(request.body)
            serializer = NoteSerializer(instance=note, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    def delete(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        note.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)
