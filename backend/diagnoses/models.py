from django.db import models
from django.conf import settings


class DiagnosisResult(models.Model):

    RISK_LEVEL_CHOICES = [
        ('safe', '안전'),
        ('caution', '주의'),
        ('danger', '위험'),
    ]

    # 진단을 받은 사용자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diagnosis_results'
    )

    # 전체 위험 점수
    risk_score = models.IntegerField(default=0)

    # 최종 위험 등급
    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES
    )

    # 진단 결과 요약
    summary = models.TextField(blank=True)

    # 위험 판정 근거
    reasons = models.JSONField(default=list, blank=True)

    # 진단을 실시한 시각
    scanned_at = models.DateTimeField()

    # 서버에 저장된 시각
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scanned_at']

    def __str__(self):
        return f'{self.user.username} - {self.risk_level}'