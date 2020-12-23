from django.db import models


class Sample(models.Model):
    name = models.CharField(default='' , max_length=50 , blank=False)

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def filter_fields():
        form = dict()
        form['a'] = 'A'
        fields = __class__._meta.get_fields()
        for f in fields:
            print('type:' , __class__._meta.get_field(f.name).get_internal_type())
            print(f.get_internal_type())
            form[f.name] = f.get_internal_type()
        # for f in fields[0].__dict__:
        #     print(f'{f:<20} | {fields[0].__dict__[f]}')
        return form
