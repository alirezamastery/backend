from django.db import models
from django.core.validators import MinValueValidator
from .product_base import ProductBase
from .category import Category

class MB(ProductBase):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False,
                                 related_name='product_mb')
    pcie_lanes = models.IntegerField(validators=[MinValueValidator(0)] , blank=True , null=True)
