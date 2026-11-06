import json
import logging
import urllib.error
import urllib.request

from django.conf import settings


logger = logging.getLogger(__name__)


class BE2AnalysisError(Exception):
    """Backend 2 분석 요청 실패"""


def request_be2_analysis(payload):
    """
    Android 이벤트 데이터를 Backend 2로 전달하고 분석 결과를 반환한다.
    """

    analysis_url = getattr(settings, 'BE2_ANALYSIS_URL', '')
    timeout = getattr(settings, 'BE2_TIMEOUT', 25)

    if not analysis_url or '실제_BE2_서버_IP' in analysis_url:
        raise BE2AnalysisError(
            'Backend 2 서버 주소가 아직 설정되지 않았습니다.'
        )

    request_body = json.dumps(
        payload,
        ensure_ascii=False
    ).encode('utf-8')

    request = urllib.request.Request(
        analysis_url,
        data=request_body,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout
        ) as response:
            response_body = response.read().decode('utf-8')

    except urllib.error.HTTPError as error:
        error_body = error.read().decode('utf-8', errors='replace')
        logger.error(
            'BE2 HTTP 오류: status=%s, body=%s',
            error.code,
            error_body,
        )
        raise BE2AnalysisError(
            f'Backend 2에서 HTTP {error.code} 오류가 발생했습니다.'
        )

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        logger.exception('BE2 서버 연결 실패')
        raise BE2AnalysisError(
            'Backend 2 서버에 연결할 수 없습니다.'
        ) from error

    try:
        result = json.loads(response_body)
    except json.JSONDecodeError as error:
        raise BE2AnalysisError(
            'Backend 2가 올바른 JSON 응답을 반환하지 않았습니다.'
        ) from error

    if not isinstance(result, dict):
        raise BE2AnalysisError(
            'Backend 2 응답 형식이 올바르지 않습니다.'
        )

    return result