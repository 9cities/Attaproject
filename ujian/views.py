from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Q

from .models import Soal, JawabanPeserta, SesiUjian, PaketUjian, SubTest, SoalSesi, KategoriSetting, SistemSetting
import random
import csv
import io
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from django.contrib import messages
import re


CATEGORY_MAP = {
    "konsep dasar 1": "KD1",
    "konsep dasar 2": "KD2",
    "try out easy": "EASY",
    "try out medium": "MEDIUM",
    "try out hard": "HARD",
}


def normalize_category(raw_category):
    if not raw_category:
        return "KD1"

    raw = str(raw_category).strip()
    if not raw:
        return "KD1"

    raw_upper = raw.upper()
    if raw_upper in {"KD1", "KD2", "EASY", "MEDIUM", "HARD"}:
        return raw_upper

    return CATEGORY_MAP.get(raw.lower(), raw_upper)

def get_balanced_random_soal_ids(subtest, jumlah_tampil):
    """
    Mengambil ID soal dari subtest sejumlah `jumlah_tampil` SECARA BERURUTAN (TIDAK ACAK).
    Diubah atas permintaan untuk mempertahankan urutan soal secara permanen.
    """
    # Ambil soal berdasarkan urutan aslinya
    semua_soal = subtest.soal.order_by('urutan', 'id')
    
    if jumlah_tampil > 0 and jumlah_tampil < semua_soal.count():
        semua_soal = semua_soal[:jumlah_tampil]
        
    return list(semua_soal.values_list('id', flat=True))


KATEGORI_LABEL = {
    "KD1": "Konsep Dasar 1",
    "KD2": "Konsep Dasar 2",
    "EASY": "Try Out Easy",
    "MEDIUM": "Try Out Medium",
    "HARD": "Try Out Hard",
}

# Preferred ordering of subtest names when progressing through a package
SUBTEST_ORDER = [
    'PU', 'PPU', 'PBM', 'PK', 'LBI saintek', 'LBI soshum', 'LBE', 'PM'
]


# ==========================================================
# HALAMAN DEPAN
# ==========================================================

def home(request):
    return render(request, "home/index.html")



# ==========================================================
# DAFTAR SOAL
# ==========================================================


@login_required
def daftar_soal(request, kategori=None):
    if kategori:
        kategori_norm = normalize_category(kategori)

        if kategori_norm in {"KD1", "KD2", "EASY", "MEDIUM", "HARD"}:
            label = KATEGORI_LABEL.get(kategori_norm, kategori_norm)
            prefix_num = "1" if kategori_norm == "KD1" else "2"

            # Map package names that have questions in DB
            existing_map = {}
            if kategori_norm in {"KD1", "KD2"}:
                filter_str = f"Konsep Dasar {prefix_num}"
            else:
                filter_str = f"Try Out {kategori_norm.capitalize()}"

            for p in PaketUjian.objects.filter(nama__icontains=filter_str):
                if Soal.objects.filter(subtest__paket=p).exists():
                    existing_map[p.nama.lower().strip()] = p.nama
                    # Also normalize space <-> dot
                    space_variant = p.nama.lower().replace('.', ' ').strip()
                    dot_variant = p.nama.lower().replace(' ', '.').strip()
                    existing_map[space_variant] = p.nama
                    existing_map[dot_variant] = p.nama

            paket_selesai = set(SesiUjian.objects.filter(user=request.user, selesai=True).exclude(subtest__paket__isnull=True).values_list('subtest__paket__nama', flat=True))
            paket_selesai_lower = {p.lower().strip() for p in paket_selesai}
            packages = []
            if kategori_norm == "KD1": max_paket = 51
            elif kategori_norm == "KD2": max_paket = 52
            elif kategori_norm == "EASY": max_paket = 21
            elif kategori_norm == "MEDIUM": max_paket = 21
            elif kategori_norm == "HARD": max_paket = 41
            else: max_paket = 2

            for i in range(1, max_paket):
                if kategori_norm in {"KD1", "KD2"}:
                    dot_name = f"Konsep Dasar {prefix_num}.{i}"
                    space_name = f"Konsep Dasar {prefix_num} {i}"
                else:
                    dot_name = f"Try Out {kategori_norm.capitalize()} {i}"
                    space_name = dot_name

                real_nama = (
                    existing_map.get(dot_name.lower()) or
                    existing_map.get(space_name.lower()) or
                    dot_name
                )
                is_available = (dot_name.lower() in existing_map) or (space_name.lower() in existing_map)
                is_finished = (real_nama.lower().strip() in paket_selesai_lower)

                packages.append({
                    "nama": real_nama,
                    "exists": is_available,
                    "finished": is_finished,
                    "url": reverse('daftar_soal_kategori', args=[real_nama]),
                })

            return render(request, "ujian/concept_package_list.html", {
                "kategori_label": label,
                "packages": packages,
            })

        paket = PaketUjian.objects.filter(nama__iexact=kategori).first()
        if not paket:
            paket = PaketUjian.objects.filter(nama__iexact=kategori_norm).first()

        if paket:
            subtests_qs = paket.subtests.all()
            # hide subtests that look like numeric package identifiers (e.g. '1.1', '2.3')
            subtests = [s for s in subtests_qs if not re.match(r'^\d+(?:\.\d+)?$', s.nama.strip())]
            
            total_soal = sum(s.soal.count() for s in subtests)
            total_waktu = sum(s.get_timer_menit() for s in subtests)
            subtest_names = ", ".join(s.nama for s in subtests)

            return render(request, "ujian/subtest_list.html", {
                "paket": paket,
                "subtests": subtests,
                "total_soal": total_soal,
                "total_waktu": total_waktu,
                "subtest_names": subtest_names,
            })

        first_soal = Soal.objects.filter(kategori__iexact=kategori_norm).order_by('id').first()
        if first_soal:
            return redirect("tampil_soal_kategori", kategori=kategori_norm, nomor=first_soal.id)

        return redirect("home")

    first_soal = Soal.objects.order_by('id').first()
    if not first_soal:
        return redirect("home")

    return redirect("tampil_soal", nomor=first_soal.id)



@login_required
def mulai_paket_ujian(request, paket_id):
    paket = get_object_or_404(PaketUjian, id=paket_id)
    subtests = list(paket.subtests.all())
    
    print(f"DEBUG MULAI PAKET: user={request.user} paket_id={paket_id} paket_nama={paket.nama} subtests_count={len(subtests)}")
    
    if not subtests:
        print("DEBUG MULAI PAKET: subtests is empty, redirecting to home")
        return redirect("home")

    def _order_key(s):
        try:
            return SUBTEST_ORDER.index(s.nama)
        except ValueError:
            return len(SUBTEST_ORDER) + s.id

    subtests.sort(key=_order_key)
    first_subtest = subtests[0]

    # Blokir jika paket ini sudah pernah diselesaikan
    if SesiUjian.objects.filter(user=request.user, selesai=True, subtest__paket=paket).exists():
        messages.error(request, "Anda sudah menyelesaikan paket ini dan tidak dapat mengulangnya.")
        kategori_norm = normalize_category(paket.nama)
        if kategori_norm == "KD1":
            return redirect("daftar_soal_kategori", kategori="Konsep Dasar 1")
        elif kategori_norm == "KD2":
            return redirect("daftar_soal_kategori", kategori="Konsep Dasar 2")
        else:
            return redirect("daftar_soal_kategori", kategori=paket.nama)

    if "konsep dasar 1" in paket.nama.lower():
        # Go to video first
        slug = first_subtest.nama.lower().strip()
        return redirect("materi_detail_ujian", subtest_id=first_subtest.id)
    else:
        # Straight to subtest
        return redirect("start_subtest", kategori=paket.nama, subtest_id=first_subtest.id)

@login_required
def start_subtest(request, kategori, subtest_id):
    print(f"DEBUG START SUBTEST: user={request.user} kategori={kategori} subtest_id={subtest_id}")
    paket = PaketUjian.objects.filter(nama__iexact=kategori).first()

    if not paket:
        print("DEBUG START SUBTEST: paket not found, redirecting to home")
        return redirect("home")

    subtest = SubTest.objects.filter(id=subtest_id, paket=paket).first()

    if not subtest:
        print("DEBUG START SUBTEST: subtest not found, redirecting to daftar_soal_kategori")
        return redirect("daftar_soal_kategori", kategori=kategori)

    # Blokir jika paket ini sudah pernah diselesaikan (cek HasilPaketUjian)
    from .models import HasilPaketUjian
    if HasilPaketUjian.objects.filter(user=request.user, paket_nama=paket.nama).exists():
        print("DEBUG START SUBTEST: paket sudah selesai (HasilPaketUjian exists)")
        messages.error(request, "Anda sudah menyelesaikan paket ini dan tidak dapat mengulangnya.")
        return redirect("daftar_soal_kategori", kategori=kategori)

    # ── FIX: Cari SesiUjian SPESIFIK untuk subtest ini, bukan sesi manapun yg belum selesai ──
    # Ini mencegah sesi subtest sebelumnya tertimpa
    sesi = SesiUjian.objects.filter(
        user=request.user,
        subtest=subtest,
        selesai=False
    ).first()

    if not sesi:
        # Buat SesiUjian baru yang terikat ke subtest ini
        sesi = SesiUjian.objects.create(
            user=request.user,
            subtest=subtest,
            selesai=False,
            waktu_mulai=timezone.now()
        )
    else:
        # Update waktu mulai jika masuk ulang ke subtest yang sama
        sesi.waktu_mulai = timezone.now()
        sesi.save()

    # ── Hapus SoalSesi lama untuk sesi ini dan buat ulang ──
    SoalSesi.objects.filter(sesi=sesi).delete()

    # ── Pilih soal sesuai batas soal_tampil ──
    soal_terpilih_ids = get_balanced_random_soal_ids(subtest, subtest.get_jumlah_soal_tampil())

    # Simpan soal terpilih ke SoalSesi
    soal_sesi_objs = [
        SoalSesi(sesi=sesi, soal_id=soal_id, urutan=idx)
        for idx, soal_id in enumerate(soal_terpilih_ids)
    ]
    SoalSesi.objects.bulk_create(soal_sesi_objs)

    if not soal_terpilih_ids:
        return redirect("daftar_soal_kategori", kategori=kategori)

    return redirect("tampil_soal", nomor=soal_terpilih_ids[0])



