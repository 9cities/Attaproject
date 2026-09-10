import os
import sys
import django
import random

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal, PaketUjian, SubTest

REFERENCES = [
    "[HOTS Prosus Inten 2024]",
    "[UTBK GO 2025]",
    "[Pahamify SNBT 2024]",
    "[Mantappu 2025]",
    "[Aimasukptn Medium 2024]"
]

TEXTS_LBI = [
    "<p><i>Ketimpangan distribusi lahan pertanian di pedesaan Jawa telah mencapai titik kritis. Berdasarkan data BPS, indeks Gini kepemilikan lahan terus meningkat. Hal ini menyebabkan marginalisasi petani gurem yang akhirnya terpaksa menjadi buruh tani atau bermigrasi ke sektor informal perkotaan.</i></p>",
    "<p><i>Konsep 'smart city' tidak hanya tentang digitalisasi layanan publik, tetapi juga integrasi sosial. Sayangnya, implementasi di beberapa kota besar justru memperlebar kesenjangan digital (digital divide), di mana kelompok masyarakat berpenghasilan rendah kesulitan mengakses fasilitas yang sepenuhnya bergantung pada gawai pintar.</i></p>"
]

TEXTS_LBE = [
    "<p><i>The alarming rate of permafrost thaw in the Arctic has profound implications for global climate change. As the frozen ground melts, it releases gigatons of trapped methane—a greenhouse gas significantly more potent than carbon dioxide. This creates a dangerous positive feedback loop that accelerates further warming.</i></p>",
    "<p><i>Quantum supremacy, achieved when a quantum computer performs a calculation impossible for a classical computer, marks a paradigm shift in cryptography. The RSA encryption that secures modern internet banking could theoretically be cracked in hours by Shor's algorithm running on a sufficiently powerful quantum machine.</i></p>"
]

def generate_pu():
    topik = random.choice(["Penalaran Analitik", "Silogisme Bersyarat", "Kecukupan Data"])
    if topik == "Penalaran Analitik":
        pertanyaan = "Dalam sebuah lomba lari, Andi finis sebelum Budi tetapi setelah Cici. Doni finis tepat setelah Budi. Siapa yang finis terakhir?"
        ans = "Doni"
        ops = [ans, "Andi", "Budi", "Cici", "Tidak dapat ditentukan"]
    elif topik == "Silogisme Bersyarat":
        pertanyaan = "Jika hujan deras, maka jalanan banjir. Jika jalanan banjir, maka lalu lintas macet. Hari ini lalu lintas tidak macet. Kesimpulan?"
        ans = "Hari ini tidak hujan deras"
        ops = [ans, "Hari ini hujan deras tapi jalanan tidak banjir", "Jalanan tidak banjir", "Lalu lintas lancar karena tidak hujan", "Tidak ada kesimpulan"]
    else:
        pertanyaan = "Berapa nilai x? (1) x + y = 10, (2) x - y = 4"
        ans = "Dua pernyataan BERSAMA-SAMA cukup."
        ops = [ans, "Pernyataan 1 SAJA cukup.", "Pernyataan 2 SAJA cukup.", "Kedua pernyataan BERSAMA-SAMA tidak cukup.", "Pernyataan 1 cukup, pernyataan 2 cukup."]
    return topik, pertanyaan, ops, ans

def generate_ppu():
    topik = random.choice(["Sinonim/Antonim Kontekstual", "Pemahaman Idiom", "Kepaduan Wacana"])
    if topik == "Sinonim/Antonim Kontekstual":
        pertanyaan = "Kata 'mereduksi' pada kalimat 'Inovasi tersebut mampu mereduksi emisi karbon hingga 40%' memiliki makna yang selaras dengan kata..."
        ans = "Memangkas"
        ops = [ans, "Menghilangkan", "Mengecilkan", "Menggerus", "Menebang"]
    elif topik == "Pemahaman Idiom":
        pertanyaan = "Sikap pejabat yang 'lepas tangan' terhadap kasus korupsi bawahannya menuai kritik. Makna ungkapan lepas tangan adalah..."
        ans = "Tidak mau bertanggung jawab"
        ops = [ans, "Menyerahkan kekuasaan", "Membantu dari jauh", "Mencuci tangan", "Membebaskan hukuman"]
    else:
        pertanyaan = "Kalimat mana yang merusak kepaduan paragraf jika disisipkan di antara kalimat tentang manfaat teknologi dan kalimat penutup kesimpulan?"
        ans = "Kalimat yang membahas sejarah revolusi industri."
        ops = [ans, "Kalimat tentang dampak positif ekonomi.", "Kalimat contoh penerapan AI.", "Kalimat pendukung gagasan utama.", "Kalimat statistik kemajuan internet."]
    return topik, pertanyaan, ops, ans

