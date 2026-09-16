from django.forms import ModelForm, TextInput, Textarea, URLInput

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
            "category": TextInput(
                attrs={
                    "placeholder": "University",
                    "maxlength": 50,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
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