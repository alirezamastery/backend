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
        # full_path = [self.name]
        # k = self.parent
        # while k is not None:
        #     full_path.append(k.name)
        #     k = k.parent
        # return ' | '.join(full_path[::-1])
        return str(self.name)