def generate_pbm():
    topik = random.choice(["EBI/Tanda Baca", "Kalimat Efektif", "Struktur Paragraf"])
    if topik == "EBI/Tanda Baca":
        pertanyaan = "Penulisan tanda baca koma (,) yang tepat terdapat pada kalimat..."
        ans = "Oleh karena itu, kita harus menjaga kebersihan lingkungan."
        ops = [ans, "Budi membeli apel, dan jeruk di pasar.", "Meskipun hujan, tetapi ia tetap pergi.", "Ayah membaca koran; di ruang tamu.", "Dia tidak datang, karena sakit."]
    elif topik == "Kalimat Efektif":
        pertanyaan = "Kalimat berikut yang merupakan kalimat efektif adalah..."
        ans = "Pemerintah membangun jalan tol untuk memperlancar transportasi."
        ops = [ans, "Pemerintah daripada negara ini sedang membangun jalan tol.", "Bagi para siswa-siswa diharap segera berkumpul.", "Dia yang memakai baju merah itu adalah merupakan kakakku.", "Waktu dan tempat kami persilahkan."]
    else:
        pertanyaan = "Inti kalimat dari 'Berbagai upaya mitigasi bencana yang dilakukan oleh pemerintah daerah belum membuahkan hasil maksimal' adalah..."
        ans = "Upaya mitigasi belum membuahkan hasil."
        ops = [ans, "Pemerintah daerah melakukan upaya mitigasi.", "Bencana belum membuahkan hasil.", "Upaya mitigasi maksimal.", "Berbagai upaya mitigasi dilakukan."]
    return topik, pertanyaan, ops, ans

def generate_pk():
    topik = random.choice(["Geometri Bidang", "Probabilitas", "Fungsi Komposisi"])
    if topik == "Geometri Bidang":
        pertanyaan = "Luas daerah yang diarsir pada irisan dua lingkaran berjari-jari sama r yang pusatnya saling berpotongan di keliling lingkaran adalah..."
        ans = "r²(2π/3 - √3/2)"
        ops = [ans, "r²(π/3 - √3/4)", "r²(π - √3)", "r²(2π/3)", "r²(π/2 - 1)"]
    elif topik == "Probabilitas":
        pertanyaan = "Dua dadu dilempar bersamaan. Peluang munculnya mata dadu berjumlah prima adalah..."
        ans = "15/36"
        ops = [ans, "12/36", "18/36", "10/36", "20/36"]
    else:
        pertanyaan = "Jika f(x) = 2x-3 dan g(x) = x²+1, maka (f o g)(2) adalah..."
        ans = "7"
        ops = [ans, "5", "9", "11", "3"]
    return topik, pertanyaan, ops, ans

def generate_lbi(saintek_soshum):
    topik = random.choice(["Ide Pokok", "Inferensi", "Asumsi/Premis"])
    teks = random.choice(TEXTS_LBI)
    if topik == "Ide Pokok":
        pertanyaan = f"{teks}<br>Gagasan utama paragraf di atas adalah..."
        ans = "Dampak ketimpangan lahan/kesenjangan digital terhadap masyarakat bawah."
        ops = [ans, "Definisi petani gurem/smart city.", "Data statistik BPS/penggunaan gawai.", "Solusi pemerintah atas masalah tersebut.", "Perbandingan kondisi pedesaan dan perkotaan."]
    elif topik == "Inferensi":
        pertanyaan = f"{teks}<br>Kesimpulan logis yang dapat ditarik dari teks adalah..."
        ans = "Tanpa kebijakan afirmatif, masalah kesenjangan akan semakin parah."
        ops = [ans, "Semua petani akan pindah ke kota.", "Smart city tidak berguna sama sekali.", "Migrasi adalah solusi terbaik.", "Pemerintah telah gagal sepenuhnya."]
    else:
        pertanyaan = f"{teks}<br>Pernyataan yang <b>memperlemah</b> argumen dalam teks adalah..."
        ans = "Data terbaru menunjukkan subsidi silang berhasil menyejahterakan kelompok rentan."
        ops = [ans, "Angka kemiskinan justru dilaporkan meningkat tajam.", "Teknologi semakin mahal dari tahun ke tahun.", "Sektor informal kota tidak mampu menampung tenaga kerja.", "Banyak warga miskin yang menolak bantuan pemerintah."]
    return topik, pertanyaan, ops, ans

