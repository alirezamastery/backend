from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from assets.unique_slug import unique_slugify


def validate_inventory_number(value):
    if value < 0:
        raise ValidationError(_('%(value)s is not acceptable as inventory value') ,
                              params={'value': value} , )


class Category(models.Model):
    name = models.CharField(max_length=100 , blank=False)
    parent = models.ForeignKey('Category' , blank=True , null=True , related_name='children' , on_delete=models.RESTRICT)
    slug = models.SlugField(allow_unicode=True , unique=True , editable=True)

    class Meta:
        unique_together = ('slug' , 'parent' ,)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' | '.join(full_path[::-1])

    def save(self , *args , **kwargs):
        if not self.id:
            # Newly created object, so set slug
            slug_str = f'{self.name}'
            unique_slugify(self , slug_str)  # this snippet creates unique slugs

        super().save(*args , **kwargs)


class Sample(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    name = models.CharField(default='' , max_length=50 , blank=False)
    inventory = models.IntegerField(default=0 , validators=[validate_inventory_number])
    slug = models.SlugField(allow_unicode=True , unique=True , editable=True)

    def __str__(self):
        return f'{self.name}'

    def save(self , *args , **kwargs):
        if not self.id:
            # Newly created object, so set slug
            slug_str = f'{self.name}'
            unique_slugify(self , slug_str)  # this snippet creates unique slugs

        super().save(*args , **kwargs)

    def in_stock(self):
        return self.inventory > 0

    in_stock.filterable = True

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
