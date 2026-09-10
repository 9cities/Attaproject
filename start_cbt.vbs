Set WshShell = CreateObject("WScript.Shell")

' 1. Matikan semua proses python yang mungkin masih berjalan (agar port 8000 tidak bentrok)
WshShell.Run "taskkill /F /IM python.exe /T", 0, True

' 2. Jalankan server Django secara diam-diam (0 = hidden window, False = don't wait to finish)
WshShell.Run "cmd.exe /c cd /d ""C:\CBT TRY OUT"" && venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8000", 0, False

' 3. Tunggu 3 detik agar server siap
WScript.Sleep 3000

' 4. Buka browser default langsung ke halaman CBT
WshShell.Run "http://127.0.0.1:8000"
