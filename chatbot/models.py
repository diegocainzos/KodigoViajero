from django.db import models

# Create your models here.
class Destinations(models.Model):
    country = models.CharField(max_length=100)
    text = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.country