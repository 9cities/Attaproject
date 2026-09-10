import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from ujian.models import PaketUjian

for pkt_name in ['Konsep Dasar 1.3', 'Konsep Dasar 2.3']:
    print(f'\nPaket: {pkt_name}')
    paket = PaketUjian.objects.filter(nama=pkt_name).first()
    if paket:
        subtests = paket.subtests.all()
        print(f'Total Subtests: {subtests.count()}')
        for st in subtests:
            print(f' - {st.nama}: {st.soal.count()} soal')
    else:
        print('Paket not found!')
