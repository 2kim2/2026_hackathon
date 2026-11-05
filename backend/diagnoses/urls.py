from django.urls import path

from .views import (
    DiagnosisResultListCreateView,
    DiagnosisResultDetailView,
    DiagnosisAnalyzeView,
)


urlpatterns = [

    # 진단 결과 등록 및 목록 조회
    path(
        '',
        DiagnosisResultListCreateView.as_view(),
        name='diagnosis-list-create'
    ),

    # 새 앱 이벤트 분석 요청
    path(
        'analyze/',
        DiagnosisAnalyzeView.as_view(),
        name='diagnosis-analyze'
    ),

    # 진단 결과 상세 조회
    path(
        '<int:pk>/',
        DiagnosisResultDetailView.as_view(),
        name='diagnosis-detail'
    ),

]