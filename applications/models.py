
from django.db import models
from django.conf import settings


class InstalledApp(models.Model):
    # 앱을 소유한 사용자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='installed_apps'
    )

    # 앱 기본 정보
    package_name = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255)
    version_name = models.CharField(
        max_length=100,
        blank=True
    )

    is_system_app = models.BooleanField(default=False)

    first_seen = models.DateTimeField(auto_now_add=True)
    last_scanned = models.DateTimeField(auto_now=True)

    class Meta:
        # 한 사용자의 동일한 앱은 중복 등록하지 않음
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'package_name'],
                name='unique_user_package'
            )
        ]

    def __str__(self):
        return f'{self.app_name} ({self.package_name})'


class AppPermission(models.Model):
    # 권한이 속한 앱
    app = models.ForeignKey(
        InstalledApp,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    # 권한 이름
    permission_name = models.CharField(max_length=255)

    # 권한 허용 여부
    is_granted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['app', 'permission_name'],
                name='unique_app_permission'
            )
        ]

    def __str__(self):
        return f'{self.app.app_name} - {self.permission_name}'


class AppExecutionLog(models.Model):

    EXECUTION_TYPES = [
        ('direct', '직접 실행'),
        ('background', '백그라운드 실행'),
    ]

    # 실행 기록이 속한 앱
    app = models.ForeignKey(
        InstalledApp,
        on_delete=models.CASCADE,
        related_name='execution_logs'
    )

    # 실행 유형
    execution_type = models.CharField(
        max_length=20,
        choices=EXECUTION_TYPES
    )

    # 실행 기록 발생 시각
    occurred_at = models.DateTimeField()

    # 백엔드에 기록이 저장된 시각
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-occurred_at']

    def __str__(self):
        return f'{self.app.app_name} - {self.execution_type}'
