from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm , CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    search_fields = ('username' , 'first_name' , 'last_name' , 'phone_number')
    list_display = ('username' , 'phone_number' , 'is_staff' , 'is_active' , 'pk')
    list_filter = ('is_staff' , 'is_active' ,)
    fieldsets = (
        (None , {'fields': ('username' , 'password')}) ,

        (_('Personal info') , {
            'fields': ('first_name' , 'last_name' , 'phone_number' , 'email')
        }) ,

        (_('Permissions') , {
            'fields': ('is_active' , 'is_staff' , 'is_superuser' , 'groups' , 'user_permissions') ,
        }) ,

        (_('Important dates') , {'fields': ('last_login' , 'date_joined')}) ,
    )
    add_fieldsets = (
        (None , {
            'classes': ('wide' , 'extrapretty') ,
            'fields':  ('username' , 'password1' , 'password2') ,
        }) ,
    )
    # search_fields = ('email',)
    # ordering = ('email',)


admin.site.register(CustomUser , CustomUserAdmin)
