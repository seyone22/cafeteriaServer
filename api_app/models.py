from django.db import models


# Create your models here.
class Review(models.Model):
    date = models.DateTimeField()
    rating = models.FloatField()
    site = models.CharField(max_length=32)
