from django.db import models
from django.core.validators import MinValueValidator
from .product_base import ProductBase, validate_positive_number
from .category import Category

class ProductCPU(ProductBase):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False,
                                 related_name='product_cpu')
    cores = models.IntegerField(validators=[MinValueValidator(0)])
    clock_speed = models.DecimalField(decimal_places=2 , max_digits=20)
