from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Education


def show_main(request):
    context = {
        "full_name": "Muhammad Ridho Anwar",
        "nickname": "Ridho",
        "npm": "2506595745",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "full_name": "Muhammad Ridho Anwar",
        "nickname": "Ridho",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_education(request):
    context = {
        "full_name": "Muhammad Ridho Anwar",
        "nickname": "Ridho",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "full_name": "Muhammad Ridho Anwar",
        "nickname": "Ridho",
        "form": form,
    }
    return render(request, "education_form.html", context)