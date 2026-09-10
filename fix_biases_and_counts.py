import os
import django
import random
import re
from collections import Counter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from ujian.models import PaketUjian, SubTest, Soal

def rebalance_subtest_keys(paket_nama, subtest_nama):
    st = SubTest.objects.filter(paket__nama=paket_nama, nama=subtest_nama).first()
    if not st:
        print(f"Subtest {subtest_nama} in {paket_nama} not found!")
        return

    soals = list(Soal.objects.filter(subtest=st).order_by('id'))
    n = len(soals)
    if n == 0:
        return

    print(f"\n--- Rebalancing {paket_nama} -> {subtest_nama} ({n} soals) ---")
    before_keys = Counter(s.jawaban_benar.strip().upper() for s in soals)
    print(f"Before keys: {dict(before_keys)}")

    # Target balanced keys
    target_letters = ['A', 'B', 'C', 'D', 'E']
    # Create a balanced target list
    target_keys = []
    for i in range(n):
        target_keys.append(target_letters[i % 5])
    random.seed(42)  # reproducible
    random.shuffle(target_keys)

    for i, s in enumerate(soals):
        old_key = s.jawaban_benar.strip().upper()
        new_key = target_keys[i]

        if old_key == new_key:
            continue

        # Get existing options mapping
        opts = {
            'A': s.pilihan_a,
            'B': s.pilihan_b,
            'C': s.pilihan_c,
            'D': s.pilihan_d,
            'E': s.pilihan_e
        }
        
        # We want the text of old_key to become the text of new_key
        # We can swap old_key and new_key
        correct_text = opts[old_key]
        target_text = opts[new_key]

        opts[new_key] = correct_text
        opts[old_key] = target_text

        s.pilihan_a = opts['A']
        s.pilihan_b = opts['B']
        s.pilihan_c = opts['C']
        s.pilihan_d = opts['D']
        s.pilihan_e = opts['E']
        s.jawaban_benar = new_key

        # Update explanation if it mentions old option letter at start or in "Jawaban: X"
        pemb = s.pembahasan
        if pemb:
            # Replace occurrences of "Jawaban: X" or "kunci: X"
            pemb = re.sub(rf'(Jawaban\s*:\s*){old_key}\b', rf'\g<1>{new_key}', pemb, flags=re.IGNORECASE)
            pemb = re.sub(rf'(Kunci\s*:\s*){old_key}\b', rf'\g<1>{new_key}', pemb, flags=re.IGNORECASE)
            pemb = re.sub(rf'(Pilihan\s+){old_key}\b', rf'\g<1>{new_key}', pemb, flags=re.IGNORECASE)
            pemb = re.sub(rf'(Opsi\s+){old_key}\b', rf'\g<1>{new_key}', pemb, flags=re.IGNORECASE)
            s.pembahasan = pemb

        s.save()

    after_keys = Counter(s.jawaban_benar.strip().upper() for s in Soal.objects.filter(subtest=st))
    print(f"After keys: {dict(after_keys)}")

def fix_medium_12_pm():
    st = SubTest.objects.filter(paket__nama="Try Out Medium 12", nama="PM").first()
    if not st:
        return
    soals = list(Soal.objects.filter(subtest=st).order_by('id'))
    if len(soals) > 22:
        print(f"\n--- Trimming Try Out Medium 12 -> PM from {len(soals)} to 22 ---")
        to_delete = soals[22:]
        for s in to_delete:
            s.delete()
        print(f"Remaining soals in Try Out Medium 12 -> PM: {Soal.objects.filter(subtest=st).count()}")

if __name__ == '__main__':
    # 1. Fix PM 18
    rebalance_subtest_keys("Try Out Medium 18", "PM")
    
    # 2. Fix Medium 16 subtests with bias
    rebalance_subtest_keys("Try Out Medium 16", "LBI soshum")
    rebalance_subtest_keys("Try Out Medium 16", "LBI saintek")
    rebalance_subtest_keys("Try Out Medium 16", "PM")

    # 3. Fix Medium 13 LBE
    rebalance_subtest_keys("Try Out Medium 13", "LBE")

    # 4. Standardize Medium 12 PM to 22 questions
    fix_medium_12_pm()

    print("\n[ALL BIAS & TRIMMING FIXES COMPLETED SUCCESSFULLY!]")
