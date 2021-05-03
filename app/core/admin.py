from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Tag,Ingredient
from django.utils.translation import gettext as _

# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email','name']
    fieldsets = (
        (None,{'fields':('email','password')}),
        (_('Personal Info'),{'fields':('name',)}),
        (_('Permissions'),{'fields':('is_active','is_superuser','is_staff')}),
        (_('Important Dates'),{'fields':('last_login',)})
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2')
        }),
    )


admin.site.register(User,UserAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)

