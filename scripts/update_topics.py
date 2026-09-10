import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal, SubTest

def update_topics():
    # Ambil soal-soal di Try Out Easy 1
    soal_qs = Soal.objects.filter(subtest__paket__nama="Try Out Easy 1")
    count = soal_qs.count()
    print(f"Total soal di Try Out Easy 1: {count}")
    
    updated = 0
    for s in soal_qs:
        st_name = s.subtest.nama.lower()
        
        # Penugasan topik berdasarkan isi pertanyaan/subtest
        if "pk" in st_name or "matematika" in st_name:
            if "persamaan linear" in s.pertanyaan.lower():
                s.topik_materi = "Aljabar"
            elif "diskon" in s.pertanyaan.lower():
                s.topik_materi = "Aritmatika Sosial"
            else:
                s.topik_materi = "Kuantitatif Umum"
        elif "pu" in st_name:
            if "premis" in s.pertanyaan.lower():
                # Misal bedakan antara profesi
                if "petani" in s.pertanyaan.lower() or "ilmuwan" in s.pertanyaan.lower():
                    s.topik_materi = "Logika Deduktif"
                else:
                    s.topik_materi = "Silogisme"
            else:
                s.topik_materi = "Logika Analitik"
        elif "lbe" in st_name or "inggris" in st_name:
            if "main idea" in s.pertanyaan.lower():
                s.topik_materi = "Main Idea"
            else:
                s.topik_materi = "Inference"
        else:
            # LBI / PBM / PPU
            if "gagasan utama" in s.pertanyaan.lower():
                s.topik_materi = "Gagasan Utama"
            else:
                s.topik_materi = "Kesimpulan Logis"
                
        s.save()
        updated += 1
        
    print(f"Berhasil mengupdate topik materi untuk {updated} soal.")

if __name__ == "__main__":
    update_topics()
