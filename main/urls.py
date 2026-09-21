from django.urls import path

from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/educations/", get_education_json, name="get_education_json"),
    path("api/experiences/", get_experience_json, name="get_experiences_json"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
]