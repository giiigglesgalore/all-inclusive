from django.shortcuts import render
from emails.forms import EmailForm
from emails.models import Email, EmailVerificationEvent
from emails import services as emails_services
from django.conf import settings

EMAIL_ADDRESS = settings.EMAIL_HOST_USER

def home_view(request, *args, **kwargs):
    template_name = 'home.html'

    # request POST data (to send the data)
    print(request.POST)
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": ""
    }
    
    if form.is_valid():
        email_val = form.cleaned_data.get('email')
        obj = emails_services.start_verification_event(email_val)
        print(obj)
        context['form'] = EmailForm()
        context['message'] = f"Success! Check you email for verification from {EMAIL_ADDRESS}."
    else:
        print(form.errors)
    print('email_id', request.session.get('email_id'))
    print(form.is_valid())
    return render(request, template_name, context)

def login_logout_template_view(request):
    return render(request, "auth/login-logout.html", {})