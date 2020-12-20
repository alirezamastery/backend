from django.contrib import admin

from .models import Product , RatingModel


class CustomModelAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

    def slug(self , obj):  # does not work as suggested
        print(f'*** CLASSIFIED *** {obj.slug}')
        return f'*** CLASSIFIED *** {obj.slug}'


admin.site.register(Product , CustomModelAdmin)
admin.site.register(RatingModel)