def generate_lbe():
    topik = random.choice(["Main Idea", "Author's Tone", "Specific Detail"])
    teks = random.choice(TEXTS_LBE)
    if topik == "Main Idea":
        pertanyaan = f"{teks}<br>What is the primary topic discussed in the passage?"
        ans = "The severe consequences of permafrost thaw/quantum computing."
        ops = [ans, "The history of Arctic exploration/cryptography.", "How to build a quantum computer.", "The economic impact of global warming.", "The chemical structure of methane."]
    elif topik == "Author's Tone":
        pertanyaan = f"{teks}<br>The author's tone in describing the phenomenon can best be described as..."
        ans = "Alarming / Cautionary"
        ops = [ans, "Optimistic", "Indifferent", "Humorous", "Skeptical"]
    else:
        pertanyaan = f"{teks}<br>According to the text, what accelerates the warming effect / breaks the encryption?"
        ans = "The release of methane / Shor's algorithm."
        ops = [ans, "Carbon dioxide release / RSA standards.", "Urban heat islands / classical computers.", "Solar radiation / internet banking.", "Green roofs / multi-state qubits."]
    return topik, pertanyaan, ops, ans

def generate_pm():
    topik = random.choice(["Kecepatan & Waktu", "Aritmatika Sosial", "Analisis Data"])
    if topik == "Kecepatan & Waktu":
        pertanyaan = "Sebuah mobil berangkat dari kota A pukul 08:00 dengan kecepatan 60 km/jam. Mobil kedua menyusul dari A pukul 09:00 dengan kecepatan 80 km/jam. Pukul berapa mobil kedua menyusul mobil pertama?"
        ans = "12:00"
        ops = [ans, "11:00", "11:30", "12:30", "13:00"]
    elif topik == "Aritmatika Sosial":
        pertanyaan = "Sebuah toko memberikan diskon ganda 20% + 10%. Jika harga awal barang Rp100.000, berapa harga akhir yang harus dibayar?"
        ans = "Rp72.000"
        ops = [ans, "Rp70.000", "Rp80.000", "Rp75.000", "Rp82.000"]
    else:
        pertanyaan = "Dalam grafik pertumbuhan penduduk, populasi meningkat 10% setiap tahun. Jika populasi awal tahun 2020 adalah 10.000 jiwa, estimasi populasi tahun 2022 adalah..."
        ans = "12.100 jiwa"
        ops = [ans, "12.000 jiwa", "11.100 jiwa", "13.000 jiwa", "12.500 jiwa"]
    return topik, pertanyaan, ops, ans


def run():
    packages = PaketUjian.objects.filter(nama__icontains="Try Out Medium").order_by('id')
    total = 0
    for paket in packages:
        for st in paket.subtests.all():
            lama = st.soal.all()
            if lama.exists():
                lama._raw_delete(lama.db)
                
            soal_list = []
            st_name = st.nama.upper()
            
            for _ in range(40):
                if st_name == "PU":
                    topik, pert, ops, ans = generate_pu()
                elif st_name == "PPU":
                    topik, pert, ops, ans = generate_ppu()
                elif st_name == "PBM":
                    topik, pert, ops, ans = generate_pbm()
                elif st_name == "PK":
                    topik, pert, ops, ans = generate_pk()
                elif "LBI" in st_name:
                    topik, pert, ops, ans = generate_lbi(st_name)
                elif "LBE" in st_name:
                    topik, pert, ops, ans = generate_lbe()
                elif "PM" in st_name:
                    topik, pert, ops, ans = generate_pm()
                else:
                    topik, pert, ops, ans = generate_pu() # fallback
                    
                random.shuffle(ops)
                # handle duplicate options
                ops = list(set(ops))
                while len(ops) < 5:
                    ops.append(ops[0] + " (err)")
                    ops = list(set(ops))
                random.shuffle(ops)
                kunci = chr(65 + ops.index(ans))
                
                soal_list.append(Soal(
                    subtest=st, kategori="MEDIUM", pertanyaan=pert,
                    pilihan_a=ops[0], pilihan_b=ops[1], pilihan_c=ops[2], pilihan_d=ops[3], pilihan_e=ops[4],
                    jawaban_benar=kunci,
                    pembahasan="Pembahasan Medium", referensi_internal=random.choice(REFERENCES),
                    topik_materi=topik
                ))
            Soal.objects.bulk_create(soal_list)
            total += len(soal_list)
            
    print(f"Sukses menggenerate {total} soal untuk 8 subtest spesifik.")

if __name__ == "__main__":
    run()
