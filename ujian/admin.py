from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .models import Soal, JawabanPeserta, PaketUjian, SubTest, KategoriSetting, SoalSesi


# ==================================================
# SOAL
# ==================================================

@admin.register(Soal)
class SoalAdmin(admin.ModelAdmin):
    list_display = ("id", "pertanyaan_singkat", "jawaban_benar", "kategori", "subtest")
    search_fields = ("pertanyaan",)
    list_filter = ("kategori", "subtest__paket")

    def pertanyaan_singkat(self, obj):
        return obj.pertanyaan[:60]
    pertanyaan_singkat.short_description = "Pertanyaan"


# ==================================================
# JAWABAN PESERTA
# ==================================================

@admin.register(JawabanPeserta)
class JawabanPesertaAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "soal", "jawaban", "dibuat_pada")
    list_filter = ("jawaban",)


# ==================================================
# PAKET UJIAN
# ==================================================

@admin.register(PaketUjian)
class PaketUjianAdmin(admin.ModelAdmin):
    list_display = ("id", "nama", "jumlah_subtest")

    def jumlah_subtest(self, obj):
        return obj.subtests.count()
    jumlah_subtest.short_description = "Jumlah SubTest"


# ==================================================
# SUBTEST
# ==================================================

@admin.register(SubTest)
class SubTestAdmin(admin.ModelAdmin):
    list_display = (
        "id", "nama", "paket", "timer_menit", "soal_tampil",
        "jumlah_soal_pool", "status_setting"
    )
    list_filter = ("paket",)
    search_fields = ("nama", "paket__nama")
    list_editable = ("timer_menit", "soal_tampil")

    def jumlah_soal_pool(self, obj):
        return obj.soal.count()
    jumlah_soal_pool.short_description = "Pool Soal"

    def status_setting(self, obj):
        tampil = obj.soal_tampil
        pool = obj.soal.count()
        if tampil == 0:
            return format_html('<span style="color: gray;">Semua ({} soal)</span>', pool)
        elif tampil > pool:
            return format_html(
                '<span style="color: orange;">{} soal acak (pool hanya {}!)</span>',
                tampil, pool
            )
        else:
            return format_html(
                '<span style="color: green;">{} soal acak dari {}</span>',
                tampil, pool
            )
    status_setting.short_description = "Soal Ditampilkan"


# ==================================================
# PENGATURAN KATEGORI
# ==================================================

@admin.action(description="Terapkan setting ini ke semua SubTest dalam kategori")
def terapkan_ke_subtests(modeladmin, request, queryset):
    total_updated = 0
    for setting in queryset:
        subtest_ids = (
            Soal.objects
            .filter(kategori=setting.kategori, subtest__isnull=False)
            .values_list('subtest_id', flat=True)
            .distinct()
        )
        subtests = SubTest.objects.filter(id__in=subtest_ids)
        count = subtests.count()
        updated_timer = 0
        updated_soal = 0

        for st in subtests:
            changed = False
            if setting.timer_menit > 0 and st.timer_menit != setting.timer_menit:
                st.timer_menit = setting.timer_menit
                changed = True
                updated_timer += 1
            if setting.soal_per_subtest > 0 and st.soal_tampil != setting.soal_per_subtest:
                st.soal_tampil = setting.soal_per_subtest
                changed = True
                updated_soal += 1
            if changed:
                st.save()

        total_updated += count
        messages.success(
            request,
            f"Kategori '{setting.get_kategori_display()}': "
            f"{count} SubTest diupdate "
            f"(timer diubah: {updated_timer}, soal_tampil diubah: {updated_soal})"
        )

    if total_updated == 0:
        messages.warning(request, "Tidak ada SubTest yang perlu diupdate.")


@admin.register(KategoriSetting)
class KategoriSettingAdmin(admin.ModelAdmin):
    list_display = (
        "get_kategori_display_name", "soal_per_subtest", "timer_menit",
        "jumlah_subtest_terdampak", "status_info"
    )
    actions = [terapkan_ke_subtests]

    def get_kategori_display_name(self, obj):
        return obj.get_kategori_display()
    get_kategori_display_name.short_description = "Kategori"

    def jumlah_subtest_terdampak(self, obj):
        count = (
            Soal.objects
            .filter(kategori=obj.kategori, subtest__isnull=False)
            .values('subtest_id')
            .distinct()
            .count()
        )
        return f"{count} subtest"
    jumlah_subtest_terdampak.short_description = "SubTest Terdampak"

    def status_info(self, obj):
        soal_label = str(obj.soal_per_subtest) if obj.soal_per_subtest > 0 else "Semua"
        timer_label = f"{obj.timer_menit} menit" if obj.timer_menit > 0 else "Tak terbatas"
        return format_html(
            '<span style="color: #2563eb; font-weight: bold;">'
            '{} soal acak &bull; {}/subtest</span>',
            soal_label, timer_label
        )
    status_info.short_description = "Konfigurasi Aktif"

    fieldsets = (
        ("Kategori", {
            "fields": ("kategori",)
        }),
        ("Pengaturan Soal & Waktu", {
            "fields": ("soal_per_subtest", "timer_menit"),
            "description": (
                "Atur jumlah soal acak dan durasi timer untuk seluruh SubTest "
                "dalam kategori ini. Gunakan action 'Terapkan' setelah menyimpan "
                "untuk mengupdate semua SubTest sekaligus."
            )
        }),
    )


# ==================================================
# SOAL SESI (monitoring)
# ==================================================

@admin.register(SoalSesi)
class SoalSesiAdmin(admin.ModelAdmin):
    list_display = ("id", "sesi", "soal", "urutan")
    list_filter = ("sesi__subtest__paket",)
    readonly_fields = ("sesi", "soal", "urutan")