import os
import sys
import django
import random
import uuid

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(r"C:\CBT TRY OUT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_project.settings")
django.setup()

from ujian.models import Soal, SubTest

# --- DATA BANK UNTUK LITERASI & LOGIKA ---
TEXTS_INDO = [
    "<p><i>Dalam dekade terakhir, kecerdasan buatan (AI) telah merevolusi berbagai sektor industri. Di bidang kesehatan, algoritma pembelajaran mesin digunakan untuk menganalisis citra medis dengan tingkat akurasi yang melampaui radiolog manusia dalam beberapa kasus. Namun, tantangan etika dan privasi data pasien tetap menjadi hambatan utama dalam adopsi massal teknologi ini.</i></p>",
    "<p><i>Perubahan iklim global memicu anomali cuaca yang ekstrem. Fenomena El Nino dan La Nina yang semakin sering terjadi menyebabkan siklus gagal panen di negara-negara agraris. Hal ini mendorong urgensi pengembangan varietas tanaman yang tahan terhadap kekeringan dan salinitas tinggi untuk menjamin ketahanan pangan global.</i></p>",
    "<p><i>Pemerintah merencanakan transisi energi dari bahan bakar fosil menuju energi terbarukan. Meski investasi awal untuk panel surya dan turbin angin sangat besar, perhitungan jangka panjang menunjukkan bahwa biaya Levelized Cost of Energy (LCOE) dari energi terbarukan sudah lebih murah dibandingkan Pembangkit Listrik Tenaga Uap (PLTU) batu bara.</i></p>"
]

TEXTS_ENG = [
    "<p><i>The rapid development of quantum computing poses a significant threat to current cryptographic standards. Unlike classical computers, quantum systems use qubits that can exist in multiple states simultaneously, allowing them to crack complex encryption algorithms like RSA in hours rather than millennia.</i></p>",
    "<p><i>Urbanization has led to the rise of 'heat islands' in major metropolitan areas. Concrete and asphalt absorb solar radiation during the day and release it at night, significantly raising local temperatures. Urban planners are now advocating for green roofs and increased canopy cover to mitigate this effect.</i></p>"
]

# --- GENERATORS ---

def generate_math_pk():
    # Aljabar / Persamaan
    a = random.randint(2, 9)
    b = random.randint(10, 50)
    c = random.randint(2, 5)
    x = random.randint(1, 10)
    
    # Equation: a*x + b = result
    result = a * x + b
    
    pertanyaan = f"Jika diketahui persamaan linear {a}x + {b} = {result}, maka berapakah nilai dari {c}x?"
    ans = c * x
    
    options = [ans, ans+c, ans-c, ans+(2*c), ans-(2*c)]
    random.shuffle(options)
    
    opt_dict = {
        'A': str(options[0]), 'B': str(options[1]), 'C': str(options[2]),
        'D': str(options[3]), 'E': str(options[4])
    }
    
    ans_key = 'A'
    for k, v in opt_dict.items():
        if v == str(ans):
            ans_key = k
            break
            
    pembahasan = f"Langkah 1: {a}x = {result} - {b} = {result-b}. Langkah 2: x = {x}. Maka {c}x = {c} * {x} = {ans}."
    return pertanyaan, opt_dict, ans_key, pembahasan

def generate_math_pm():
    # Soal Cerita
    harga_awal = random.choice([100000, 150000, 200000, 250000])
    diskon1 = random.choice([20, 30, 40])
    diskon2 = random.choice([10, 20])
    
    pertanyaan = f"Sebuah toko baju memberikan diskon ganda {diskon1}% + {diskon2}% untuk sebuah kemeja seharga Rp{harga_awal:,}. Berapakah total harga yang harus dibayar pembeli?"
    
    harga_setelah_d1 = harga_awal * (1 - diskon1/100)
    harga_akhir = int(harga_setelah_d1 * (1 - diskon2/100))
    
    # Pengecoh
    fake1 = int(harga_awal * (1 - (diskon1+diskon2)/100)) # Diskon dijumlahkan (salah kaprah)
    fake2 = int(harga_awal * (1 - diskon1/100) - diskon2) # Diskon 2 dikurang nominal
    fake3 = harga_akhir + 5000
    fake4 = harga_akhir - 5000
    
    options = [harga_akhir, fake1, fake2, fake3, fake4]
    options = list(set(options))
    while len(options) < 5:
        options.append(options[0] + random.randint(1,10)*1000)
        options = list(set(options))
    
    random.shuffle(options)
    
    opt_dict = {
        'A': f"Rp{options[0]:,}", 'B': f"Rp{options[1]:,}", 'C': f"Rp{options[2]:,}",
        'D': f"Rp{options[3]:,}", 'E': f"Rp{options[4]:,}"
    }
    
    ans_key = 'A'
    for k, v in opt_dict.items():
        if v == f"Rp{harga_akhir:,}":
            ans_key = k
            break
            
    pembahasan = f"Harga setelah diskon 1 = {100-diskon1}% x {harga_awal} = {int(harga_setelah_d1)}. Harga akhir = {100-diskon2}% x {int(harga_setelah_d1)} = {harga_akhir}."
    return pertanyaan, opt_dict, ans_key, pembahasan

