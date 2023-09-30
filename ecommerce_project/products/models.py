from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='product_photos/')
    photo_thumbnail = models.ImageField(upload_to='product_photos/thumbnails/')

    def __str__(self):
        return self.name
