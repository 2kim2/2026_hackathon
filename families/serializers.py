from rest_framework import serializers
from .models import FamilyConnection


class FamilyConnectionSerializer(serializers.ModelSerializer):

    guardian_username = serializers.CharField(
        source='guardian.username',
        read_only=True
    )

    senior_username = serializers.CharField(
        source='senior.username',
        read_only=True
    )

    class Meta:
        model = FamilyConnection

        fields = [
            'id',
            'guardian_username',
            'senior_username',
            'status',
            'created_at',
            'updated_at',
        ]
        