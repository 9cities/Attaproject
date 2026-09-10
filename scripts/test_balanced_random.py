import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import SubTest, Soal
from ujian.views import get_balanced_random_soal_ids
from collections import Counter

st = SubTest.objects.filter(paket__nama="Try Out Easy 1", nama__icontains="pu").first()
if st:
    print(f"Menguji penarikan 12 soal seimbang dari Subtest: {st.nama}")
    
    # Menarik 12 soal
    ids = get_balanced_random_soal_ids(st, 12)
    print(f"Total ditarik: {len(ids)}")
    
    # Hitung persebarannya
    soals = Soal.objects.filter(id__in=ids)
    topics = [s.topik_materi for s in soals]
    counts = Counter(topics)
    
    for t, c in counts.items():
        print(f"Topik: {t} -> {c} soal")
