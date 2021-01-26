from django.db import models
from django.core.validators import MinValueValidator
from .product_base import ProductBase

class RAM(models.Model):
    clock_speed = models.DecimalField(decimal_places=2 , max_digits=20)
