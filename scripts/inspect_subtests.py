import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
import django
django.setup()

from ujian.models import PaketUjian, SubTest

paket = PaketUjian.objects.filter(nama__startswith='Konsep Dasar 1 1').first()
if not paket:
    paket = PaketUjian.objects.filter(nama='Konsep Dasar 1 1').first()

print('Paket:', paket)

for sub in paket.subtests.all():
    qs = list(sub.soal.order_by('id'))
    ids = [s.id for s in qs]
    print('\nSubtest:', sub.nama, 'count=', len(ids))
    print('first 15 ids:', ids[:15])
    # show indices mapping
    for i, sid in enumerate(ids[:15], start=1):
        print(i, sid)

# also check a few other packages
paket2 = PaketUjian.objects.filter(nama='Konsep Dasar 1 2').first()
if paket2:
    print('\nPaket 1 2 found')
    for sub in paket2.subtests.all():
        ids = [s.id for s in sub.soal.order_by('id')]
        print('Sub', sub.nama, 'count', len(ids), 'ids sample', ids[:12])
else:
    print('\nPaket 1 2 not found')
