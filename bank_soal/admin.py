from django.contrib import admin

from .models import Soal



# ==========================
# SOAL
# ==========================

@admin.register(Soal)
class SoalAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "kategori",
        "pertanyaan",
        "jawaban_benar",
    )

    list_filter = (
        "kategori",
    )

    search_fields = (
        "pertanyaan",
    )