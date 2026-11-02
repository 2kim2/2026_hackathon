
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
        constraints = [
            models.UniqueConstraint(
                fields=['guardian', 'senior'],
                name='unique_family_connection'
            ),
            models.CheckConstraint(
                condition=~models.Q(guardian=models.F('senior')),
                name='family_connection_not_self'
            ),
        ]

    def __str__(self):
        return f'{self.guardian.username} → {self.senior.username}'


class FamilyConnectionCode(models.Model):

    # 코드를 발급한 어르신
    senior = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='family_connection_codes'
    )

    # 8자리 연결 코드
    code = models.CharField(
        max_length=8,
        unique=True
    )

    # 코드 만료 시각
    expires_at = models.DateTimeField()

    # 사용 여부
    is_used = models.BooleanField(default=False)

    # 생성 시각
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.senior.username} - {self.code}'
