# analyzer/services/permission_analyzer.py
# 앱의 위험 권한 보유 여부 (PackageManager 권한 목록 기반)
# 권한은 이벤트 시점과 수집 시점 사이에 거의 바뀌지 않으므로 시간차 신뢰도를 적용하지 않음
 
# 알림 접근은 매니페스트 권한이 아니라 '특별 접근'이라 requestedPermissions 에 나오지 않음.
# 프론트가 NotificationManagerCompat.getEnabledListenerPackages() 로 확인해
# 아래 이름으로 권한 목록에 넣어 보내기로 약속
NOTIFICATION_LISTENER = "android.permission.BIND_NOTIFICATION_LISTENER_SERVICE"
 
# 권한명 → (점수, 사유)
SENSITIVE_PERMISSIONS = {
    NOTIFICATION_LISTENER: (15, "알림 접근 권한 사용"),
    "android.permission.SYSTEM_ALERT_WINDOW": (15, "다른 앱 위에 표시 권한 사용"),
}
 
# 백그라운드 동작 가능성을 높이는 권한
BACKGROUND_CAPABLE_PERMISSIONS = {
    "android.permission.RECEIVE_BOOT_COMPLETED": (5, "부팅 시 자동 실행 권한 사용"),
    "android.permission.FOREGROUND_SERVICE": (5, "포그라운드 서비스 실행 권한 사용"),
}
 
 
def analyze_permissions(permissions):
    """permissions: {권한명: 허용여부} (snapshot.normalize_snapshot 결과)"""
    risk_score = 0
    risk_reasons = []
    has_sensitive_access = False
 
    for name, (score, reason) in SENSITIVE_PERMISSIONS.items():
        if permissions.get(name) is True:
            risk_score += score
            risk_reasons.append(reason)
            has_sensitive_access = True
 
    for name, (score, reason) in BACKGROUND_CAPABLE_PERMISSIONS.items():
        if permissions.get(name) is True:
            risk_score += score
            risk_reasons.append(reason)
 
    return {
        "risk_score": risk_score,
        "risk_reasons": risk_reasons,
        "has_sensitive_access": has_sensitive_access,
    }
 