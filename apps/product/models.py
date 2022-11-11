from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

from .utils import get_time

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    parent_category = models.ForeignKey(
        verbose_name='Родительская категория',
        to='self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True
        )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, primary_key=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def save(self, *args, **kwargs):
        self.in_stock = self.quantity > 0
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images')
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self) -> str:
        return f'Image to {self.product.title}'