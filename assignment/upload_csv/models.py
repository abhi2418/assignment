from turtle import up
from django.db import models

# Create your models here.

class Csv(models.Model):
    image_name = models.CharField(max_length=100)
    objects_detected = models.CharField(max_length=250)
    date = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.image_name}"
