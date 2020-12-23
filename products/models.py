from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image

from assets.unique_slug import unique_slugify

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=300 , unique=True)
    price = models.DecimalField(max_digits=20 , decimal_places=0 , default=0)
    image = models.ImageField(default='default.jpg' , upload_to='product_pics')
    description = models.TextField(default='')
    created_date = models.DateTimeField(auto_now_add=True)
    inventory = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(allow_unicode=True , unique=True , editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('products:product-detail' , kwargs={'pk': self.pk})

    def save(self , *args , **kwargs):
        if not self.id:
            # Newly created object, so set slug
            slug_str = f'{self.name}'
            unique_slugify(self , slug_str)  # this snippet creates unique slugs
            # self.slug = slugify(self.name , allow_unicode=True) # this slug may not be unique

        super().save(*args , **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300 , 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def has_inventory(self):
        return self.inventory > 0


class RatingModel(models.Model):
    """
    use RatingModel.objects.update_or_create() when working with this model
    """

    class rates(models.IntegerChoices):
        poor = 1
        Average = 2
        Good = 3
        Very_Good = 4
        Excellent = 5

    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='product')
    product_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='product_user')
    rating = models.IntegerField(choices=rates.choices)

    def __str__(self):
        return f'Rating of {self.product.name} from {self.product_user.username} is {self.rating}'
