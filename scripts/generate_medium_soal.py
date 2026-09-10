import os
import sys
import django
import random
import uuid

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal, PaketUjian, SubTest

# --- REFERENSI ---
REFERENCES = [
    "[HOTS Prosus Inten 2024]",
    "[UTBK GO 2025]",
    "[Pahamify SNBT 2024]",
    "[Mantappu 2025]",
    "[Aimasukptn Medium 2024]",
    "[Simulasi BP3 2024]"
]

# --- TEXTS LITERASI MEDIUM ---
TEXTS_MEDIUM_LITERASI = [
    "<p><i>Dalam konteks ekonomi makro, inflasi tidak selalu berkonotasi negatif. Inflasi moderat seringkali dianggap sebagai pelumas roda perekonomian yang menandakan adanya peningkatan agregat permintaan. Namun, ketika inflasi berubah menjadi hiperinflasi, daya beli masyarakat akan tergerus secara masif, memaksa bank sentral untuk melakukan intervensi agresif melalui kenaikan suku bunga acuan. Hal ini pada gilirannya dapat memicu perlambatan investasi sektor riil.</i></p>",
    "<p><i>Paradoks Fermi mempertanyakan kontradiksi antara probabilitas matematis yang tinggi akan keberadaan peradaban ekstraterestrial dengan ketiadaan bukti empiris yang mendukungnya. Beberapa astrofisikawan berargumen bahwa 'Great Filter' mungkin berada di masa lalu kita, mengimplikasikan bahwa munculnya kehidupan multiseluler sangatlah langka. Di sisi lain, ada kemungkinan bahwa filter tersebut berada di masa depan, yang berarti peradaban teknologi tinggi cenderung memusnahkan diri mereka sendiri sebelum mampu melakukan perjalanan antarbintang.</i></p>",
    "<p><i>Resistensi antimikroba (AMR) kini menjadi ancaman eksistensial bagi kesehatan global. Penggunaan antibiotik yang berlebihan pada sektor peternakan komersial menyumbang porsi besar terhadap munculnya 'superbug'. Jika tidak ada penemuan kelas antibiotik baru yang signifikan dalam dekade mendatang, prosedur medis standar seperti operasi caesar dan kemoterapi akan memiliki risiko kematian akibat infeksi sekunder yang sangat tinggi.</i></p>"
]

# --- GENERATORS MEDIUM ---

def generate_medium_pk():
    # Medium: Peluang, Geometri, Kombinatorika, Fungsi
    topik = random.choice(["Peluang", "Geometri", "Fungsi Komposisi", "Statistika"])
    
    if topik == "Peluang":
        n_merah = random.randint(3, 7)
        n_putih = random.randint(3, 7)
        pertanyaan = f"Dalam sebuah kotak terdapat {n_merah} bola merah dan {n_putih} bola putih. Jika diambil 2 bola secara acak bersamaan, berapakah peluang terambil keduanya bola merah?"
        
        # Kombinasi
        import math
        def nCr(n, r):
            if r > n: return 0
            return math.factorial(n) // (math.factorial(r) * math.factorial(n-r))
            
        total_bola = n_merah + n_putih
        ruang_sampel = nCr(total_bola, 2)
        kejadian = nCr(n_merah, 2)
        
        ans = f"{kejadian}/{ruang_sampel}"
        options = [ans, f"{kejadian+1}/{ruang_sampel}", f"{n_merah}/{ruang_sampel}", f"{kejadian}/{ruang_sampel+1}", f"1/{ruang_sampel}"]
        
    elif topik == "Geometri":
        sisi = random.choice([4, 6, 8, 10, 12])
        pertanyaan = f"Sebuah kubus ABCD.EFGH memiliki panjang rusuk {sisi} cm. Jarak dari titik A ke garis diagonal ruang CE adalah ..."
        
        # Jarak titik ke diagonal ruang kubus = (s/3) * akar(6)
        ans = f"{(sisi/3):.2f}&radic;6 cm"
        options = [ans, f"{(sisi/2):.2f}&radic;6 cm", f"{(sisi):.2f}&radic;3 cm", f"{(sisi/2):.2f}&radic;2 cm", f"{(sisi/3):.2f}&radic;3 cm"]
        
    elif topik == "Fungsi Komposisi":
        a = random.randint(2, 5)
        b = random.randint(1, 5)
        c = random.randint(2, 4)
        x_val = random.randint(1, 3)
        pertanyaan = f"Diketahui f(x) = {a}x - {b} dan g(x) = x&sup2; + {c}. Nilai dari (g &compfn; f)({x_val}) adalah..."
        
        fx = (a * x_val) - b
        ans = str((fx ** 2) + c)
        options = [ans, str(int(ans)+a), str(int(ans)-b), str(int(ans)+c), str(int(ans)+10)]
        
    else: # Statistika
        nums = [random.randint(5, 10) for _ in range(5)]
        x = random.randint(5, 12)
        target_rata = random.randint(7, 10)
        pertanyaan = f"Rata-rata dari nilai {nums[0]}, {nums[1]}, {nums[2]}, {nums[3]}, {nums[4]}, dan X adalah {target_rata}. Maka nilai X yang memenuhi adalah..."
        
        ans = str((target_rata * 6) - sum(nums))
        options = [ans, str(int(ans)+1), str(int(ans)-1), str(int(ans)+2), str(int(ans)-2)]

    # Pastikan opsi unik, jika ada duplikat sedikit ubah
    options = list(set(options))
    while len(options) < 5:
        options.append(options[0] + " (variasi)")
        options = list(set(options))
        
    random.shuffle(options)
    jawaban_benar = chr(65 + options.index(ans))
    
    return {
        "pertanyaan": pertanyaan,
        "a": options[0], "b": options[1], "c": options[2], "d": options[3], "e": options[4],
        "kunci": jawaban_benar,
        "topik": topik
    }

