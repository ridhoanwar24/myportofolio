from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from main.models import Experience, Education

User = get_user_model()


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

        self.education = Education.objects.create(
            institution_name ="SDN Rambutan 05 Pagi",
            category="elementary school",
            year_started=2013,
            year_ended=2019,   
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_education_model(self):
        self.assertEqual(str(self.education), "SDN Rambutan 05 Pagi")
        self.assertEqual(self.education.category, "elementary school")
        self.assertFalse(self.education.is_ongoing)

    # def test_experience_page(self):
    #     response = self.client.get(reverse("main:show_experience"))

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "experience.html")
    #     self.assertContains(response, self.experience.title)
    #     self.assertContains(response, self.experience.description)
    #     self.assertContains(response, "Part-Time")
    #     self.assertContains(response, "Sedang berlangsung")
    #     self.assertContains(response, f'href="{reverse("main:show_main")}"')

    # def test_education_page(self):
    #     response = self.client.get(reverse("main:show_education"))

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "education.html")
    #     self.assertContains(response, self.education.institution_name)
    #     self.assertContains(response, "Elementary School")
    #     self.assertContains(response, "2019")
    #     self.assertContains(response, f'href="{reverse("main:show_main")}"')

    # def test_empty_experience_page(self):
    #     Experience.objects.all().delete()
    #     response = self.client.get(reverse("main:show_experience"))

    #     self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    # def test_empty_education_page(self):
    #     Education.objects.all().delete()
    #     response = self.client.get(reverse("main:show_education"))

    #     self.assertContains(response, "Belum ada pendidikan yang ditambahkan.")

    # def test_completed_experience(self):
    #     self.experience.ended_at = timezone.now()
    #     self.experience.save()
    #     response = self.client.get(reverse("main:show_experience"))

    #     self.assertFalse(self.experience.is_ongoing)
    #     self.assertContains(response, "Selesai")
    #     self.assertNotContains(response, "Sedang berlangsung")

class ExperiencePageTest(TestCase):
    def test_experience_page_shell(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        # Kartu dirender JS, jadi yang dicek adalah kerangka & endpoint-nya
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, reverse("api:experience-list"))
        self.assertContains(response, f'href="{reverse("main:show_main")}"')


    def test_add_button_only_for_superuser(self):
        marker = 'popovertarget="add-experience-modal"'

        response = self.client.get(reverse("main:show_experience"))
        self.assertNotContains(response, marker)

        admin = User.objects.create_superuser("admin", password="pass12345")
        self.client.force_login(admin)
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, marker)


class ExperienceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
        self.list_url = reverse("api:experience-list")

    def results(self, response):
        data = response.json()
        return data["results"] if isinstance(data, dict) else data

    def test_list_returns_experience(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        items = self.results(response)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Asisten Dosen PBP")
        self.assertEqual(items[0]["category"], "part-time")
        self.assertIsNone(items[0]["ended_at"])       # pengganti "Sedang berlangsung"
        self.assertEqual(items[0]["star_count"], 0)
        self.assertFalse(items[0]["is_starred"])

    def test_completed_experience_has_ended_at(self):
        self.experience.ended_at = timezone.now()     # pengganti "Selesai"
        self.experience.save()

        items = self.results(self.client.get(self.list_url))
        self.assertIsNotNone(items[0]["ended_at"])

    def test_empty_list(self):
        Experience.objects.all().delete()
        self.assertEqual(self.results(self.client.get(self.list_url)), [])

    def test_search_by_title(self):
        Experience.objects.create(title="Magang Backend", category="internship")

        items = self.results(self.client.get(self.list_url, {"title": "Magang"}))
        self.assertEqual([i["title"] for i in items], ["Magang Backend"])

    def test_create_requires_superuser(self):
        payload = {"title": "Baru", "description": "x", "category": "part-time"}

        self.assertIn(self.client.post(self.list_url, payload, format="json").status_code, (401, 403))

        admin = User.objects.create_superuser("admin", password="pass12345")
        self.client.force_authenticate(admin)
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 201)

    
    def test_title_is_sanitized(self):
        admin = User.objects.create_superuser("admin", password="pass12345")
        self.client.force_authenticate(admin)

        response = self.client.post(
            self.list_url,
            {"title": "<b>Halo</b>", "description": "x", "category": "part-time"},
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.json()["title"], "Halo")

        response = self.client.post(
            self.list_url,
            {"title": "<b></b>", "description": "x", "category": "part-time"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json())

    def test_star_requires_login(self):
        url = reverse("api:experience-star", args=[self.experience.pk])
        self.assertIn(self.client.post(url).status_code, (401, 403))

        user = User.objects.create_user("budi", password="pass12345")
        self.client.force_authenticate(user)
        self.assertEqual(self.client.post(url).status_code, 200)
        items = self.results(self.client.get(self.list_url))
        self.assertEqual(items[0]["star_count"], 1)
        self.assertTrue(items[0]["is_starred"])