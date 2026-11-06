
from django.db import models
from django.conf import settings


class DiagnosisResult(models.Model):

    RISK_LEVEL_CHOICES = [
        ('safe', '안전'),
        ('caution', '주의'),
        ('danger', '위험'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diagnosis_results'
    )

    # 분석 대상 앱 정보
    package_name = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )

    apk_sha256 = models.CharField(
        max_length=64,
        blank=True,
        default=''
    )

    event_type = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    # Android에서 전달한 원본 시각
    occurred_at = models.DateTimeField(
        null=True,
        blank=True
    )

    collected_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # 분석 결과
    risk_score = models.IntegerField(default=0)

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES
    )

    summary = models.TextField(blank=True)

    reasons = models.JSONField(default=list, blank=True)

    confidence = models.FloatField(default=0.2)

    confidence_level = models.CharField(
        max_length=20,
        blank=True,
        default=''
    )

    time_gap_seconds = models.FloatField(
        null=True,
        blank=True
    )

    score_breakdown = models.JSONField(
        default=dict,
        blank=True
    )

    virustotal = models.JSONField(
        default=dict,
        blank=True
    )

    scanned_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scanned_at']

    def __str__(self):
        return f'{self.user.username} - {self.risk_level}'
