from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from users.models import CustomUser
from users.views import index, login_view


class UserURLTest(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse("users:index")
        self.assertEqual(resolve(url).func, index)

    def test_login_url_resolves(self):
        url = reverse("users:login")
        self.assertEqual(resolve(url).func, login_view)


class UserViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="pass123")

    def test_index_view(self):
        url = reverse("users:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Click the button")

    def test_login_view(self):
        url = reverse("users:login")
        response = self.client.post(url, {"username": "testuser", "password": "pass123"})
        self.assertEqual(response.status_code, 302)  # redirect on successful login
