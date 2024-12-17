from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users

# Custom UserAdmin class
class CustomUserAdmin(UserAdmin):
    model = Users
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'role']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['email']

    # Fields for the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'birth_date', 'gender', 'is_staff')}
        ),
    )

    # Fields for the user change form
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'birth_date', 'gender', 'image', 'is_active', 'is_staff')}
        ),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_superuser', 'user_permissions')}
        ),
    )

# Register the custom user model with the custom UserAdmin
admin.site.register(Users, CustomUserAdmin)
