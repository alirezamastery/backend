from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from PIL import Image


class ProductImage(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=False, upload_to='images/products/')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.title

    def image_path(self):
        return self.image.path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > settings.PRODUCT_IMAGE_HEIGHT or img.width > settings.PRODUCT_IMAGE_WIDTH:
            output_size = (settings.PRODUCT_IMAGE_HEIGHT, settings.PRODUCT_IMAGE_WIDTH)
            img.thumbnail(output_size)
            img.save(self.image.path)
