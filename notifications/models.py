from django.db import models
from django.conf import settings


class FCMToken(models.Model):

    # 토큰을 등록한 사용자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fcm_tokens'
    )

    # Firebase 기기 토큰
    token = models.TextField(unique=True)

    # 기기 정보
    device_name = models.CharField(
        max_length=100,
        blank=True
    )

    # 토큰 등록 시각
    created_at = models.DateTimeField(auto_now_add=True)

    # 토큰 갱신 시각
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.device_name}'