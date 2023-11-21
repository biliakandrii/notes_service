from rest_framework import serializers
from app.models import Note, NoteAuthor, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()

    def get_authors(self, obj):
        authors = NoteAuthor.objects.filter(note=obj)
        return [{'user': UserSerializer(author.user).data, 'permission': author.permission} for author in authors]

    class Meta:
        model = Note
        fields = '__all__'