def generate_logic_pu():
    # Silogisme
    subjek = random.choice(["Petani", "Ilmuwan", "Dokter", "Guru", "Insinyur"])
    objek = random.choice(["mesin traktor", "data satelit", "vaksin baru", "modul ajar", "rancang bangun"])
    akibat1 = random.choice(["panen meningkat", "riset selesai", "pasien sembuh", "siswa pintar", "proyek tuntas"])
    
    pertanyaan = f"Premis 1: Jika {subjek} menganalisis {objek}, maka {akibat1}.\nPremis 2: Fakta menunjukkan bahwa {akibat1} TIDAK TERJADI.\n\nKesimpulan yang paling tepat adalah..."
    
    ans = f"{subjek} TIDAK menganalisis {objek}."
    fake1 = f"{subjek} menganalisis {objek}."
    fake2 = f"Meskipun {akibat1} tidak terjadi, {subjek} tetap menganalisis {objek}."
    fake3 = f"{subjek} menganalisis hal lain selain {objek}."
    fake4 = f"Tidak ada kesimpulan yang bisa ditarik."
    
    options = [ans, fake1, fake2, fake3, fake4]
    random.shuffle(options)
    
    opt_dict = {
        'A': options[0], 'B': options[1], 'C': options[2],
        'D': options[3], 'E': options[4]
    }
    
    ans_key = 'A'
    for k, v in opt_dict.items():
        if v == ans:
            ans_key = k
            break
            
    pembahasan = f"Menggunakan modus Tollens: Jika p -> q, dan ~q, maka kesimpulannya adalah ~p."
    return pertanyaan, opt_dict, ans_key, pembahasan

def generate_reading(text_pool, q_type):
    teks = random.choice(text_pool)
    
    if q_type == "INDO":
        q_options = [
            ("Berdasarkan paragraf tersebut, manakah pernyataan yang PALING TEPAT mewakili gagasan utamanya?", 
             ["Pengenalan suatu teknologi baru atau isu global dan dampaknya terhadap sektor terkait.",
              "Rincian detail teknis mengenai cara kerja sistem secara spesifik.",
              "Biaya dan investasi finansial adalah satu-satunya hal yang dibahas.",
              "Kritik terhadap pemerintah atau lembaga terkait yang gagal menangani masalah.",
              "Penjelasan mengenai sejarah masa lalu sebelum era modern."]),
            ("Kesimpulan apa yang dapat ditarik dari informasi dalam teks di atas?",
             ["Terdapat hubungan sebab-akibat antara fenomena yang terjadi dengan tantangan/solusi yang harus dihadapi.",
              "Semua hal yang disebutkan dalam teks tidak ada kaitannya satu sama lain.",
              "Masalah yang dibahas sudah sepenuhnya terselesaikan tanpa sisa.",
              "Hanya satu kelompok masyarakat yang terdampak secara langsung.",
              "Tidak ada yang bisa dilakukan manusia untuk mengubah keadaan."])
        ]
    else:
        q_options = [
            ("What is the main idea of the passage?", 
             ["The passage primarily discusses a modern scientific or environmental issue and its implications.",
              "The text is a historical account of events from centuries ago.",
              "The author is mainly complaining about personal experiences.",
              "It is an advertisement for a new technological product.",
              "The passage focuses strictly on the mathematical formulas behind the concept."]),
            ("Which of the following can be inferred from the text?",
             ["The phenomenon described requires specific countermeasures or adaptations.",
              "The issue has absolutely no impact on human society.",
              "Scientists have completely abandoned research on this topic.",
              "The current situation will remain exactly the same forever.",
              "The text contradicts all known laws of physics."])
        ]
        
    q_pair = random.choice(q_options)
    pertanyaan = teks + "<p>" + q_pair[0] + "</p>"
    ans = q_pair[1][0]
    fakes = q_pair[1][1:]
    
    options = [ans] + fakes
    random.shuffle(options)
    
    opt_dict = {
        'A': options[0], 'B': options[1], 'C': options[2],
        'D': options[3], 'E': options[4]
    }
    
    ans_key = 'A'
    for k, v in opt_dict.items():
        if v == ans:
            ans_key = k
            break
            
    pembahasan = "Jawaban ini merupakan sintesis paling relevan dari gagasan utama teks yang disajikan."
    return pertanyaan, opt_dict, ans_key, pembahasan


# --- MAIN EXECUTION ---
def run():
    print("Mulai memproses Paket Try Out Easy 1...")
    subtests = SubTest.objects.filter(paket__nama="Try Out Easy 1")
    
    if not subtests:
        print("Paket 'Try Out Easy 1' tidak ditemukan!")
        return
        
    total_updated = 0
    
    for st in subtests:
        st_name = st.nama.lower()
        soals = Soal.objects.filter(subtest=st, kategori="EASY")
        print(f"\nMemperbarui {soals.count()} soal pada SubTest: {st.nama}")
        
        for soal in soals:
            if "pk" in st_name or "matematika" in st_name:
                p, opt, ans, pemb = generate_math_pk()
            elif "pm" in st_name or "penalaran matematika" in st_name:
                p, opt, ans, pemb = generate_math_pm()
            elif "pu" in st_name or "penalaran umum" in st_name:
                p, opt, ans, pemb = generate_logic_pu()
            elif "lbe" in st_name or "inggris" in st_name:
                p, opt, ans, pemb = generate_reading(TEXTS_ENG, "ENG")
            else:
                p, opt, ans, pemb = generate_reading(TEXTS_INDO, "INDO")
                
            soal.pertanyaan = p
            soal.pilihan_a = opt['A']
            soal.pilihan_b = opt['B']
            soal.pilihan_c = opt['C']
            soal.pilihan_d = opt['D']
            soal.pilihan_e = opt['E']
            soal.jawaban_benar = ans
            soal.pembahasan = pemb
            
            # Kita tandai metadata bahwa ini soal kualitas baru
            soal.referensi_internal = "[SNBT/UTBK 2024-2025 Premium]"
            
            soal.save()
            total_updated += 1
            
    print(f"\nSelesai! Berhasil merombak total {total_updated} soal di Try Out Easy 1.")

if __name__ == "__main__":
    run()