# ==========================================================
# TAMPIL SOAL
# ==========================================================


@login_required
def tampil_soal(request, nomor, kategori=None):

    target_soal = Soal.objects.filter(id=nomor).first()
    if not target_soal:
        return redirect("home")

    # ── FIX: Cari SesiUjian SPESIFIK untuk subtest soal ini ──
    # Prioritas 1: sesi aktif (selesai=False) untuk subtest ini
    # Prioritas 2: sesi apapun untuk subtest ini (sudah selesai pun boleh untuk read-only)
    sesi = None
    if target_soal.subtest:
        sesi = SesiUjian.objects.filter(
            user=request.user,
            subtest=target_soal.subtest,
            selesai=False
        ).first()
        # Jika tidak ada sesi aktif, coba cari yang sudah selesai (untuk tampil baca)
        if not sesi:
            sesi = SesiUjian.objects.filter(
                user=request.user,
                subtest=target_soal.subtest
            ).order_by('-id').first()

    # Fallback: jika masih tidak ada, buat sesi baru
    if not sesi:
        sesi = SesiUjian.objects.create(user=request.user, selesai=False)

    # ── Tentukan queryset soal yang relevan ──
    if sesi and sesi.subtest:
        soal_sesi_qs = SoalSesi.objects.filter(sesi=sesi).order_by('urutan')
        if soal_sesi_qs.exists():
            soal_ids_ordered = list(soal_sesi_qs.values_list('soal_id', flat=True))
            from django.db.models import Case, When, IntegerField as DBIntegerField
            preserved_order = Case(
                *[When(id=pk, then=pos) for pos, pk in enumerate(soal_ids_ordered)],
                output_field=DBIntegerField()
            )
            soal_queryset = Soal.objects.filter(id__in=soal_ids_ordered).order_by(preserved_order)
        else:
            soal_queryset = sesi.subtest.soal.all().order_by('id')
    elif target_soal.subtest:
        soal_queryset = target_soal.subtest.soal.all().order_by('id')
    else:
        # Fallback ke kategori dari target_soal atau parameter/session
        kat = target_soal.kategori or kategori or request.session.get('active_kategori') or 'KD1'
        request.session['active_kategori'] = kat
        soal_queryset = Soal.objects.filter(kategori=kat).order_by('id')

    if not soal_queryset.exists():
        return redirect("home")

    soal_ids = list(soal_queryset.values_list('id', flat=True))

    if target_soal.id in soal_ids:
        soal = target_soal
    else:
        soal = get_object_or_404(Soal, id=soal_ids[0])

    total_soal = len(soal_ids)
    current_index = soal_ids.index(soal.id) + 1

    # POST handling moved after next_soal_id is computed

    jawaban_user = JawabanPeserta.objects.filter(
        user=request.user,
        soal=soal
    ).first()

    jawaban_semua = JawabanPeserta.objects.filter(user=request.user)

    soal_dijawab = [item.soal_id for item in jawaban_semua if item.soal_id]

    nomor_links = []
    for idx, sid in enumerate(soal_ids):
        nomor_links.append({
            "index": idx + 1,
            "id": sid,
            "answered": sid in soal_dijawab,
        })

    prev_soal_id = None
    next_soal_id = None
    if current_index > 1:
        prev_soal_id = soal_ids[current_index - 2]
    if current_index < total_soal:
        next_soal_id = soal_ids[current_index]

    next_subtest = None
    if soal.subtest:
        paket = soal.subtest.paket
        subtests = list(paket.subtests.all())

        def _order_key(s):
            try:
                return SUBTEST_ORDER.index(s.nama)
            except ValueError:
                return len(SUBTEST_ORDER) + s.id

        subtests.sort(key=_order_key)

        try:
            idx = subtests.index(soal.subtest)
        except ValueError:
            idx = -1

        if idx != -1:
            for candidate in subtests[idx + 1:]:
                if candidate.soal.exists():
                    next_subtest = candidate
                    break

    has_next_subtest = next_subtest is not None
    has_next_step = bool(next_soal_id or next_subtest)

    # Calculate sisa_waktu first to prevent cheating
    sisa_waktu = 0
    waktu_habis = False
    if sesi and sesi.waktu_mulai:
        waktu_berjalan = (timezone.now() - sesi.waktu_mulai).seconds
        timer = sesi.subtest.get_timer_menit() if sesi.subtest else 0
        batas_waktu = timer * 60 if timer > 0 else 3600
        sisa_waktu = batas_waktu - waktu_berjalan
        # Grace period of 10 seconds for network latency
        if sisa_waktu < -10:
            waktu_habis = True
        if sisa_waktu < 0:
            sisa_waktu = 0

    # Handle form submission: save answer and optionally navigate to next soal
    if request.method == "POST":
        jawaban = request.POST.get("jawaban")
        action = request.POST.get("action")
        
        # Only save if time is not up
        if jawaban and not waktu_habis:
            JawabanPeserta.objects.update_or_create(
                user=request.user,
                soal=soal,
                defaults={
                    "jawaban": jawaban,
                    "is_benar_snapshot": (jawaban == soal.jawaban_benar),
                    "kategori_snapshot": soal.kategori,
                    "subtest_id_snapshot": soal.subtest.id if soal.subtest else None,
                    "paket_id_snapshot": soal.subtest.paket.id if (soal.subtest and soal.subtest.paket) else None,
                    "subtest_nama_snapshot": soal.subtest.nama if soal.subtest else "",
                    "paket_nama_snapshot": soal.subtest.paket.nama if (soal.subtest and soal.subtest.paket) else ""
                }
            )

        if action == 'ajax_save' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if action == 'ajax_cheat_flag':
                c = request.session.get('cheat_count', 0) + 1
                request.session['cheat_count'] = c
                if sesi:
                    sesi.terindikasi_curang = True
                    sesi.save(update_fields=['terindikasi_curang'])
                return JsonResponse({'status': 'ok', 'cheat_count': c})
            
            if waktu_habis:
                return JsonResponse({'status': 'time_up', 'message': 'Waktu habis.'})
            return JsonResponse({'status': 'ok', 'jawaban': jawaban, 'soal_id': soal.id})

        if action == 'next' or waktu_habis:
            # if time is up, force advance. If action is next and time is not up, also advance.
            # if there is a next soal in the current subtest and time is NOT up, go there
            if next_soal_id and not waktu_habis:
                return redirect('tampil_soal', nomor=next_soal_id)

            # if there is a next subtest (or if time is up and we must force next subtest), advance there automatically
            if next_subtest:
                # Cek jika ini paket Konsep Dasar 1, arahkan ke video materi dulu
                if "konsep dasar 1" in next_subtest.paket.nama.lower():
                    return redirect("materi_detail_ujian", subtest_id=next_subtest.id)

                # ── Tandai sesi lama sebagai selesai ──
                sesi.selesai = True
                sesi.save()

                # ── Buat sesi BARU untuk subtest berikutnya ──
                new_sesi = SesiUjian.objects.create(
                    user=request.user,
                    selesai=False,
                    subtest=next_subtest,
                    waktu_mulai=timezone.now()
                )

                semua_soal_ids = list(next_subtest.soal.values_list('id', flat=True))
                jumlah_tampil = next_subtest.get_jumlah_soal_tampil()

                soal_terpilih_ids = get_balanced_random_soal_ids(next_subtest, jumlah_tampil)

                soal_sesi_objs = [
                    SoalSesi(sesi=new_sesi, soal_id=sid, urutan=idx)
                    for idx, sid in enumerate(soal_terpilih_ids)
                ]
                SoalSesi.objects.bulk_create(soal_sesi_objs)

                if soal_terpilih_ids:
                    return redirect('tampil_soal', nomor=soal_terpilih_ids[0])

            # otherwise finish the exam
            return redirect('selesai_ujian')

        # default: reload current soal
        return redirect('tampil_soal', nomor=soal.id)

    sisa_waktu = 0
    if sesi and sesi.waktu_mulai:
        waktu_berjalan = (timezone.now() - sesi.waktu_mulai).seconds
        # Gunakan get_timer_menit() yang sudah memperhitungkan KategoriSetting
        timer = sesi.subtest.get_timer_menit() if sesi.subtest else 0
        if timer > 0:
            batas_waktu = timer * 60
        else:
            batas_waktu = 60 * 60  # default 1 jam jika tidak ada batas

        sisa_waktu = batas_waktu - waktu_berjalan
        if sisa_waktu < 0:
            sisa_waktu = 0

    sistem_setting = SistemSetting.get_setting()

    return render(request, "ujian/satu_soal.html", {
        "soal": soal,
        "nomor": nomor,
        "total": total_soal,
        "current_index": current_index,
        "nomor_links": nomor_links,
        "jawaban_user": jawaban_user,
        "soal_dijawab": soal_dijawab,
        "sisa_waktu": sisa_waktu,
        "kategori": kategori,
        "kategori_label": KATEGORI_LABEL.get(kategori, "Semua Soal"),
        "subtest": sesi.subtest if sesi else None,
        "next_subtest": next_subtest,
        "prev_soal_id": prev_soal_id,
        "next_soal_id": next_soal_id,
        "has_next_step": has_next_step,
        "sistem_setting": sistem_setting,
    })



