import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from ujian.models import HasilPaketUjian, JawabanPeserta, User

# Cari user yang punya HasilPaketUjian untuk Konsep Dasar 2.3
hasil = HasilPaketUjian.objects.filter(paket_nama='Konsep Dasar 2.3').first()
if hasil:
    print(f'User: {hasil.user.username}')
    print(f'Skor JSON: {hasil.skor_json}')
    
    jawabans = JawabanPeserta.objects.filter(
        user=hasil.user, 
        soal__subtest__paket__nama='Konsep Dasar 2.3'
    ).select_related('soal__subtest')
    
    subtests = {}
    for j in jawabans:
        st_nama = j.soal.subtest.nama
        if st_nama not in subtests:
            subtests[st_nama] = 0
        subtests[st_nama] += 1
        
    print('Jawaban per subtest:')
    for st, count in subtests.items():
        print(f' - {st}: {count} jawaban')
else:
    print('Belum ada HasilPaketUjian untuk Konsep Dasar 2.3')
