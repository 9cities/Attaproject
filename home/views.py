from django.shortcuts import render
from ujian.models import Soal


def home(request):
    if 'active_kategori' in request.session:
        request.session.pop('active_kategori', None)
    jumlah_soal = Soal.objects.count()
    return render(request, "home/index.html", {
        "jumlah_soal": jumlah_soal,
    })