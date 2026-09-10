import os
import sys
import django

sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal

remaining = Soal.objects.filter(pertanyaan__contains="[HOTS").count()
print(f"Total soal yang masih ada '[HOTS' di pertanyaan: {remaining}")

sample = Soal.objects.exclude(referensi_internal__isnull=True).exclude(referensi_internal__exact="")[:3]
print("\nContoh Soal yang sudah diupdate:")
for q in sample:
    print("-" * 50)
    print(f"ID: {q.id}")
    print(f"Referensi: {q.referensi_internal}")
    print(f"Pertanyaan: {repr(q.pertanyaan[:150])}")
