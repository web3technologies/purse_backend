from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from purse_auth.models import User
# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('first_name', 'last_name', 'email', "phone_number", 'is_staff', 'is_active',)
    list_filter = ('first_name', 'last_name', 'email', "phone_number", 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name','email', 'password', "phone_number",)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active', "phone_number",)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
