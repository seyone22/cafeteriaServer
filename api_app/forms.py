from django import forms
from .models import EmailConfig

class EmailConfigForm(forms.ModelForm):
    class Meta:
        model = EmailConfig
        fields = ('smtp_server', 'smtp_port', 'sender_email', 'send_time', 'email_subject', 'email_body')

    def clean(self):
        # Ensure only one instance of EmailConfig exists
        if EmailConfig.objects.count() > 0:
            raise forms.ValidationError("There can only be one Email Configuration. Please edit the existing "
                                        "configuration.")
        return super().clean()
