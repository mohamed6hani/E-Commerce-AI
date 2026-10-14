from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.title