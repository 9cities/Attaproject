import os
import sys
import django
from datetime import datetime, timedelta

# ensure project root on path
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from django.contrib.auth.models import User
from ujian.models import SubTest, Soal, JawabanPeserta, SesiUjian

patterns = [
    (['1.1', 'Konsep Dasar 1.1', 'Konsep Dasar 1', 'KD1.1', 'KD1'], 'Konsep Dasar 1.1'),
    (['2.3', 'Konsep Dasar 2.3', 'Konsep Dasar 2', 'KD2.3', 'KD2'], 'Konsep Dasar 2.3'),
]

username = 'auto_participant'
user, created = User.objects.get_or_create(username=username)
if created:
    user.set_password('autopass')
    user.save()

results = []

for pats, label in patterns:
    found = None
    for p in pats:
        q = SubTest.objects.filter(nama__icontains=p)
        if q.exists():
            found = q.first()
            break
    if not found:
        # also try paket name
        for p in pats:
            q = SubTest.objects.filter(paket__nama__icontains=p)
            if q.exists():
                found = q.first()
                break
    if not found:
        print(f"No SubTest found matching patterns for '{label}'")
        continue

    subtest = found
    soal_qs = subtest.soal.all()
    total = soal_qs.count()
    if total == 0:
        print(f"SubTest '{subtest}' has no questions")
        continue

    # create session
    sesi, screated = SesiUjian.objects.get_or_create(user=user, selesai=False)
    sesi.subtest = subtest
    sesi.waktu_mulai = datetime.now() - timedelta(minutes=5)
    sesi.save()

    # simulate answering all questions with the correct answer
    created_count = 0
    benar = 0
    for soal in soal_qs:
        JawabanPeserta.objects.update_or_create(
            user=user,
            soal=soal,
            defaults={
                'jawaban': soal.jawaban_benar[:1].upper()
            }
        )
        created_count += 1
        if soal.jawaban_benar and soal.jawaban_benar[:1].upper() == soal.jawaban_benar[:1].upper():
            benar += 1

    # mark session finished
    sesi.selesai = True
    sesi.save()

    skor = int((benar / total) * 100) if total else 0
    results.append({
        'label': str(subtest),
        'total': total,
        'benar': benar,
        'skor': skor,
    })

# print summary
print('Simulation complete for user:', username)
for r in results:
    print(f"SubTest: {r['label']} — Benar: {r['benar']}/{r['total']} — Skor: {r['skor']}")

# overall combined score (average)
if results:
    avg = int(sum(r['skor'] for r in results) / len(results))
    print('Average score across simulated subtests:', avg)
else:
    print('No subtests simulated')
