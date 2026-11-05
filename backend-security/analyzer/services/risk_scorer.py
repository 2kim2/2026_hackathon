# analyzer/services/risk_scorer.py
# 권한 + 화면/인터넷 상태 + VirusTotal 결과로 최종 위험 점수와 등급 산출
# 응답 키는 BE1 진단 결과 저장 API(reasons, summary, safe/caution/danger)에 맞춤
from analyzer.services.permission_analyzer import analyze_permissions
from analyzer.services.background_analyzer import analyze_background
 
MAX_SCORE = 100
 
LEVEL_SAFE = "safe"
LEVEL_CAUTION = "caution"
LEVEL_DANGER = "danger"
 
SUMMARY_BY_LEVEL = {
    LEVEL_SAFE: "특별한 위험 징후가 발견되지 않았습니다.",
    LEVEL_CAUTION: "주의가 필요한 앱입니다.",
    LEVEL_DANGER: "위험 가능성이 높은 앱입니다.",
}
 
 
def calculate_risk(snapshot, virustotal_result=None, recent_snapshots=None):
    """
    snapshot          : snapshot.normalize_snapshot() 결과
    virustotal_result : check_virustotal(snapshot["apk_sha256"]) 결과 (기존과 동일)
    recent_snapshots  : 같은 앱의 최근 24시간 스냅샷 목록 (선택)
    """
 
    # 1. 권한 분석 (시간차 영향 없음)
    permission_result = analyze_permissions(snapshot["permissions"])
 
    # 2. 화면/인터넷 상태 분석 (시간차 신뢰도 반영)
    background_result = analyze_background(snapshot, recent_snapshots)
 
    total_score = permission_result["risk_score"] + background_result["risk_score"]
    reasons = permission_result["risk_reasons"] + background_result["risk_reasons"]
 
    # 3. 조합 규칙: 민감 권한 + 화면 꺼짐 + 인터넷 연결
    combo_score = 0
    combo_reason = None
    if (
        permission_result["has_sensitive_access"]
        and background_result["screen_off"]
        and background_result["network_on"]
    ):
        combo_score = round(10 * background_result["confidence"])
        if combo_score:
            combo_reason = "민감 권한을 가진 앱이 화면이 꺼진 상태에서 인터넷 연결 중 동작"
            reasons.append(combo_reason)
    total_score += combo_score
 
    # 4. VirusTotal 결과 반영 (기존 로직 그대로)
    virustotal_score = 0
    virustotal_status = "not_checked"
    virustotal_reason = None
 
    malicious = None
    suspicious = None
    undetected = None
    total_engines = None
    detection_ratio = None
 
    if virustotal_result:
        virustotal_status = virustotal_result.get("status", "error")
 
        if virustotal_status == "completed":
 
            malicious = virustotal_result.get("malicious", 0)
            suspicious = virustotal_result.get("suspicious", 0)
            undetected = virustotal_result.get("undetected", 0)
            total_engines = virustotal_result.get("total_engines", 0)
            detection_ratio = virustotal_result.get("detection_ratio", "0/0")
 
            if malicious >= 6:
                virustotal_score = 40
            elif malicious >= 3:
                virustotal_score = 20
            elif malicious >= 1:
                virustotal_score = 10
 
            if malicious > 0:
                virustotal_reason = f"VirusTotal에서 악성으로 탐지한 엔진 {malicious}개"
                reasons.append(virustotal_reason)
 
    # 5. 최종 점수 계산
    total_score = min(total_score + virustotal_score, MAX_SCORE)
 
    # 6. 위험 등급 분류
    risk_level = classify_risk(total_score)
 
    # 7. 요약 문장: 등급 문구 + 가장 중요한 근거 1개
    main_reason = next(
        (r for r in [
            virustotal_reason,
            combo_reason,
            (background_result["risk_reasons"] or [None])[0],
            (permission_result["risk_reasons"] or [None])[0],
        ] if r),
        None,
    )
    summary = build_summary(risk_level, main_reason, len(reasons))
 
    return {
        "package_name": snapshot["package_name"],
        "risk_score": total_score,
        "risk_level": risk_level,
        "summary": summary,
        "reasons": reasons,
 
        # 판정 근거 신뢰도
        "confidence": background_result["confidence"],
        "confidence_level": background_result["confidence_level"],
        "time_gap_seconds": background_result["time_gap_seconds"],
 
        "score_breakdown": {
            "permission": permission_result["risk_score"],
            "background": background_result["risk_score"],
            "combination": combo_score,
            "virustotal": virustotal_score,
        },
 
        "virustotal": {
            "status": virustotal_status,
            "malicious": malicious,
            "suspicious": suspicious,
            "undetected": undetected,
            "total_engines": total_engines,
            "detection_ratio": detection_ratio,
            "risk_score": virustotal_score
        }
    }
 
 
def build_summary(risk_level, main_reason, reason_count):
    text = SUMMARY_BY_LEVEL[risk_level]
    if risk_level == LEVEL_SAFE or not main_reason:
        return text
    if reason_count > 1:
        return f"{text} ({main_reason} 외 {reason_count - 1}건)"
    return f"{text} ({main_reason})"
 
 
def classify_risk(score):
    if score < 30:
        return LEVEL_SAFE
    elif score < 60:
        return LEVEL_CAUTION
    else:
        return LEVEL_DANGER
 