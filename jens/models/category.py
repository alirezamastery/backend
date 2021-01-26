from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import inspect


class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        # print(print(inspect.stack()[1].function))
        if '__repr__' in inspect.stack()[1].function:
            return str(self.name)
        ancestors = self.get_ancestors(include_self=True)
        ancestors = [ancestor for ancestor in ancestors]
        print(ancestors)

        # print(' | '.join(str(ancestors)))
        return str(self.name)
