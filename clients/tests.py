from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from clients.form import ClientForm
from clients.models.client import Client, ClientCareUnit, FamilyMember
from clients.models.lookup import Choice, DS_Division, DiagnosisType, District, Province, ThalassemiaUnit
from clients.views import ClientFormView, ClientListView, ClientUpdateView
from users.models import CustomUser as User


class ClientModelTest(TestCase):
    def setUp(self):
        self.province = Province.objects.create(name="Northwestern")
        self.district = District.objects.create(name="Kurunegala", province=self.province)
        self.ds_division = DS_Division.objects.create(name="Polpithigama", district=self.district)
        self.primary_unit = ThalassemiaUnit.objects.create(name="Kurunegala")
        Choice.objects.create(category="marital_status", name="Single")

        self.client = Client.objects.create(
            registration_number="T-525",
            full_name="John Silva",
            common_name="John",
            gender="M",
            date_of_birth="1990-01-01",
            blood_group="A+",
            ds_division=self.ds_division,
            address="123 Main Street",
            marital_status=Choice.objects.get(name="Single"),
        )
        ClientCareUnit.objects.create(
            client=self.client,
            unit=self.primary_unit,
            role=ClientCareUnit.Role.PRIMARY,
        )

    def test_client_str(self):
        self.assertEqual(str(self.client), "T-525 : John Silva")

    def test_client_has_valid_ds_division(self):
        self.assertEqual(self.client.ds_division.name, "Polpithigama")
        self.assertEqual(self.client.ds_division.district.name, "Kurunegala")
        self.assertEqual(self.client.ds_division.district.province.name, "Northwestern")

    def test_client_creation(self):
        self.assertEqual(self.client.registration_number, "T-525")
        self.assertEqual(self.client.full_name, "John Silva")
        self.assertEqual(self.client.common_name, "John")
        self.assertEqual(self.client.gender, "M")
        self.assertEqual(self.client.blood_group, "A+")
        self.assertEqual(self.client.address, "123 Main Street")

    def test_primary_care_unit(self):
        self.assertEqual(self.client.primary_care_unit, self.primary_unit)

    def test_client_marital_status(self):
        self.assertEqual(self.client.marital_status.name, "Single")

    def test_duplicate_registration_number_raises_error(self):
        with self.assertRaises(IntegrityError):
            Client.objects.create(registration_number="T-525", full_name="Jane", ds_division=self.ds_division)

    def test_name_cannot_be_blank(self):
        client = Client(registration_number="T-522", full_name="", ds_division=self.ds_division)
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_reverse_relationship(self):
        clients = self.ds_division.client_set.all()
        self.assertIn(self.client, clients)

    def test_client_ds_division_set_to_null_when_deleted(self):
        self.ds_division.delete()
        client = Client.objects.get(pk=self.client.pk)
        self.assertIsNone(client.ds_division)

    def test_only_one_active_primary_per_client(self):
        other_unit = ThalassemiaUnit.objects.create(name="Other Unit")
        with self.assertRaises(IntegrityError):
            ClientCareUnit.objects.create(
                client=self.client,
                unit=other_unit,
                role=ClientCareUnit.Role.PRIMARY,
            )


class FamilyMemberOnDeleteTest(TestCase):
    def setUp(self):
        self.province = Province.objects.create(name="Northwestern")
        self.district = District.objects.create(name="Kurunegala", province=self.province)
        self.ds_division = DS_Division.objects.create(name="Polpithigama", district=self.district)

        self.client = Client.objects.create(registration_number="T-300", full_name="Sunil Perera", ds_division=self.ds_division)
        self.diagnosis = DiagnosisType.objects.create(name="Beta Thalassaemia Trait")
        self.family_member = FamilyMember.objects.create(
            client=self.client,
            relationship="Father",
            name="John Perera",
            diagnosis=self.diagnosis,
        )

    def test_family_member_deleted_when_client_deleted(self):
        self.client.delete()
        members = FamilyMember.objects.all()
        self.assertEqual(members.count(), 0)

    def test_diagnosis_set_null_when_deleted(self):
        self.diagnosis.delete()
        member = FamilyMember.objects.get(pk=self.family_member.pk)
        self.assertIsNone(member.diagnosis)


