import os
import django
import re
from collections import Counter, defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from ujian.models import PaketUjian, SubTest, Soal

def run_qc_inspection():
    print("=" * 80)
    print("QC AUDIT INSPECTION REPORT: TRY OUT MEDIUM 1 - 20")
    print("=" * 80)

    packages = PaketUjian.objects.filter(nama__startswith="Try Out Medium").order_by('id')
    
    total_packages = packages.count()
    print(f"Total 'Try Out Medium' packages found in DB: {total_packages}\n")

    issues_found = []
    subtest_stats = defaultdict(list)
    key_distribution_global = Counter()

    for paket in packages:
        subtests = SubTest.objects.filter(paket=paket).order_by('id')
        paket_soal_count = 0
        
        # Check subtests count
        if subtests.count() != 8:
            issues_found.append(f"[{paket.nama}] WARNING: Has {subtests.count()} subtests instead of 8.")

        for st in subtests:
            soals = Soal.objects.filter(subtest=st).order_by('id')
            st_count = soals.count()
            paket_soal_count += st_count
            subtest_stats[paket.nama].append((st.nama, st_count))

            # Track duplicate questions within subtest
            seen_questions = set()
            st_keys = Counter()

            for s in soals:
                st_keys[s.jawaban_benar.strip().upper()] += 1
                key_distribution_global[s.jawaban_benar.strip().upper()] += 1

                # 1. Check empty / missing fields
                q_text = s.pertanyaan.strip() if s.pertanyaan else ""
                pa = s.pilihan_a.strip() if s.pilihan_a else ""
                pb = s.pilihan_b.strip() if s.pilihan_b else ""
                pc = s.pilihan_c.strip() if s.pilihan_c else ""
                pd = s.pilihan_d.strip() if s.pilihan_d else ""
                pe = s.pilihan_e.strip() if s.pilihan_e else ""
                ans = s.jawaban_benar.strip().upper() if s.jawaban_benar else ""
                pemb = s.pembahasan.strip() if s.pembahasan else ""

                if not q_text:
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Pertanyaan KOSONG!")
                elif len(q_text) < 15:
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Pertanyaan terlalu pendek ({len(q_text)} chars): '{q_text}'")

                if not pa or not pb or not pc or not pd:
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Pilihan A/B/C/D ada yang kosong!")
                
                if not pe:
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Pilihan E kosong!")

                # 2. Check duplicate options
                opts = [pa, pb, pc, pd, pe]
                non_empty_opts = [o for o in opts if o]
                if len(non_empty_opts) != len(set(non_empty_opts)):
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Pilihan jawaban ada yang kembar/duplikat!")

                # 3. Check invalid answer key
                if ans not in ['A', 'B', 'C', 'D', 'E']:
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Kunci jawaban tidak valid: '{s.jawaban_benar}'")

                # 4. Check explanation quality
                if not pemb:
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Pembahasan KOSONG!")
                elif len(pemb) < 10 or pemb.lower() in ["pembahasan: a", "pembahasan a", "cukup jelas", "-"]:
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Pembahasan terlalu singkat/placeholder: '{pemb}'")

                # 5. Check raw json leaking into pertanyaan
                if q_text.startswith('[{"') or q_text.startswith('{"'):
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Pertanyaan berupa raw JSON bocor!")

                # 6. Check duplicate questions in same subtest
                clean_q = re.sub(r'\s+', ' ', q_text).lower()
                if clean_q in seen_questions:
                    issues_found.append(f"[{paket.nama} -> {st.nama} -> Soal #{s.id}] Pertanyaan DUPLIKAT di subtes yang sama!")
                seen_questions.add(clean_q)

            # Check for extreme answer key imbalance in subtest (e.g. all 22 questions have answer A)
            if len(st_keys) == 1 and st_count > 5:
                issues_found.append(f"[{paket.nama} -> {st.nama}] ANOMALI KUNCI: 100% kunci bernilai '{list(st_keys.keys())[0]}' ({st_count} soal)!")

    # Summary Output
    print("--- 1. RINGKASAN STRUKTUR PAKET & SUBTES ---")
    for pkg_name, st_list in subtest_stats.items():
        total_soal = sum(cnt for _, cnt in st_list)
        st_desc = ", ".join([f"{n}: {c}" for n, c in st_list])
        print(f"{pkg_name:<20} | Total Soal: {total_soal:<4} | {st_desc}")

    print("\n--- 2. DISTRIBUSI KUNCI JAWABAN GLOBAL ---")
    total_keys = sum(key_distribution_global.values())
    for k in sorted(key_distribution_global.keys()):
        pct = (key_distribution_global[k] / total_keys) * 100 if total_keys else 0
        print(f"Kunci {k}: {key_distribution_global[k]:<5} ({pct:.1f}%)")

    print("\n--- 3. DAFTAR TEMUAN / ANOMALI QC ---")
    if not issues_found:
        print(">> SEMPURNA! Tidak ditemukan anomali format, pilihan kosong, kunci invalid, atau soal duplikat!")
    else:
        print(f">> Ditemukan {len(issues_found)} catatan / temuan QC:")
        for idx, iss in enumerate(issues_found, 1):
            print(f"  {idx}. {iss}")

if __name__ == '__main__':
    run_qc_inspection()
