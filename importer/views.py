from collections import defaultdict

from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .services.excel_import import ExcelImporter
from .services.validator import ExcelValidator
from .services.database_import import DatabaseImporter
from ujian.models import PaketUjian, SubTest, Soal


@login_required
def import_soal(request):
    if not request.user.is_staff:
        messages.error(request, "Akses khusus Administrator.")
        return redirect("home")

    if request.method == "POST":

        file = request.FILES.get("file")

        if not file:

            messages.error(
                request,
                "Silakan pilih file Excel."
            )

            return render(
                request,
                "importer/import_soal.html"
            )

        try:

            # ===========================
            # Baca Excel
            # ===========================

            importer = ExcelImporter(file)

            importer.open()

            headers = importer.headers()

            # ===========================
            # Validasi Header
            # ===========================

            validator = ExcelValidator(headers)

            missing = validator.validate()

            if missing:

                messages.error(
                    request,
                    "Kolom berikut belum ada : "
                    + ", ".join(missing)
                )

                return render(
                    request,
                    "importer/import_soal.html"
                )

            # ===========================
            # Import Database
            # ===========================

            replace_mode = request.POST.get("replace_mode") == "1"
            database = DatabaseImporter(
                importer.rows(),
                replace_mode=replace_mode
            )

            result = database.import_data()
            jumlah = result["jumlah"]
            errors = result["errors"]

            if jumlah:
                messages.success(
                    request,
                    f"{jumlah} soal berhasil diimport."
                )
            else:
                messages.warning(
                    request,
                    "Tidak ada soal berhasil diimport."
                )

            for error in errors:
                messages.error(
                    request,
                    error
                )

        except Exception as e:

            messages.error(
                request,
                str(e)
            )

    return render(
        request,
        "importer/import_soal.html"
    )


@login_required
def build_concept_subtests(request):
    if not request.user.is_staff:
        messages.error(request, "Akses khusus Administrator.")
        return redirect("home")

    if request.method != "POST":
        return redirect("import_soal")

    summary = []
    for kode, label in [("KD1", "Konsep Dasar 1"), ("KD2", "Konsep Dasar 2")]:
        soal_qs = Soal.objects.filter(kategori__iexact=kode, urutan__isnull=False).order_by("urutan", "id")
        if not soal_qs.exists():
            messages.warning(
                request,
                f"Tidak ditemukan soal berurutan untuk kategori {label} ({kode}). Pastikan field urutan sudah terisi."
            )
            continue

        soal_by_urutan = defaultdict(list)
        for soal in soal_qs:
            soal_by_urutan[soal.urutan].append(soal)

        for urutan in sorted(soal_by_urutan):
            paket_nama = f"{label} {urutan}"
            sub_nama = f"{urutan}"
            paket, _ = PaketUjian.objects.get_or_create(nama=paket_nama)
            subtest, _ = SubTest.objects.get_or_create(paket=paket, nama=sub_nama)

            existing_texts = set(subtest.soal.values_list("pertanyaan", flat=True))
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

            summary.append(
                f"{label} {urutan}: paket '{paket_nama}', subtest '{sub_nama}' dibuat {created}, dilewati {skipped}."
            )

    if summary:
        for msg in summary:
            messages.success(request, msg)
    else:
        messages.warning(request, "Tidak ada subtest konsep yang dibangun karena data urutan belum tersedia.")

    return redirect("import_soal")