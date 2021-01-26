from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html, mark_safe

from .models import ProductCPU, Category, ProductImage


class CategoryInline(admin.TabularInline):
    model = Category


class CategoryAdmin(DraggableMPTTAdmin):
    model = Category
    inlines = [CategoryInline]
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'date_created', 'id')
    list_display_links = ('indented_title',)


class ProductImageInline(GenericTabularInline):
    model = ProductImage
    fields = ('title','image', 'render_image')
    readonly_fields = ('render_image',)

    def render_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')


# class ProductImageAdmin(admin.ModelAdmin):


class ProductCPUAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("css/sample_admin.css",)}

    inlines = [ProductImageInline]
    readonly_fields = ['slug', 'image_tag']
    list_display = ('name', 'price', 'inventory', 'date_created', 'image_tag_list', 'pk',)

    def image_tag_list(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')

    image_tag_list.short_description = 'Image'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = Category.objects.filter(children__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductCPU, ProductCPUAdmin)
