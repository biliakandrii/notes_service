from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    numberOfNotes = models.IntegerField()

    def __str__(self):
        return self.username


class Note(models.Model):
    header = models.CharField(max_length=255)
    body = models.TextField()
    authors = models.ManyToManyField('User', through='NoteAuthor')

class NoteAuthor(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=[('read', 'Read'), ('write', 'Write'), ('admin', 'Admin')])
