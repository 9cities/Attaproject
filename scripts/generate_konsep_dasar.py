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
    "[Fundamental BP3 2024]",
    "[Konsep Dasar GO]",
    "[Teori Dasar Pahamify]",
    "[Basic SNBT Mantappu]",
    "[Inten Foundation]"
]

NAMES = ["Andi", "Budi", "Cici", "Deni", "Eka", "Fani", "Gilang", "Hani", "Iwan", "Joko"]
SUBJECTS = ["Kucing", "Anjing", "Burung", "Ikan", "Kelinci"]
PROFESSIONS = ["Dokter", "Guru", "Polisi", "Petani", "Ilmuwan"]

def gen_pk():
    topik = random.choice(["Aljabar Dasar", "Operasi Pecahan", "Aritmatika Dasar"])
    if topik == "Aljabar Dasar":
        a = random.randint(2, 9)
        b = random.randint(1, 20)
        c = random.randint(10, 50)
        pertanyaan = f"Konsep Aljabar: Jika {a}x - {b} = {c}, maka nilai x yang memenuhi persamaan tersebut adalah..."
        # a*x = c + b => x = (c+b)/a. To make it exact, let's redefine c
        x_val = random.randint(2, 12)
        c = (a * x_val) - b
        pertanyaan = f"Konsep Aljabar: Jika {a}x - {b} = {c}, maka nilai x yang memenuhi persamaan tersebut adalah..."
        ans = str(x_val)
        ops = [ans, str(x_val+1), str(x_val-1), str(x_val+2), str(x_val-2)]
    elif topik == "Operasi Pecahan":
        a = random.randint(1, 5)
        b = random.randint(2, 5)
        c = random.randint(1, 5)
        pertanyaan = f"Konsep Pecahan: Berapakah hasil dari ({a}/{b}) &times; {c}?"
        ans = f"{a*c}/{b}"
        ops = [ans, f"{a*c+1}/{b}", f"{a*c}/{b+1}", f"{a}/{b*c}", f"{a+c}/{b}"]
    else:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        pertanyaan = f"Konsep Aritmatika: Hasil penjumlahan {a} dan {b} dikurangi 10 adalah..."
        ans = str(a + b - 10)
        ops = [ans, str(a+b), str(a+b-5), str(a+b-15), str(a+b+10)]
    return topik, pertanyaan, ops, ans

def gen_pm():
    topik = random.choice(["Konsep Diskon", "Konsep Jarak Kecepatan", "Konsep Skala"])
    if topik == "Konsep Diskon":
        harga = random.choice([50000, 100000, 150000, 200000])
        diskon = random.choice([10, 20, 25, 50])
        pertanyaan = f"Konsep Diskon: Sebuah barang seharga Rp{harga:,} didiskon sebesar {diskon}%. Berapa besar potongan harga yang didapat?"
        ans = f"Rp{int(harga * diskon / 100):,}"
        ops = [ans, f"Rp{int(harga * (diskon+10) / 100):,}", f"Rp{int(harga * (diskon-5) / 100):,}", f"Rp{int(harga * 0.9):,}", f"Rp{int(harga):,}"]
    elif topik == "Konsep Jarak Kecepatan":
        v = random.choice([40, 50, 60, 80])
        t = random.choice([2, 3, 4, 5])
        pertanyaan = f"Konsep Kecepatan: Jika sebuah mobil melaju dengan kecepatan {v} km/jam selama {t} jam, maka jarak yang ditempuh adalah..."
        ans = f"{v*t} km"
        ops = [ans, f"{v*t + 10} km", f"{v*t - 20} km", f"{v+t} km", f"{v*t + 40} km"]
    else:
        jarak_peta = random.randint(2, 8)
        skala = random.choice([1000, 5000, 10000])
        pertanyaan = f"Konsep Skala: Jarak pada peta adalah {jarak_peta} cm dengan skala 1:{skala:,}. Berapa cm jarak sebenarnya?"
        ans = f"{jarak_peta * skala:,} cm"
        ops = [ans, f"{jarak_peta * skala + 1000:,} cm", f"{jarak_peta * skala - 1000:,} cm", f"{skala // jarak_peta:,} cm", f"{jarak_peta * skala * 10:,} cm"]
    return topik, pertanyaan, ops, ans