# ==========================================================
# SELESAI UJIAN + STATISTIK
# ==========================================================


@login_required
def selesai_ujian(request):

    # ── Ambil sesi ujian (aktif atau yang terakhir dikerjakan) ──
    sesi = SesiUjian.objects.filter(user=request.user).order_by('-id').first()

    durasi = 0
    paket = None
    paket_nama = None
    waktu_test = None

    if sesi:
        if sesi.waktu_mulai:
            waktu_test = sesi.waktu_mulai
            durasi = (timezone.now() - sesi.waktu_mulai).seconds // 60
        if sesi.subtest and sesi.subtest.paket:
            paket = sesi.subtest.paket
            paket_nama = paket.nama

        # ── FIX: Tandai SEMUA SesiUjian untuk paket ini sebagai selesai ──
        if paket:
            SesiUjian.objects.filter(
                user=request.user,
                subtest__paket=paket,
                selesai=False
            ).update(selesai=True)

        from .models import HasilPaketUjian
        if paket and not HasilPaketUjian.objects.filter(user=request.user, paket_nama=paket.nama).exists():
            hasil_obj, _ = HasilPaketUjian.objects.get_or_create(user=request.user, paket_nama=paket.nama)
            
            # Check for cheat
            cheat_count = request.session.get('cheat_count', 0)
            if cheat_count >= 3:
                if not isinstance(hasil_obj.skor_json, dict):
                    hasil_obj.skor_json = {}
                hasil_obj.skor_json['cheat_flag'] = True
                hasil_obj.save()
            request.session['cheat_count'] = 0 # reset

            jawaban_paket = list(JawabanPeserta.objects.filter(user=request.user, soal__subtest__paket=paket))
            subtest_map = {}
            for j in jawaban_paket:
                st_id = j.soal.subtest_id if j.soal else j.subtest_id_snapshot
                if not st_id: continue
                if st_id not in subtest_map: subtest_map[st_id] = []
                subtest_map[st_id].append(j)
            
            # Harus iterasi ke SEMUA subtest dalam paket ini, bukan cuma yang ada jawabannya
            sts = list(paket.subtests.all())
            tot_skor = 0
            tot_sub = 0
            scores_dict = {}
            
            for st in sts:
                js = subtest_map.get(st.id, [])
                
                # Cek jumlah soal yang HARUSNYA dikerjakan (berdasarkan KategoriSetting/SubTest)
                # Jika peserta bolong jawab, denominatornya tetap jumlah soal total
                total_soal_st = st.soal.count()
                jumlah_tampil = st.get_jumlah_soal_tampil()
                if jumlah_tampil > 0 and jumlah_tampil < total_soal_st:
                    ts = jumlah_tampil
                else:
                    ts = total_soal_st
                    
                if ts == 0: 
                    continue # Bypass jika subtest kosong
                    
                bn = sum(1 for j in js if (j.soal and j.jawaban == j.soal.jawaban_benar) or (not j.soal and j.is_benar_snapshot))
                sc = round((bn/ts)*100, 1)
                scores_dict[st.nama.replace(" ", "_")] = sc
                tot_skor += sc
                tot_sub += 1
                
            na = round(tot_skor/tot_sub, 1) if tot_sub > 0 else 0
            kat = paket.subtests.first().soal.first().kategori if paket.subtests.first() and paket.subtests.first().soal.first() else "-"
            waktu_aktual_menit = 0
            durasi_total = sum(st.get_timer_menit() for st in paket.subtests.all())
            jawaban_terakhir = [j for j in jawaban_paket if j.dibuat_pada]
            if jawaban_terakhir and sesi.waktu_mulai:
                latest_j = max(jawaban_terakhir, key=lambda x: x.dibuat_pada)
                if latest_j.dibuat_pada > sesi.waktu_mulai:
                    waktu_aktual_menit = (latest_j.dibuat_pada - sesi.waktu_mulai).seconds // 60
            hasil_obj.kategori = kat
            hasil_obj.skor_json = scores_dict
            hasil_obj.nilai_akhir = na
            hasil_obj.durasi_teks = f"{waktu_aktual_menit}/{durasi_total}"
            hasil_obj.save()

    # ── Jika paket belum terdeteksi, cari dari JawabanPeserta ──
    if not paket:
        latest_j = JawabanPeserta.objects.filter(user=request.user).select_related('soal__subtest__paket').last()
        if latest_j and latest_j.soal.subtest and latest_j.soal.subtest.paket:
            paket = latest_j.soal.subtest.paket
            paket_nama = paket.nama

    # ── Ambil semua jawaban user (untuk tampil detail per soal) ──
    if paket:
        all_j_paket = [j for j in JawabanPeserta.objects.filter(user=request.user).select_related('soal', 'soal__subtest') if (j.soal and j.soal.subtest and j.soal.subtest.paket_id == paket.id) or (not j.soal and j.paket_id_snapshot == paket.id)]
    else:
        all_j_paket = list(JawabanPeserta.objects.filter(user=request.user).select_related('soal', 'soal__subtest'))

    jawaban_map = {}
    for j in all_j_paket:
        if j.soal:
            jawaban_map[j.soal_id] = j

    # ── SINGLE SOURCE OF TRUTH: Gunakan HasilPaketUjian.skor_json ──
    # Ini menjamin nilai di halaman peserta IDENTIK dengan yang tampil di admin statistik
    subtest_hasil = []
    total_skor_semua = []
    from .models import HasilPaketUjian

    hasil_tersimpan = HasilPaketUjian.objects.filter(user=request.user, paket_nama=paket_nama).first() if paket_nama else None

    if hasil_tersimpan and hasil_tersimpan.skor_json and isinstance(hasil_tersimpan.skor_json, dict) and 'cheat_flag' not in hasil_tersimpan.skor_json:
        # Gunakan skor yang sudah tersimpan (hasil dari selesai_ujian) — sama persis dengan admin
        if paket:
            subtests = list(paket.subtests.all())
            def _order_key(s):
                try: return SUBTEST_ORDER.index(s.nama)
                except ValueError: return len(SUBTEST_ORDER) + s.id
            subtests.sort(key=_order_key)

            for st in subtests:
                soal_ids = list(st.soal.values_list('id', flat=True))
                if not soal_ids:
                    continue

                key = st.nama.replace(" ", "_")
                skor_st = hasil_tersimpan.skor_json.get(key, None)
                if skor_st is None:
                    continue  # subtest ini tidak dikerjakan

                # Hitung benar/salah dari JawabanPeserta untuk detail tampil
                active_soal_ids = [sid for sid in soal_ids if sid in jawaban_map]
                total_st = len(active_soal_ids) if active_soal_ids else 0
                benar_st = sum(1 for sid in active_soal_ids if jawaban_map[sid].jawaban == jawaban_map[sid].soal.jawaban_benar)
                dijawab_st = total_st
                salah_st = total_st - benar_st

                # Gunakan skor_st dari HasilPaketUjian (bukan hitung ulang) agar INLINE
                total_skor_semua.append(skor_st)

                practice_key = f"practice_wrong_{request.user.id}"
                practice_map = request.session.get(practice_key, {})
                diperbaiki_st = sum(1 for sid in active_soal_ids
                    if sid in jawaban_map
                    and jawaban_map[sid].jawaban != jawaban_map[sid].soal.jawaban_benar
                    and practice_map.get(str(sid)) == jawaban_map[sid].soal.jawaban_benar)
                sisa_salah_st = salah_st - diperbaiki_st

                subtest_hasil.append({
                    'id': st.id,
                    'nama': st.nama,
                    'paket_nama': paket.nama,
                    'total': total_st,
                    'dijawab': dijawab_st,
                    'benar': benar_st,
                    'salah': salah_st,
                    'sisa_salah': sisa_salah_st,
                    'skor': skor_st,  # ← dari HasilPaketUjian, inline dengan admin
                })
    else:
        # Fallback: hitung langsung dari JawabanPeserta (paket belum selesai / baru dikerjakan)
        if paket:
            subtests = list(paket.subtests.all())
            def _order_key(s):
                try: return SUBTEST_ORDER.index(s.nama)
                except ValueError: return len(SUBTEST_ORDER) + s.id
            subtests.sort(key=_order_key)

            for st in subtests:
                soal_ids = list(st.soal.values_list('id', flat=True))
                if not soal_ids:
                    continue

                soal_sesi_ids = list(SoalSesi.objects.filter(
                    sesi__user=request.user, sesi__subtest=st
                ).values_list('soal_id', flat=True))

                active_soal_ids = soal_sesi_ids if soal_sesi_ids else soal_ids
                total_st = len(active_soal_ids)
                if total_st == 0:
                    continue

                benar_st = sum(1 for sid in active_soal_ids if sid in jawaban_map and jawaban_map[sid].jawaban == jawaban_map[sid].soal.jawaban_benar)
                dijawab_st = sum(1 for sid in active_soal_ids if sid in jawaban_map)
                skor_st = round((benar_st / total_st) * 100, 1) if total_st > 0 else 0
                total_skor_semua.append(skor_st)
                salah_st = total_st - benar_st

                practice_key = f"practice_wrong_{request.user.id}"
                practice_map = request.session.get(practice_key, {})
                diperbaiki_st = sum(1 for sid in active_soal_ids
                    if sid in jawaban_map and jawaban_map[sid].jawaban != jawaban_map[sid].soal.jawaban_benar
                    and practice_map.get(str(sid)) == jawaban_map[sid].soal.jawaban_benar)

                subtest_hasil.append({
                    'id': st.id, 'nama': st.nama, 'paket_nama': paket.nama,
                    'total': total_st, 'dijawab': dijawab_st, 'benar': benar_st,
                    'salah': salah_st, 'sisa_salah': salah_st - diperbaiki_st, 'skor': skor_st,
                })

    # ── Jika masih tidak ada data, buat format default 8 subtest ──
    if not subtest_hasil:
        default_subtests = ['PU', 'PPU', 'PBM', 'PK', 'LBI saintek', 'LBI soshum', 'LBE', 'PM']
        for idx, st_nama in enumerate(default_subtests, 1):
            subtest_hasil.append({
                'id': idx, 'nama': st_nama,
                'paket_nama': paket_nama if paket_nama else "-",
                'total': 0, 'dijawab': 0, 'benar': 0, 'salah': 0, 'sisa_salah': 0, 'skor': 0.0,
            })

    # ── Total keseluruhan ──
    total_soal = sum(s['total'] for s in subtest_hasil)
    total_benar = sum(s['benar'] for s in subtest_hasil)
    total_dijawab = sum(s['dijawab'] for s in subtest_hasil)
    total_salah = total_soal - total_benar
    total_sisa_salah = sum(s.get('sisa_salah', 0) for s in subtest_hasil)
    rata_rata = round(sum(total_skor_semua) / len(total_skor_semua), 1) if total_skor_semua else 0.0

    # ── HITUNG RIWAYAT PAKET (dari HasilPaketUjian — single source of truth) ──
    riwayat_paket = []
    hasil_statis = HasilPaketUjian.objects.filter(user=request.user).order_by('waktu_selesai')
    for h in hasil_statis:
        if not h.skor_json:
            continue
        riwayat_paket.append({
            'paket_nama': h.paket_nama,
            'kategori': h.kategori,
            'tanggal': h.waktu_selesai.strftime("%d/%m") if h.waktu_selesai else "-",
            'durasi': h.durasi_teks,
            'scores': h.skor_json,
            'nilai_akhir': h.nilai_akhir
        })

    return render(request, "ujian/hasil.html", {
        "paket_nama": paket_nama,
        "waktu_test": waktu_test,
        "subtest_hasil": subtest_hasil,
        "total_soal": total_soal,
        "total_benar": total_benar,
        "total_dijawab": total_dijawab,
        "total_salah": total_salah,
        "total_sisa_salah": total_sisa_salah,
        "rata_rata": rata_rata,
        "durasi": durasi,
        "username": request.user.username,
        "riwayat_paket": riwayat_paket,
    })


