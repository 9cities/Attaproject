from django.urls import path
from . import views


urlpatterns = [

    path(
        "network-gateway/",
        views.network_gateway,
        name="network_gateway"
    ),

    # HALAMAN DEPAN UJIAN
    path(
        "soal/",
        views.daftar_soal,
        name="daftar_soal"
    ),

    path(
        "soal/mulai-paket/<int:paket_id>/",
        views.mulai_paket_ujian,
        name="mulai_paket_ujian"
    ),

    path(
        "materi-ujian/<int:subtest_id>/",
        views.materi_detail_ujian,
        name="materi_detail_ujian"
    ),

    path(
        "soal/<str:kategori>/start/<int:subtest_id>/",
        views.start_subtest,
        name="start_subtest"
    ),

    # SATU SOAL
    path(
        "soal/<int:nomor>/",
        views.tampil_soal,
        name="tampil_soal"
    ),

    path(
        "soal/<str:kategori>/",
        views.daftar_soal,
        name="daftar_soal_kategori"
    ),

    path(
        "soal/<str:kategori>/<int:nomor>/",
        views.tampil_soal,
        name="tampil_soal_kategori"
    ),



    # SELESAI UJIAN
    path(
        "selesai/",
        views.selesai_ujian,
        name="selesai_ujian"
    ),

    path(
        "latihan-soal-salah/",
        views.latihan_soal_salah,
        name="latihan_soal_salah"
    ),

    path(
        "latihan-soal-salah/<int:subtest_id>/<int:nomor>/",
        views.latihan_soal_salah,
        name="latihan_soal_salah_nav"
    ),



    # REVIEW JAWABAN
    path(
        "review/",
        views.review_jawaban,
        name="review_jawaban"
    ),



    # STATISTIK ADMIN
    path(
        "admin-statistik/",
        views.admin_statistik,
        name="admin_statistik"
    ),

    path(
        "admin-statistik/detail/",
        views.admin_statistik_detail,
        name="admin_statistik_detail"
    ),

    path(
        "admin-statistik/update-massal/",
        views.admin_statistik_update_massal,
        name="admin_statistik_update_massal"
    ),

    path(
        "admin-statistik/ubah-akun/",
        views.admin_change_credentials,
        name="admin_change_credentials"
    ),

    path(
        "admin-statistik/delete-peserta/<int:user_id>/",
        views.admin_delete_peserta,
        name="admin_delete_peserta"
    ),

    path(
        "admin-statistik/export-peserta/<int:user_id>/",
        views.admin_export_peserta_excel,
        name="admin_export_peserta_excel"
    ),

    path(
        "admin-statistik/export-all/",
        views.admin_export_all_excel,
        name="admin_export_all_excel"
    ),

    path(
        "admin-statistik/export-soal/",
        views.admin_export_soal_excel,
        name="admin_export_soal_excel"
    ),

    path(
        "demo-animasi/",
        views.demo_animasi,
        name="demo_animasi"
    ),

    path(
        "materi/",
        views.materi_list,
        name="materi_list"
    ),

    path(
        "materi/<str:slug>/",
        views.materi_detail,
        name="materi_detail"
    ),

    path(
        "admin/upload/",
        views.upload_paket,
        name="upload_paket"
    ),

]