from rest_framework import serializers
from .models import DiagnosisResult


class DiagnosisResultSerializer(serializers.ModelSerializer):

    scanned_at = serializers.DateTimeField(required=False)

    class Meta:
        model = DiagnosisResult

        fields = [
            'id',
            'risk_score',
            'risk_level',
            'summary',
            'reasons',
            'scanned_at',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate_reasons(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "reasons는 배열 형식이어야 합니다."
            )

        return value