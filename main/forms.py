from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from main.models import *

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution_name",
            "category",
            "thumbnail",
            "year_started",
            "year_ended",
        ]

        labels = {
            "institution_name": "Nama Institusi",
            "category": "Jenjang Pendidikan",
            "thumbnail": "URL Foto Institusi",
            "year_started": "Tahun Masuk",
            "year_ended": "Tahun Lulus",
        }

        widgets = {
            "institution_name": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=156ZjN3yK8Ok9EaGgoEqwWoHIYzvumKss&sz=w1000",
                }
            ),
            "year_started": TextInput(
                attrs={
                    "placeholder": "2020",
                }
            ),
            "year_ended": TextInput(
                attrs={
                    "placeholder": "2025",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]
    
        labels = {
            "title": "Pengalaman",
            "description": "Deskripsi pengalaman",
            "category": "Kategori pengalaman",
            "thumbnail": "URL Pengalaman",
            "ended_at": "Waktu selesai",
        }
    
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Freelance",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=156ZjN3yK8Ok9EaGgoEqwWoHIYzvumKss&sz=w1000",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()