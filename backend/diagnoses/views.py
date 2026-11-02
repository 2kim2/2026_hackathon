from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import DiagnosisResult
from .serializers import DiagnosisResultSerializer


# 진단 결과 등록 및 목록 조회
class DiagnosisResultListCreateView(generics.ListCreateAPIView):

    serializer_class = DiagnosisResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 로그인한 사용자의 진단 결과만 조회
        return DiagnosisResult.objects.filter(
            user=self.request.user
        ).order_by('-scanned_at')

    def perform_create(self, serializer):
        # 사용자를 요청 데이터가 아닌 로그인 정보에서 가져옴
        scanned_at = serializer.validated_data.get('scanned_at')

        if scanned_at is None:
            serializer.save(
                user=self.request.user,
                scanned_at=timezone.now()
            )
        else:
            serializer.save(
                user=self.request.user
            )


# 진단 결과 상세 조회
class DiagnosisResultDetailView(generics.RetrieveAPIView):

    serializer_class = DiagnosisResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 본인의 진단 결과만 상세 조회 가능
        return DiagnosisResult.objects.filter(
            user=self.request.user
        )
        