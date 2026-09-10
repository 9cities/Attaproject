import os
import sys
import django
from collections import defaultdict

# setup
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from ujian.models import PaketUjian, SubTest, Soal

CATEGORY_LABEL = {
    'KD1': 'Konsep Dasar 1',
    'KD2': 'Konsep Dasar 2',
    'EASY': 'TO Easy',
    'MEDIUM': 'TO Medium',
    'HARD': 'TO hard',
}

CATEGORY_LOOKUP = {
    'konsep dasar 1': 'KD1',
    'konsep dasar 2': 'KD2',
    'try out easy': 'EASY',
    'to easy': 'EASY',
    'easy': 'EASY',
    'try out medium': 'MEDIUM',
    'to medium': 'MEDIUM',
    'medium': 'MEDIUM',
    'try out hard': 'HARD',
    'to hard': 'HARD',
    'hard': 'HARD',
}

TARGET_CATEGORIES = ['KD1', 'KD2']


def normalize_category(raw):
    if raw is None:
        return None
    value = str(raw).strip()
    if not value:
        return None
    lookup = CATEGORY_LOOKUP.get(value.lower())
    if lookup:
        return lookup
    if value.upper() in CATEGORY_LABEL:
        return value.upper()
    return value.upper()


def main():
    print('Membangun subtest konsep secara otomatis berdasarkan urutan...')

    summary = defaultdict(int)
    for kode in TARGET_CATEGORIES:
        label = CATEGORY_LABEL.get(kode, kode)
        soal_by_urutan = defaultdict(list)
        source_qs = Soal.objects.filter(kategori__iexact=kode, urutan__isnull=False).order_by('urutan', 'id')
        if not source_qs.exists():
            print(f"Tidak ditemukan soal berurutan untuk kategori {label} ({kode}).")
            continue

        for soal in source_qs:
            soal_by_urutan[soal.urutan].append(soal)

        for urutan in sorted(soal_by_urutan):
            paket_name = f"{label} {urutan}"
            sub_name = f"{urutan}"
            paket, _ = PaketUjian.objects.get_or_create(nama=paket_name)
            subtest, _ = SubTest.objects.get_or_create(paket=paket, nama=sub_name)

            existing_texts = set(
                subtest.soal.values_list('pertanyaan', flat=True)
            )
            created = 0
            skipped = 0
            for soal in soal_by_urutan[urutan]:
                if soal.pertanyaan.strip() in existing_texts:
                    skipped += 1
                    continue
                Soal.objects.create(
                    kategori=soal.kategori,
                    subtest=subtest,
                    pertanyaan=soal.pertanyaan,
                    pilihan_a=soal.pilihan_a,
                    pilihan_b=soal.pilihan_b,
                    pilihan_c=soal.pilihan_c,
                    pilihan_d=soal.pilihan_d,
                    pilihan_e=soal.pilihan_e,
                    jawaban_benar=soal.jawaban_benar,
                    pembahasan=soal.pembahasan,
                    urutan=soal.urutan,
                )
                created += 1

            total_now = subtest.soal.count()
            print(
                f"{label} {urutan}: paket '{paket_name}', subtest '{sub_name}' -> "
                f"created {created}, skipped {skipped}, total in subtest {total_now}"
            )
            summary[kode] += created

    print('\nRingkasan:')
    for kode, created in summary.items():
        label = CATEGORY_LABEL.get(kode, kode)
        print(f"  {label} ({kode}): total baru = {created}")


if __name__ == '__main__':
    main()
