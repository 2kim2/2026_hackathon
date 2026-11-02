from django.db import models
from django.conf import settings


class FamilyConnection(models.Model):

    STATUS_CHOICES = [
        ('pending', '연결 대기'),
        ('accepted', '연결 완료'),
        ('rejected', '연결 거절'),
    ]

    # 보호자 계정
    guardian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='guardian_connections'
    )

    # 어르신 계정
    senior = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='senior_connections'
    )

    # 연결 상태
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # 연결 요청 및 변경 시각
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 동일한 두 계정 사이의 중복 연결 방지
        constraints = [
            models.UniqueConstraint(
                fields=['guardian', 'senior'],
                name='unique_family_connection'
            ),
            # 자기 자신과 연결할 수 없음
            models.CheckConstraint(
                condition=~models.Q(guardian=models.F('senior')),
                name='family_connection_not_self'
            ),
        ]

    def __str__(self):
        return f'{self.guardian.username} → {self.senior.username}'