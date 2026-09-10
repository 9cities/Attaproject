import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from pathlib import Path
from importer.services.excel_import import ExcelImporter
from ujian.models import PaketUjian, SubTest, Soal


HEADER_ALIASES = {
    "kategori": "kategori",
    "pertanyaan": "pertanyaan",
    "soal": "pertanyaan",
    "a": "a",
    "b": "b",
    "c": "c",
    "d": "d",
    "e": "e",
    "jawaban": "jawaban",
    "jawaban_benar": "jawaban",
    "pembahasan": "pembahasan",
    "penjelasan": "pembahasan",
    "sub": "sub",
    "sub_test": "sub",
    "subtest": "sub",
    "urutan": "urutan",
    "timer_menit": "timer_menit",
}

CATEGORY_MAP = {
    "konsep dasar 1": "KD1",
    "konsep dasar 2": "KD2",
    "try out easy": "EASY",
    "try out medium": "MEDIUM",
    "try out hard": "HARD",
}

VALID_ANSWERS = {"A", "B", "C", "D", "E"}


def _normalize_header(h):
    if h is None:
        return None
    return HEADER_ALIASES.get(str(h).strip().lower())


def _normalize_category(raw):
    if not raw:
        return "KD1"
    raw = str(raw).strip()
    if not raw:
        return "KD1"
    raw_upper = raw.upper()
    if raw_upper in {"KD1", "KD2", "EASY", "MEDIUM", "HARD"}:
        return raw_upper
    return CATEGORY_MAP.get(raw.lower(), raw_upper)


def _is_blank_row(data):
    return not any(
        str(v).strip()
        for v in data.values()
        if v is not None
    )


class Command(BaseCommand):
    help = "Import bank soal (CSV or XLSX) in chunks with bulk_create"

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Path to CSV or XLSX file")
        parser.add_argument("--batch-size", type=int, default=500, help="bulk_create batch size")

    def handle(self, *args, **options):
        file_path = options["file"]
        batch_size = options["batch_size"]

        p = Path(file_path)
        if not p.exists():
            raise CommandError(f"File not found: {file_path}")

        # generator of dict rows
        def row_generator_csv(fp):
            with open(fp, newline='', encoding='utf-8') as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    yield row

        def row_generator_xlsx(fp):
            with open(fp, 'rb') as fh:
                importer = ExcelImporter(fh)
                importer.open()
                for r in importer.rows():
                    yield r

        ext = p.suffix.lower()
        if ext in {'.csv'}:
            rows = row_generator_csv(str(p))
        elif ext in {'.xlsx', '.xlsm', '.xltx'}:
            rows = row_generator_xlsx(str(p))
        else:
            raise CommandError("Unsupported file type. Use .csv or .xlsx")

        created_total = 0
        errors = []

        paket_cache = {}
        sub_cache = {}

        batch = []

        def flush_batch():
            nonlocal batch, created_total
            if not batch:
                return
            with transaction.atomic():
                Soal.objects.bulk_create(batch, batch_size=batch_size)
            created_total += len(batch)
            self.stdout.write(f"Inserted chunk: {len(batch)} (total {created_total})")
            batch = []

        row_num = 1
        for raw in rows:
            row_num += 1
            # normalize headers
            data = {}
            for k, v in raw.items():
                nk = _normalize_header(k)
                if nk:
                    data[nk] = v

            if _is_blank_row(data):
                continue

            pertanyaan = str(data.get('pertanyaan') or '').strip()
            jawaban = str(data.get('jawaban') or '').strip().upper()
            if not pertanyaan:
                errors.append(f"Row {row_num}: empty question")
                continue
            if not jawaban or jawaban[0] not in VALID_ANSWERS:
                errors.append(f"Row {row_num}: invalid answer '{jawaban}'")
                continue

            kategori = _normalize_category(data.get('kategori'))
            paket_nama = str(data.get('paket') or data.get('paket_ujian') or kategori).strip() or kategori
            sub_name = str(data.get('sub') or '').strip()
            timer = data.get('timer_menit') or data.get('timer')
            urutan = None
            raw_urutan = data.get('urutan')
            if raw_urutan is not None:
                try:
                    urutan = int(raw_urutan)
                except (ValueError, TypeError):
                    urutan = None

            # get or create paket
            paket = paket_cache.get(paket_nama)
            if paket is None:
                paket, _ = PaketUjian.objects.get_or_create(nama=paket_nama)
                paket_cache[paket_nama] = paket

            sub = None
            if sub_name:
                sub_key = f"{paket.id}::{sub_name}"
                sub = sub_cache.get(sub_key)
                if sub is None:
                    sub, _ = SubTest.objects.get_or_create(paket=paket, nama=sub_name)
                    # set timer if provided
                    try:
                        if timer:
                            sub.timer_menit = int(timer)
                            sub.save()
                        elif sub.timer_menit == 0:
                            sub.timer_menit = 10
                            sub.save()
                    except Exception:
                        pass
                    sub_cache[sub_key] = sub

            soal = Soal(
                kategori=kategori,
                subtest=sub,
                pertanyaan=pertanyaan,
                pilihan_a=str(data.get('a') or '').strip(),
                pilihan_b=str(data.get('b') or '').strip(),
                pilihan_c=str(data.get('c') or '').strip(),
                pilihan_d=str(data.get('d') or '').strip(),
                pilihan_e=str(data.get('e') or '').strip(),
                jawaban_benar=jawaban[0],
                pembahasan=str(data.get('pembahasan') or '').strip(),
                urutan=urutan,
            )

            batch.append(soal)
            if len(batch) >= batch_size:
                flush_batch()

        # flush remaining
        flush_batch()

        self.stdout.write(self.style.SUCCESS(f"Import finished. Inserted: {created_total}. Errors: {len(errors)}"))
        if errors:
            for e in errors[:50]:
                self.stdout.write(self.style.WARNING(e))