class ClientViewTest(TestCase):
    def setUp(self):
        self.province = Province.objects.create(name="Northwestern")
        self.district = District.objects.create(name="Kurunegala", province=self.province)
        self.ds_division = DS_Division.objects.create(name="Polpithigama", district=self.district)
        self.unit_a = ThalassemiaUnit.objects.create(name="Unit A")
        self.unit_b = ThalassemiaUnit.objects.create(name="Unit B")

        self.user = User.objects.create_user(
            username="testuser",
            password="pass123",
            thalassemia_unit=self.unit_a,
        )
        self.user.user_permissions.add(Permission.objects.get(codename="view_client"))
        self.user.user_permissions.add(Permission.objects.get(codename="change_client"))

        self.client_obj = Client.objects.create(
            registration_number="T-501",
            full_name="Saman",
            ds_division=self.ds_division,
        )
        ClientCareUnit.objects.create(client=self.client_obj, unit=self.unit_a, role=ClientCareUnit.Role.PRIMARY)

        self.other_unit_client = Client.objects.create(
            registration_number="T-502",
            full_name="Kamal",
            ds_division=self.ds_division,
        )
        ClientCareUnit.objects.create(client=self.other_unit_client, unit=self.unit_b, role=ClientCareUnit.Role.PRIMARY)

    def test_client_list_view_scoped_to_user_unit(self):
        self.client.login(username="testuser", password="pass123")
        response = self.client.get(reverse("clients:client-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Saman")
        self.assertNotContains(response, "Kamal")

    def test_client_update_view_blocked_for_other_unit(self):
        self.client.login(username="testuser", password="pass123")
        url = reverse("clients:client-update", args=[self.other_unit_client.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ClientFormTest(TestCase):
    def setUp(self):
        self.province = Province.objects.create(name="Western")
        self.district = District.objects.create(name="Colombo", province=self.province)
        self.ds_division = DS_Division.objects.create(name="Kaduwela", district=self.district)
        self.unit = ThalassemiaUnit.objects.create(name="Western Unit")

    def test_valid_form(self):
        form_data = {
            "registration_number": "T-600",
            "full_name": "Nimal",
            "ds_division": self.ds_division.id,
            "gender": "M",
            "primary_unit": self.unit.id,
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_primary_unit_required_for_new_client(self):
        form_data = {
            "registration_number": "T-601",
            "full_name": "Nimal",
            "ds_division": self.ds_division.id,
            "gender": "M",
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("primary_unit", form.errors)

    def test_blank_name_not_valid(self):
        form_data = {
            "registration_number": "T-602",
            "full_name": "",
            "ds_division": self.ds_division.id,
            "gender": "M",
            "primary_unit": self.unit.id,
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("full_name", form.errors)


class ClientURLTest(SimpleTestCase):
    def test_client_list_url_resolves(self):
        url = reverse("clients:client-list")
        self.assertEqual(resolve(url).func.view_class, ClientListView)

    def test_client_update_url_resolves(self):
        url = reverse("clients:client-update", args=[1])
        self.assertEqual(resolve(url).func.view_class, ClientUpdateView)

    def test_client_add_url_resolves(self):
        url = reverse("clients:client-add")
        self.assertEqual(resolve(url).func.view_class, ClientFormView)


class ClientAuthTest1(TestCase):
    def setUp(self):
        self.url = reverse("clients:client-list")
        self.user = User.objects.create_user(username="testuser", password="pass123")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_without_permission_gets_forbidden(self):
        self.client.login(username="testuser", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ClientAuthTest2(TestCase):
    def setUp(self):
        self.url = reverse("clients:client-list")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")
