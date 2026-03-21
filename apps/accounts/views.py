from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django_otp.plugins.otp_totp.models import TOTPDevice


class AdminLoginView(View):
    template_name = 'accounts/admin_login.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.is_verified():
            return redirect('/admin/')
        return render(request, self.template_name, {'error': None})

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        totp_token = request.POST.get('totp_token', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, self.template_name, {
                'error': 'Invalid username or password.',
                'username': username,
            })

        if not user.is_staff:
            return render(request, self.template_name, {
                'error': 'You do not have permission to access this area.',
                'username': username,
            })

        # Verify TOTP if user has a device
        devices = TOTPDevice.objects.filter(user=user, confirmed=True)
        if devices.exists():
            verified = False
            for device in devices:
                if device.verify_token(totp_token):
                    verified = True
                    break
            if not verified:
                return render(request, self.template_name, {
                    'error': 'Invalid two-factor authentication code.',
                    'username': username,
                    'needs_totp': True,
                })

        login(request, user)
        return redirect(request.POST.get('next', '/admin/'))
