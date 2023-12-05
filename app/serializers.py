from rest_framework import serializers
from app.models import Note, NoteAuthor, User


class UserSerializer(serializers.ModelSerializer):
    note_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'note_count']
        extra_kwargs = {
            'password': {'write_only': True},  # Mark password as write-only during creation
        }
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class NoteAuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer
    note = NoteSerializer

    class Meta:
        model = NoteAuthor
        fields = ['user', 'note']

