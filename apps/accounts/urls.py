from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.AdminLoginView.as_view(), name='admin-login'),
]
