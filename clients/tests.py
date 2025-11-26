from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.urls import reverse
from users.models import CustomUser as User
from django.test import TestCase, SimpleTestCase
from django.urls import resolve
from clients.views import ClientListView, ClientUpdateView, ClientFormView
from users.views import index, login_view
from clients.models import Client, District, DS_Division, Province, Choice, ThalassemiaUnit, FamilyMember, DiagnosisType
from clients.form import ClientForm


class ClientModelTest(TestCase):
    def setUp(self):
        # Create related objects first
        self.province = Province.objects.create(name="Northwestern")
        self.district = District.objects.create(name="Kurunegala", province=self.province)
        self.ds_division = DS_Division.objects.create(name="Polpithigama", district=self.district)

        # create choices for marital status
        Choice.objects.create(category="marital_status", name="Single")

        # Create a ThalassemiaUnit
        self.thalassemiaUnit = ThalassemiaUnit.objects.create(name="Kurunegala")

        # Create a client
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
            unit=self.thalassemiaUnit,
        )

    def test_client_str(self):
        """Test string representation of client"""
        self.assertEqual(str(self.client), "T-525 : John Silva")

    def test_client_has_valid_ds_division(self):
        """Test client belongs to the correct DS division and related objects are correctly set"""
        self.assertEqual(self.client.ds_division.name, "Polpithigama")
        self.assertEqual(self.client.ds_division.district.name, "Kurunegala")
        self.assertEqual(self.client.ds_division.district.province.name, "Northwestern")
        self.assertEqual(self.province.name, "Northwestern")
        self.assertEqual(self.district.name, "Kurunegala")
        self.assertEqual(self.ds_division.name, "Polpithigama")

    def test_client_creation(self):
        """Test client creation and field values"""
        self.assertEqual(self.client.registration_number, "T-525")
        self.assertEqual(self.client.full_name, "John Silva")
        self.assertEqual(self.client.common_name, "John")
        self.assertEqual(self.client.gender, "M")
        self.assertEqual(self.client.date_of_birth, "1990-01-01")
        self.assertEqual(self.client.blood_group, "A+")
        self.assertEqual(self.client.address, "123 Main Street")
        self.assertEqual(self.client.ds_division, self.ds_division)
        self.assertEqual(self.client.unit, self.thalassemiaUnit)
        self.assertEqual(self.client.unit.name, self.thalassemiaUnit.name)
        self.assertEqual(self.client.unit.name, "Kurunegala")

    def test_client_marital_status(self):
        """Test client marital status"""
        self.assertEqual(self.client.marital_status.name, "Single")

    def test_duplicate_registration_number_raises_error(self):
        """Duplicate registration_number should raise IntegrityError"""
        with self.assertRaises(IntegrityError):
            Client.objects.create(registration_number="T-525", full_name="Jane", ds_division=self.ds_division)

    def test_name_cannot_be_blank(self):
        client = Client(registration_number="T-522", full_name="", ds_division=self.ds_division)
        with self.assertRaises(ValidationError):
            client.full_clean()  # runs Django’s model validation
            # client.save()

    def test_reverse_relationship(self):
        """DS Division should access its clients via related_name"""
        clients = self.ds_division.client_set.all()
        self.assertIn(self.client, clients)

    def test_client_ds_division_set_to_null_when_deleted(self):
        """Deleting a DS Division should set client's ds_division to NULL"""
        self.ds_division.delete()
        client = Client.objects.get(pk=self.client.pk)
        self.assertIsNone(client.ds_division)


class FamilyMemberOnDeleteTest(TestCase):
    def setUp(self):
        # Create province, district, DS division
        self.province = Province.objects.create(name="Northwestern")
        self.district = District.objects.create(name="Kurunegala", province=self.province)
        self.ds_division = DS_Division.objects.create(name="Polpithigama", district=self.district)

        # Create client
        self.client = Client.objects.create(
            registration_number="T-300",
            full_name="Sunil Perera",
            ds_division=self.ds_division
        )

        # Create diagnosis type
        self.diagnosis = DiagnosisType.objects.create(name="Beta Thalassaemia Trait")

        # Create family member
        self.family_member = FamilyMember.objects.create(
            client=self.client,
            relationship="Father",
            name="John Perera",
            diagnosis=self.diagnosis,
        )

    def test_family_member_deleted_when_client_deleted(self):
        """Deleting a client should delete their family members"""
        self.client.delete()
        members = FamilyMember.objects.all()
        self.assertEqual(members.count(), 0)

    def test_diagnosis_set_null_when_deleted(self):
        """Deleting a diagnosis type should set diagnosis field to NULL"""
        self.diagnosis.delete()
        member = FamilyMember.objects.get(pk=self.family_member.pk)
        self.assertIsNone(member.diagnosis)


class ClientViewTest(TestCase):
    def setUp(self):
        self.province = Province.objects.create(name="Northwestern")
        self.district = District.objects.create(name="Kurunegala", province=self.province)
        self.ds_division = DS_Division.objects.create(name="Polpithigama", district=self.district)
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client_obj = Client.objects.create(
            registration_number="T-501", full_name="Saman", ds_division=self.ds_division
        )

    def test_client_list_view(self):
        self.client.login(username="testuser", password="pass123")
        url = reverse("clients:client-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # redirect to login
        self.assertContains(response, "Saman")

    def test_client_detail_view(self):
        self.client.login(username="testuser", password="pass123")
        url = reverse("clients:client-update", args=[self.client_obj.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # redirect to login
        self.assertContains(response, "Saman")


class ClientFormTest(TestCase):
    def setUp(self):
        self.province = Province.objects.create(name="Western")
        self.district = District.objects.create(name="Colombo", province=self.province)
        self.ds_division = DS_Division.objects.create(name="Kaduwela", district=self.district)

    def test_valid_form(self):
        form_data = {
            "registration_number": "T-600",
            "full_name": "Nimal",
            "ds_division": self.ds_division.id,
            "gender": "M",
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_name_not_valid(self):
        form_data = {
            "registration_number": "T-601",
            "full_name": "",
            "ds_division": self.ds_division.id,
            "gender": "M",
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
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_logged_in_user_can_access(self):
        self.client.login(username="testuser", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class ClientAuthTest2(TestCase):
    def setUp(self):
        self.url = reverse("clients:client-list")  # protected page

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        # 1️⃣ Check for redirect
        self.assertEqual(response.status_code, 302)
        # 2️⃣ Check destination URL
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")
