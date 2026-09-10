import os
import subprocess
import threading
import time
import re
from django.db import transaction

# Global variable to hold the subprocess so we can kill it later
# Note: In a production server (like Gunicorn/uWSGI) this global state might not persist across workers,
# but for Django runserver (development server), it works perfectly.
_TUNNEL_PROCESS = None

def _run_tunnel_thread():
    global _TUNNEL_PROCESS
    
    # 1. Turn off firewall if possible
    try:
        # This will fail silently if not running as administrator
        subprocess.run(
            ['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'off'],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        print(f"[Tunnel] Failed to disable firewall: {e}")

    # 2. Kill existing node processes that might be orphaned localtunnels
    # (Optional, but good for cleanup if things got stuck)
    # We will skip this to avoid killing other node projects, relying on Process Tree killing instead.
    
    # 3. Start localtunnel
    try:
        print("[Tunnel] Starting localtunnel...")
        _TUNNEL_PROCESS = subprocess.Popen(
            ['npx.cmd', 'localtunnel', '--port', '8000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Read output line by line to find the URL
        for line in iter(_TUNNEL_PROCESS.stdout.readline, ''):
            print(f"[Tunnel Output] {line.strip()}")
            if "your url is:" in line:
                match = re.search(r'(https://[a-zA-Z0-9-]+\.loca\.lt)', line)
                if match:
                    public_url = match.group(1)
                    print(f"[Tunnel] Found Public URL: {public_url}")
                    
                    # Update database
                    from ujian.models import SistemSetting
                    with transaction.atomic():
                        setting = SistemSetting.objects.first()
                        if setting:
                            setting.public_url = public_url
                            setting.save()
                    break # We found it, stop reading and let it run
                
    except Exception as e:
        print(f"[Tunnel] Error starting localtunnel: {e}")

def start_tunnel():
    """Starts the tunnel in a background thread."""
    stop_tunnel() # Ensure any existing tunnel is stopped
    
    thread = threading.Thread(target=_run_tunnel_thread, daemon=True)
    thread.start()

def stop_tunnel():
    """Stops the running tunnel and attempts to re-enable firewall."""
    global _TUNNEL_PROCESS
    
    if _TUNNEL_PROCESS:
        print("[Tunnel] Stopping localtunnel...")
        try:
            subprocess.call(
                ['taskkill', '/F', '/T', '/PID', str(_TUNNEL_PROCESS.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass
        _TUNNEL_PROCESS = None
        
    # Clear the URL from database
    try:
        from ujian.models import SistemSetting
        setting = SistemSetting.objects.first()
        if setting and setting.public_url:
            setting.public_url = None
            setting.save()
    except Exception:
        pass
        
    # Turn firewall back on
    try:
        subprocess.run(
            ['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'on'],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception:
        pass
