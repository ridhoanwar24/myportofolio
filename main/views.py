from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Education
from main.forms import EducationForm


def get_education_json(request):
    institution_name_query = request.GET.get("institution_name", "").strip()
    educations = Education.objects.all()

    if institution_name_query:
        educations = educations.filter(institution_name__icontains=institution_name_query)

    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")

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
    json_response = get_education_json(request)

    educations = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    educations = [education.object for education in educations]
    institution_name_query = request.GET.get("institution_name", "").strip()

    context = {
        "full_name": "Muhammad Ridho Anwar",
        "nickname": "Ridho",
        "institution_name_query": institution_name_query,
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

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Data pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")