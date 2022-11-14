from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product


User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открыт'),
        ('in_process', 'В обработке'),
        ('canceled', 'Отменен'),
        ('finished', 'Завершен')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    products = models.ManyToManyField(
        to=Product,
        through='OrderItems'
    )
    total_sum = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='open')

    def __str__(self) -> str:
        return f'Order №{self.id}'



class OrderItems(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.RESTRICT,
        related_name='items'
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.RESTRICT,
        related_name='items'
    )
    quantity = models.PositiveIntegerField(default=1)