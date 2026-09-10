import os
import sys
import django
import random

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal, SubTest

print("=== VERIFIKASI SOAL BARU ===")

# Ambil satu soal matematika (PK)
pk_soals = Soal.objects.filter(subtest__nama="PK", kategori="EASY")
if pk_soals.exists():
    s = pk_soals.first()
    print("\n--- CONTOH SOAL PK ---")
    print(s.pertanyaan)
    print("A.", s.pilihan_a)
    print("B.", s.pilihan_b)
    print("C.", s.pilihan_c)
    print("D.", s.pilihan_d)
    print("E.", s.pilihan_e)
    print("Jawaban:", s.jawaban_benar)

# Ambil satu soal LBI (Literasi Bahasa Indonesia saintek)
lbi_soals = Soal.objects.filter(subtest__nama="LBI saintek", kategori="EASY")
if lbi_soals.exists():
    s = lbi_soals.first()
    print("\n--- CONTOH SOAL LITERASI ---")
    print(s.pertanyaan)
    print("A.", s.pilihan_a)
    print("B.", s.pilihan_b)
    print("C.", s.pilihan_c)
    print("D.", s.pilihan_d)
    print("E.", s.pilihan_e)
    print("Jawaban:", s.jawaban_benar)
