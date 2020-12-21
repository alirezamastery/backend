from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Order , OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('item' , 'order' , 'quantity')

    def get_orderer(self , obj):
        return obj.book.author


class OrderItemInline(admin.TabularInline):
    class Media:
        css = {"all": ("css/hide_admin_original.css" ,)}

    model = OrderItem

    extra = 0
    verbose_name = None
    readonly_fields = ['item' , 'quantity' , 'date_created' , 'date_modified']

    def has_add_permission(self , request , obj):
        return False

    def has_delete_permission(self , request , obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]

    list_display = ('user' , 'order_date' , 'checkout' , 'pk')
    readonly_fields = ['user' , 'order_date' , 'get_user_phone_number' , 'get_items_number' , 'checkout']
    fieldsets = (
        (None , {'fields': ('user' , 'get_user_phone_number' , 'order_date' , 'get_items_number')}) ,
        (_('Order Status') , {'fields': ('checkout' ,)})
    )


admin.site.register(Order , OrderAdmin)
admin.site.register(OrderItem , OrderItemAdmin)
