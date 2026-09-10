import os
import sys
import django
import random

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal, PaketUjian

REFERENCES = [
    "[Syllabus SNBT 2024]",
    "[Syllabus BPPP 2024]",
    "[TKA & SNBT Konsep]",
    "[Materi Wajib UTBK]"
]

def gen_pk():
    materi_list = [
        "Operasi Bilangan", "Persamaan & Pertidaksamaan", "Fungsi & Grafik", 
        "Sistem Persamaan", "Barisan & Deret", "Peluang", "Eksponen", 
        "Trigonometri", "Geometri Bidang", "Geometri Ruang", "Limit", 
        "Turunan", "Integral", "Matriks"
    ]
    topik = random.choice(materi_list)
    x = random.randint(2, 10)
    
    if topik in ["Operasi Bilangan", "Eksponen"]:
        pertanyaan = f"Konsep {topik}: Berapakah nilai dari {x}&sup2; + {x}?"
        ans = str(x**2 + x)
        ops = [ans, str(x**2 - x), str(x**2 + 2*x), str((x+1)**2), str(x**2)]
    elif topik in ["Persamaan & Pertidaksamaan", "Sistem Persamaan"]:
        pertanyaan = f"Konsep {topik}: Jika 2x = {2*x}, berapakah nilai x?"
        ans = str(x)
        ops = [ans, str(x+1), str(x-1), str(x*2), str(x//2)]
    elif topik in ["Peluang", "Barisan & Deret"]:
        pertanyaan = f"Konsep {topik}: Suku pertama deret adalah {x}, beda adalah 2. Suku ke-3 adalah..."
        ans = str(x + 4)
        ops = [ans, str(x + 2), str(x + 6), str(x + 8), str(x)]
    else: # Geometri, Trigonometri, dll
        pertanyaan = f"Konsep {topik}: Jika sisi sebuah kubus adalah {x} cm, maka luas permukaannya adalah..."
        ans = f"{6 * (x**2)} cm&sup2;"
        ops = [ans, f"{4 * (x**2)} cm&sup2;", f"{x**3} cm&sup2;", f"{12 * x} cm&sup2;", f"{8 * x} cm&sup2;"]
        
    return topik, pertanyaan, ops, ans

def gen_pm():
    materi_list = ["Statistika", "Analisis Data & Grafik", "Pemodelan Matematika"]
    topik = random.choice(materi_list)
    base = random.randint(10, 50)
    
    if topik == "Statistika":
        pertanyaan = f"Konsep {topik}: Rata-rata dari data {base}, {base+2}, dan {base+4} adalah..."
        ans = str(base+2)
        ops = [ans, str(base), str(base+4), str(base+1), str(base+3)]
    elif topik == "Analisis Data & Grafik":
        pertanyaan = f"Konsep {topik}: Pada grafik lingkaran, jika suatu sektor memiliki sudut 90&deg;, maka persentasenya adalah..."
        ans = "25%"
        ops = [ans, "20%", "30%", "50%", "90%"]
    else:
        pertanyaan = f"Konsep {topik}: Kecepatan {base} km/jam jika diubah ke bentuk model persamaan v(t) linear konstan adalah..."
        ans = f"v(t) = {base}"
        ops = [ans, f"v(t) = {base}t", f"v(t) = t + {base}", f"v(t) = {base}/t", f"v(t) = {base}&sup2;"]
        
    return topik, pertanyaan, ops, ans

def gen_lbe():
    materi_list = [
        "Kosa Kata (Vocabulary)", "Ide Pokok (Main Idea)", "Informasi Rinci (Detail Information)",
        "Rujukan Teks (Reference)", "Kesimpulan (Inference)", "Sinonim & Antonim",
        "Tata Bahasa Dasar (Grammar Basic)", "Waktu (Tenses)", "Bentuk Pasif (Passive Voice)",
        "Kalimat Bersyarat (Conditional Sentences)", "Klausa Relatif (Relative Clauses)",
        "Subject-Verb Agreement", "Pemahaman Bacaan (Reading Comprehension)",
        "Analisis Wacana (Discourse Analysis)", "Evaluasi Argumen dalam Teks"
    ]
    topik = random.choice(materi_list)
    
    if topik in ["Waktu (Tenses)", "Tata Bahasa Dasar (Grammar Basic)", "Subject-Verb Agreement"]:
        verb = random.choice(["go", "play", "eat", "study"])
        pertanyaan = f"Konsep {topik}: The correct simple past form of '{verb}' is..."
        past_forms = {"go":"went", "play":"played", "eat":"ate", "study":"studied"}
        ans = past_forms[verb]
        ops = [ans, f"{verb}s", f"is {verb}ing", f"has {verb}ed", f"will {verb}"]
    elif topik in ["Sinonim & Antonim", "Kosa Kata (Vocabulary)"]:
        adj = random.choice(["happy", "fast", "big", "smart"])
        pertanyaan = f"Konsep {topik}: What is the closest meaning (synonym) of '{adj}'?"
        syns = {"happy":"joyful", "fast":"quick", "big":"large", "smart":"clever"}
        ans = syns[adj]
        ops = [ans, "sad", "slow", "small", "stupid"]
    elif topik in ["Bentuk Pasif (Passive Voice)", "Kalimat Bersyarat (Conditional Sentences)"]:
        pertanyaan = f"Konsep {topik}: 'The letter ___ by John yesterday.' Choose the correct passive verb."
        ans = "was written"
        ops = [ans, "is written", "writes", "wrote", "has written"]
    else:
        pertanyaan = f"Konsep {topik}: In a reading passage, a statement that summarizes the whole paragraph is called..."
        ans = "Main Idea"
        ops = [ans, "Detail Information", "Supporting Sentence", "Inference", "Reference"]
        
    return topik, pertanyaan, ops, ans

def gen_indo(subtest_type):
    materi_list = [
        "Ide Pokok & Gagasan Utama", "Simpulan Teks", "Informasi Tersurat & Tersirat",
        "Makna Kata & Frasa", "Hubungan Antarparagraf", "Kalimat Efektif",
        "Ejaan & Tanda Baca", "Konjungsi", "Perbaikan Kalimat", "Kepaduan Paragraf",
        "Jenis-Jenis Teks", "Struktur Teks", "Kebahasaan Teks", "Analisis Argumen",
        "Evaluasi Kalimat", "Penalaran Bacaan"
    ]
    topik = random.choice(materi_list)
    
    if "LBI" in subtest_type:
        tema = "Saintek (Sains & Teknologi)" if "SAINTEK" in subtest_type else "Soshum (Sosial Humaniora)"
        teks_saintek = "Penelitian genetika terbaru menunjukkan mutasi DNA tertentu dapat meningkatkan resistensi bakteri."
        teks_soshum = "Perkembangan Revolusi Industri 4.0 berdampak langsung pada stratifikasi sosial masyarakat urban."
        teks = teks_saintek if "SAINTEK" in subtest_type else teks_soshum
        
        if topik in ["Ide Pokok & Gagasan Utama", "Simpulan Teks"]:
            pertanyaan = f"Teks Tema {tema}: <i>'{teks}'</i><br>Konsep {topik} dari kalimat di atas adalah..."
            ans = "Inti utama atau ringkasan gagasan dari teks tersebut."
            ops = [ans, "Informasi pelengkap", "Opini penulis semata", "Data statistik mentah", "Sebuah kutipan langsung"]
        else:
            pertanyaan = f"Teks Tema {tema}: <i>'{teks}'</i><br>Berdasarkan Konsep {topik}, teks di atas berupaya untuk..."
            ans = "Menyampaikan informasi secara logis dan terstruktur."
            ops = [ans, "Menghibur pembaca", "Membujuk pembeli", "Menggambarkan suatu tempat secara fisik", "Menceritakan pengalaman pribadi"]
            
    elif subtest_type == "PBM":
        if topik in ["Ejaan & Tanda Baca", "Kalimat Efektif", "Perbaikan Kalimat", "Konjungsi"]:
            pertanyaan = f"Konsep {topik}: Penggunaan tanda baca atau struktur yang tepat sangat penting. Kata manakah yang baku?"
            ans = "Apotek"
            ops = [ans, "Apotik", "Praktek", "Nasehat", "Resiko"]
        else:
            pertanyaan = f"Konsep {topik}: Ciri utama sebuah paragraf yang baik adalah memiliki kesatuan dan..."
            ans = "Kepaduan (Koherensi)"
            ops = [ans, "Panjang", "Banyak tanda seru", "Opini yang kontroversial", "Subjektivitas"]
            
    else: # PPU
        if topik in ["Makna Kata & Frasa", "Hubungan Antarparagraf", "Informasi Tersurat & Tersirat"]:
            pertanyaan = f"Konsep {topik}: Makna konotatif berbeda dengan denotatif. Makna denotatif adalah..."
            ans = "Makna sebenarnya (kamus)"
            ops = [ans, "Makna kiasan", "Makna ganda", "Makna sindiran", "Makna yang tidak jelas"]
        else:
            pertanyaan = f"Konsep {topik}: Untuk menghubungkan dua kalimat yang bertentangan, konjungsi yang tepat adalah..."
            ans = "Namun"
            ops = [ans, "Oleh karena itu", "Dan", "Sehingga", "Dengan demikian"]
            
    return topik, pertanyaan, ops, ans

def gen_pu():
    topik = random.choice(["Silogisme", "Penalaran Analitik", "Kecukupan Data"])
    nama = random.choice(["A", "B", "C"])
    if topik == "Silogisme":
        pertanyaan = f"Konsep Dasar Logika: Jika p &rarr; q dan q &rarr; r, maka kesimpulannya adalah..."
        ans = "p &rarr; r"
        ops = [ans, "r &rarr; p", "q &rarr; p", "p &rarr; q", "r &rarr; q"]
    elif topik == "Penalaran Analitik":
        pertanyaan = f"Konsep Dasar Posisi: Jika {nama} berada di depan D, dan D di depan E, siapa yang paling depan?"
        ans = nama
        ops = [ans, "D", "E", "Tidak ada", "Semua sama"]
    else:
        pertanyaan = f"Konsep {topik}: Jika diketahui x = 5, apakah cukup untuk mencari nilai y jika y = x + 2?"
        ans = "Cukup"
        ops = [ans, "Tidak Cukup", "Mungkin", "Bergantung nilai z", "Mustahil"]
    return topik, pertanyaan, ops, ans


def run():
    packages = PaketUjian.objects.filter(nama__icontains="Konsep Dasar 1.").order_by('id')
    total = 0
    target_packages = []
    
    for pkt in packages:
        try:
            num_str = pkt.nama.split("Konsep Dasar 1.")[1].strip()
            num = int(num_str)
            if 6 <= num <= 50:
                target_packages.append(pkt)
        except:
            pass
            
    print(f"Ditemukan {len(target_packages)} paket Konsep Dasar (1.6 - 1.50) untuk kurikulum V3.")
    
    for paket in target_packages:
        print(f"Memproses {paket.nama}...")
        for st in paket.subtests.all():
            lama = st.soal.all()
            if lama.exists():
                lama.delete()
                
            soal_list = []
            st_name = st.nama.upper()
            
            for _ in range(40):
                if st_name == "PU":
                    topik, pert, ops, ans = gen_pu()
                elif st_name == "PK":
                    topik, pert, ops, ans = gen_pk()
                elif st_name == "PM":
                    topik, pert, ops, ans = gen_pm()
                elif st_name == "LBE":
                    topik, pert, ops, ans = gen_lbe()
                else: # PBM, PPU, LBI SAINTEK, LBI SOSHUM
                    topik, pert, ops, ans = gen_indo(st_name)
                    
                random.shuffle(ops)
                ops = list(set(ops))
                counter = 1
                while len(ops) < 5:
                    ops.append(f"{ops[0]} (var {counter})")
                    ops = list(set(ops))
                    counter += 1
                    
                random.shuffle(ops)
                kunci = chr(65 + ops.index(ans))
                
                soal_list.append(Soal(
                    subtest=st, kategori="KD1", pertanyaan=pert,
                    pilihan_a=ops[0], pilihan_b=ops[1], pilihan_c=ops[2], pilihan_d=ops[3], pilihan_e=ops[4],
                    jawaban_benar=kunci,
                    pembahasan="Pembahasan Teori Dasar Kurikulum SNBT.", referensi_internal=random.choice(REFERENCES),
                    topik_materi=topik
                ))
            Soal.objects.bulk_create(soal_list)
            total += len(soal_list)
            
    print(f"Sukses menggenerate {total} soal konsep dasar dengan kurikulum tabel V3 untuk 45 paket.")

if __name__ == "__main__":
    run()
