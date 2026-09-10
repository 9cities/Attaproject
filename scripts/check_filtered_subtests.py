import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
import django
django.setup()

import re
from ujian.models import PaketUjian

paket = PaketUjian.objects.filter(nama__startswith='Konsep Dasar 1 1').first()
if not paket:
    paket = PaketUjian.objects.filter(nama='Konsep Dasar 1 1').first()
print('Paket:', paket)
all_sub = [s.nama for s in paket.subtests.all()]
print('All subtests:', all_sub)
filtered = [s.nama for s in paket.subtests.all() if not re.match(r'^\d+(?:\.\d+)?$', s.nama.strip())]
print('Filtered subtests:', filtered)