@login_required
def latihan_soal_salah(request, subtest_id=0, nomor=1):
    jawaban_salah_qs = JawabanPeserta.objects.filter(
        user=request.user
    ).exclude(jawaban=models.F('soal__jawaban_benar')).select_related('soal', 'soal__subtest', 'soal__subtest__paket')

    if subtest_id and subtest_id > 0:
        jawaban_salah_qs = jawaban_salah_qs.filter(soal__subtest_id=subtest_id)

    if not jawaban_salah_qs.exists():
        messages.success(request, "Luar Biasa! Sempurna! Seluruh materi di paket ini telah Anda selesaikan dengan baik termasuk perbaikan soal yang salah")
        return redirect("selesai_ujian")

    soal_list = [j.soal for j in jawaban_salah_qs]
    total_soal = len(soal_list)

    nomor = int(nomor)
    if nomor < 1:
        nomor = 1
    elif nomor > total_soal:
        nomor = total_soal

    current_soal = soal_list[nomor - 1]

    practice_key = f"practice_wrong_{request.user.id}"
    if practice_key not in request.session:
        request.session[practice_key] = {}

    jawaban_latihan_map = request.session.get(practice_key, {})

    if request.method == "POST":
        jawaban_user = request.POST.get("jawaban")
        if jawaban_user:
            jawaban_latihan_map[str(current_soal.id)] = jawaban_user
        else:
            # Jika user mengeklik Cek Jawaban tanpa memilih radio button
            jawaban_latihan_map[str(current_soal.id)] = "CEK"

        request.session[practice_key] = jawaban_latihan_map
        request.session.modified = True

        # Check if all wrong questions in this list are now correct
        all_correct = True
        for s in soal_list:
            if jawaban_latihan_map.get(str(s.id)) != s.jawaban_benar:
                all_correct = False
                break
                
        if all_correct and is_correct:
            messages.success(request, "Luar Biasa! Sempurna! Seluruh materi di paket ini telah Anda selesaikan dengan baik termasuk perbaikan soal yang salah")
            return redirect("selesai_ujian")

        next_nomor = request.POST.get("next_nomor")
        if next_nomor:
            return redirect(reverse("latihan_soal_salah_nav", kwargs={"subtest_id": subtest_id or 0, "nomor": next_nomor}))

    jawaban_user_sekarang = jawaban_latihan_map.get(str(current_soal.id))
    is_correct = (jawaban_user_sekarang == current_soal.jawaban_benar)
    has_checked = bool(jawaban_user_sekarang)

    return render(request, "ujian/latihan_soal_salah.html", {
        "soal": current_soal,
        "total_soal": total_soal,
        "current_index": nomor,
        "subtest_id": subtest_id or 0,
        "jawaban_user": jawaban_user_sekarang if jawaban_user_sekarang != "CEK" else None,
        "is_correct": is_correct,
        "has_checked": has_checked,
    })



# ==========================================================
# REVIEW JAWABAN
# ==========================================================


@login_required
def review_jawaban(request):
    from .models import HasilPaketUjian
    
    # Ambil sesi terakhir yang sudah selesai untuk mengetahui paket
    sesi_selesai = SesiUjian.objects.filter(
        user=request.user, selesai=True
    ).select_related('subtest__paket').order_by('-id').first()

    paket = None
    paket_nama = None
    if sesi_selesai and sesi_selesai.subtest:
        paket = sesi_selesai.subtest.paket
        paket_nama = paket.nama
        
        # VALIDASI KETAT: Pastikan HasilPaketUjian sudah terbentuk (kecuali untuk admin)
        if not request.user.is_staff and not request.user.is_superuser:
            if not HasilPaketUjian.objects.filter(user=request.user, paket_nama=paket_nama).exists():
                messages.warning(request, f"Anda belum menyelesaikan semua subtest pada paket {paket_nama}. Hasil ujian belum tersedia.")
                return redirect("home")

    if paket:
        all_j = JawabanPeserta.objects.filter(user=request.user).select_related("soal", "soal__subtest")
        jawaban_peserta = [j for j in all_j if (j.soal and j.soal.subtest and j.soal.subtest.paket_id == paket.id) or (not j.soal and j.paket_id_snapshot == paket.id)]
    else:
        jawaban_peserta = list(JawabanPeserta.objects.filter(user=request.user).select_related("soal", "soal__subtest"))

    data_review = []
    soal_berubah = False
    
    for item in jawaban_peserta:
        # Deteksi perubahan soal
        if not item.soal:
            soal_berubah = True
            continue
            
        is_benar_now = (item.jawaban == item.soal.jawaban_benar)
        if hasattr(item, 'is_benar_snapshot') and is_benar_now != item.is_benar_snapshot:
            # Jika ada perbedaan status benar antara histori dan soal saat ini
            soal_berubah = True
            
        status = "BENAR" if is_benar_now else "SALAH"
        data_review.append({
            "soal": item.soal,
            "subtest_nama": item.soal.subtest.nama if item.soal.subtest else "-",
            "jawaban_user": item.jawaban,
            "jawaban_benar": item.soal.jawaban_benar,
            "status": status,
        })

    return render(request, "ujian/review.html", {
        "data_review": data_review,
        "paket_nama": paket_nama,
        "soal_berubah": soal_berubah,
    })


# ==========================================================
# DASHBOARD STATISTIK ADMIN CBT
# ==========================================================


