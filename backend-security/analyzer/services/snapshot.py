# analyzer/services/snapshot.py
# 프론트가 5초 주기로 UsageStatsManager 를 조회하다 새 앱 사용 이벤트를 발견하면
# 그 순간의 권한 목록 / 인터넷 연결 / 화면 활성 상태를 묶어 보내는 스냅샷을 정규화
from datetime import datetime, timezone
 
# 이벤트 발생(occurred_at) ↔ 상태 수집(collected_at) 시간차별 신뢰도.
# 정상이라면 폴링 주기(5초) 안쪽이지만, Doze 등으로 조회가 밀리면 시간차가 커진다.
TIME_GAP_CONFIDENCE = [
    (10, 1.0, "high"),        # 10초 이내: 폴링 주기 2회 이내, 정상
    (60, 0.7, "medium"),      # 1분 이내
    (5 * 60, 0.4, "low"),     # 5분 이내
]
MIN_CONFIDENCE = (0.2, "very_low")  # 5분 초과
 
 
def _parse_time(value):
    """ISO 8601 문자열 또는 epoch milliseconds(UsageEvents 기본 단위)."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
    if isinstance(value, str):
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    raise ValueError(f"시간 형식을 해석할 수 없습니다: {value!r}")
 
 
def _normalize_permissions(raw):
    """
    허용 형식
      - ["android.permission.SYSTEM_ALERT_WINDOW", ...]           (목록에 있으면 허용으로 간주)
      - [{"name": "...", "granted": true}, ...]                   (requestedPermissionsFlags 반영)
    결과: {권한명: 허용여부}
    """
    result = {}
    for item in raw or []:
        if isinstance(item, str):
            result[item] = True
        elif isinstance(item, dict) and item.get("name"):
            result[item["name"]] = bool(item.get("granted", True))
    return result
 
 
def normalize_snapshot(data):
    """요청 바디(dict) → 분석용 dict. 필수값이 없으면 ValueError."""
    if not data.get("package_name"):
        raise ValueError("package_name은 필수입니다.")
 
    occurred_at = _parse_time(data.get("occurred_at"))
    collected_at = _parse_time(data.get("collected_at"))
    if occurred_at is None or collected_at is None:
        raise ValueError("occurred_at, collected_at은 필수입니다.")
 
    network = data.get("network") or {}
    screen = data.get("screen") or {}
 
    return {
        "package_name": data["package_name"],
        "apk_sha256": data.get("apk_sha256"),
        "event_type": data.get("event_type"),
        "occurred_at": occurred_at,
        "collected_at": collected_at,
        "permissions": _normalize_permissions(data.get("permissions")),
        "network": {
            "is_connected": bool(network.get("is_connected", False)),
            "type": network.get("type", "NONE"),
        },
        "screen": {
            # PowerManager.isInteractive()
            "is_interactive": bool(screen.get("is_interactive", True)),
        },
        # 안드로이드 제한으로 프론트에서 항상 null 전송. 받기만 하고 점수에는 쓰지 않음
        "app_process_importance": data.get("app_process_importance"),
    }
 
 
def get_time_gap_confidence(snapshot):
    """시간차(초), 신뢰도(0~1), 신뢰도 등급."""
    gap = (snapshot["collected_at"] - snapshot["occurred_at"]).total_seconds()
    gap = max(gap, 0.0)  # 기기 시계 오차로 음수면 0 취급
 
    for limit, confidence, label in TIME_GAP_CONFIDENCE:
        if gap <= limit:
            return {"time_gap_seconds": gap, "confidence": confidence, "confidence_level": label}
 
    confidence, label = MIN_CONFIDENCE
    return {"time_gap_seconds": gap, "confidence": confidence, "confidence_level": label}
 