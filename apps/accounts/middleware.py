from django.conf import settings
from django.http import HttpResponseForbidden


class AdminIPWhitelistMiddleware:
    """
    Restricts access to /admin/ and /admin-login/ to whitelisted IPs.
    If ADMIN_ALLOWED_IPS is empty, all IPs are allowed (development mode).
    """

    PROTECTED_PREFIXES = ('/admin/', '/admin-login/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._is_protected(request.path):
            allowed_ips = getattr(settings, 'ADMIN_ALLOWED_IPS', [])
            if allowed_ips:
                client_ip = self._get_client_ip(request)
                if client_ip not in allowed_ips:
                    return HttpResponseForbidden(
                        '<h1>403 Forbidden</h1>'
                        '<p>Your IP address is not authorized to access this area.</p>'
                    )
        return self.get_response(request)

    def _is_protected(self, path: str) -> bool:
        return any(path.startswith(prefix) for prefix in self.PROTECTED_PREFIXES)

    @staticmethod
    def _get_client_ip(request) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
