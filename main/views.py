from django.shortcuts import render

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