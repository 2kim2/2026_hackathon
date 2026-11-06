
from rest_framework import serializers
from .models import DiagnosisResult


class DiagnosisResultSerializer(serializers.ModelSerializer):

    scanned_at = serializers.DateTimeField(required=False)

    class Meta:
        model = DiagnosisResult

        fields = [
            'id',
            'package_name',
            'apk_sha256',
            'event_type',
            'occurred_at',
            'collected_at',
            'risk_score',
            'risk_level',
            'summary',
            'reasons',
            'confidence',
            'confidence_level',
            'time_gap_seconds',
            'score_breakdown',
            'virustotal',
            'scanned_at',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate_risk_score(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError(
                "risk_score는 0부터 100 사이여야 합니다."
            )
        return value

    def validate_reasons(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "reasons는 배열 형식이어야 합니다."
            )
        if not all(isinstance(item, str) for item in value):
            raise serializers.ValidationError(
                "reasons의 각 항목은 문자열이어야 합니다."
            )
        return value

    def validate_confidence(self, value):
        if not 0.2 <= value <= 1.0:
            raise serializers.ValidationError(
                "confidence는 0.2부터 1.0 사이여야 합니다."
            )
        return value

    def validate_time_gap_seconds(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "time_gap_seconds는 0 이상이어야 합니다."
            )
        return value

    def validate_score_breakdown(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "score_breakdown은 객체 형식이어야 합니다."
            )
        return value

    def validate_virustotal(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "virustotal은 객체 형식이어야 합니다."
            )
        return value

    def validate_apk_sha256(self, value):
        if value and (
            len(value) != 64
            or any(char not in '0123456789abcdefABCDEF' for char in value)
        ):
            raise serializers.ValidationError(
                "apk_sha256는 64자리 16진수여야 합니다."
            )
        return value

class AnalysisRequestSerializer(serializers.Serializer):
    """
    Android에서 전달하는 앱 이벤트 스냅샷 검증
    """

    package_name = serializers.CharField(max_length=255)

    apk_sha256 = serializers.CharField(
        max_length=64,
        required=False,
        allow_blank=True,
    )

    event_type = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )

    occurred_at = serializers.JSONField()
    collected_at = serializers.JSONField()

    permissions = serializers.JSONField(required=False)
    network = serializers.JSONField(required=False)
    screen = serializers.JSONField(required=False)

    app_process_importance = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    def validate_apk_sha256(self, value):
        if value and (
            len(value) != 64
            or any(
                char not in '0123456789abcdefABCDEF'
                for char in value
            )
        ):
            raise serializers.ValidationError(
                'apk_sha256는 64자리 16진수여야 합니다.'
            )
        return value

    def validate_permissions(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                'permissions는 배열이어야 합니다.'
            )

        for item in value:
            if isinstance(item, str):
                continue

            if isinstance(item, dict):
                if not isinstance(item.get('name'), str):
                    raise serializers.ValidationError(
                        '권한 객체에는 문자열 name이 필요합니다.'
                    )
                if 'granted' in item and not isinstance(
                    item['granted'], bool
                ):
                    raise serializers.ValidationError(
                        'granted는 true 또는 false여야 합니다.'
                    )
                continue

            raise serializers.ValidationError(
                '권한은 문자열 또는 객체 형식이어야 합니다.'
            )

        return value

    def validate_network(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                'network는 객체 형식이어야 합니다.'
            )
        return value

    def validate_screen(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                'screen은 객체 형식이어야 합니다.'
            )
        return value

    def validate_occurred_at(self, value):
        validate_event_timestamp(value, 'occurred_at')
        return value

    def validate_collected_at(self, value):
        validate_event_timestamp(value, 'collected_at')
        return value


def validate_event_timestamp(value, field_name):
    """
    ISO 8601 문자열 또는 Unix epoch 밀리초인지 확인한다.
    """

    from datetime import datetime, timezone as datetime_timezone
    from django.utils.dateparse import parse_datetime

    if isinstance(value, bool):
        raise serializers.ValidationError(
            f'{field_name}의 날짜 형식이 올바르지 않습니다.'
        )

    if isinstance(value, (int, float)):
        try:
            datetime.fromtimestamp(
                value / 1000,
                tz=datetime_timezone.utc,
            )
            return
        except (ValueError, OverflowError, OSError):
            pass

    elif isinstance(value, str):
        parsed = parse_datetime(value)

        if parsed is not None:
            return

    raise serializers.ValidationError(
        f'{field_name}은 ISO 8601 또는 Unix epoch 밀리초여야 합니다.'
    )
