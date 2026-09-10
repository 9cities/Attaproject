# c:\CBT TRY OUT\ujian\materi_data.py

MATERI_REGISTRY = {
    'matematika': {
        'title': 'Matematika Wajib (PK & PM)',
        'subtitle': 'Aljabar, Geometri, Limit, Turunan & Statistika',
        'icon': '📐',
        'gradient': 'linear-gradient(135deg, #FF4D8F 0%, #7C3AED 100%)',
        'duration': '5 Menit',
        'description': 'Kuasai trik cepat menyelesaikan fungsi, turunan, integral, matriks, serta analisis peluang dan statistika tanpa rumus panjang.',
        'steps': [
            {
                'num': 1,
                'title': 'Operasi & Persamaan Bilangan',
                'narration': 'Selamat datang di modul Matematika Wajib! Di materi Operasi dan Persamaan Bilangan, hindari menghitung manual jika angkanya terlalu besar. Gunakan sifat-sifat dasar aljabar seperti pemfaktoran selisih kuadrat atau sifat distributif. Contohnya, jika ditanya nilai x dari sebuah persamaan linear, pindahkan semua variabel x ke satu ruas terlebih dahulu.',
                'kunci1': 'Gunakan Sifat Distributif & Pemfaktoran',
                'contoh': 'Soal: a² - b² = (a+b)(a-b)',
                'trik': 'Trik: Jangan hitung manual angka besar, cari pola selisih kuadrat!'
            },
            {
                'num': 2,
                'title': 'Fungsi, Grafik & Sistem Persamaan',
                'narration': 'Untuk fungsi dan grafik, trik tercepat adalah substitusi titik potong. Jika ditanya grafik mana yang sesuai dengan fungsi f(x), cukup masukkan nilai x sama dengan nol untuk mencari titik potong sumbu y. Pada sistem persamaan linear dua variabel, eliminasi variabel yang koefisiennya paling mudah disamakan.',
                'kunci1': 'Substitusi x = 0 untuk memotong sumbu Y',
                'contoh': 'Fungsi: y = 2x + 4. Jika x=0, maka y=4. Grafik pasti memotong di (0,4).',
                'trik': 'Trik Eliminasi Cepat: Kalikan silang koefisien variabel yang ingin dihilangkan.'
            },
            {
                'num': 3,
                'title': 'Barisan, Deret & Eksponen',
                'narration': 'Pada barisan aritmatika, ingat selalu bahwa selisih antar suku itu konstan. Sedangkan untuk eksponen atau bilangan berpangkat, kuasai sifat perkalian dan pembagian pangkat. Jika basisnya sama, perkalian berarti pangkatnya ditambah, pembagian berarti pangkatnya dikurang.',
                'kunci1': 'Eksponen: (a^m) × (a^n) = a^(m+n)',
                'contoh': 'Barisan: 2, 5, 8, 11 (Beda = 3). Suku ke-n = 3n - 1.',
                'trik': 'Trik Eksponen: Ubah semua basis angka menjadi bilangan prima terkecil (misal 8 menjadi 2 pangkat 3).'
            },
            {
                'num': 4,
                'title': 'Peluang, Statistika & Analisis Data',
                'narration': 'Dalam soal statistika SNBT, yang sering ditanyakan adalah rata-rata gabungan atau median. Median adalah nilai tengah setelah data diurutkan! Untuk peluang, rumusnya sederhana: jumlah kejadian yang diharapkan dibagi total ruang sampel. Jangan lupa baca grafik dengan teliti sebelum menghitung.',
                'kunci1': 'Peluang = (Kejadian yang Diharapkan) / (Total Kemungkinan)',
                'contoh': 'Rata-rata: (Total Nilai) / (Jumlah Data).',
                'trik': 'Trik Analisis Grafik: Fokus pada sumbu X dan Y, jangan terjebak visualisasi 3D atau warna grafik.'
            },
            {
                'num': 5,
                'title': 'Geometri & Trigonometri',
                'narration': 'Geometri bidang dan ruang menuntut kemampuan visualisasi. Hafalkan triple Pythagoras wajib seperti 3-4-5 atau 5-12-13. Untuk trigonometri, hafalkan nilai sudut istimewa kuadran pertama, karena sudut di kuadran lain bisa dicari dengan relasi sudut.',
                'kunci1': 'Hafalkan Triple Pythagoras: 3-4-5, 5-12-13, 7-24-25',
                'contoh': 'Diagonal sisi kubus = a√2. Diagonal ruang kubus = a√3.',
                'trik': 'Trik Cepat: Sudut Segitiga selalu berjumlah 180 derajat.'
            },
            {
                'num': 6,
                'title': 'Limit, Turunan, Integral & Matriks',
                'narration': 'Ini adalah materi andalan! Untuk soal Limit bentuk tak tentu 0/0, langsung gunakan aturan L\'Hopital, yaitu turunkan pembilang dan penyebutnya! Turunan menurunkan pangkat, sementara Integral menaikkan pangkat. Untuk matriks, ingat bahwa Determinan dari matriks singular adalah nol.',
                'kunci1': 'Limit 0/0 -> Gunakan L\'Hopital (Turunan Atas & Bawah)',
                'contoh': 'Turunan: f(x) = x³ ➔ f\'(x) = 3x²',
                'trik': 'Trik Matriks: Invers 2x2 cukup tukar posisi diagonal utama dan beri minus pada diagonal lainnya.'
            }
        ]
    },
    'b_inggris': {
        'title': 'Bahasa Inggris Wajib (LBE)',
        'subtitle': 'Main Idea, Inference, Tenses & Passive Voice',
        'icon': '🌐',
        'gradient': 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)',
        'duration': '5 Menit',
        'description': 'Trik skimming dan scanning reading comprehension, serta penguasaan grammar fundamental UTBK tanpa perlu membaca seluruh teks.',
        'steps': [
            {
                'num': 1,
                'title': 'Main Idea & Detail Information',
                'narration': 'Welcome to the English Section! Untuk menjawab pertanyaan Main Idea atau Ide Pokok, Anda TIDAK PERLU membaca seluruh teks. Cukup baca kalimat pertama dan kalimat terakhir di setiap paragraf. Main idea biasanya terletak di awal atau akhir. Untuk Detail Information, gunakan teknik Scanning: cari kata kunci dari soal langsung di dalam teks.',
                'kunci1': 'Ide Pokok selalu ada di Kalimat Pertama atau Terakhir',
                'contoh': 'Soal: What is the main idea of the passage?',
                'trik': 'Trik Scanning: Jangan baca kata per kata. Sapu teks dengan cepat untuk mencari nama, angka, atau kata unik.'
            },
            {
                'num': 2,
                'title': 'Reference, Inference, & Discourse Analysis',
                'narration': 'Pertanyaan Reference meminta Anda mencari kata ganti seperti \'it\' atau \'they\' merujuk ke mana. Jawabannya SELALU ada di kalimat sebelum kata tersebut! Sedangkan Inference meminta Anda menyimpulkan informasi yang tersirat, artinya jawabannya tidak tertulis mentah-mentah di teks. Analisis wacana menguji pemahaman alur ide penulis.',
                'kunci1': 'Reference: Mundur satu kalimat ke belakang!',
                'contoh': 'Soal: The word "they" in line 5 refers to...',
                'trik': 'Trik Inference: Eliminasi opsi jawaban yang menyatakan fakta eksplisit (tersurat) di dalam teks.'
            },
            {
                'num': 3,
                'title': 'Vocabulary & Synonym-Antonym',
                'narration': 'Tidak tahu arti sebuah kata? Tenang! Gunakan context clues atau petunjuk konteks. Baca kalimat sebelum dan sesudahnya untuk menebak apakah kata tersebut bermakna positif atau negatif. Biasanya, konjungsi seperti \'but\' atau \'however\' menunjukkan lawan kata.',
                'kunci1': 'Tebak Makna dari Konteks Kalimat (Context Clues)',
                'contoh': 'He is very PENURIOUS, but his wife is very generous. (Berarti penurious = pelit/miskin).',
                'trik': 'Trik: Jika soal minta antonim, cari dua opsi jawaban yang bersinonim dan abaikan keduanya.'
            },
            {
                'num': 4,
                'title': 'Grammar: Tenses & Passive Voice',
                'narration': 'Dalam ujian, Passive Voice atau kalimat pasif sangat sering diujikan. Kunci pasif adalah to be ditambah Verb bentuk ke tiga (Past Participle). Untuk tenses, fokus pada keterangan waktu. \'Yesterday\' berarti Past Tense, \'Since\' atau \'For\' biasanya penanda Present Perfect.',
                'kunci1': 'Pasif = to be + V3',
                'contoh': 'Aktif: He writes a letter. Pasif: A letter is written by him.',
                'trik': 'Trik Cepat Tenses: Lihat penanda waktu di ujung kalimat!'
            },
            {
                'num': 5,
                'title': 'Subject-Verb Agreement',
                'narration': 'Aturan emas bahasa Inggris: Subjek tunggal (seperti He, She, It) harus dipasangkan dengan kata kerja tunggal (berakhiran s/es). Subjek jamak tidak perlu s/es. Hati-hati dengan kalimat yang dipisahkan oleh frasa preposisi, subjek aslinya tetap yang paling depan!',
                'kunci1': 'Singular Subject = Verb + s/es',
                'contoh': 'The box of chocolates IS on the table. (Subjeknya box, bukan chocolates).',
                'trik': 'Trik: Coret frasa di antara dua koma untuk melihat subjek dan verb aslinya.'
            }
        ]
    },
    'lbi_saintek': {
        'title': 'Bahasa Indonesia (LBI Saintek & PPU)',
        'subtitle': 'Ide Pokok & Penalaran Teks (Konteks Sains/Eksak)',
        'icon': '🧬',
        'gradient': 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
        'duration': '5 Menit',
        'description': 'Kupas tuntas strategi menjawab soal pemahaman bacaan dan analisis argumen khusus untuk wacana Sains, Teknologi, dan Medis.',
        'steps': [
            {
                'num': 1,
                'title': 'Ide Pokok & Kepaduan (Teks Sains)',
                'narration': 'Pada wacana Saintek seperti Biologi atau Fisika, ide pokok seringkali berupa penemuan baru atau masalah lingkungan. Kepaduan paragraf terjadi jika semua kalimat mendukung satu gagasan utama ilmiah tersebut tanpa ada kalimat sumbang yang di luar topik sains.',
                'kunci1': 'Ide Pokok Sains = Kalimat Utama Penemuan/Fakta',
                'contoh': 'Jika paragraf membahas DNA, kalimat sumbang adalah kalimat yang membahas sejarah candi.',
                'trik': 'Trik: Jika diminta mencari kalimat sumbang, carilah kalimat yang tidak mengandung istilah teknis/ilmiah.'
            },
            {
                'num': 2,
                'title': 'Informasi Tersurat & Penalaran (Sains)',
                'narration': 'Informasi tersurat adalah data atau angka eksperimen yang tertulis nyata di teks sains. Tersirat berarti kesimpulan implisit dari hasil riset tersebut. Ingat, jangan pernah menyimpulkan hasil riset menggunakan opini pribadi Anda!',
                'kunci1': 'Tersurat = Data Eksperimen. Tersirat = Konklusi Riset.',
                'contoh': 'Pertanyaan: Berdasarkan grafik eksperimen di teks, simpulan yang benar adalah...',
                'trik': 'Trik Cepat: Cocokkan opsi dengan angka/data sains secara langsung.'
            },
            {
                'num': 3,
                'title': 'Makna Istilah Ilmiah & Frasa',
                'narration': 'Teks Saintek sangat kaya akan istilah teknis (seperti sel, atom, mutasi). Anda harus mampu menebak maknanya dari konteks kalimat sebelum dan sesudahnya meskipun Anda belum pernah mendengar istilah itu.',
                'kunci1': 'Pahami Makna Istilah dari Konteks Kalimat Sekitar',
                'contoh': 'Istilah "fotosintesis" dapat ditebak jika kalimat sekitarnya membahas tanaman dan cahaya.',
                'trik': 'Trik: Baca kalimat sebelumnya untuk mencari definisi tersembunyi.'
            },
            {
                'num': 4,
                'title': 'Kalimat Efektif (Laporan Ilmiah)',
                'narration': 'Kalimat efektif harus logis dan bebas ambiguitas, sangat penting dalam laporan ilmiah sains. Hindari preposisi di awal kalimat yang mengaburkan subjek, seperti "Di dalam eksperimen ini menunjukkan..." (Seharusnya: Eksperimen ini menunjukkan...).',
                'kunci1': 'Hilangkan Kata Depan (Di, Ke, Dari, Bagi) di Awal Kalimat Subjek',
                'contoh': 'SALAH: Di penelitian ini membuktikan. BENAR: Penelitian ini membuktikan.',
                'trik': 'Trik Hemat: Hindari pemborosan kata pada teks deskriptif ilmiah.'
            },
            {
                'num': 5,
                'title': 'Analisis Argumen & Evaluasi (Saintek)',
                'narration': 'Dalam mengevaluasi argumen, Anda harus mencari data sains yang berkontradiksi untuk memperlemah opini, atau data sains pendukung untuk memperkuat. Jika penulis pro-kendaraan listrik, maka data bahwa "baterai sulit didaur ulang" akan memperlemah argumennya.',
                'kunci1': 'Mencari Antitesis/Data Kontradiktif',
                'contoh': 'Tesis: Obat X aman. Pernyataan memperlemah: "Uji klinis menunjukkan 30% pasien mengalami efek samping".',
                'trik': 'Trik Argumen: Cari pernyataan yang langsung membantah data utama penulis.'
            }
        ]
    },
    'lbi_soshum': {
        'title': 'Bahasa Indonesia (LBI Soshum & PPU)',
        'subtitle': 'Ide Pokok & Penalaran Teks (Konteks Sosial Humaniora)',
        'icon': '🏛️',
        'gradient': 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
        'duration': '5 Menit',
        'description': 'Kupas tuntas strategi menjawab soal pemahaman bacaan dan analisis argumen khusus untuk wacana Sejarah, Sosiologi, Ekonomi, dan Budaya.',
        'steps': [
            {
                'num': 1,
                'title': 'Ide Pokok & Kepaduan (Teks Soshum)',
                'narration': 'Pada wacana Soshum seperti Sejarah atau Ekonomi, ide pokok biasanya berupa latar belakang peristiwa atau tren sosial ekonomi. Kepaduan paragraf terjadi jika seluruh kalimat mendeskripsikan runtutan sejarah atau argumen sosiologis yang sama.',
                'kunci1': 'Ide Pokok Soshum = Tren Sosial atau Runtutan Peristiwa',
                'contoh': 'Jika paragraf membahas inflasi ekonomi, kalimat sumbang adalah yang membahas rumus fisika.',
                'trik': 'Trik: Ide pokok biasanya ada di kalimat pertama (deduktif) yang merangkum masalah sosial.'
            },
            {
                'num': 2,
                'title': 'Informasi Tersurat & Penalaran (Soshum)',
                'narration': 'Teks Soshum seringkali argumentatif. Informasi tersurat adalah opini tokoh atau tanggal sejarah yang tertulis nyata. Tersirat berarti pesan moral atau kesimpulan tak tertulis dari fenomena sosial tersebut.',
                'kunci1': 'Tersurat = Opini/Fakta Sosial. Tersirat = Pesan Implisit.',
                'contoh': 'Pertanyaan: Pernyataan mana yang SESUAI dengan kronologi sejarah di atas?',
                'trik': 'Trik Cepat: Jangan gunakan asumsi pribadi politik/sosial Anda, selalu merujuk pada teks penulis.'
            },
            {
                'num': 3,
                'title': 'Makna Ungkapan & Frasa Sosial',
                'narration': 'Teks Soshum sering menggunakan ungkapan atau idiom (seperti "kambing hitam", "meja hijau"). Selain itu, Anda harus memahami konotasi (makna rasa) dari kata yang dipilih penulis, apakah bernuansa menyindir, mengkritik, atau memuji.',
                'kunci1': 'Pahami Makna Konotatif (Kiasan) dan Nada Penulis',
                'contoh': 'Penulis menggunakan kata "menggila" untuk menunjukkan harga pasar yang tidak terkendali.',
                'trik': 'Trik: Perhatikan konjungsi pertentangan untuk menangkap nada kritik penulis.'
            },
            {
                'num': 4,
                'title': 'Kalimat Efektif & Ejaan (PUEBI)',
                'narration': 'Kalimat narasi sejarah harus efektif dan bebas ambigu. Perhatikan penggunaan huruf kapital untuk nama peristiwa sejarah (seperti Perang Dunia II) dan huruf miring untuk istilah budaya asing/daerah.',
                'kunci1': 'Kapitalisasi Peristiwa Sejarah & Huruf Miring Istilah Daerah',
                'contoh': 'Penulisan benar: bulan Agustus, Suku Jawa, Perang Padri.',
                'trik': 'Trik Ejaan: Konjungsi "Namun" wajib di awal kalimat dan diikuti koma.'
            },
            {
                'num': 5,
                'title': 'Analisis Argumen & Evaluasi (Soshum)',
                'narration': 'Dalam mengevaluasi argumen sosiologis, Anda harus bisa membedakan mana yang merupakan FAKTA dan mana yang merupakan OPINI. Pernyataan yang memperlemah argumen adalah fakta sosial baru yang bertolak belakang dengan kesimpulan penulis.',
                'kunci1': 'Membedakan Fakta dan Opini Sosial',
                'contoh': 'Tesis Penulis: Sistem urbanisasi berdampak positif. Pernyataan memperlemah: "Statistik menunjukkan peningkatan kriminalitas di kota akibat urbanisasi".',
                'trik': 'Trik Argumen: Cari pernyataan yang memberikan bukti nyata (statistik/angka) yang berlawanan dengan teori penulis.'
            }
        ]
    }
}

