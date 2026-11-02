from django.contrib import admin
from .models import FCMToken


@admin.register(FCMToken)
class FCMTokenAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'device_name',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'user__username',
        'device_name',
    )