import os
import sys
import django

# Ensure project root is on sys.path so Django settings module can be imported
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from ujian.models import Soal
from django.db.models import Q

qs = Soal.objects.filter(Q(pertanyaan__isnull=True) | Q(pertanyaan__exact=''))
count = qs.count()
print('Found empty questions:', count)
if count:
    qs.delete()
    print('Deleted', count, 'empty question(s)')
else:
    print('Nothing to delete')
