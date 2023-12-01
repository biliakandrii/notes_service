from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseNotFound
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from app.models import User, Note, NoteAuthor
from .serializers import UserSerializer, NoteSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def get(self, request, user_id=None):
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            return render(request, 'user_detail.html', {'user': user})
        else:
            users = User.objects.all()
            return render(request, 'user_list.html', {'users': users})

    def post(self, request):
        data = json.loads(request.body)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'user_detail.html', {'user': serializer.data}, status=201)
        else:
            return render(request, 'user_form.html', {'form_errors': serializer.errors})


    def delete(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return HttpResponseNotFound('<h1>User deleted successfully</h1>', status=204)


@method_decorator(csrf_exempt, name='dispatch')
class NoteView(View):
    def get(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        return render(request, 'note_detail.html', {'note': note})

    def post(self, request):
        data = json.loads(request.body)
        authors_data = data.pop('authors', [])
        permission_data = data.pop('permissions', [])

        with transaction.atomic():
            serializer = NoteSerializer(data=data)
            if serializer.is_valid():
                note = serializer.save()
                note.authors.set(authors_data)
                if len(authors_data) != len(permission_data):
                    return JsonResponse(serializer.errors, status=400)
                for author, permission in zip(authors_data, permission_data):
                    note_author = get_object_or_404(NoteAuthor, user_id=author, note_id=note.id)
                    note_author.permission = permission
                    note_author.save()
                    author_ = get_object_or_404(User, pk=author)
                    author_.numberOfNotes += 1
                    author_.save()

                note.refresh_from_db()
                return render(request, 'note_detail.html', {'note': serializer.data})
            else:
                return render(request, 'note_form.html', {'form_errors': serializer.errors})


    def put(self, request, note_id):
        data = json.loads(request.body)
        authors_data = data.pop('authors', [])
        permission_data = data.pop('permissions', [])

        with transaction.atomic():
            note = get_object_or_404(Note, pk=note_id)
            serializer = NoteSerializer(instance=note, data=data)
            note.delete_authors()

            if serializer.is_valid():
                note = serializer.save()
                note.authors.set(authors_data)
                if len(authors_data) != len(permission_data):
                    return JsonResponse(serializer.errors, status=400)
                for author, permission in zip(authors_data, permission_data):
                    note_author = get_object_or_404(NoteAuthor, user_id=author, note_id=note.id)
                    note_author.permission = permission
                    note_author.save()

                    author_ = get_object_or_404(User, pk=author)
                    author_.numberOfNotes += 1
                    author_.save()

                note.refresh_from_db()
                return render(request, 'note_detail.html', {'note': NoteSerializer(note).data})
            else:
                return render(request, 'note_form.html', {'form_errors': serializer.errors})

    def delete(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        note.delete_authors()
        note.delete()
        return HttpResponseNotFound('<h1>Note deleted successfully</h1>', status=204)