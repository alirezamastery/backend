from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Sample, Genre, Band, MediaFile


class SampleAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("css/sample_admin.css",)}

    model = Sample
    readonly_fields = ['slug', 'image_tag']
    list_display = ('name', 'category_tree', 'in_stock', 'inventory', 'created_date', 'image_tag_list', 'pk',)

    def image_tag_list(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')

    image_tag_list.short_description = 'Image'


class SampleAdminInline(admin.TabularInline):
    model = Sample
    extra = 0
    verbose_name = None
    exclude = ['slug']


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = [SampleAdminInline]
    readonly_fields = ['slug']


class BandInline(admin.TabularInline):
    class Media:
        css = {"all": ("css/hide_admin_original.css",)}

    model = Band


class GenreAdmin(DraggableMPTTAdmin):
    inlines = [BandInline]
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'id')
    list_display_links = ('indented_title',)


class BandAdmin(admin.ModelAdmin):
    # fields = ['name' , 'genre']
    list_display = ['name', 'id']


class MediaFileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Band, BandAdmin)
admin.site.register(MediaFile, MediaFileAdmin)
