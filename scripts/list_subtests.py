import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
import django
django.setup()
from ujian.models import SubTest

patterns = ['1.1','1.','2.3','2.']
print('All SubTests (id, paket, nama, question_count):')
for s in SubTest.objects.all().order_by('id'):
    print(s.id, '|', s.paket.nama, '|', s.nama, '|', s.soal.count())

print('\nFiltered matches:')
for p in ['1.1','2.3']:
    print(f"\nPattern '{p}':")
    found = SubTest.objects.filter(nama__icontains=p) | SubTest.objects.filter(paket__nama__icontains=p)
    for s in found:
        print('  ', s.id, '|', s.paket.nama, '|', s.nama, '|', s.soal.count())
    if not found.exists():
        print('  (no exact match)')
