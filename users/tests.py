from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import Group
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
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login"))

    def test_django_login_view_authenticates_user(self):
        url = reverse("login")
        response = self.client.post(url, {"username": "testuser", "password": "pass123"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_role_groups_are_bootstrapped(self):
        expected_roles = {"unit_data_entry", "unit_clinician", "unit_admin"}
        existing_roles = set(Group.objects.filter(name__in=expected_roles).values_list("name", flat=True))
        self.assertEqual(existing_roles, expected_roles)
