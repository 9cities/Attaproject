import os
import sys
import django

sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal, SubTest

print("=== DAFTAR SUBTEST UNTUK KATEGORI EASY ===")

subtests = SubTest.objects.filter(soal__kategori="EASY").distinct()
for st in subtests:
    count = Soal.objects.filter(kategori="EASY", subtest=st).count()
    print(f"- {st.nama} (Paket: {st.paket.nama}) -> {count} soal")

if not subtests:
    print("Tidak ada SubTest yang secara spesifik menempel pada soal EASY.")
    # Coba cari semua SubTest
    print("\nSemua SubTest di database:")
    for st in SubTest.objects.all():
        print(f"- {st.nama} (Paket: {st.paket.nama})")
