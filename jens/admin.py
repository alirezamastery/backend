from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _

from .models import ProductCPU, Category, ProductImage, Changer


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

    fieldsets = [
        (None, {'fields': ('category', 'name')}),
        (_('price'), {'fields': ('price', 'discount', 'inventory')}),
        (_('status'), {'fields': ('available',)}),
        (_('information'), {'fields': ('manufacturer', 'description')}),
        (_('slug'), {'fields': ('slug',)}),
    ]

    def image_tag_list(self, obj):
        img = obj.other_images.first()  # to get generic ProductImage objects related to the obj
        if img is None:
            img_url = '/media/default.jpg'
        else:
            img_url = img.image.url

        return format_html(f'<img src="{img_url}" width="50" height="50" />')

    image_tag_list.short_description = 'Image'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = Category.objects.filter(children__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):  # this is not a good way to dynamically add fieldsets!
        fields_sets = super().get_fieldsets(request, obj)
        specific_fields = []
        fields = obj._meta.get_fields()
        start = False
        for field in fields:
            if not start and field.name != 'date_updated':
                continue
            else:
                start = True
            if start and field.name != 'date_updated':
                if field.editable:
                    specific_fields.append(field.name)
        fields_sets.append((_('details'), {'fields': specific_fields}))
        return fields_sets


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


class ChangerAdmin(admin.ModelAdmin):
    change_list_template = 'admin/jens/change_list_changer.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['from_me'] = 'this is it'

        # extra_context['categories'] = Category.objects.filter(level=0)
        # extra_context['sub_categories'] = list()
        extra_context['selectable_categories'] = [None]
        extra_context['selectable_categories'][0] = {'selected': None,
                                                     'options':  Category.objects.filter(level=0)
                                                     }
        extra_context['leaves'] = None

        print(extra_context['selectable_categories'])

        if request.method == 'POST':
            counter = 0
            while True:
                print('-' * 50)
                selected_category = None
                try:
                    selected_category = request.POST.get(f'category_selector_{counter}')
                    print(counter, selected_category)
                except:
                    break
                extra_context['selectable_categories'][counter]['selected'] = selected_category
                if selected_category:
                    selected_category_obj = Category.objects.get(name=selected_category)
                    children = selected_category_obj.get_children()
                    print(children)
                    if not children:
                        selected_product = None
                        try:
                            selected_product = request.POST.get(f'leaves_selector')
                            print(selected_product)
                        except:
                            pass
                        if selected_product:
                            extra_context['leaves'] = {'selected': selected_product,
                                                       'options':  selected_category_obj.products.all()
                                                       }
                            break
                        extra_context['leaves'] = {'selected': None,
                                                   'options':  selected_category_obj.products.all()
                                                   }
                        print('reached to the products')  # insert what you want to do here
                        break
                    print('all passed')
                    extra_context['selectable_categories'].append({'selected': None,
                                                                   'options':  children
                                                                   })
                else:
                    break
                counter += 1

        return super().changelist_view(request, extra_context)


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductCPU, ProductCPUAdmin)
admin.site.register(Changer, ChangerAdmin)
