"""
Top-level URL patterns for the registrant sign-in flow.
Mounted at /my-registration/ in config/urls.py for a clean public URL,
separate from the /register/ registration wizard.
"""
from django.urls import path
from . import views

app_name = 'registrant'

urlpatterns = [
    path('', views.RegistrantLoginView.as_view(), name='login'),
    path('dashboard/', views.RegistrantDashboardView.as_view(), name='dashboard'),
    path('presentation/edit/', views.PresentationEditView.as_view(), name='presentation-edit'),
    path('logout/', views.RegistrantLogoutView.as_view(), name='logout'),
]
