from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from assets.unique_slug import unique_slugify

from .category import Category
from .product_image import ProductImage


def validate_positive_number(value):
    if value < 0:
        raise ValidationError(_('%(value)s is not acceptable as inventory value'),
                              params={'value': value}, )


class ProductBase(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False,
    #                              related_name='products')

    name = models.CharField(max_length=500, blank=False)
    price = models.IntegerField(blank=False, validators=[MinValueValidator(0)])
    manufacturer = models.CharField(max_length=500)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    inventory = models.IntegerField(blank=False, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = RichTextUploadingField(default='', blank=True, null=True)
    available = models.BooleanField(default=True)
    slug = models.SlugField(allow_unicode=True, unique=True, editable=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    other_images = GenericRelation(ProductImage, related_query_name='other_images')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            slug_str = f'{self.name}'
            unique_slugify(self, slug_str)  # this snippet creates unique slugs

        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > settings.PRODUCT_IMAGE_HEIGHT or img.width > settings.PRODUCT_IMAGE_WIDTH:
            output_size = (settings.PRODUCT_IMAGE_HEIGHT, settings.PRODUCT_IMAGE_WIDTH)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def image_tag(self):
        return mark_safe(f'<img src="/media/{self.image}" width="100" height="100" />')

    image_tag.short_description = 'Image'

    def in_stock(self):
        return self.inventory > 0

    in_stock.boolean = True
