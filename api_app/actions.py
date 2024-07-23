import csv

from django.core.mail import send_mail
from django.http import HttpResponse

from cafeteriaServer import settings
from .models import Review


def export_reviews_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reviews.csv"'

    writer = csv.writer(response)
    # Write the headers
    writer.writerow(['date', 'rating', 'site'])  # Replace with your actual model fields

    # Write data rows
    for obj in queryset:
        writer.writerow([obj.date, obj.rating, obj.site])  # Replace with your actual model fields

    return response


export_reviews_as_csv.short_description = "Export Selected as CSV"


def send_email_to_recipients(modeladmin, request, queryset):
    selected_recipients = queryset.values_list('email_address', flat=True)

    # Example email subject and body
    subject = 'Test Email to Selected Recipients'
    body = 'This is a test email sent to selected recipients.'

    # Fetching default email configuration (assuming only one exists)
    from .models import EmailConfig
    config = EmailConfig.objects.first()
    if config:
        smtp_server = config.smtp_server
        smtp_port = config.smtp_port

        # Set the SMTP backend details
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        settings.EMAIL_HOST = smtp_server
        settings.EMAIL_PORT = smtp_port
        settings.EMAIL_USE_TLS = True

        # Send email to selected recipients
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, selected_recipients)

    # Optionally, add a success message
    modeladmin.message_user(request, "Email sent to selected recipients successfully.")


send_email_to_recipients.short_description = "Send email to selected recipients"
