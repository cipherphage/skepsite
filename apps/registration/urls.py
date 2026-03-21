from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [
    path('', views.RegistrationGatewayView.as_view(), name='gateway'),
    path('attendee/', views.AttendeeWizardView.as_view(), name='attendee'),
    path('presenter/', views.PresenterWizardView.as_view(), name='presenter'),
    path('volunteer/', views.VolunteerWizardView.as_view(), name='volunteer'),
    path('submit/<str:registration_type>/', views.RegistrationSubmitView.as_view(), name='submit'),
    path('confirmation/<uuid:token>/', views.ConfirmationView.as_view(), name='confirmation'),
    path('confirmation/<uuid:token>/calendar.ics', views.CalendarICSView.as_view(), name='calendar-ics'),
]
