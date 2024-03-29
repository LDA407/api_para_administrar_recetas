from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
# metodo para traducir a texto los objetos
from django.utils.translation import gettext as _
 


# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display= ['email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username',)}),
        (_('Permissions'), {'fields':('is_active', 'is_staff', 'is_superuser')}),
        (_('Important Date'), {'fields':('last_login',)}),
    )
    add_fieldsets = (
    	(None,{
    		'classes': ('wide',),
    		'fields': ('email', 'password1', 'password2'),
    	}),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)