def gen_pu():
    topik = random.choice(["Modus Ponens", "Modus Tollens", "Negasi Pernyataan"])
    A = random.choice(["hujan", "panas", "mendung"])
    B = random.choice(["bawa payung", "diam di rumah", "tidur"])
    if topik == "Modus Ponens":
        pertanyaan = f"Teori Dasar (Modus Ponens): Premis 1: Jika hari ini {A}, maka saya {B}. Premis 2: Hari ini {A}. Kesimpulan yang sah adalah..."
        ans = f"Saya {B}."
        ops = [ans, f"Saya tidak {B}.", f"Hari ini tidak {A}.", f"Saya {B} dan hari ini {A}.", "Tidak ada kesimpulan sah."]
    elif topik == "Modus Tollens":
        pertanyaan = f"Teori Dasar (Modus Tollens): Premis 1: Jika hari ini {A}, maka saya {B}. Premis 2: Saya tidak {B}. Kesimpulan yang sah adalah..."
        ans = f"Hari ini tidak {A}."
        ops = [ans, f"Hari ini {A}.", f"Saya {B}.", f"Mungkin hari ini {A}.", "Tidak ada kesimpulan sah."]
    else:
        obj = random.choice(SUBJECTS)
        pertanyaan = f"Konsep Logika: Ingkaran (negasi) dari pernyataan 'Semua {obj} bernapas dengan insang' adalah..."
        ans = f"Ada {obj} yang tidak bernapas dengan insang."
        ops = [ans, f"Semua {obj} tidak bernapas dengan insang.", f"Tidak ada {obj} yang bernapas dengan insang.", f"Beberapa {obj} bernapas dengan paru-paru.", f"Sebagian {obj} bernapas dengan insang."]
    return topik, pertanyaan, ops, ans

def gen_ppu():
    topik = random.choice(["Makna Kata", "Sinonim Dasar", "Antonim Dasar"])
    kata = random.choice(["fluktuasi", "signifikan", "stagnan", "inovasi", "efektif"])
    if topik == "Makna Kata":
        arti = {"fluktuasi": "gejala naik turunnya harga", "signifikan": "berarti/penting", "stagnan": "keadaan terhenti/tidak bergerak", "inovasi": "penemuan baru", "efektif": "berhasil guna"}
        pertanyaan = f"Konsep Kosakata: Menurut KBBI, makna dari kata '{kata}' adalah..."
        ans = arti[kata]
        ops = [ans, "Sesuatu yang tidak berguna", "Pergerakan maju secara lambat", "Keadaan tanpa arah", "Proses penguraian unsur"]
    elif topik == "Sinonim Dasar":
        sin = {"fluktuasi": "Goncangan", "signifikan": "Penting", "stagnan": "Mandek", "inovasi": "Pembaruan", "efektif": "Manjur"}
        pertanyaan = f"Konsep Kosakata: Padanan kata (sinonim) yang tepat untuk kata '{kata}' adalah..."
        ans = sin[kata]
        ops = [ans, "Konstan", "Biasa", "Mundur", "Kuno"]
    else:
        ant = {"fluktuasi": "Stabil", "signifikan": "Sepele", "stagnan": "Dinamis", "inovasi": "Konservasi", "efektif": "Mubazir"}
        pertanyaan = f"Konsep Kosakata: Lawan kata (antonim) yang tepat untuk kata '{kata}' adalah..."
        ans = ant[kata]
        ops = [ans, "Penting", "Berubah", "Lama", "Cepat"]
    return topik, pertanyaan, ops, ans

def gen_pbm():
    topik = random.choice(["Penggunaan Preposisi", "Huruf Kapital", "Kata Baku"])
    nama = random.choice(NAMES)
    if topik == "Penggunaan Preposisi":
        pertanyaan = f"Konsep EBI: Manakah penulisan kata depan 'di' yang TEPAT?"
        ans = f"{nama} sedang belajar di rumah."
        ops = [ans, f"Buku itu sedang dibaca diperpustakaan.", f"Dia di pukul oleh temannya.", f"{nama} meletakkan sepatu di rak, lalu di tinggal pergi.", f"Pintu itu di buka dari luar."]
    elif topik == "Huruf Kapital":
        pertanyaan = f"Konsep EBI: Penggunaan huruf kapital yang TEPAT terdapat pada kalimat..."
        ans = f"{nama} lahir pada bulan Agustus."
        ops = [ans, f"{nama} suka makan Jeruk Bali.", f"Dia berenang menyeberangi selat sunda.", f"Saya membaca novel Laskar pelangi.", f"Ayah berangkat ke Kota surabaya."]
    else:
        pertanyaan = f"Konsep EBI: Manakah kelompok kata berikut yang semuanya merupakan KATA BAKU?"
        ans = "Apotek, analisis, aktivitas"
        ops = [ans, "Apotik, analisa, aktifitas", "Apotek, analisa, aktivitas", "Apotik, analisis, aktifitas", "Apotek, analisis, aktifitas"]
    return topik, pertanyaan, ops, ans

