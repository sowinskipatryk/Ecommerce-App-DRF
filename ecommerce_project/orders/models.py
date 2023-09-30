from django.conf import settings
from django.db import models
from products.models import Product


class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='OrderItem')
    date_ordered = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    summary_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order for {self.client} placed on {self.date_ordered}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product} in order {self.order}"
