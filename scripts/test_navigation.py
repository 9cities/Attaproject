import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from ujian.models import PaketUjian, SubTest, Soal

User = get_user_model()

c = Client()
user, created = User.objects.get_or_create(username='tmp_tester')
if created:
    user.set_password('pass')
    user.save()

# force login
c.force_login(user)

paket = PaketUjian.objects.filter(nama='Konsep Dasar 1 1').first()
if not paket:
    print('paket not found')
    sys.exit(1)

sub = paket.subtests.filter(nama='PU').first()
if not sub:
    print('sub PU not found')
    sys.exit(1)

# start subtest
resp = c.get(f"/soal/{paket.nama}/start/{sub.id}/", HTTP_HOST='localhost')
print('start status', resp.status_code)

# get first soal ids
qs = list(sub.soal.order_by('id'))
ids = [s.id for s in qs]
print('ids', ids)
if len(ids) < 10:
    print('not enough questions')
    sys.exit(1)

# simulate navigating to soal 9
soal9 = ids[8]
resp = c.get(f"/soal/{soal9}/", HTTP_HOST='localhost')
print('get soal9 status', resp.status_code)

# post answer with action next
resp = c.post(f"/soal/{soal9}/", {'jawaban':'A','action':'next'}, HTTP_HOST='localhost')
print('post next status', resp.status_code)
if resp.status_code in (301,302):
    print('redirected to', resp['Location'])
    resp2 = c.get(resp['Location'], HTTP_HOST='localhost')
    print('after redirect url', resp2.request['PATH_INFO'])
else:
    print('no redirect, status', resp.status_code)

# show which soal id displayed
if b'Soal' in resp2.content:
    print('page contains Soal')

print('Test complete')