def gen_lbi():
    topik = random.choice(["Struktur Kalimat", "Konjungsi Dasar", "Pengertian Fakta/Opini"])
    if topik == "Struktur Kalimat":
        nama = random.choice(NAMES)
        pertanyaan = f"Konsep LBI: Dalam kalimat '{nama} membaca buku di perpustakaan', kata 'buku' menduduki fungsi sebagai..."
        ans = "Objek"
        ops = [ans, "Subjek", "Predikat", "Keterangan Tempat", "Keterangan Waktu"]
    elif topik == "Konjungsi Dasar":
        pertanyaan = "Konsep LBI: Konjungsi yang digunakan untuk menyatakan 'pertentangan' adalah..."
        ans = "Tetapi, sedangkan, namun"
        ops = [ans, "Dan, serta, lalu", "Atau, maupun", "Jika, maka, andai", "Karena, sebab, oleh karena itu"]
    else:
        pertanyaan = "Konsep LBI: Pernyataan yang berisi gagasan, pendapat, atau prediksi seseorang dan belum dapat dibuktikan kebenarannya disebut..."
        ans = "Opini"
        ops = [ans, "Fakta", "Asumsi Murni", "Aksioma", "Hipotesis"]
    return topik, pertanyaan, ops, ans

def gen_lbe():
    topik = random.choice(["Basic Vocabulary", "Tenses Concept", "Pronoun Concept"])
    nama = random.choice(NAMES)
    if topik == "Basic Vocabulary":
        pertanyaan = "Concept of LBE: What is the antonym of the word 'ABUNDANT'?"
        ans = "Scarce"
        ops = [ans, "Plentiful", "Large", "Heavy", "Empty"]
    elif topik == "Tenses Concept":
        pertanyaan = f"Concept of LBE: Choose the correct verb form: 'Yesterday, {nama} ___ to the market.'"
        ans = "went"
        ops = [ans, "go", "goes", "gone", "going"]
    else:
        pertanyaan = f"Concept of LBE: '{nama} is a good student. ___ always does ___ homework.' The correct pronouns are..."
        ans = "He, his (or She, her)"
        ops = [ans, "They, their", "It, its", "Him, his", "We, our"]
    return topik, pertanyaan, ops, ans

def run():
    packages = PaketUjian.objects.filter(nama__icontains="Konsep Dasar 1.").order_by('id')
    total = 0
    target_packages = []
    
    # Filter KD 1.6 to 1.50
    for pkt in packages:
        try:
            num_str = pkt.nama.split("Konsep Dasar 1.")[1].strip()
            num = int(num_str)
            if 6 <= num <= 50:
                target_packages.append(pkt)
        except:
            pass
            
    print(f"Ditemukan {len(target_packages)} paket Konsep Dasar (1.6 - 1.50).")
    
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
                elif st_name == "PPU":
                    topik, pert, ops, ans = gen_ppu()
                elif st_name == "PBM":
                    topik, pert, ops, ans = gen_pbm()
                elif st_name == "PK":
                    topik, pert, ops, ans = gen_pk()
                elif "LBI" in st_name:
                    topik, pert, ops, ans = gen_lbi()
                elif "LBE" in st_name:
                    topik, pert, ops, ans = gen_lbe()
                elif "PM" in st_name:
                    topik, pert, ops, ans = gen_pm()
                else:
                    topik, pert, ops, ans = gen_pu()
                    
                random.shuffle(ops)
                ops = list(set(ops))
                counter = 1
                while len(ops) < 5:
                    ops.append(f"{ops[0]} (variasi {counter})")
                    ops = list(set(ops))
                    counter += 1
                random.shuffle(ops)
                kunci = chr(65 + ops.index(ans))
                
                soal_list.append(Soal(
                    subtest=st, kategori="KD1", pertanyaan=pert,
                    pilihan_a=ops[0], pilihan_b=ops[1], pilihan_c=ops[2], pilihan_d=ops[3], pilihan_e=ops[4],
                    jawaban_benar=kunci,
                    pembahasan="Pembahasan Teori Dasar.", referensi_internal=random.choice(REFERENCES),
                    topik_materi=topik
                ))
            Soal.objects.bulk_create(soal_list)
            total += len(soal_list)
            
    print(f"Sukses menggenerate {total} soal konsep dasar untuk {len(target_packages)} paket.")

if __name__ == "__main__":
    run()
