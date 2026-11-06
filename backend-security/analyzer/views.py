import re

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from analyzer.services.snapshot import normalize_snapshot
from analyzer.services.risk_scorer import calculate_risk
from analyzer.services.virustotal import check_virustotal


SHA256_PATTERN = re.compile(r"[a-fA-F0-9]{64}")


def _bad_request(message):
    return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def test_api(request):
    return Response({
        "message": "Security Analysis Server is running!"
    })


@api_view(["POST"])
def analyze_snapshot(request):
    data = request.data

    # 1. 요청 데이터 확인
    if not isinstance(data, dict):
        return _bad_request("요청 데이터는 JSON 객체여야 합니다.")

    # 2. 권한 목록 형식 확인 (문자열 또는 {"name", "granted"} 객체의 배열)
    permissions = data.get("permissions", [])
    if not isinstance(permissions, list):
        return _bad_request("permissions는 배열이어야 합니다.")
    for item in permissions:
        if isinstance(item, str):
            continue
        if not (isinstance(item, dict) and isinstance(item.get("name"), str)):
            return _bad_request("permissions의 각 항목은 권한명 문자열 또는 {name, granted} 객체여야 합니다.")
        if "granted" in item and not isinstance(item["granted"], bool):
            return _bad_request("granted는 true 또는 false여야 합니다.")

    # 3. 인터넷 연결 / 화면 상태 형식 확인
    network = data.get("network", {})
    if not isinstance(network, dict):
        return _bad_request("network는 객체 형식이어야 합니다.")
    if "is_connected" in network and not isinstance(network["is_connected"], bool):
        return _bad_request("network.is_connected는 true 또는 false여야 합니다.")

    screen = data.get("screen", {})
    if not isinstance(screen, dict):
        return _bad_request("screen은 객체 형식이어야 합니다.")
    if "is_interactive" in screen and not isinstance(screen["is_interactive"], bool):
        return _bad_request("screen.is_interactive는 true 또는 false여야 합니다.")

    # 4. SHA-256 형식 확인
    sha256 = data.get("apk_sha256")
    if sha256 is not None:
        if not isinstance(sha256, str) or not SHA256_PATTERN.fullmatch(sha256):
            return _bad_request("SHA-256은 64자리 16진수 문자열이어야 합니다.")

    # 5. 스냅샷 정규화 (package_name, occurred_at, collected_at 필수 확인 포함)
    try:
        snapshot = normalize_snapshot(data)
    except ValueError as e:
        return _bad_request(str(e))

    # 6. VirusTotal 조회 (기존과 동일)
    virustotal_result = check_virustotal(sha256) if sha256 else None

    # 7. 종합 위험도 분석
    result = calculate_risk(snapshot, virustotal_result)

    return Response(result)
