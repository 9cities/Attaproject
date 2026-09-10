from django.db import transaction

from ujian.models import PaketUjian, SubTest, Soal


class DatabaseImporter:

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
        "pembahasan": "pembahasan",
        "penjelasan": "pembahasan",
        "sub": "sub",
        "subtest": "sub",
        "sub test": "sub",
        "sub_test": "sub",
        "paket": "paket",
        "paket ujian": "paket",
        "paket_ujian": "paket",
        "urutan": "urutan",
        "no": "no",
        "id": "id_soal",
        "id soal": "id_soal",
        "id_soal": "id_soal",
    }

    CATEGORY_MAP = {
        "konsep dasar 1": "KD1",
        "konsep dasar 2": "KD2",
        "try out easy": "EASY",
        "try out medium": "MEDIUM",
        "try out hard": "HARD",
    }

    VALID_ANSWERS = {"A", "B", "C", "D", "E"}

    def __init__(self, rows, replace_mode=False):
        self.rows = list(rows)
        self.replace_mode = replace_mode
        self.cleared_subtests = set()

    def _parse_urutan(self, value):
        if value is None:
            return None
        if isinstance(value, int):
            return value
        try:
            return int(str(value).strip())
        except (ValueError, TypeError):
            return None

    def _normalize_header(self, header):
        if header is None:
            return None
        return self.HEADER_ALIASES.get(str(header).strip().lower())

    def _normalize_row(self, row):
        normalized = {}
        for header, value in row.items():
            key = self._normalize_header(header)
            if key:
                normalized[key] = value
        return normalized

    def _normalize_category(self, raw_category):
        if raw_category is None:
            return "KD1"

        raw = str(raw_category).strip()
        if not raw:
            return "KD1"

        raw_upper = raw.upper()
        if raw_upper in {"KD1", "KD2", "EASY", "MEDIUM", "HARD"}:
            return raw_upper

        return self.CATEGORY_MAP.get(raw.lower(), raw_upper)

    def _is_blank_row(self, data):
        return not any(
            str(value).strip()
            for value in data.values()
            if value is not None
        )

    def _validate_row(self, data, row_number):
        errors = []
        pertanyaan = str(data.get("pertanyaan") or "").strip()
        jawaban = str(data.get("jawaban") or "").strip().upper()

        if not pertanyaan:
            errors.append(f"Baris {row_number}: kolom Pertanyaan/Soal kosong.")

        if not jawaban:
            errors.append(f"Baris {row_number}: kolom Jawaban kosong.")
        elif jawaban[0] not in self.VALID_ANSWERS:
            errors.append(
                f"Baris {row_number}: Jawaban harus salah satu dari A, B, C, D, E. Ditemukan '{jawaban}'."
            )

        return errors

    @transaction.atomic
    def import_data(self):
        jumlah = 0
        errors = []
        row_number = 1

        for row in self.rows:
            row_number += 1
            data = self._normalize_row(row)

            if self._is_blank_row(data):
                continue

            row_errors = self._validate_row(data, row_number)
            if row_errors:
                errors.extend(row_errors)
                continue

            kategori = self._normalize_category(data.get("kategori"))
            pertanyaan = str(data.get("pertanyaan") or "").strip()
            pilihan_a = str(data.get("a") or "").strip()
            pilihan_b = str(data.get("b") or "").strip()
            pilihan_c = str(data.get("c") or "").strip()
            pilihan_d = str(data.get("d") or "").strip()
            pilihan_e = str(data.get("e") or "").strip()
            jawaban_benar = str(data.get("jawaban") or "").strip().upper()[0]
            pembahasan = str(data.get("pembahasan") or "").strip()
            sub_name = str(data.get("sub") or "").strip()
            paket_raw = str(data.get("paket") or "").strip()
            urutan = self._parse_urutan(data.get("urutan"))
            id_soal = data.get("id_soal")

            # Penentuan nama paket ujian secara presisi
            if paket_raw:
                paket_nama = paket_raw
            elif urutan and kategori in ("KD1", "KD2"):
                cat_label = "Konsep Dasar 1" if kategori == "KD1" else "Konsep Dasar 2"
                paket_nama = f"{cat_label} {urutan}"
            else:
                paket_nama = f"Paket {kategori}"

            paket, _ = PaketUjian.objects.get_or_create(
                nama=paket_nama
            )

            subtest = None
            if sub_name:
                subtest, _ = SubTest.objects.get_or_create(
                    paket=paket,
                    nama=sub_name
                )

            # Jika Mode Replace/Timpa diaktifkan dan subtest belum dibersihkan
            if self.replace_mode and subtest and (subtest.id not in self.cleared_subtests):
                # Jika file Excel memuat ID Soal, jangan hapus subtest agar riwayat ujian peserta 100% AMAN (In-Place Update)
                has_id_col = any(
                    "id_soal" in self._normalize_row(r) or "id" in self._normalize_row(r)
                    for r in self.rows[:5]
                )
                if not has_id_col:
                    subtest.soal.all().delete()
                self.cleared_subtests.add(subtest.id)

            # Cek pencarian soal (berdasarkan ID Soal atau urutan atau pertanyaan)
            soal_obj = None
            if id_soal:
                try:
                    soal_obj = Soal.objects.filter(id=int(id_soal)).first()
                except (ValueError, TypeError):
                    pass

            if not soal_obj and subtest and urutan:
                soal_obj = Soal.objects.filter(subtest=subtest, urutan=urutan).first()

            if not soal_obj and subtest and not self.replace_mode:
                soal_obj = Soal.objects.filter(subtest=subtest, pertanyaan=pertanyaan).first()

            if soal_obj:
                # Update soal yang sudah ada
                soal_obj.kategori = kategori
                if subtest:
                    soal_obj.subtest = subtest
                soal_obj.pertanyaan = pertanyaan
                soal_obj.pilihan_a = pilihan_a
                soal_obj.pilihan_b = pilihan_b
                soal_obj.pilihan_c = pilihan_c
                soal_obj.pilihan_d = pilihan_d
                soal_obj.pilihan_e = pilihan_e
                soal_obj.jawaban_benar = jawaban_benar
                soal_obj.pembahasan = pembahasan
                soal_obj.urutan = urutan
                soal_obj.save()
            else:
                # Tambahkan soal baru
                Soal.objects.create(
                    kategori=kategori,
                    subtest=subtest,
                    pertanyaan=pertanyaan,
                    pilihan_a=pilihan_a,
                    pilihan_b=pilihan_b,
                    pilihan_c=pilihan_c,
                    pilihan_d=pilihan_d,
                    pilihan_e=pilihan_e,
                    jawaban_benar=jawaban_benar,
                    pembahasan=pembahasan,
                    urutan=urutan,
                )

            jumlah += 1

        return {
            "jumlah": jumlah,
            "errors": errors,
        }