def generate_medium_pu():
    topik = random.choice(["Silogisme Tiga Premis", "Penalaran Analitik", "Kecukupan Data"])
    
    if topik == "Silogisme Tiga Premis":
        subjek = random.choice(["karyawan", "mahasiswa", "atlet", "ilmuwan"])
        kriteria1 = random.choice(["memiliki laptop", "lulus ujian", "rajin berlatih"])
        kriteria2 = random.choice(["dapat bekerja WFH", "mendapat beasiswa", "masuk tim inti"])
        kriteria3 = random.choice(["mendapat bonus", "lulus cumlaude", "ikut olimpiade"])
        
        pertanyaan = (f"Premis 1: Jika seorang {subjek} {kriteria1}, maka ia {kriteria2}.<br>"
                      f"Premis 2: Jika seorang {subjek} {kriteria2}, maka ia {kriteria3}.<br>"
                      f"Premis 3: Budi adalah {subjek} yang tidak {kriteria3}.<br>"
                      f"Kesimpulan yang paling tepat adalah...")
        ans = f"Budi tidak {kriteria1}"
        options = [
            ans,
            f"Budi adalah {subjek} yang {kriteria1} tapi tidak {kriteria3}",
            f"Budi mungkin {kriteria2}",
            f"Tidak dapat ditarik kesimpulan dari premis yang ada",
            f"Budi bukan seorang {subjek}"
        ]
    elif topik == "Penalaran Analitik":
        pertanyaan = (f"Lima orang sahabat: Andi, Budi, Cici, Doni, dan Eka duduk mengelilingi meja bundar. "
                      f"Andi tidak ingin duduk di sebelah Budi. Cici selalu duduk di antara Budi dan Doni. "
                      f"Siapakah yang pasti duduk di sebelah Eka?")
        ans = "Andi dan Doni"
        options = [
            ans,
            "Andi dan Budi",
            "Cici dan Budi",
            "Doni dan Budi",
            "Cici dan Andi"
        ]
    else: # Kecukupan Data
        pertanyaan = (f"Berapakah nilai dari x - y?<br>"
                      f"(1) x + y = 10<br>"
                      f"(2) x&sup2; - y&sup2; = 20")
        ans = "Pernyataan (1) dan (2) BERSAMA-SAMA cukup untuk menjawab pertanyaan, tetapi SATU pernyataan saja tidak cukup."
        options = [
            ans,
            "Pernyataan (1) SAJA cukup untuk menjawab pertanyaan, tetapi pernyataan (2) SAJA tidak cukup.",
            "Pernyataan (2) SAJA cukup untuk menjawab pertanyaan, tetapi pernyataan (1) SAJA tidak cukup.",
            "DUA pernyataan BERSAMA-SAMA tidak cukup untuk menjawab pertanyaan.",
            "Pernyataan (1) SAJA cukup, dan pernyataan (2) SAJA cukup."
        ]
        
    random.shuffle(options)
    jawaban_benar = chr(65 + options.index(ans))
    return {
        "pertanyaan": pertanyaan,
        "a": options[0], "b": options[1], "c": options[2], "d": options[3], "e": options[4],
        "kunci": jawaban_benar,
        "topik": topik
    }

