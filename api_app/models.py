from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings


# Create your models here.
class Review(models.Model):
    date = models.DateTimeField()
    rating = models.FloatField()
    site = models.CharField(max_length=32)


class EmailConfig(models.Model):
    send_time = models.TimeField()
    email_body = models.TextField()
    sender_list = models.CharField(max_length=255)
    sender_email = models.CharField(max_length=255)
    email_subject = models.CharField(max_length=255)
    smtp_server = models.CharField(max_length=255)
    smtp_port = models.IntegerField()

    class EmailConfigManager(models.Manager):
        def get_or_create_singleton(self):
            obj, created = self.get_or_create(pk=1)  # Ensure only one instance exists
            return obj

    objects = EmailConfigManager()

    def __str__(self):
        return self.smtp_server  # Customize as per your requirement


class Recipient(models.Model):
    email_address = models.EmailField()

    def __str__(self):
        return self.email_address
