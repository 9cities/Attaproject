import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from ujian.models import PaketUjian, SubTest

User = get_user_model()
user, _ = User.objects.get_or_create(username='tmp_tester_2')
user.set_password('pass')
user.save()

client = Client()
client.force_login(user)

paket = PaketUjian.objects.filter(nama='Konsep Dasar 1 1').first()
if not paket:
    raise SystemExit('paket not found')
sub = paket.subtests.filter(nama='PU').first()
if not sub:
    raise SystemExit('sub PU not found')

start_resp = client.get(f'/soal/{paket.nama}/start/{sub.id}/', HTTP_HOST='localhost')
print('start status', start_resp.status_code)
print('start location', start_resp.get('Location'))

ids = list(sub.soal.order_by('id').values_list('id', flat=True))
print('PU ids', ids)
last_id = ids[-1]
print('last id', last_id)

resp = client.post(f'/soal/{last_id}/', {'jawaban': 'A', 'action': 'next'}, HTTP_HOST='localhost')
print('status', resp.status_code)
print('location', resp.get('Location'))
print('content', resp.content[:200])
