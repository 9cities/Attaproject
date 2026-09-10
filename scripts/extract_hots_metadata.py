import os
import sys
import django
import re

sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal

def process_soal():
    # Regex untuk mengambil text dalam kurung siku di awal string (opsional ada spasi sebelum/sesudahnya)
    pattern = re.compile(r'^\s*(\[.*?\])\s*(.*)', re.DOTALL)
    
    # Ambil semua soal yang ada kurung siku
    soals = Soal.objects.filter(pertanyaan__contains="[")
    
    updated_soals = []
    
    print(f"Total soal to check: {soals.count()}")
    count_updated = 0
    
    for soal in soals:
        match = pattern.match(soal.pertanyaan)
        if match:
            tag = match.group(1)
            rest_of_question = match.group(2)
            
            # Jika tag seperti [HOTS...] atau sejenisnya
            soal.referensi_internal = tag
            soal.pertanyaan = rest_of_question
            updated_soals.append(soal)
            count_updated += 1
            
            if count_updated % 1000 == 0:
                print(f"Processed {count_updated}...")
    
    print(f"Total Soal yang akan diupdate: {count_updated}")
    
    # Update bulk untuk efisiensi
    if updated_soals:
        batch_size = 1000
        for i in range(0, len(updated_soals), batch_size):
            Soal.objects.bulk_update(
                updated_soals[i:i+batch_size], 
                ['pertanyaan', 'referensi_internal']
            )
        print("Selesai mengupdate database.")
    else:
        print("Tidak ada yang perlu diupdate.")

if __name__ == '__main__':
    process_soal()
