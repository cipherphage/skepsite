from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-login/', include('apps.accounts.urls')),
    path('register/', include('apps.registration.urls')),
    path('my-registration/', include('apps.registration.urls_registrant')),
    path('', include('apps.pages.urls')),
]