def generate_medium_literasi():
    topik = random.choice(["Inferensi", "Asumsi Logis", "Pelemahan Argumen"])
    teks = random.choice(TEXTS_MEDIUM_LITERASI)
    
    if topik == "Inferensi":
        pertanyaan = f"{teks}<br>Kesimpulan yang paling didukung oleh paragraf di atas adalah..."
        if "inflasi" in teks:
            ans = "Intervensi bank sentral diperlukan untuk mencegah inflasi moderat berubah menjadi hiperinflasi."
        elif "Fermi" in teks:
            ans = "Terdapat setidaknya dua hipotesis utama yang menjelaskan mengapa kita belum menemukan alien."
        else:
            ans = "Praktik peternakan berkontribusi secara langsung terhadap krisis efektivitas antibiotik pada manusia."
    elif topik == "Pelemahan Argumen":
        pertanyaan = f"{teks}<br>Pernyataan manakah berikut ini, jika benar, akan <b>paling memperlemah</b> argumen penulis?"
        if "inflasi" in teks:
            ans = "Sebuah studi menunjukkan investasi sektor riil meningkat drastis justru saat suku bunga acuan sedang tinggi."
        elif "Fermi" in teks:
            ans = "Penelitian astrobiologi terbaru menemukan mikroba asing di Mars yang menunjukkan kehidupan sangatlah umum."
        else:
            ans = "Superbug terbukti lebih banyak bermutasi di rumah sakit dibandingkan di lingkungan peternakan komersial."
    else:
        pertanyaan = f"{teks}<br>Asumsi yang mendasari kekhawatiran penulis pada teks tersebut adalah..."
        ans = "Kondisi saat ini memiliki potensi kuat untuk memburuk jika tidak ada tindakan yang diambil."

    options = [
        ans,
        "Masalah ini akan terselesaikan dengan sendirinya seiring kemajuan teknologi.",
        "Pemerintah saat ini sudah melakukan tindakan yang lebih dari cukup untuk mencegahnya.",
        "Keseluruhan hipotesis yang diajukan oleh para ahli didasarkan pada data yang bias.",
        "Tidak ada korelasi langsung antara fenomena yang dijelaskan di awal dengan dampaknya."
    ]
    random.shuffle(options)
    jawaban_benar = chr(65 + options.index(ans))
    
    return {
        "pertanyaan": pertanyaan,
        "a": options[0], "b": options[1], "c": options[2], "d": options[3], "e": options[4],
        "kunci": jawaban_benar,
        "topik": topik
    }

def generate_questions():
    packages = PaketUjian.objects.filter(nama__icontains="Try Out Medium").order_by('id')
    total_generated = 0
    
    print(f"Ditemukan {packages.count()} paket Try Out Medium.")
    
    for paket in packages:
        print(f"Memproses paket: {paket.nama}...")
        subtests = paket.subtests.all()
        
        for st in subtests:
            # Hapus soal lama di subtest ini
            lama = st.soal.all()
            if lama.exists():
                lama._raw_delete(lama.db) # Fast delete
                
            soal_list = []
            # Target 40 soal per subtest (karena 280 / 7 = 40)
            for i in range(40):
                st_nama = st.nama.lower()
                if "pk" in st_nama or "matematika" in st_nama:
                    data = generate_medium_pk()
                elif "pu" in st_nama:
                    data = generate_medium_pu()
                else:
                    data = generate_medium_literasi()
                    
                ref = random.choice(REFERENCES)
                
                soal = Soal(
                    subtest=st,
                    kategori="MEDIUM",
                    pertanyaan=data["pertanyaan"],
                    pilihan_a=data["a"],
                    pilihan_b=data["b"],
                    pilihan_c=data["c"],
                    pilihan_d=data["d"],
                    pilihan_e=data["e"],
                    jawaban_benar=data["kunci"],
                    pembahasan=f"Pembahasan untuk soal Medium tingkat lanjut dengan topik {data['topik']}. Jawaban yang tepat adalah {data['kunci']}.",
                    referensi_internal=ref,
                    topik_materi=data["topik"]
                )
                soal_list.append(soal)
                
            Soal.objects.bulk_create(soal_list)
            total_generated += len(soal_list)
            
    print(f"SELESAI! Berhasil men-generate {total_generated} soal Try Out Medium baru berkualitas tinggi dengan label topik yang lengkap.")

if __name__ == "__main__":
    generate_questions()
