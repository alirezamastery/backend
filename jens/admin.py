from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _

from .models import ProductCPU, Category, ProductImage, Changer, RAM


class CategoryInline(admin.TabularInline):
    model = Category


class CategoryAdmin(DraggableMPTTAdmin):
    model = Category
    inlines = [CategoryInline]
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'date_created', 'id')
    list_display_links = ('indented_title',)
    list_filter = ('name',)


class ProductImageInline(GenericTabularInline):
    model = ProductImage
    fields = ('title', 'image', 'render_image')
    readonly_fields = ('render_image',)

    def render_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="max-width:300px;max-height:300px" />')


class ProductAdminBase(admin.ModelAdmin):
    class Media:
        css = {"all": ("css/sample_admin.css",)}

    inlines = [ProductImageInline]
    readonly_fields = ['slug', 'image_tag']
    list_display = ['name', 'price', 'inventory', 'in_stock', 'available', 'date_created', 'image_tag_list', 'pk']
    list_editable = ['price', 'inventory', 'available']
    list_filter = ('available', 'price', 'inventory', 'manufacturer')
    search_fields = ('name', 'category__name', 'manufacturer')

    # fieldsets = [
    #     (None, {'fields': ('category', 'name')}),
    #     (_('price'), {'fields': ('price', 'discount', 'inventory')}),
    #     (_('status'), {'fields': ('available',)}),
    #     (_('information'), {'fields': ('manufacturer', 'description')}),
    #     (_('slug'), {'fields': ('slug',)}),
    # ]

    def image_tag_list(self, obj):
        img = obj.other_images.first()  # to get generic ProductImage objects related to the obj
        if img is None:
            img_url = '/media/default.jpg'
        else:
            img_url = img.image.url

        return format_html(f'<img src="{img_url}" width="50" height="50" />')

    image_tag_list.short_description = 'Image'

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['category'].widget.can_add_related = False
        form.base_fields['category'].widget.can_change_related = False
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.GET.get('category'):  # when coming from product_create view prepopulate category choice
            kwargs['initial'] = request.GET.get('category')
            kwargs['queryset'] = Category.objects.filter(name=request.GET.get('category'))
        elif db_field.name == 'category':
            kwargs['queryset'] = Category.objects.filter(children__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_fieldsets(self, request, obj=None):  # this is not a good way to dynamically add fieldsets!
    #     fields_sets = super().get_fieldsets(request, obj)
    #     specific_fields = []
    #     fields = obj._meta.get_fields()
    #     start = False
    #     for field in fields:
    #         if not start and field.name != 'date_updated':
    #             continue
    #         else:
    #             start = True
    #         if start and field.name != 'date_updated':
    #             if field.editable:
    #                 specific_fields.append(field.name)
    #     fields_sets.append((_('details'), {'fields': specific_fields}))
    #     return fields_sets


class ProductCPUAdmin(ProductAdminBase):
    change_form_template = 'admin/jens/change_form_custom.html'
    change_list_template = 'admin/jens/change_list_custom.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['from_me'] = 'from me with love'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['from_me'] = 'this is it'

        return super().changelist_view(request, extra_context)


# example of modifying a view on a model:
class ChangerAdmin(admin.ModelAdmin):
    change_list_template = 'admin/jens/change_list_changer.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['from_me'] = 'whatever'
        return super().changelist_view(request, extra_context)


# class RAMAdmin(ProductAdminBase):
#     pass

    # def get_model_perms(self, request):
    #     """
    #     Return empty perms dict thus hiding the model from admin index.
    #     """
    #     return {}
    #
    # def get_changeform_initial_data(self, request):
    #     name = request.GET.get('category')
    #     print(name)
    #     return {'category': name}


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductCPU, ProductCPUAdmin)
admin.site.register(Changer, ChangerAdmin)
# admin.site.register(RAM, RAMAdmin)
