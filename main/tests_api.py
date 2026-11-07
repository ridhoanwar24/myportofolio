import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Education

User = get_user_model()
PASSWORD = "pass12345"

class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.experience = Experience.objects.create(
            title="Portfolio", description="My website", category="part-time",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "New experience", "description": "A useful app", "category": "part-time",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EducationAPITest(APITestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution_name="Fasilkom UI",
            category="university",
            year_started=2025,
        )

        group, _ = Group.objects.get_or_create(name="Editor")

        self.owner = User.objects.create_superuser("owner", password=PASSWORD)
        self.editor = User.objects.create_user("editor", password=PASSWORD)
        self.editor.groups.add(group)
        self.regular = User.objects.create_user("budi", password=PASSWORD)

        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.pk])
        self.star_url = reverse("api:education-star", args=[self.education.pk])
        self.payload = {
            "institution_name": "SMA Baru",
            "category": "high school",
            "year_started": 2020,
            "year_ended": 2023,
        }

    def snapshot(self):
        """Isi tabel Education saat ini, untuk dibandingkan sebelum/sesudah."""
        return list(Education.objects.order_by("pk").values())

    def results(self, response):
        data = response.json()
        return data["results"] if isinstance(data, dict) else data

    def assert_write_denied(self):
        """Semua operasi tulis ditolak dan database tidak berubah."""
        before = self.snapshot()
        responses = {
            "POST": self.client.post(self.list_url, self.payload, format="json"),
            "PATCH": self.client.patch(self.detail_url, {"institution_name": "Diretas"}, format="json"),
            "PUT": self.client.put(self.detail_url, self.payload, format="json"),
            "DELETE": self.client.delete(self.detail_url),
        }
        for method, response in responses.items():
            with self.subTest(method=method):
                self.assertEqual(response.status_code, 403, response.content)
        self.assertEqual(self.snapshot(), before)


class EducationRolePermissionTest(EducationAPITest):
    def test_visitor_can_read(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.results(response)), 1)
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)

    def test_visitor_cannot_write(self):
        self.assert_write_denied()

    def test_regular_user_cannot_write(self):
        self.client.force_authenticate(self.regular)
        self.assert_write_denied()

    def test_editor_can_patch(self):
        self.client.force_authenticate(self.editor)
        response = self.client.patch(self.detail_url, {"institution_name": "Fasilkom UI Depok"}, format="json")

        self.assertEqual(response.status_code, 200, response.content)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution_name, "Fasilkom UI Depok")

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(self.editor)
        before = self.snapshot()

        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Education.objects.filter(institution_name="SMA Baru").exists())

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())

        self.assertEqual(self.snapshot(), before)

    def test_owner_can_create(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")

        self.assertEqual(response.status_code, 201, response.content)
        self.assertTrue(Education.objects.filter(institution_name="SMA Baru").exists())
        self.assertEqual(Education.objects.count(), 2)

    def test_owner_can_delete(self):
        self.client.force_authenticate(self.owner)
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Education.objects.filter(pk=self.education.pk).exists())


class EducationValidationTest(EducationAPITest):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.owner)

    def assert_rejected(self, payload, field):
        before = self.snapshot()
        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, 400, response.content)
        self.assertIn(field, response.json())
        self.assertEqual(self.snapshot(), before)  # tidak ada data tersimpan

    def test_empty_institution_name_rejected(self):
        self.assert_rejected({**self.payload, "institution_name": ""}, "institution_name")

    def test_html_only_institution_name_rejected(self):
        self.assert_rejected({**self.payload, "institution_name": "<b></b>"}, "institution_name")

    def test_missing_institution_name_rejected(self):
        payload = {k: v for k, v in self.payload.items() if k != "institution_name"}
        self.assert_rejected(payload, "institution_name")

    def test_year_ended_before_year_started_rejected(self):
        self.assert_rejected({**self.payload, "year_started": 2023, "year_ended": 2020}, "year_ended")

    def test_html_tags_are_stripped(self):
        response = self.client.post(
            self.list_url, {**self.payload, "institution_name": "<b>SMA Baru</b>"}, format="json"
        )
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.json()["institution_name"], "SMA Baru")
        self.assertTrue(Education.objects.filter(institution_name="SMA Baru").exists())


class EducationStarTest(EducationAPITest):
    def test_visitor_cannot_star(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_user_can_star_and_unstar(self):
        self.client.force_authenticate(self.regular)

        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(self.education.starred_by.count(), 1)
        self.assertTrue(self.education.starred_by.filter(pk=self.regular.pk).exists())
        self.assertEqual(response.json()["star_count"], 1)
        self.assertTrue(response.json()["is_starred"])

        response = self.client.post(self.star_url)
        self.assertEqual(self.education.starred_by.count(), 0)
        self.assertFalse(response.json()["is_starred"])

    def test_star_count_is_shared_but_is_starred_is_per_user(self):
        self.client.force_authenticate(self.regular)
        self.client.post(self.star_url)

        self.client.force_authenticate(self.editor)
        item = self.results(self.client.get(self.list_url))[0]
        self.assertEqual(item["star_count"], 1)
        self.assertFalse(item["is_starred"])


class EducationCSRFTest(EducationAPITest):
    def setUp(self):
        super().setUp()
        self.csrf_client = APIClient(enforce_csrf_checks=True)
        # .login() memakai sesi sungguhan; force_authenticate akan melewati CSRF
        self.assertTrue(self.csrf_client.login(username="owner", password=PASSWORD))

    def test_write_without_csrf_token_is_rejected(self):
        before = self.snapshot()

        response = self.csrf_client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertIn("CSRF", str(response.json().get("detail", "")))

        response = self.csrf_client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(self.snapshot(), before)

    def test_write_with_csrf_token_succeeds(self):
        """Kontrol positif: tanpa ini, test di atas bisa lulus karena alasan lain."""
        token = "a" * 64
        self.csrf_client.cookies["csrftoken"] = token

        response = self.csrf_client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token
        )
        self.assertEqual(response.status_code, 201, response.content)
        self.assertTrue(Education.objects.filter(institution_name="SMA Baru").exists())