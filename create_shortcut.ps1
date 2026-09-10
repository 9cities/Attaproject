$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\DELL\Desktop\Buka CBT Try Out.lnk")
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = """C:\CBT TRY OUT\start_cbt.vbs"""
$Shortcut.WorkingDirectory = "C:\CBT TRY OUT"
$Shortcut.IconLocation = "shell32.dll,13"
$Shortcut.Save()
