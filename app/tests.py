import json

from django.test import TestCase, Client
from django.urls import reverse
from app.models import User, Note


class UserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpassword")

    def test_get_user(self):
        url = reverse("user-retrieve-destroy", kwargs={"user_id": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_detail.html')

    def test_get_all_users(self):
        url = reverse("user-create-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')

    def test_create_user(self):
        url = reverse("user-create-list")
        data = {"username": "newuser", "email": "new@example.com", "password": "newpassword"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_delete_user(self):
        url = reverse("user-retrieve-destroy", kwargs={"user_id": self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(username="testuser").exists())


class NoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpassword")
        self.note = Note.objects.create(header="Test Note", body="Test content")

    def test_get_note(self):
        url = reverse("note-retrieve-update-delete", kwargs={"note_id": self.note.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'note_detail.html')

    def test_create_note(self):
        url = reverse("note-create")
        data = {"header": "New Note", "body": "New content", "authors": [self.user.id], "permissions": ["read"]}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Note.objects.filter(header="New Note").exists())

    def test_update_note(self):
        url = reverse("note-retrieve-update-delete", kwargs={"note_id": self.note.id})
        data = {"header": "Updated Note", "body": "Updated content", "authors": [self.user.id], "permissions": ["write"]}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.get(id=self.note.id).header, "Updated Note")

    def test_delete_note(self):
        url = reverse("note-retrieve-update-delete", kwargs={"note_id": self.note.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Note.objects.filter(header="Test Note").exists())


