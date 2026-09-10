from django.shortcuts import redirect
from django.urls import reverse
from ujian.models import SistemSetting

class NetworkGatewayMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow requests to static files, media, admin, or the gateway itself
        path = request.path_info
        if path.startswith('/static/') or path.startswith('/media/') or path.startswith('/admin/') or path.startswith('/network-gateway/'):
            return self.get_response(request)

        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # If local request (Server PC), allow access
        if ip in ('127.0.0.1', 'localhost'):
            return self.get_response(request)

        # External IP logic
        setting = SistemSetting.get_setting()
        
        # If network is offline, redirect to offline warning
        if not setting.network_online and not setting.network_local:
            return redirect(reverse('network_gateway') + "?status=offline")

        # If network is online, check for access token in session
        if not request.session.get('network_access_granted'):
            return redirect('network_gateway')

        response = self.get_response(request)
        return response