def network_gateway(request):
    setting = SistemSetting.get_setting()
    
    if not setting.network_online and not setting.network_local:
        return render(request, "ujian/network_gateway.html", {"offline": True})

    error_msg = ""
    if request.method == "POST":
        password = request.POST.get("network_password")
        if password == setting.network_password:
            request.session['network_access_granted'] = True
            return redirect('home')
        else:
            error_msg = "Password salah!"

    return render(request, "ujian/network_gateway.html", {"offline": False, "error": error_msg})


@login_required
def admin_statistik(request):
    if not request.user.is_staff:
        return redirect("home")

    sistem_setting = SistemSetting.get_setting()

    if request.method == "POST":
        if "toggle_anti_cheat" in request.POST:
            sistem_setting.anti_cheat_aktif = not sistem_setting.anti_cheat_aktif
            sistem_setting.save()
            return redirect("admin_statistik")
            
        elif "save_network_settings" in request.POST:
            is_online = request.POST.get("network_online") == "on"
            is_local = request.POST.get("network_local") == "on"
            password = request.POST.get("network_password", "").strip()
            
            # Start/stop tunnel
            from ujian.utils_tunnel import start_tunnel, stop_tunnel
            if is_online and not sistem_setting.network_online:
                start_tunnel()
            elif not is_online and sistem_setting.network_online:
                stop_tunnel()
                
            # Toggle firewall based on Mode Lokal
            import subprocess
            if is_local and not sistem_setting.network_local:
                try:
                    subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'off'], creationflags=subprocess.CREATE_NO_WINDOW)
                except:
                    pass
            elif not is_local and sistem_setting.network_local:
                # Turn firewall back on ONLY if we are not also running Mode Global (which needs it off)
                if not is_online:
                    try:
                        subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'on'], creationflags=subprocess.CREATE_NO_WINDOW)
                    except:
                        pass
                
            sistem_setting.network_online = is_online
            sistem_setting.network_local = is_local
            sistem_setting.network_password = password
            sistem_setting.save()
            return redirect("admin_statistik")

    import socket
    local_ip = "127.0.0.1"
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        pass

    soal_sesi_aktif = SoalSesi.objects.select_related('sesi', 'sesi__user', 'soal', 'soal__subtest').order_by('-id')

    total_peserta = User.objects.count()
    total_ujian = SesiUjian.objects.filter(selesai=True).count()

    paket_id = request.GET.get("paket")
    subtest_id = request.GET.get("subtest")
    kategori_filter = request.GET.get("kategori")

    pakets = PaketUjian.objects.all()
    subtests = SubTest.objects.all()

    semua_user = User.objects.all()

    soal_queryset = None   # None = tidak ada filter aktif (Semua Soal)
    filter_label = None
    filter_active = False  # Flag: apakah filter spesifik sedang aktif?

    if subtest_id:
        soal_queryset = Soal.objects.filter(subtest__id=subtest_id)
        sel_sub = SubTest.objects.filter(id=subtest_id).first()
        filter_label = str(sel_sub) if sel_sub else f"SubTest {subtest_id}"
        filter_active = True
    elif paket_id:
        soal_queryset = Soal.objects.filter(subtest__paket__id=paket_id)
        sel_paket = PaketUjian.objects.filter(id=paket_id).first()
        filter_label = sel_paket.nama if sel_paket else f"Paket {paket_id}"
        filter_active = True
    elif kategori_filter:
        soal_queryset = Soal.objects.filter(kategori__iexact=kategori_filter)
        filter_label = KATEGORI_LABEL.get(kategori_filter, kategori_filter)
        filter_active = True
    else:
        filter_label = "Semua Soal"

    # ── Optimasi #3: Hitung total soal tanpa subquery besar jika tidak ada filter ──
    total_soal_subset = soal_queryset.count() if filter_active else Soal.objects.count()

    daftar_peserta = []

    for user in semua_user:
        # ── Optimasi #3: Hindari subquery soal__in=all saat filter kosong ──
        if filter_active:
            from django.db.models import Q
            q_filter = Q(soal__in=soal_queryset) if soal_queryset is not None else Q()
            if subtest_id:
                q_filter |= Q(soal__isnull=True, subtest_id_snapshot=subtest_id)
            elif paket_id:
                q_filter |= Q(soal__isnull=True, paket_id_snapshot=paket_id)
            elif kategori_filter:
                q_filter |= Q(soal__isnull=True, kategori_snapshot=kategori_filter)
            jawaban = JawabanPeserta.objects.filter(q_filter, user=user).select_related('soal', 'soal__subtest', 'soal__subtest__paket')
        else:
            jawaban = JawabanPeserta.objects.filter(user=user).select_related('soal', 'soal__subtest', 'soal__subtest__paket')
        total_dikerjakan = jawaban.count()
        benar = 0
        for item in jawaban:
            if item.soal:
                if item.jawaban == item.soal.jawaban_benar:
                    benar += 1
            else:
                if item.is_benar_snapshot:
                    benar += 1

        sesi = (total_dikerjakan > 0) and SesiUjian.objects.filter(user=user, selesai=True).exists()

        # Breakdown per-paket & per-subtest untuk modal/expandable view
        breakdown = []
        paket_ids = list(set([j.soal.subtest.paket.id if j.soal and j.soal.subtest and j.soal.subtest.paket else j.paket_id_snapshot for j in jawaban if (j.soal and j.soal.subtest and j.soal.subtest.paket) or j.paket_id_snapshot]))
        
        total_p_nilai = 0
        valid_p_count = 0
        
        for p_id in paket_ids:
            if not p_id:
                continue
            paket_obj = PaketUjian.objects.filter(id=p_id).first()
            
            paket_jawaban = [j for j in jawaban if (j.soal and j.soal.subtest and j.soal.subtest.paket_id == p_id) or (not j.soal and j.paket_id_snapshot == p_id)]
            p_total = len(paket_jawaban)
            p_benar = sum(1 for j in paket_jawaban if (j.soal and j.jawaban == j.soal.jawaban_benar) or (not j.soal and j.is_benar_snapshot))

            sub_breakdown = []
            sub_ids = list(set([j.soal.subtest.id if j.soal and j.soal.subtest else j.subtest_id_snapshot for j in paket_jawaban if (j.soal and j.soal.subtest) or j.subtest_id_snapshot]))
            
            tot_skor_sub = 0
            tot_sub = 0
            
            for s_id in sub_ids:
                if not s_id:
                    continue
                sub_obj = SubTest.objects.filter(id=s_id).first()
                sub_nama = sub_obj.nama if sub_obj else "SubTest Terhapus"
                sub_j = [j for j in paket_jawaban if (j.soal and j.soal.subtest_id == s_id) or (not j.soal and j.subtest_id_snapshot == s_id)]
                st_total = len(sub_j)
                st_benar = sum(1 for j in sub_j if (j.soal and j.jawaban == j.soal.jawaban_benar) or (not j.soal and j.is_benar_snapshot))
                st_nilai = round((st_benar / st_total) * 100, 1) if st_total > 0 else 0.0
                
                tot_skor_sub += st_nilai
                tot_sub += 1
                
                # Cek curang di subtest ini
                st_curang = SesiUjian.objects.filter(user=user, subtest_id=s_id, terindikasi_curang=True).exists()
                
                sub_breakdown.append({
                    'subtest_nama': sub_nama,
                    'benar': st_benar,
                    'total': st_total,
                    'nilai': st_nilai,
                    'terindikasi_curang': st_curang,
                })

            p_nilai = round(tot_skor_sub / tot_sub, 1) if tot_sub > 0 else 0.0
            
            # CEK APAKAH PAKET INI SUDAH SELESAI PENUH (HASIL_PAKET_UJIAN EXISTS)
            from .models import HasilPaketUjian
            is_finished = HasilPaketUjian.objects.filter(user=user, paket_nama=paket_obj.nama).exists()
            
            if is_finished:
                total_p_nilai += p_nilai
                valid_p_count += 1
            else:
                p_nilai = "Belum Selesai"

            # Cek apakah ada indikasi curang di paket ini
            curang_di_paket = SesiUjian.objects.filter(
                user=user,
                subtest__paket=paket_obj,
                terindikasi_curang=True
            ).exists()
            hasil_p = HasilPaketUjian.objects.filter(user=user, paket_nama=paket_obj.nama).first()
            if hasil_p and isinstance(hasil_p.skor_json, dict) and hasil_p.skor_json.get('cheat_flag'):
                curang_di_paket = True

            breakdown.append({
                'paket_nama': paket_obj.nama,
                'paket_id': paket_obj.id,
                'benar': p_benar,
                'total': p_total,
                'nilai': p_nilai,
                'subtests': sub_breakdown,
                'is_finished': is_finished,
                'terindikasi_curang': curang_di_paket,
            })
            
        nilai = round(total_p_nilai / valid_p_count, 1) if valid_p_count > 0 else 0.0

        is_curang = SesiUjian.objects.filter(user=user, terindikasi_curang=True).exists()
        daftar_peserta.append({
            "id": user.id,
            "username": user.username,
            "nilai": nilai,
            "total_dikerjakan": total_dikerjakan,
            "selesai": sesi,
            "benar": benar,
            "is_superuser": user.is_superuser,
            "terindikasi_curang": is_curang,
            "breakdown": breakdown,
        })

    nilai_list = [item["nilai"] for item in daftar_peserta]

    if nilai_list:
        nilai_tertinggi = max(nilai_list)
        nilai_terendah = min(nilai_list)
        rata_rata = int(sum(nilai_list) / len(nilai_list))
    else:
        nilai_tertinggi = 0
        nilai_terendah = 0
        rata_rata = 0

    # ── Pengaturan Kategori (waktu & jumlah soal) ──
    kategori_settings = []
    from .models import HasilPaketUjian
    for s in KategoriSetting.objects.all().order_by('kategori'):
        jumlah_soal_kat = Soal.objects.filter(kategori=s.kategori).count()
        jumlah_subtest_kat = (
            Soal.objects
            .filter(kategori=s.kategori, subtest__isnull=False)
            .values('subtest_id').distinct().count()
        )
        jumlah_paket_kat = (
            Soal.objects
            .filter(kategori=s.kategori, subtest__paket__isnull=False)
            .values('subtest__paket_id').distinct().count()
        )
        paket_dikerjakan_kat = (
            HasilPaketUjian.objects
            .filter(kategori=s.kategori)
            .values('paket_nama').distinct().count()
        )
        kategori_settings.append({
            'id': s.id,
            'label': s.get_kategori_display(),
            'kategori': s.kategori,
            'jumlah_soal': jumlah_soal_kat,
            'jumlah_subtest': jumlah_subtest_kat,
            'jumlah_paket': jumlah_paket_kat,
            'paket_dikerjakan': paket_dikerjakan_kat,
            'soal_per_subtest': s.soal_per_subtest,
            'timer_menit': s.timer_menit,
        })

    # ── Optimasi #5: Ambil nama subtest unik HANYA dari kategori aktif (bukan semua) ──
    # Hanya ambil 8 nama subtest unik yang dikenal, bukan full scan seluruh tabel
    distinct_subtest_names = sorted(list(
        SubTest.objects.values_list('nama', flat=True).distinct()[:50]
    ))

    # ── Optimasi #6: Data SubTest per kategori untuk Live Preview JS ──
    # Gunakan filter langsung dari SubTest ke Soal via subtest__soal
    category_subtests_map = {}
    for code in KATEGORI_LABEL:
        seen_names = set()
        sub_list = []
        for st in SubTest.objects.filter(
            soal__kategori=code
        ).order_by('nama').distinct():
            if st.nama not in seen_names:
                seen_names.add(st.nama)
                sub_list.append({
                    'nama': st.nama,
                    'timer_menit': st.get_timer_menit(),
                    'soal_tampil': st.get_jumlah_soal_tampil(),
                })
        category_subtests_map[code] = sub_list

    category_subtests_json = json.dumps(category_subtests_map)

    return render(request, "ujian/admin_statistik.html", {
        "local_ip": local_ip,
        "total_peserta": total_peserta,
        "total_ujian": total_ujian,
        "nilai_tertinggi": nilai_tertinggi,
        "nilai_terendah": nilai_terendah,
        "rata_rata": rata_rata,
        "daftar_peserta": daftar_peserta,
        "pakets": pakets,
        "subtests": subtests,
        "selected_paket": int(paket_id) if paket_id else None,
        "selected_subtest": int(subtest_id) if subtest_id else None,
        "selected_kategori": kategori_filter,
        "total_soal_subset": total_soal_subset,
        "filter_label": filter_label,
        "kategori_choices": list(KATEGORI_LABEL.items()),
        "kategori_settings": kategori_settings,
        "distinct_subtest_names": distinct_subtest_names,
        "category_subtests_json": category_subtests_json,
        "sistem_setting": sistem_setting,
    })


