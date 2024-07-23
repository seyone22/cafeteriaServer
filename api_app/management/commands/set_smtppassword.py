# In api_app/management/commands/set_smtppassword.py
from django.core.management.base import BaseCommand
from api_app.models import EmailConfig
from getpass import getpass


class Command(BaseCommand):
    help = 'Set SMTP password for email configuration'

    def handle(self, *args, **options):
        try:
            email_config = EmailConfig.objects.first()  # Assuming only one config exists
            if email_config:
                new_password = getpass("Enter SMTP password: ")
                email_config.smtp_password = new_password
                email_config.save()
                self.stdout.write(self.style.SUCCESS('SMTP password updated successfully.'))
            else:
                self.stdout.write(self.style.WARNING('No EmailConfig instance found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to set SMTP password: {str(e)}'))
