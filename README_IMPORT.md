Import instructions for the `import_bank` management command

Quick steps (Windows PowerShell):

1) Backup DB

```powershell
copy .\db.sqlite3 .\db.sqlite3.bak
```

2) Activate venv and run import

```powershell
& ".\venv\Scripts\Activate.ps1"
python manage.py import_bank --file "C:\CBT TRY OUT\sample_questions.csv" --batch-size 500
```

Supported formats: `.csv`, `.xlsx`.

Expected column headers (case-insensitive). Aliases supported.
- kategori
- pertanyaan
- a, b, c, d, e
- jawaban (jawaban_benar)
- pembahasan
- paket (paket_ujian)
- sub, subtest
- timer_menit

Recommendations:
- Start with a small sample file to verify mapping.
- Keep `--batch-size` between 200–2000 depending on available RAM; 500 is a safe default.
- For production/very large imports (>>50k rows) use PostgreSQL.
- If you want web-based uploads, upload file to `media/imports/` and run the same management command on the server pointing to that file.

If you want, I can add an upload view that stores files and shows an "Run import" button. Otherwise, run the CLI as shown above.