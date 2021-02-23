from django.db import models
from django.core.validators import MinValueValidator
from .product_base import ProductBase
from .category import Category


class RAM(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False,
                                 related_name='product_ram')
    clock_speed = models.DecimalField(decimal_places=2 , max_digits=20)