# --- ALIASES UNTUK MAPPING SUBTEST ---
# Subtest di database menggunakan nama seperti 'PK', 'PM', 'LBE', dll.
# Agar slug (nama subtest) bisa memanggil materi yang tepat, kita buat alias-nya:
MATERI_REGISTRY['pk'] = MATERI_REGISTRY['matematika']
MATERI_REGISTRY['pm'] = MATERI_REGISTRY['matematika']
MATERI_REGISTRY['lbe'] = MATERI_REGISTRY['b_inggris']
MATERI_REGISTRY['lbi saintek'] = MATERI_REGISTRY['lbi_saintek']
MATERI_REGISTRY['lbi soshum'] = MATERI_REGISTRY['lbi_soshum']
MATERI_REGISTRY['ppu'] = MATERI_REGISTRY['lbi_soshum']  # PPU menggunakan modul LBI
MATERI_REGISTRY['pbm'] = MATERI_REGISTRY['lbi_soshum']  # PBM menggunakan modul LBI
MATERI_REGISTRY['pu'] = {
    'title': 'Penalaran Umum (PU)',
    'subtitle': 'Silogisme, Logika & Penarikan Kesimpulan',
    'icon': '🧠',
    'gradient': 'linear-gradient(135deg, #FF4D8F 0%, #7C3AED 100%)',
    'duration': '5 Menit',
    'description': 'Pelajari cara cepat menarik kesimpulan logis yang PASTI BENAR menggunakan aturan silogisme baku tanpa terjebak opini.',
    'steps': [
        {
            'num': 1,
            'title': 'Modus Ponens',
            'narration': 'Mari kita pelajari Modus Ponens. Premis 1: Jika P terjadi, maka Q pasti terjadi. Premis 2: Fakta di lapangan menunjukkan bahwa P benar-benar terjadi. Maka kesimpulan logisnya adalah: Q pasti terjadi!',
            'visual_type': 'modus_ponens',
            'p1': 'p ➔ q',
            'p2': 'p',
            'q': '∴ q'
        },
        {
            'num': 2,
            'title': 'Modus Tollens',
            'narration': 'Sekarang Modus Tollens. Premis 1 masih sama: Jika P terjadi maka Q terjadi. Namun Premis 2 adalah kebalikannya: Q TERNYATA TIDAK TERJADI. Maka kesimpulannya: P juga pasti TIDAK TERJADI. Ini disebut negasi mundur.',
            'visual_type': 'modus_tollens',
            'p1': 'p ➔ q',
            'p2': '~q',
            'q': '∴ ~p'
        },
        {
            'num': 3,
            'title': 'Silogisme (Rantai Logika)',
            'narration': 'Dalam Silogisme, kita menyambung dua pernyataan bersyarat. Premis 1: Jika P maka Q. Premis 2: Jika Q maka R. Karena Q saling menyambung, kita bisa mencoretnya. Kesimpulannya: Jika P terjadi, maka R pasti terjadi.',
            'visual_type': 'silogisme',
            'p1': 'p ➔ q',
            'p2': 'q ➔ r',
            'q': '∴ p ➔ r'
        },
        {
            'num': 4,
            'title': 'Tips Penting Penalaran',
            'narration': 'Dalam mengerjakan soal silogisme PU, JANGAN PERNAH menyimpulkan berdasarkan opini pribadi atau fakta di dunia nyata. Anda hanya boleh menyimpulkan berdasarkan premis yang tertulis murni di dalam soal.',
            'kunci1': 'Gunakan Rumus Baku (Ponens, Tollens, Silogisme)',
            'contoh': 'Walau secara logika dunia nyata salah, jika premis bilang "Semua ayam bisa terbang", anggap itu FAKTA MUTLAK.',
            'trik': 'Trik: Jika premis tidak memenuhi 3 rumus tadi, jawabannya pasti "Tidak dapat ditarik kesimpulan".'
        }
    ]
}
