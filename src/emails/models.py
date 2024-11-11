from django.db import models
import uuid
from django.conf import urls
from django.conf import settings

# Create your models here.
'''
Email verification for short-lived access
- Views:
    - Collect user email
    - Verify user email
        - Activate session
- Models:
    - Email
    - EmailVerificationToken
'''

class Email(models.Model):
    # user =
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

# class Purchase(models.Model):
#     email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
#     course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

class EmailVerificationEvent(models.Model):
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    # token
    # ip_address
    token = models.UUIDField(default=uuid.uuid1)
    attempts = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    expired = models.BooleanField(default=False)
    expired_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    # did_sent -> for celery task
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_link(self):
        return f"{settings.BASE_URL}/verify/{self.token}/"