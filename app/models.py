from django.db import models
from django.shortcuts import get_object_or_404


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    numberOfNotes = models.IntegerField(default=0) #fix

    def __str__(self):
        return self.username


class Note(models.Model):
    header = models.CharField(max_length=255)
    body = models.TextField()
    authors = models.ManyToManyField('User', through='NoteAuthor')  #fix

    def get_author_ids(self):
        return list(self.authors.values_list('pk', flat=True))
    def delete_authors(self):
        authors_list = self.get_author_ids()
        for author in authors_list:
            author_ = get_object_or_404(User, pk=author)
            author_.numberOfNotes -= 1
            author_.save()

    def authors_(note):
        result = ''
        authors_list = note.get_author_ids()
        for author in authors_list:
            author_ = get_object_or_404(User, pk=author)
            perm = get_object_or_404(NoteAuthor, user_id=author, note_id=note.id)
            result += str(author_.username) + ' - ' + str(perm.permission) + ', '
        return result


class NoteAuthor(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=[('read', 'Read'), ('write', 'Write'), ('admin', 'Admin'),
                                                          ('inactive', 'Inactive')])
