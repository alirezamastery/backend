from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_phone_number(value):
    if value < 0:
        raise ValidationError(
                _('%(value)s is not acceptable as inventory value') ,
                params={'value': value} ,
        )


class Sample(models.Model):
    name = models.CharField(default='' , max_length=50 , blank=False)
    inventory = models.IntegerField(default=0 , validators=[validate_phone_number])

    def __str__(self):
        return f'{self.name}'

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
