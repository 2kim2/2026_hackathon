# analyzer/services/background_analyzer.py
# 스냅샷의 화면 상태 + 인터넷 연결 상태로 백그라운드 활동 위험 분석
#
# 프로세스 중요도(app_process_importance)는 안드로이드 제한으로 항상 null 이므로
# "앱이 실제로 백그라운드였는가"는 직접 알 수 없다.
# 대신 "화면이 꺼져 있는데 앱 사용 이벤트가 발생했다" = 사용자가 보고 있지 않은 동작 으로 판단한다.
from analyzer.services.snapshot import get_time_gap_confidence
 
# 최근 스냅샷 중 '화면 꺼짐 + 인터넷 연결' 이벤트 반복 기준 (신뢰도 가중 건수)
REPEAT_HIGH = 30
REPEAT_MEDIUM = 10
 
 
def _is_screen_off_with_network(snapshot):
    return (not snapshot["screen"]["is_interactive"]) and snapshot["network"]["is_connected"]
 
 
def _score_single(snapshot):
    """시간차 신뢰도를 곱하기 전의 단일 스냅샷 점수."""
    screen_off = not snapshot["screen"]["is_interactive"]
    network_on = snapshot["network"]["is_connected"]

    if screen_off and network_on:
        return 20, "화면이 꺼진 상태에서 인터넷에 연결된 채 앱 동작"
    if screen_off:
        return 5, "화면이 꺼진 상태에서 앱 동작"
    return 0, None
 
 
def analyze_background(snapshot, recent_snapshots=None):
    """
    snapshot         : 이번에 들어온 스냅샷 (normalize_snapshot 결과)
    recent_snapshots : 같은 앱의 최근 24시간 스냅샷 목록 (선택, 이번 스냅샷 제외)
    """
    gap = get_time_gap_confidence(snapshot)
    confidence = gap["confidence"]
 
    raw_score, reason = _score_single(snapshot)
    risk_reasons = [reason] if reason else []
 
    # 화면·인터넷 상태는 '수집 시점' 값이므로 시간차만큼 덜 믿는다
    risk_score = round(raw_score * confidence)
 
    if raw_score > 0 and confidence < 1.0:
        risk_reasons.append(
            f"이벤트 발생 {int(gap['time_gap_seconds'])}초 뒤 상태가 수집되어 "
            f"상태 기반 점수를 {int(confidence * 100)}%만 반영"
        )
 
    # 반복 규칙: 화면 꺼짐 + 인터넷 연결 이벤트를 신뢰도로 가중해 센다
    weighted_repeat = confidence if _is_screen_off_with_network(snapshot) else 0.0
    for s in recent_snapshots or []:
        if _is_screen_off_with_network(s):
            weighted_repeat += get_time_gap_confidence(s)["confidence"]
 
    if weighted_repeat >= REPEAT_HIGH:
        risk_score += 20
        risk_reasons.append("화면이 꺼진 상태의 인터넷 활동이 매우 자주 반복됨")
    elif weighted_repeat >= REPEAT_MEDIUM:
        risk_score += 10
        risk_reasons.append("화면이 꺼진 상태의 인터넷 활동이 반복됨")
 
    return {
        "risk_score": risk_score,
        "risk_reasons": risk_reasons,
        "screen_off": not snapshot["screen"]["is_interactive"],
        "network_on": snapshot["network"]["is_connected"],
        "repeat_count_weighted": round(weighted_repeat, 1),
        **gap,  # time_gap_seconds, confidence, confidence_level
    }
 