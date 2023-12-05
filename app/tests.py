from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User, Note, NoteAuthor
from .serializers import UserSerializer, NoteSerializer, NoteAuthorSerializer


class TestUserListCreateView(APITestCase):

    def setUp(self):
        self.url = reverse('user-create-list')

        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@example.com',
            password='abc121212'
        )
        self.client.force_login(self.user)

    def test_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, UserSerializer(User.objects.all(), many=True).data)

    # Add more tests for user creation, validation, etc.


class TestUserRetrieveUpdateDestroyView(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user_2',
            email='test_user_2@example.com',
            password='def343434'
        )
        self.url = reverse('user-retrieve-update-destroy', kwargs={'pk': self.test_user.id})

        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@example.com',
            password='abc121212'
        )
        self.client.force_login(self.user)

    def test_retrieve(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        data.pop('note_count')
        self.assertEqual(data, UserSerializer(User.objects.get(pk=self.test_user.id)).data)

    # Add more tests for user update, deletion, validation, etc.


class TestNoteCreateView(APITestCase):

    def setUp(self):
        self.url = reverse('note-create')

        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@example.com',
            password='abc121212'
        )
        self.client.force_login(self.user)

    def test_create(self):
        data = {
            'header': 'Test Note Header',
            'body': 'Test Note Body'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, NoteSerializer(Note.objects.get(header='Test Note Header')).data)

    # Add more tests for note creation, validation, etc.

class TestNoteRetrieveUpdateDestroyView(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            email='test_user@example.com',
            password='abc121212'
        )
        self.test_note = Note.objects.create(
            header='Test Note Header',
            body='Test Note Body'
        )
        NoteAuthor.objects.create(user=self.test_user, note=self.test_note)
        self.url = reverse('note-retrieve-update-delete', kwargs={'pk': self.test_note.id})

        self.user = User.objects.create_user(
            username='another_user',
            email='another_user@example.com',
            password='xyz090909'
        )
        self.client.force_login(self.user)

    def test_update(self):
        data = {
            'header': 'Updated Note Header',
            'body': 'Updated Note Body'
        }

        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Only the note author can update

    def test_destroy(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Only the note author can delete


class TestNoteAuthorCreateView(APITestCase):

    def setUp(self):
        self.url = reverse('note-author')

        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@example.com',
            password='abc121212'
        )
        self.client.force_login(self.user)

        self.test_user_2 = User.objects.create_user(
            username='another_user',
            email='another_user@example.com',
            password='xyz090909'
        )
        self.test_note = Note.objects.create(
            header='Test Note Header',
            body='Test Note Body'
        )

    def test_create_valid_relationship(self):
        data = {
            'user': self.test_user_2.id,
            'note': self.test_note.id
        }

        response = self.client.post(self.url, data)

        self.assertFalse(NoteAuthor.objects.filter(user=self.test_user_2, note=self.test_note).exists())

    def test_create_duplicate_relationship(self):
        NoteAuthor.objects.create(user=self.test_user_2, note=self.test_note)

        data = {
            'user': self.test_user_2.id,
            'note': self.test_note.id
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(NoteAuthor.objects.filter(user=self.test_user_2, note=self.test_note).exists())

    def test_create_invalid_user(self):
        data = {
            'user': 999,  # Non-existent user
            'note': self.test_note.id
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(NoteAuthor.objects.filter(note=self.test_note).exists())

    def test_create_invalid_note(self):
        data = {
            'user': self.test_user_2.id,
            'note': 999  # Non-existent note
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(NoteAuthor.objects.filter(user=self.test_user_2).exists())
