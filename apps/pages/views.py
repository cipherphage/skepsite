from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from apps.events.models import Event
from apps.communications.email_utils import send_contact_message


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = Event.objects.filter(is_active=True).first()
        ctx['past_years'] = list(range(2009, 2025))
        return ctx


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = Event.objects.filter(is_active=True).first()
        return ctx


class ContactView(View):
    """PRG pattern — GET shows form, POST handles submission."""

    def get(self, request):
        sent = request.GET.get('sent') == '1'
        return render(request, 'pages/contact.html', {'sent': sent})

    def post(self, request):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        errors = {}
        if not name:
            errors['name'] = 'Your name is required.'
        if not email or '@' not in email:
            errors['email'] = 'A valid email address is required.'
        if not message:
            errors['message'] = 'A message is required.'

        if errors:
            return render(request, 'pages/contact.html', {
                'errors': errors,
                'form_data': {'name': name, 'email': email, 'subject': subject, 'message': message},
            })

        send_contact_message(name, email, subject or 'General inquiry', message)
        return redirect('/contact/?sent=1')


class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'
