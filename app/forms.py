# forms.py

from django import forms
from .models import User, Note, NoteAuthor

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
