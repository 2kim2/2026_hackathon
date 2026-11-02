from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'role',
        'phone_number',
        'is_staff',
        'created_at',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('시니어 가드 정보', {
            'fields': ('role', 'phone_number', 'created_at')
        }),
    )

    readonly_fields = ('created_at',)