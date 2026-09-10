from django.db import models



# ==========================
# SOAL
# ==========================

class Soal(models.Model):

    KATEGORI = [
        ("KD1", "Konsep Dasar 1"),
        ("KD2", "Konsep Dasar 2"),
        ("EASY", "Try Out Easy"),
        ("MEDIUM", "Try Out Medium"),
        ("HARD", "Try Out Hard"),
    ]


    JAWABAN = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
    ]


    kategori = models.CharField(
        max_length=10,
        choices=KATEGORI,
        default="KD1"
    )


    pertanyaan = models.TextField()


    gambar_soal = models.ImageField(
        upload_to="soal/",
        blank=True,
        null=True
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
        max_length=1,
        choices=JAWABAN
    )


    pembahasan = models.TextField(
        blank=True
    )


    dibuat_pada = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.pertanyaan[:50]