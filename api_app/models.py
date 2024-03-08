from django.db import models


# Create your models here.
class Review(models.Model):
    date = models.DateTimeField()
    rating_average = models.FloatField()
    rating_count = models.FloatField()
