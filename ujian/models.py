from django.db import models
from django.contrib.auth.models import User



# ==================================================
# ==================================================
# DATA SOAL
# ==================================================

class Soal(models.Model):

    KATEGORI = [
        ("KD1", "Konsep Dasar 1"),
        ("KD2", "Konsep Dasar 2"),
        ("EASY", "Try Out Easy"),
        ("MEDIUM", "Try Out Medium"),
        ("HARD", "Try Out Hard"),
    ]


    kategori = models.CharField(
        max_length=10,
        choices=KATEGORI,
        default="KD1"
    )

    subtest = models.ForeignKey(
        'SubTest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='soal'
    )


    pertanyaan = models.TextField()


    referensi_internal = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Menyimpan metadata asli seperti [HOTS Prosus/Inten]"
    )

    topik_materi = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Kategori spesifik (misal: Premis, Konklusi) untuk pengelompokan porsi seimbang saat soal diacak secara terbatas."
    )


    pilihan_a = models.CharField(
        max_length=255
    )

    pilihan_b = models.CharField(
        max_length=255
    )

    pilihan_c = models.CharField(
        max_length=255
    )

    pilihan_d = models.CharField(
        max_length=255
    )

    pilihan_e = models.CharField(
        max_length=255,
        blank=True
    )


    jawaban_benar = models.CharField(
        max_length=1
    )


    pembahasan = models.TextField(
        blank=True
    )

    urutan = models.PositiveIntegerField(
        null=True,
        blank=True
    )


    def __str__(self):

        return self.pertanyaan[:50]



class PaketUjian(models.Model):

    nama = models.CharField(max_length=200, unique=True)

    def __str__(self):

        return self.nama



class SubTest(models.Model):

    paket = models.ForeignKey(
        PaketUjian,
        on_delete=models.CASCADE,
        related_name="subtests"
    )

    nama = models.CharField(max_length=200)

    timer_menit = models.IntegerField(
        default=0,
        help_text="Durasi waktu ujian dalam menit. 0 = tidak ada batas waktu."
    )

    soal_tampil = models.PositiveIntegerField(
        default=0,
        help_text="Jumlah soal yang ditampilkan secara acak. 0 = tampilkan semua soal."
    )

    def get_jumlah_soal_tampil(self):
        """Kembalikan jumlah soal yang akan ditampilkan (0 = semua)."""
        if self.soal_tampil > 0:
            return self.soal_tampil
        # Fallback ke KategoriSetting jika ada
        try:
            soal_pertama = self.soal.first()
            if soal_pertama:
                setting = KategoriSetting.objects.filter(
                    kategori=soal_pertama.kategori
                ).first()
                if setting and setting.soal_per_subtest > 0:
                    return setting.soal_per_subtest
        except Exception:
            pass
        return 0  # 0 berarti tampilkan semua

    def get_timer_menit(self):
        """Kembalikan timer yang berlaku (dari SubTest atau KategoriSetting)."""
        if self.timer_menit > 0:
            return self.timer_menit
        try:
            soal_pertama = self.soal.first()
            if soal_pertama:
                setting = KategoriSetting.objects.filter(
                    kategori=soal_pertama.kategori
                ).first()
                if setting and setting.timer_menit > 0:
                    return setting.timer_menit
        except Exception:
            pass
        return 0

    def __str__(self):

        return f"{self.paket.nama} - {self.nama}"


# ==================================================
# PENGATURAN SISTEM GLOBAL
# ==================================================

class SistemSetting(models.Model):
    anti_cheat_aktif = models.BooleanField(
        default=False,
        help_text="Aktifkan mode Anti-Cheat (blokir copy, klik kanan, F12, pindah tab)"
    )
    
    network_online = models.BooleanField(
        default=False,
        help_text="Tentukan apakah server bisa diakses perangkat lain secara online global (Tunnel)."
    )
    
    network_local = models.BooleanField(
        default=False,
        help_text="Tentukan apakah server bisa diakses perangkat lain secara lokal (Satu Wi-Fi)."
    )
    
    network_password = models.CharField(
        max_length=50, 
        blank=True, 
        default="admin123",
        help_text="Password wajib untuk perangkat luar (HP/Tablet/Laptop lain) jika mode jaringan sedang Online."
    )
    
    public_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="URL publik sementara yang dihasilkan oleh LocalTunnel (otomatis)."
    )


    class Meta:
        verbose_name = "Pengaturan Sistem"
        verbose_name_plural = "Pengaturan Sistem"

    @classmethod
    def get_setting(cls):
        setting, created = cls.objects.get_or_create(id=1)
        return setting


