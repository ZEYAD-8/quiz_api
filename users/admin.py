from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserCustom


class UserCustomAdmin(UserAdmin):
    model = UserCustom
    list_display = ('id', 'email', 'is_creator', 'is_admin', 'is_active', 'date_joined')
    list_filter = ('is_creator', 'is_admin')
    search_fields = ('email',)
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'is_creator', 'is_admin')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_creator', 'is_admin', 'is_active')}
        ),
    )

admin.site.register(UserCustom, UserCustomAdmin)
