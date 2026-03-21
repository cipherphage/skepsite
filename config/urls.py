from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-login/', include('apps.accounts.urls')),
    path('register/', include('apps.registration.urls')),
    path('', include('apps.pages.urls')),
]
