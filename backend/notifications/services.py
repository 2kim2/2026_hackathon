
import logging

import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings

from families.models import FamilyConnection
from .models import FCMToken


logger = logging.getLogger(__name__)


def get_firebase_app():
    """
    Firebase Admin SDK 초기화.
    이미 초기화되어 있다면 기존 앱을 사용한다.
    """
    try:
        return firebase_admin.get_app()

    except ValueError:
        credential_path = settings.FIREBASE_CREDENTIALS_PATH

        if not credential_path.exists():
            raise FileNotFoundError(
                f"Firebase 키 파일을 찾을 수 없습니다: {credential_path}"
            )

        credential = credentials.Certificate(str(credential_path))

        return firebase_admin.initialize_app(credential)


def send_push_notification(tokens, title, body, data=None):
    """
    여러 기기에 FCM 푸시 알림 발송.
    FCM은 한 번에 최대 500개 토큰을 처리할 수 있다.
    """

    if not tokens:
        return {
            "success_count": 0,
            "failure_count": 0,
        }

    app = get_firebase_app()

    success_count = 0
    failure_count = 0

    # FCM 데이터 메시지는 문자열 값만 허용
    data = {
        str(key): str(value)
        for key, value in (data or {}).items()
    }

    for start in range(0, len(tokens), 500):
        token_batch = tokens[start:start + 500]

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            tokens=token_batch,
        )

        response = messaging.send_each_for_multicast(
            message,
            app=app,
        )

        success_count += response.success_count
        failure_count += response.failure_count

        # 만료되거나 잘못된 토큰 정리
        for token, result in zip(token_batch, response.responses):
            if result.success:
                continue

            error = result.exception
            error_code = getattr(error, "code", "")

            if error_code in (
                "UNREGISTERED",
                "SENDER_ID_MISMATCH",
                "invalid-registration-token",
            ):
                FCMToken.objects.filter(token=token).delete()

            logger.warning(
                "FCM 발송 실패: token 일부=%s, error=%s",
                token[:12],
                error,
            )

    return {
        "success_count": success_count,
        "failure_count": failure_count,
    }


def notify_guardians_of_danger(diagnosis):
    """
    위험 진단 결과가 발생하면 연결된 보호자에게 알림을 발송한다.
    """

    if diagnosis.risk_level != "danger":
        return {
            "success_count": 0,
            "failure_count": 0,
        }

    # 연결이 수락된 보호자만 검색
    guardian_ids = (
        FamilyConnection.objects.filter(
            senior=diagnosis.user,
            status="accepted",
            guardian__role="guardian",
        )
        .values_list("guardian_id", flat=True)
        .distinct()
    )

    # 보호자에게 등록된 모든 기기의 FCM 토큰
    tokens = list(
        FCMToken.objects.filter(
            user_id__in=guardian_ids
        ).values_list("token", flat=True)
    )

    if not tokens:
        logger.info(
            "알림을 발송할 보호자 FCM 토큰이 없습니다. diagnosis_id=%s",
            diagnosis.id,
        )

        return {
            "success_count": 0,
            "failure_count": 0,
        }

    summary = diagnosis.summary.strip()

    if not summary:
        summary = "어르신의 기기에서 위험 상황이 감지되었습니다."

    result = send_push_notification(
        tokens=tokens,
        title="시니어가드 위험 알림",
        body=summary,
        data={
            "diagnosis_id": diagnosis.id,
            "risk_level": diagnosis.risk_level,
            "risk_score": diagnosis.risk_score,
        },
    )

    logger.info(
        "위험 알림 발송 완료: diagnosis_id=%s, result=%s",
        diagnosis.id,
        result,
    )

    return result
