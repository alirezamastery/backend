from django.contrib import admin

from .models import Category , Sample


class SampleAdmin(admin.ModelAdmin):
    model = Sample
    readonly_fields = ['slug']


class SampleAdminInline(admin.TabularInline):
    model = Sample
    extra = 0
    verbose_name = None
    exclude = ['slug']


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = [SampleAdminInline]
    readonly_fields = ['slug']


admin.site.register(Category , CategoryAdmin)
admin.site.register(Sample , SampleAdmin)
