import os
import sys
import django
import random

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal

categories = ["KD2", "EASY", "MEDIUM", "HARD"]

print("=== QUALITY CONTROL SOAL REPORT ===")

for cat in categories:
    soals = Soal.objects.filter(kategori=cat)
    total = soals.count()
    print(f"\nKategori: {cat} (Total Soal: {total})")
    
    if total == 0:
        print("Tidak ada soal di kategori ini.")
        continue
        
    indices = random.sample(range(total), min(2, total))
    samples = [soals[i] for i in indices]
    
    for i, s in enumerate(samples, 1):
        print(f"\n--- Sampel {i} (ID: {s.id}) ---")
        print(f"Pertanyaan: {s.pertanyaan}")
        print(f"A. {s.pilihan_a}")
        print(f"B. {s.pilihan_b}")
        print(f"C. {s.pilihan_c}")
        print(f"D. {s.pilihan_d}")
        print(f"E. {s.pilihan_e}")
        print(f"Jawaban Benar: {s.jawaban_benar}")
        if s.pembahasan:
            print(f"Pembahasan: ADA")
        else:
            print(f"Pembahasan: KOSONG")
