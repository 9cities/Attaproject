import os
import django
import random
import re
from collections import Counter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from ujian.models import PaketUjian, SubTest, Soal

def balance_all_subtests(start_pkg=11, end_pkg=20):
    print(f"=== UNIVERSAL KEY BALANCER: MEDIUM {start_pkg} TO {end_pkg} ===")
    
    target_letters = ['A', 'B', 'C', 'D', 'E']
    
    for p_num in range(start_pkg, end_pkg + 1):
        pname = f"Try Out Medium {p_num}"
        paket = PaketUjian.objects.filter(nama=pname).first()
        if not paket:
            continue
            
        subtests = SubTest.objects.filter(paket=paket).order_by('id')
        print(f"\n--- Processing {pname} ---")
        
        for st in subtests:
            soals = list(Soal.objects.filter(subtest=st).order_by('id'))
            n = len(soals)
            if n == 0:
                continue
                
            before = Counter(s.jawaban_benar.strip().upper() for s in soals)
            
            # Construct balanced target list
            target_keys = []
            for i in range(n):
                target_keys.append(target_letters[i % 5])
            
            random.seed(p_num * 100 + st.id)
            random.shuffle(target_keys)
            
            for i, s in enumerate(soals):
                old_key = s.jawaban_benar.strip().upper()
                new_key = target_keys[i]
                
                if old_key == new_key:
                    continue
                    
                opts = {
                    'A': s.pilihan_a,
                    'B': s.pilihan_b,
                    'C': s.pilihan_c,
                    'D': s.pilihan_d,
                    'E': s.pilihan_e
                }
                
                # Swap options
                correct_text = opts.get(old_key, '')
                target_text = opts.get(new_key, '')
                
                opts[new_key] = correct_text
                opts[old_key] = target_text
                
                s.pilihan_a = opts['A']
                s.pilihan_b = opts['B']
                s.pilihan_c = opts['C']
                s.pilihan_d = opts['D']
                s.pilihan_e = opts['E']
                s.jawaban_benar = new_key
                
                # Update explanation
                pemb = s.pembahasan
                if pemb:
                    pemb = re.sub(rf'(Jawaban\s*:\s*){old_key}\b', rf'\g<1>{new_key}', pemb, flags=re.IGNORECASE)
                    pemb = re.sub(rf'(Kunci\s*:\s*){old_key}\b', rf'\g<1>{new_key}', pemb, flags=re.IGNORECASE)
                    pemb = re.sub(rf'(Pilihan\s+){old_key}\b', rf'\g<1>{new_key}', pemb, flags=re.IGNORECASE)
                    pemb = re.sub(rf'(Opsi\s+){old_key}\b', rf'\g<1>{new_key}', pemb, flags=re.IGNORECASE)
                    s.pembahasan = pemb
                
                s.save()
                
            after = Counter(s.jawaban_benar.strip().upper() for s in Soal.objects.filter(subtest=st))
            print(f"  [{st.nama:<12}] Before: {dict(before)} -> After: {dict(after)}")

if __name__ == '__main__':
    balance_all_subtests(11, 20)
