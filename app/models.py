from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.shortcuts import get_object_or_404


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.password == password:
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class Note(models.Model):
    header = models.CharField(max_length=255)
    body = models.TextField()
    authors = models.ManyToManyField('User', through='NoteAuthor')


class NoteAuthor(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)
