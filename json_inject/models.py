from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from assets.unique_slug import unique_slugify
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey


def validate_inventory_number(value):
    if value < 0:
        raise ValidationError(_('%(value)s is not acceptable as inventory value'),
                              params={'value': value}, )


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)
    parent = models.ForeignKey('Category', blank=True, null=True, related_name='children',
                               on_delete=models.RESTRICT)
    slug = models.SlugField(allow_unicode=True, unique=True, editable=True)

    class Meta:
        unique_together = ('slug', 'parent',)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' | '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            slug_str = f'{self.name}'
            unique_slugify(self, slug_str)  # this snippet creates unique slugs

        super().save(*args, **kwargs)

    def get_children(self):
        return self.children.all().values('name')


class Sample(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='samples')
    name = models.CharField(default='', max_length=50, blank=False)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    description = RichTextUploadingField(default='')
    created_date = models.DateTimeField(auto_now_add=True)
    inventory = models.IntegerField(default=0, validators=[validate_inventory_number])
    slug = models.SlugField(allow_unicode=True, unique=True, editable=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            slug_str = f'{self.name}'
            unique_slugify(self, slug_str)  # this snippet creates unique slugs

        super().save(*args, **kwargs)

    def in_stock(self):
        return self.inventory > 0

    in_stock.filterable = True
    in_stock.boolean = True

    def category_tree(self):
        full_path = []
        k = self.category
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' | '.join(full_path[::-1])

    def image_tag(self):
        return mark_safe(f'<img src="/media/{self.image}" width="100" height="100" />')

    image_tag.short_description = 'Image'

    # @staticmethod
    # def filter_fields():  # we can add a method that takes no args to serializer
    #     form = dict()
    #     form['a'] = 'A'
    #     fields = __class__._meta.get_fields()
    #     for f in fields:
    #         print('type:' , __class__._meta.get_field(f.name).get_internal_type())
    #         print(f.get_internal_type())
    #         form[f.name] = f.get_internal_type()
    #     # for f in fields[0].__dict__:
    #     #     print(f'{f:<20} | {fields[0].__dict__[f]}')
    #     return form


class Genre(MPTTModel):
    COLOR_CHOICES = (
        ('red', 'Red'),
        ('green', 'Green'),
        ('blue', 'Blue'),
    )

    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # color = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=False)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_filters(self):
        if self.level > 0:
            return
        filters = {
            'price':         {'type': 'range'},
            'name':          {'type': 'text'},
            'has_inventory': {'type': 'boolean'},
            'color':         {'type': 'choices', 'choices': ['blue', 'green', 'blue']}
        }
        return filters


class Band(models.Model):
    COLOR_CHOICES = (
        ('red', 'Red'),
        ('green', 'Green'),
        ('blue', 'Blue'),
    )
    BRANDS = (
        ('asus', 'Asus'),
        ('dell', 'Dell'),
    )
    name = models.CharField(max_length=100, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=False, related_name='leaves')
    brand = models.CharField(max_length=100, choices=BRANDS, blank=False)
    inventory = models.IntegerField(default=0)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=False)

    def __str__(self):
        return f'{self.name}'

    def has_inventory(self):
        return self.inventory > 0


class MediaFile(models.Model):
    title = models.CharField(max_length=200, blank=False)
    video = models.FileField(upload_to='video/')

    def __str__(self):
        return str(self.title)
