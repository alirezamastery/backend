from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

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


class ProductCPUAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductCPU, ProductCPUAdmin)
