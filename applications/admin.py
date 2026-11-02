from django.contrib import admin
from .models import InstalledApp, AppPermission, AppExecutionLog


class AppPermissionInline(admin.TabularInline):
    model = AppPermission
    extra = 0


class AppExecutionLogInline(admin.TabularInline):
    model = AppExecutionLog
    extra = 0


@admin.register(InstalledApp)
class InstalledAppAdmin(admin.ModelAdmin):

    list_display = (
        'app_name',
        'package_name',
        'user',
        'is_system_app',
        'last_scanned',
    )

    search_fields = (
        'app_name',
        'package_name',
        'user__username',
    )

    list_filter = ('is_system_app',)

    inlines = [
        AppPermissionInline,
        AppExecutionLogInline,
    ]


@admin.register(AppPermission)
class AppPermissionAdmin(admin.ModelAdmin):

    list_display = (
        'app',
        'permission_name',
        'is_granted',
    )

    list_filter = ('is_granted',)


@admin.register(AppExecutionLog)
class AppExecutionLogAdmin(admin.ModelAdmin):

    list_display = (
        'app',
        'execution_type',
        'occurred_at',
    )

    list_filter = ('execution_type',)