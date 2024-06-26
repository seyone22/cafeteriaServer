import csv

from django.http import HttpResponse
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
