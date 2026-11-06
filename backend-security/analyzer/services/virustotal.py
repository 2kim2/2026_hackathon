#SHA-256 해시값으로 VirusTotal 파일 분석 결과 조회
import requests
from django.conf import settings


def check_virustotal(sha256):

    api_key = settings.VIRUSTOTAL_API_KEY

    if not api_key:
        return {
            "status": "error",
            "message": "VirusTotal API Key가 설정되지 않았습니다."
        }

    url = f"https://www.virustotal.com/api/v3/files/{sha256}"

    headers = {
        "x-apikey": api_key
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        # VirusTotal에 등록되지 않은 파일
        if response.status_code == 404:
            return {
                "status": "not_found",
                "message": "VirusTotal에서 해당 파일을 찾을 수 없습니다."
            }

        # API 호출 제한
        if response.status_code == 429:
            return {
                "status": "rate_limited",
                "message": "VirusTotal API 호출 한도를 초과했습니다."
            }

        # 인증 오류
        if response.status_code in [401, 403]:
            return {
                "status": "error",
                "message": "VirusTotal API 인증에 실패했습니다."
            }

        response.raise_for_status()

        data = response.json()["data"]["attributes"]
        stats = data["last_analysis_stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        undetected = stats.get("undetected", 0)

        total_engines = sum(stats.values())

        return {
            "status": "completed",
            "malicious": malicious,
            "suspicious": suspicious,
            "undetected": undetected,
            "total_engines": total_engines,
            "detection_ratio": (
                f"{malicious + suspicious}/{total_engines}"
                if total_engines else "0/0"
            )
        }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "VirusTotal API 응답 시간이 초과되었습니다."
        }

    except requests.exceptions.RequestException:
        return {
            "status": "error",
            "message": "VirusTotal API 통신 중 오류가 발생했습니다."
        }

    except (ValueError, KeyError, TypeError):
        return {
            "status": "error",
            "message": "VirusTotal 응답 데이터를 처리할 수 없습니다."
        }