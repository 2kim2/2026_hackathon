# analyzer/services/risk_scorer.py
# 권한 + 화면/인터넷 상태 + VirusTotal 결과로 최종 위험 점수와 등급 산출
from analyzer.services.permission_analyzer import analyze_permissions
from analyzer.services.background_analyzer import analyze_background
 
MAX_SCORE = 100
 
 
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
    risk_reasons = permission_result["risk_reasons"] + background_result["risk_reasons"]
 
    # 3. 조합 규칙: 민감 권한 + 화면 꺼짐 + 인터넷 연결
    combo_score = 0
    if (
        permission_result["has_sensitive_access"]
        and background_result["screen_off"]
        and background_result["network_on"]
    ):
        combo_score = round(10 * background_result["confidence"])
        if combo_score:
            risk_reasons.append("민감 권한을 가진 앱이 화면이 꺼진 상태에서 인터넷 연결 중 동작")
    total_score += combo_score
 
    # 4. VirusTotal 결과 반영 (기존 로직 그대로)
    virustotal_score = 0
    virustotal_status = "not_checked"
 
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
                risk_reasons.append(
                    f"VirusTotal에서 악성으로 탐지한 엔진 {malicious}개"
                )
 
    # 5. 최종 점수 계산
    total_score = min(total_score + virustotal_score, MAX_SCORE)
 
    # 6. 위험 등급 분류
    risk_level = classify_risk(total_score)
 
    return {
        "package_name": snapshot["package_name"],
        "risk_score": total_score,
        "risk_level": risk_level,
        "risk_reasons": risk_reasons,
 
        # 판정 근거 품질
        "time_gap_seconds": background_result["time_gap_seconds"],
        "confidence": background_result["confidence"],
        "confidence_level": background_result["confidence_level"],
 
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
 
 
def classify_risk(score):
    if score < 30:
        return "안전"
    elif score < 60:
        return "주의"
    else:
        return "위험"
 