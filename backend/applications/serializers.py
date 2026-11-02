
from rest_framework import serializers
from .models import InstalledApp, AppPermission
from .models import AppExecutionLog


class InstalledAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstalledApp

        fields = [
            'id',
            'package_name',
            'app_name',
            'version_name',
            'is_system_app',
            'first_seen',
            'last_scanned',
        ]

        read_only_fields = [
            'id',
            'first_seen',
            'last_scanned',
        ]


class AppPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppPermission

        fields = [
            'id',
            'permission_name',
            'is_granted',
        ]

        read_only_fields = ['id']

class AppExecutionLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppExecutionLog

        fields = [
            'id',
            'execution_type',
            'occurred_at',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'occurred_at',
            'created_at',
        ]