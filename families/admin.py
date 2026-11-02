from django.contrib import admin
from .models import FamilyConnection


@admin.register(FamilyConnection)
class FamilyConnectionAdmin(admin.ModelAdmin):

    list_display = (
        'guardian',
        'senior',
        'status',
        'created_at',
    )

    list_filter = ('status',)

    search_fields = (
        'guardian__username',
        'senior__username',
    )