# ==================================================
# PENGATURAN KATEGORI
# Konfigurasi default soal & waktu per kategori
# ==================================================

class KategoriSetting(models.Model):

    KATEGORI = [
        ("KD1", "Konsep Dasar 1"),
        ("KD2", "Konsep Dasar 2"),
        ("EASY", "Try Out Easy"),
        ("MEDIUM", "Try Out Medium"),
        ("HARD", "Try Out Hard"),
    ]

    kategori = models.CharField(
        max_length=10,
        choices=KATEGORI,
        unique=True,
        verbose_name="Kategori"
    )

    soal_per_subtest = models.PositiveIntegerField(
        default=10,
        help_text="Jumlah soal acak per subtest. 0 = tampilkan semua soal."
    )

    timer_menit = models.PositiveIntegerField(
        default=10,
        help_text="Durasi waktu per subtest dalam menit. 0 = tidak ada batas waktu."
    )

    class Meta:
        verbose_name = "Pengaturan Kategori"
        verbose_name_plural = "Pengaturan Kategori"

    def __str__(self):
        return f"Setting {self.get_kategori_display()} — {self.soal_per_subtest} soal / {self.timer_menit} menit"


# ==================================================
# SOAL SESI
# Menyimpan soal acak yang terpilih untuk sesi peserta
# ==================================================

class SoalSesi(models.Model):

    sesi = models.ForeignKey(
        'SesiUjian',
        on_delete=models.CASCADE,
        related_name='soal_sesi'
    )

    soal = models.ForeignKey(
        Soal,
        on_delete=models.CASCADE,
        related_name='soal_sesi'
    )

    urutan = models.PositiveIntegerField(
        default=0,
        help_text="Urutan tampil soal dalam sesi ini"
    )

    class Meta:
        ordering = ['urutan']
        unique_together = [('sesi', 'soal')]

    def __str__(self):
        return f"Sesi {self.sesi.id} — Soal {self.soal.id} (urutan {self.urutan})"


# ==================================================
# JAWABAN PESERTA
# ==================================================

class JawabanPeserta(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


    soal = models.ForeignKey(
        Soal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_benar_snapshot = models.BooleanField(default=False)
    kategori_snapshot = models.CharField(max_length=100, null=True, blank=True)
    paket_id_snapshot = models.IntegerField(null=True, blank=True)
    subtest_id_snapshot = models.IntegerField(null=True, blank=True)
    subtest_nama_snapshot = models.CharField(max_length=255, null=True, blank=True)
    paket_nama_snapshot = models.CharField(max_length=255, null=True, blank=True)

    jawaban = models.CharField(
        max_length=1
    )


    dibuat_pada = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        if self.user:

            return f"{self.user.username} - Soal {self.soal.id} - {self.jawaban}"

        return f"Soal {self.soal.id} - {self.jawaban}"






# ==================================================
# SESI UJIAN
# MENYIMPAN WAKTU MULAI UJIAN
# ==================================================

class SesiUjian(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    waktu_mulai = models.DateTimeField(
        null=True,
        blank=True
    )

    subtest = models.ForeignKey(
        'SubTest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sesi'
    )


    selesai = models.BooleanField(
        default=False
    )
    
    terindikasi_curang = models.BooleanField(
        default=False
    )


    def __str__(self):

        return f"{self.user.username} - {self.waktu_mulai}"

class HasilPaketUjian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paket_nama = models.CharField(max_length=200)
    kategori = models.CharField(max_length=100)
    waktu_selesai = models.DateTimeField(auto_now_add=True)
    durasi_teks = models.CharField(max_length=50, blank=True, null=True)
    skor_json = models.JSONField(default=dict)
    nilai_akhir = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.paket_nama} ({self.nilai_akhir})"
