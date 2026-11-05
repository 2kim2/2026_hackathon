import logging
from datetime import datetime, timezone as datetime_timezone

from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DiagnosisResult
from .serializers import (
    DiagnosisResultSerializer,
    AnalysisRequestSerializer,
)
from .services import request_be2_analysis, BE2AnalysisError

from notifications.services import notify_guardians_of_danger


logger = logging.getLogger(__name__)


def parse_event_timestamp(value):
    """
    ISO 8601 또는 Unix epoch 밀리초를 Django DateTime으로 변환한다.
    """

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return datetime.fromtimestamp(
            value / 1000,
            tz=datetime_timezone.utc,
        )

    parsed = parse_datetime(value)

    if parsed is None:
        raise ValueError('날짜 형식이 올바르지 않습니다.')

    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(
            parsed,
            datetime_timezone.utc,
        )

    return parsed


def send_danger_notification(diagnosis):
    try:
        result = notify_guardians_of_danger(diagnosis)

        logger.info(
            '위험 진단 알림 처리 완료: diagnosis_id=%s, result=%s',
            diagnosis.id,
            result,
        )

    except Exception:
        logger.exception(
            '위험 진단 알림 발송 중 오류 발생. diagnosis_id=%s',
            diagnosis.id,
        )


# 기존 진단 결과 등록 및 목록 조회
class DiagnosisResultListCreateView(generics.ListCreateAPIView):

    serializer_class = DiagnosisResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DiagnosisResult.objects.filter(
            user=self.request.user
        ).order_by('-scanned_at')

    def perform_create(self, serializer):

        scanned_at = serializer.validated_data.get('scanned_at')

        if scanned_at is None:
            diagnosis = serializer.save(
                user=self.request.user,
                scanned_at=timezone.now()
            )
        else:
            diagnosis = serializer.save(
                user=self.request.user
            )

        if diagnosis.risk_level == 'danger':
            transaction.on_commit(
                lambda diagnosis=diagnosis:
                    send_danger_notification(diagnosis)
            )


# 새로 추가: Android 이벤트 분석 요청
class DiagnosisAnalyzeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # 1. Android에서 받은 원본 이벤트 데이터 검증
        input_serializer = AnalysisRequestSerializer(
            data=request.data
        )

        if not input_serializer.is_valid():
            return Response(
                {
                    'error': '요청 데이터가 올바르지 않습니다.',
                    'details': input_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        event_data = input_serializer.validated_data

        # 2. 원본 데이터를 BE2에 전달
        try:
            analysis_result = request_be2_analysis(
                event_data
            )

        except BE2AnalysisError as error:
            logger.error('BE2 분석 요청 실패: %s', error)

            return Response(
                {
                    'error': '외부 분석 서버 요청에 실패했습니다.',
                    'details': str(error),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # 3. BE2 응답 필수값 확인
        required_fields = [
            'risk_score',
            'risk_level',
            'summary',
            'reasons',
            'confidence',
            'confidence_level',
            'time_gap_seconds',
            'score_breakdown',
            'virustotal',
        ]

        missing_fields = [
            field for field in required_fields
            if field not in analysis_result
        ]

        if missing_fields:
            logger.error(
                'BE2 응답 필수값 누락: %s',
                missing_fields,
            )

            return Response(
                {
                    'error': 'Backend 2 응답에 필수 항목이 누락되었습니다.',
                    'missing_fields': missing_fields,
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # 4. 분석 결과 검증
        result_data = {
            'package_name': event_data['package_name'],
            'apk_sha256': event_data.get('apk_sha256', ''),
            'event_type': event_data.get('event_type', ''),
            'occurred_at': parse_event_timestamp(
                event_data['occurred_at']
            ),
            'collected_at': parse_event_timestamp(
                event_data['collected_at']
            ),
            'risk_score': analysis_result['risk_score'],
            'risk_level': analysis_result['risk_level'],
            'summary': analysis_result['summary'],
            'reasons': analysis_result['reasons'],
            'confidence': analysis_result['confidence'],
            'confidence_level': analysis_result['confidence_level'],
            'time_gap_seconds': analysis_result['time_gap_seconds'],
            'score_breakdown': analysis_result['score_breakdown'],
            'virustotal': analysis_result['virustotal'],
            'scanned_at': timezone.now(),
        }

        result_serializer = DiagnosisResultSerializer(
            data=result_data
        )

        if not result_serializer.is_valid():
            logger.error(
                'BE2 분석 결과 검증 실패: %s',
                result_serializer.errors,
            )

            return Response(
                {
                    'error': 'Backend 2의 분석 결과 형식이 올바르지 않습니다.',
                    'details': result_serializer.errors,
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # 5. DB 저장 및 위험 알림 예약
        with transaction.atomic():

            diagnosis = result_serializer.save(
                user=request.user
            )

            if diagnosis.risk_level == 'danger':
                transaction.on_commit(
                    lambda diagnosis=diagnosis:
                        send_danger_notification(diagnosis)
                )

        # 6. Android에 저장된 분석 결과 반환
        return Response(
            DiagnosisResultSerializer(diagnosis).data,
            status=status.HTTP_201_CREATED,
        )


# 기존 진단 결과 상세 조회
class DiagnosisResultDetailView(generics.RetrieveAPIView):

    serializer_class = DiagnosisResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DiagnosisResult.objects.filter(
            user=self.request.user
        )