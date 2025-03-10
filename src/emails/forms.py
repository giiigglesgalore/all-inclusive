from django import forms
from .models import Email, EmailVerificationEvent
from . import css, services


class EmailForm(forms.Form):
    email = forms.EmailField(
        # html fields
        widget=forms.EmailInput(
            attrs={
                "id": "email-login-input",
                "class": css.EMAIL_FEILD_CSS,
                "placeholder": "your email address",
            }
        )
    )
    # class Meta:
    #     model = EmailVerificationEvent
    #     fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        verified = services.verify_email(email)
        if verified:
            raise forms.ValidationError("Invalid email. Please try again.")
        return email