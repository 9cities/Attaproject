import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from ujian.models import HasilPaketUjian, JawabanPeserta, SubTest

hasils = HasilPaketUjian.objects.all()
fixed = 0

for hasil in hasils:
    if not hasil.skor_json:
        continue
    
    # We need to re-evaluate the scores for this paket
    paket_nama = hasil.paket_nama
    user = hasil.user
    
    jawaban_paket = list(JawabanPeserta.objects.filter(user=user, soal__subtest__paket__nama=paket_nama).select_related('soal__subtest', 'soal__subtest__paket'))
    
    # Get the actual paket object to list all its subtests
    paket = None
    if jawaban_paket and jawaban_paket[0].soal and jawaban_paket[0].soal.subtest and jawaban_paket[0].soal.subtest.paket:
        paket = jawaban_paket[0].soal.subtest.paket
    else:
        from ujian.models import PaketUjian
        paket = PaketUjian.objects.filter(nama=paket_nama).first()
        
    if not paket:
        continue
        
    subtest_map = {}
    for j in jawaban_paket:
        st_id = j.soal.subtest_id if j.soal else j.subtest_id_snapshot
        if not st_id: continue
        if st_id not in subtest_map: subtest_map[st_id] = []
        subtest_map[st_id].append(j)
        
    sts = list(paket.subtests.all())
    if not sts:
        continue
        
    tot_skor = 0
    tot_sub = 0
    scores_dict = {}
    
    # Preserve cheat flag if exists
    if 'cheat_flag' in hasil.skor_json:
        scores_dict['cheat_flag'] = hasil.skor_json['cheat_flag']
        
    for st in sts:
        js = subtest_map.get(st.id, [])
        total_soal_st = st.soal.count()
        jumlah_tampil = st.get_jumlah_soal_tampil()
        if jumlah_tampil > 0 and jumlah_tampil < total_soal_st:
            ts = jumlah_tampil
        else:
            ts = total_soal_st
            
        if ts == 0: continue
            
        bn = sum(1 for j in js if (j.soal and j.jawaban == j.soal.jawaban_benar) or (not j.soal and j.is_benar_snapshot))
        sc = round((bn/ts)*100, 1)
        scores_dict[st.nama.replace(" ", "_")] = sc
        tot_skor += sc
        tot_sub += 1
        
    na = round(tot_skor/tot_sub, 1) if tot_sub > 0 else 0
    
    # If the dictionary is different, update it
    if hasil.skor_json != scores_dict or hasil.nilai_akhir != na:
        hasil.skor_json = scores_dict
        hasil.nilai_akhir = na
        hasil.save(update_fields=['skor_json', 'nilai_akhir'])
        fixed += 1

print(f"Fixed {fixed} HasilPaketUjian records.")
