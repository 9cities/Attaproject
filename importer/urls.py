from django.urls import path
from . import views

urlpatterns = [
    path(
        "import-soal/",
        views.import_soal,
        name="import_soal"
    ),
    path(
        "build-konsep/",
        views.build_concept_subtests,
        name="build_concept_subtests"
    ),
]