@login_required
def admin_statistik_detail(request):
    if not request.user.is_staff:
        return redirect("home")

    paket_id = request.GET.get("paket")
    subtest_id = request.GET.get("subtest")
    kategori_filter = request.GET.get("kategori")

    if subtest_id:
        soal_queryset = Soal.objects.filter(subtest__id=subtest_id)
        title = f"Detail Statistik - SubTest {subtest_id}"
    elif paket_id:
        soal_queryset = Soal.objects.filter(subtest__paket__id=paket_id)
        title = f"Detail Statistik - Paket {paket_id}"
    elif kategori_filter:
        soal_queryset = Soal.objects.filter(kategori__iexact=kategori_filter)
        title = f"Detail Statistik - Kategori {kategori_filter}"
    else:
        soal_queryset = Soal.objects.all()
        title = "Detail Statistik - Semua Soal"

    total_soal = soal_queryset.count()

    # per-user scores
    rows = []
    
    # Ambil semua subtest_id yang relevan dengan queryset
    subtest_ids_in_qs = list(set(soal_queryset.values_list('subtest_id', flat=True)))
    
    for user in User.objects.all():
        jawaban = JawabanPeserta.objects.filter(user=user, soal__in=soal_queryset).select_related('soal')
        benar_total = 0
        
        tot_skor_sub = 0
        tot_sub = 0
        
        # Kelompokkan jawaban berdasarkan subtest_id
        for st_id in subtest_ids_in_qs:
            if not st_id:
                continue
            sub_j = [j for j in jawaban if j.soal and j.soal.subtest_id == st_id]
            # Harus membandingkan dengan total soal aktual di subtest tersebut yg difilter
            st_total_soal = soal_queryset.filter(subtest_id=st_id).count()
            if st_total_soal == 0:
                continue
                
            st_benar = sum(1 for j in sub_j if j.jawaban == j.soal.jawaban_benar)
            benar_total += st_benar
            
            st_nilai = (st_benar / st_total_soal) * 100
            tot_skor_sub += st_nilai
            tot_sub += 1
            
        if tot_sub > 0:
            skor = int(tot_skor_sub / tot_sub)
        else:
            skor = 0
            
        # Cek apakah user pernah curang di sesi ini
        sesi_selesai = SesiUjian.objects.filter(user=user, selesai=True).exists()
        is_curang = SesiUjian.objects.filter(user=user, terindikasi_curang=True).exists()
        rows.append({"username": user.username, "benar": benar_total, "skor": skor, "selesai": sesi_selesai, "id": user.id, "terindikasi_curang": is_curang})

    # distribution buckets 0-9,10-19,...,90-100
    buckets = {f"{i}-{i+9}": 0 for i in range(0, 100, 10)}
    buckets["100"] = 0
    for r in rows:
        s = r["skor"]
        if s == 100:
            buckets["100"] += 1
        else:
            key = f"{(s//10)*10}-{(s//10)*10+9}"
            buckets[key] += 1

    # summary
    skor_list = [r["skor"] for r in rows]
    if skor_list:
        tinggi = max(skor_list)
        rendah = min(skor_list)
        rata = int(sum(skor_list)/len(skor_list))
        median = sorted(skor_list)[len(skor_list)//2]
    else:
        tinggi = rendah = rata = median = 0

    return render(request, "ujian/admin_statistik_detail.html", {
        "title": title,
        "total_soal": total_soal,
        "rows": rows,
        "buckets": [{"label": k, "count": v, "height": min(140, 10 + v * 8)} for k, v in buckets.items()],
        "tinggi": tinggi,
        "rendah": rendah,
        "rata": rata,
        "median": median,
    })



@login_required
def upload_paket(request):

    if not request.user.is_staff:
        return redirect("home")

    if request.method == "POST":

        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            messages.error(request, "File tidak ditemukan.")
            return redirect("admin_panel")

        try:
            filename = uploaded_file.name.lower()
            reader = []
            
            if filename.endswith(".csv"):
                data = uploaded_file.read().decode("utf-8")
                f = io.StringIO(data)
                reader_csv = csv.DictReader(f)
                reader = list(reader_csv)
            elif filename.endswith(".xlsx"):
                wb = openpyxl.load_workbook(uploaded_file, data_only=True)
                ws = wb.active
                rows = list(ws.values)
                if len(rows) > 1:
                    headers = [str(h).strip() if h is not None else '' for h in rows[0]]
                    for row in rows[1:]:
                        row_dict = {}
                        for i, cell in enumerate(row):
                            if i < len(headers):
                                row_dict[headers[i]] = str(cell) if cell is not None else ''
                        reader.append(row_dict)
            else:
                messages.error(request, "Format file tidak didukung. Harap gunakan file .csv atau .xlsx")
                return redirect("admin_panel")

            created = 0
            upload_mode = request.POST.get("upload_mode", "append")
            cleared_subtests = set()

            for row in reader:

                paket_nama = row.get("paket") or row.get("Paket") or row.get('paket_ujian')
                sub_nama = row.get("sub_test") or row.get("subtest") or row.get('sub_test')
                timer = row.get("timer_menit") or row.get('timer') or row.get('slide/minit')

                kategori_raw = row.get("kategori") or row.get('Kategori') or row.get('kategori')
                kategori = normalize_category(kategori_raw)
                pertanyaan = row.get("pertanyaan") or row.get('Soal')
                pa = row.get("pilihan_a") or row.get('pilihan A') or row.get('A')
                pb = row.get("pilihan_b") or row.get('pilihan B') or row.get('B')
                pc = row.get("pilihan_c") or row.get('pilihan C') or row.get('C')
                pd = row.get("pilihan_d") or row.get('pilihan D') or row.get('D')
                pe = row.get("pilihan_e") or row.get('pilihan E') or row.get('E')
                jawaban_benar = (row.get("jawaban_benar") or row.get('jawaban') or '').strip()
                pembahasan = row.get("pembahasan") or ''

                if not paket_nama or not sub_nama or not pertanyaan:
                    continue

                paket, _ = PaketUjian.objects.get_or_create(nama=paket_nama.strip())
                subtest, _ = SubTest.objects.get_or_create(paket=paket, nama=sub_nama.strip())

                if upload_mode == "replace" and subtest.id not in cleared_subtests:
                    Soal.objects.filter(subtest=subtest).delete()
                    cleared_subtests.add(subtest.id)

                try:
                    if timer:
                        subtest.timer_menit = int(timer)
                        subtest.save()
                    elif subtest.timer_menit == 0:
                        subtest.timer_menit = 10
                        subtest.save()
                except Exception:
                    pass

                Soal.objects.create(
                    kategori=kategori,
                    pertanyaan=pertanyaan.strip(),
                    pilihan_a=(pa or '').strip(),
                    pilihan_b=(pb or '').strip(),
                    pilihan_c=(pc or '').strip(),
                    pilihan_d=(pd or '').strip(),
                    pilihan_e=(pe or '').strip(),
                    jawaban_benar=jawaban_benar[:1].upper(),
                    pembahasan=pembahasan.strip(),
                    subtest=subtest
                )

                created += 1

            messages.success(request, f"Berhasil menambahkan {created} soal dari file.")

        except Exception as e:
            messages.error(request, f"Terjadi error saat memproses file: {e}")

        return redirect("admin_panel")

    return redirect("admin_panel")


@login_required
def admin_statistik_update_massal(request):
    if not request.user.is_staff:
        return redirect("home")

    if request.method == "POST":
        kategori = request.POST.get("kategori")
        subtest_name = request.POST.get("subtest_name")
        timer_menit = request.POST.get("timer_menit", "0")
        soal_tampil = request.POST.get("soal_tampil", "0")

        try:
            timer_menit = int(timer_menit)
            soal_tampil = int(soal_tampil)
        except ValueError:
            messages.error(request, "Input waktu atau jumlah soal tidak valid.")
            return redirect("admin_statistik")

        if not kategori:
            messages.error(request, "Kategori harus dipilih.")
            return redirect("admin_statistik")

        # ── Ambil semua subtest yang memiliki soal dengan kategori ini ──
        subtest_ids = list(
            Soal.objects
            .filter(kategori=kategori, subtest__isnull=False)
            .values_list('subtest_id', flat=True)
            .distinct()
        )
        subtests = SubTest.objects.filter(id__in=subtest_ids)

        if subtest_name and subtest_name != "__ALL__":
            subtests = subtests.filter(nama__iexact=subtest_name.strip())

        count = subtests.count()
        if count > 0:
            subtests.update(timer_menit=timer_menit, soal_tampil=soal_tampil)
            target = "semua subtest" if subtest_name == "__ALL__" else f"subtest '{subtest_name}'"
            
            # Update the KategoriSetting object so the UI table reflects the global change
            if subtest_name == "__ALL__":
                kat_setting, _ = KategoriSetting.objects.get_or_create(kategori=kategori)
                kat_setting.soal_per_subtest = soal_tampil
                kat_setting.timer_menit = timer_menit
                kat_setting.save()

            messages.success(
                request,
                f"Sukses! Berhasil mengupdate {count} {target} di kategori '{kategori}' dengan: "
                f"{soal_tampil} soal acak & {timer_menit} menit."
            )
        else:
            messages.warning(request, f"Tidak ditemukan subtest yang cocok untuk kategori '{kategori}'.")

    return redirect("admin_statistik")


@login_required
def admin_change_credentials(request):
    if not request.user.is_staff:
        return redirect("home")

    if request.method == "POST":
        new_username = request.POST.get("username", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        user = request.user

        # ── Validasi Username ──
        if new_username and new_username != user.username:
            if User.objects.filter(username__iexact=new_username).exclude(pk=user.pk).exists():
                messages.error(request, f"Username '{new_username}' sudah digunakan oleh akun pengguna lain.")
                return render(request, "ujian/admin_ubah_akun.html")
            user.username = new_username

        # ── Validasi Password ──
        if new_password:
            if new_password != confirm_password:
                messages.error(request, "Password Baru dan Konfirmasi Password tidak cocok!")
                return render(request, "ujian/admin_ubah_akun.html")
            user.set_password(new_password)

        user.save()
        update_session_auth_hash(request, user)  # Mencegah ter-logout otomatis setelah ganti password

        messages.success(request, "Sukses! Akun Admin (Username & Password) berhasil diperbarui.")
        return redirect("admin_statistik")

    return render(request, "ujian/admin_ubah_akun.html")


@login_required
def admin_delete_peserta(request, user_id):
    if not request.user.is_staff:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Akses ditolak.'}, status=403)
        return redirect("home")

    if request.method == "POST":
        target_user = get_object_or_404(User, id=user_id)
        if target_user.is_superuser or target_user == request.user:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Akun Administrator Utama tidak dapat dihapus!'}, status=400)
            messages.error(request, "Akun Administrator Utama tidak dapat dihapus!")
            return redirect("admin_statistik")

        username = target_user.username
        paket_id = request.GET.get('paket')

        if paket_id:
            JawabanPeserta.objects.filter(user=target_user, paket_id_snapshot=paket_id).delete()
            JawabanPeserta.objects.filter(user=target_user, soal__subtest__paket_id=paket_id).delete()
            SesiUjian.objects.filter(user=target_user, subtest__paket_id=paket_id).delete()
            
            from .models import PaketUjian, HasilPaketUjian
            paket = PaketUjian.objects.filter(id=paket_id).first()
            if paket:
                HasilPaketUjian.objects.filter(user=target_user, paket_nama=paket.nama).delete()
                
            message = f"Riwayat Paket untuk '{username}' telah di-reset."
        else:
            JawabanPeserta.objects.filter(user=target_user).delete()
            SesiUjian.objects.filter(user=target_user).delete()
            target_user.delete()
            message = f"Data peserta '{username}' telah dihapus."

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': message})

        messages.success(request, f"Sukses! {message}")
    return redirect("admin_statistik")


@login_required
def admin_export_peserta_excel(request, user_id):
    if not request.user.is_staff:
        return redirect("home")

    target_user = get_object_or_404(User, id=user_id)
    wb = openpyxl.Workbook()

    header_fill = PatternFill(start_color="FF4D8F", end_color="FF4D8F", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=11, bold=True)
    paket_font = Font(name="Calibri", size=11, bold=True, color="FF4D8F")
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")

    # Sheet 1: Ringkasan Hasil (Format Sesuai Mockup)
    ws1 = wb.active
    ws1.title = "Ringkasan Hasil"
    ws1.append(["PARAMETER HASIL", "NILAI / KETERANGAN", ""])
    for cell in ws1[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_left

    jawaban_qs = JawabanPeserta.objects.filter(user=target_user).select_related('soal', 'soal__subtest', 'soal__subtest__paket')
    total_dijawab = jawaban_qs.count()
    total_benar = sum(1 for j in jawaban_qs if (j.soal and j.jawaban == j.soal.jawaban_benar) or (not j.soal and j.is_benar_snapshot))
    total_salah = total_dijawab - total_benar
    nilai_akhir = round((total_benar / total_dijawab * 100), 1) if total_dijawab > 0 else 0.0
    status_sesi = "SELESAI" if SesiUjian.objects.filter(user=target_user, selesai=True).exists() else "BELUM SELESAI"

    sesi_qs = SesiUjian.objects.filter(user=target_user)
    total_soal_tersedia = 0
    for s in sesi_qs:
        total_soal_tersedia += SoalSesi.objects.filter(sesi=s).count()
    if total_soal_tersedia == 0:
        total_soal_tersedia = total_dijawab

    ws1.append(["Username Peserta", target_user.username, ""])
    ws1.append(["Status Ujian", status_sesi, ""])

    # Grouping per Paket & SubTest
    paket_map = {}
    for j in jawaban_qs:
        st = j.soal.subtest
        if not st:
            continue
        p = st.paket
        p_name = p.nama
        st_name = st.nama

        if p_name not in paket_map:
            paket_map[p_name] = {}
        if st_name not in paket_map[p_name]:
            paket_map[p_name][st_name] = {'benar': 0, 'total': 0}

        paket_map[p_name][st_name]['total'] += 1
        if j.jawaban == j.soal.jawaban_benar:
            paket_map[p_name][st_name]['benar'] += 1

    for p_name, st_dict in paket_map.items():
        ws1.append([p_name, "nilai benar", ""])
        r_idx = ws1.max_row
        ws1.cell(row=r_idx, column=1).font = paket_font
        ws1.cell(row=r_idx, column=2).font = bold_font

        for st_name, counts in st_dict.items():
            ws1.append([f"  {st_name}", counts['benar'], f"dari {counts['total']} soal"])

    ws1.append([]) # Baris kosong

    footer_rows = [
        ("Total Soal Dikerjakan", total_soal_tersedia, "Jumlah soal"),
        ("Total Soal Dijawab", total_dijawab, "yang di kerjakan saja"),
        ("Jumlah Jawaban Benar", total_benar, "yg benar"),
        ("Jumlah Jawaban Salah", total_salah, "yang salah"),
        ("Nilai Akhir (%)", nilai_akhir, "soal benar / jumlah soal"),
    ]

    for param, val, ket in footer_rows:
        ws1.append([param, val, ket])
        r_idx = ws1.max_row
        ws1.cell(row=r_idx, column=1).font = bold_font

    # Sheet 2: Detail Jawaban Soal
    ws2 = wb.create_sheet(title="Detail Jawaban Soal")
    headers2 = ["No", "Kategori", "Paket Ujian", "SubTest", "Pertanyaan Soal", "Jawaban Peserta", "Jawaban Benar", "Status"]
    ws2.append(headers2)
    for cell in ws2[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center

    for idx, item in enumerate(jawaban_qs, 1):
        if item.soal:
            st_nama = item.soal.subtest.nama if item.soal.subtest else "-"
            p_nama = item.soal.subtest.paket.nama if (item.soal.subtest and item.soal.subtest.paket) else "-"
            status_txt = "BENAR" if item.jawaban == item.soal.jawaban_benar else "SALAH"
            kategori_txt = item.soal.get_kategori_display()
            pertanyaan_txt = item.soal.pertanyaan[:150]
            jawaban_benar_txt = item.soal.jawaban_benar
        else:
            st_nama = getattr(item, 'subtest_nama_snapshot', '-') or "-"
            p_nama = getattr(item, 'paket_nama_snapshot', '-') or "-"
            status_txt = "BENAR" if getattr(item, 'is_benar_snapshot', False) else "SALAH"
            kategori_txt = "-"
            pertanyaan_txt = getattr(item, 'pertanyaan_snapshot', '-') or "-"
            jawaban_benar_txt = "-"

        ws2.append([
            idx,
            kategori_txt,
            p_nama,
            st_nama,
            pertanyaan_txt,
            item.jawaban,
            jawaban_benar_txt,
            status_txt
        ])

    for ws in [ws1, ws2]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 15), 60)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="Hasil_Ujian_{target_user.username}.xlsx"'
    wb.save(response)
    return response


@login_required
def admin_export_all_excel(request):
    if not request.user.is_staff:
        return redirect("home")

    wb = openpyxl.Workbook()

    header_fill = PatternFill(start_color="FF4D8F", end_color="FF4D8F", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=11, bold=True)
    align_center = Alignment(horizontal="center", vertical="center")

    # Sheet 1: Rekap Semua Peserta
    ws1 = wb.active
    ws1.title = "Rekap Semua Peserta"

    headers1 = ["No", "Username Peserta", "Status Ujian", "Total Soal Dijawab", "Total Benar", "Total Salah", "Nilai Akhir (%)"]
    ws1.append(headers1)
    for cell in ws1[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center

    semua_user = User.objects.all().order_by('id')

    for idx, u in enumerate(semua_user, 1):
        jawaban = JawabanPeserta.objects.filter(user=u).select_related('soal')
        total_j = jawaban.count()
        benar = sum(1 for j in jawaban if (j.soal and j.jawaban == j.soal.jawaban_benar) or (not j.soal and getattr(j, 'is_benar_snapshot', False)))
        salah = total_j - benar
        nilai = round((benar / total_j * 100), 1) if total_j > 0 else 0.0
        status_txt = "SELESAI" if SesiUjian.objects.filter(user=u, selesai=True).exists() else "BELUM SELESAI"

        ws1.append([idx, u.username, status_txt, total_j, benar, salah, nilai])

    # Sheet 2: Detail Seluruh Jawaban
    ws2 = wb.create_sheet(title="Detail Jawaban Semua Peserta")
    headers2 = ["No", "Username Peserta", "Kategori", "Paket Ujian", "SubTest", "Pertanyaan", "Jawaban Peserta", "Jawaban Benar", "Status"]
    ws2.append(headers2)
    for cell in ws2[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center

    row_idx = 1
    for u in semua_user:
        jawaban_qs = JawabanPeserta.objects.filter(user=u).select_related('soal', 'soal__subtest', 'soal__subtest__paket')
        for item in jawaban_qs:
            if item.soal:
                st_nama = item.soal.subtest.nama if item.soal.subtest else "-"
                p_nama = item.soal.subtest.paket.nama if (item.soal.subtest and item.soal.subtest.paket) else "-"
                status_txt = "BENAR" if item.jawaban == item.soal.jawaban_benar else "SALAH"
                kategori_txt = item.soal.get_kategori_display()
                pertanyaan_txt = item.soal.pertanyaan[:120]
                jawaban_benar_txt = item.soal.jawaban_benar
            else:
                st_nama = getattr(item, 'subtest_nama_snapshot', '-') or "-"
                p_nama = getattr(item, 'paket_nama_snapshot', '-') or "-"
                status_txt = "BENAR" if getattr(item, 'is_benar_snapshot', False) else "SALAH"
                kategori_txt = "-"
                pertanyaan_txt = getattr(item, 'pertanyaan_snapshot', '-') or "-"
                jawaban_benar_txt = "-"

            ws2.append([
                row_idx,
                u.username,
                kategori_txt,
                p_nama,
                st_nama,
                pertanyaan_txt,
                item.jawaban,
                jawaban_benar_txt,
                status_txt
            ])
            row_idx += 1

    for ws in [ws1, ws2]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 15), 50)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="Semua_Hasil_Ujian_Peserta.xlsx"'
    wb.save(response)
    return response


@login_required
def admin_export_soal_excel(request):
    if not request.user.is_staff:
        return redirect("home")

    kategori_filter = request.GET.get("kategori")
    paket_id = request.GET.get("paket")
    subtest_id = request.GET.get("subtest")
    search_q = request.GET.get("q")

    soal_qs = Soal.objects.select_related('subtest', 'subtest__paket').all().order_by('-id')

    if subtest_id:
        soal_qs = soal_qs.filter(subtest__id=subtest_id)
    elif paket_id:
        soal_qs = soal_qs.filter(subtest__paket__id=paket_id)
    elif kategori_filter:
        soal_qs = soal_qs.filter(kategori__iexact=kategori_filter)

    if search_q:
        soal_qs = soal_qs.filter(pertanyaan__icontains=search_q)

    wb = openpyxl.Workbook(write_only=True)
    ws = wb.create_sheet(title="Bank Soal")

    # Header Row
    ws.append([
        "ID Soal",
        "Kategori",
        "Paket Ujian",
        "SubTest",
        "Pertanyaan Soal",
        "Pilihan A",
        "Pilihan B",
        "Pilihan C",
        "Pilihan D",
        "Pilihan E",
        "Jawaban Benar",
        "Pembahasan",
        "Urutan"
    ])

    rows_qs = soal_qs.values_list(
        'id',
        'kategori',
        'subtest__paket__nama',
        'subtest__nama',
        'pertanyaan',
        'pilihan_a',
        'pilihan_b',
        'pilihan_c',
        'pilihan_d',
        'pilihan_e',
        'jawaban_benar',
        'pembahasan',
        'urutan'
    ).iterator()

    for row in rows_qs:
        ws.append([
            row[0],
            row[1],
            row[2] or "",
            row[3] or "",
            row[4] or "",
            row[5] or "",
            row[6] or "",
            row[7] or "",
            row[8] or "",
            row[9] or "",
            row[10] or "",
            row[11] or "",
            row[12] or ""
        ])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="Export_Bank_Soal_Lengkap.xlsx"'
    wb.save(response)
    return response


# ==========================================================
# MODUL MATERI PEMBELAJARAN ANIMASI & SUARA
# ==========================================================

from .materi_data import MATERI_REGISTRY

@login_required
def materi_list(request):
    return render(request, "ujian/materi_list.html", {
        "materi_map": MATERI_REGISTRY
    })

@login_required
def materi_detail_ujian(request, subtest_id):
    subtest = get_object_or_404(SubTest, id=subtest_id)
    slug = subtest.nama.lower().strip()
    materi = MATERI_REGISTRY.get(slug)

    # If no video exists for this subtest, skip video and go straight to test
    if not materi:
        return redirect("start_subtest", kategori=subtest.paket.nama, subtest_id=subtest.id)

    # --- FITUR MOTIVASI & SKIP MATERI (KHUSUS KONSEP DASAR 1) ---
    show_skip_popup = False
    if "konsep dasar 1" in subtest.paket.nama.lower():
        from .models import HasilPaketUjian
        key = subtest.nama.replace(" ", "_")
        
        # Cari HasilPaketUjian terbaru yang mengandung skor untuk subtest ini
        for h in HasilPaketUjian.objects.filter(user=request.user).order_by('-id')[:20]:
            if h.skor_json and key in h.skor_json:
                if float(h.skor_json[key]) > 90.0:
                    show_skip_popup = True
                break # Hanya cek upaya terbaru

    return render(request, "ujian/materi_detail_ujian.html", {
        "materi": materi,
        "slug": slug,
        "subtest": subtest,
        "materi_json": json.dumps(materi),
        "show_skip_popup": show_skip_popup
    })

@login_required
def materi_detail(request, slug):
    materi = MATERI_REGISTRY.get(slug.lower())
    if not materi:
        return redirect("materi_list")
    
    return render(request, "ujian/materi_detail.html", {
        "materi": materi,
        "slug": slug,
        "materi_json": json.dumps(materi)
    })

@login_required
def demo_animasi(request):
    return render(request, "demo_animasi_bersuara.html")
