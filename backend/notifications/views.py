
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FCMToken


class FCMTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        device_name = request.data.get('device_name', '')

        if not token:
            return Response(
                {'error': 'FCM token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 같은 토큰이 이미 등록되어 있다면 사용자와 기기 정보를 갱신
        fcm_token, created = FCMToken.objects.update_or_create(
            token=token,
            defaults={
                'user': request.user,
                'device_name': device_name,
            }
        )

        return Response(
            {
                'message': 'FCM token registered successfully.',
                'token_id': fcm_token.id,
                'created': created,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def delete(self, request):
        token = request.data.get('token')

        if not token:
            return Response(
                {'error': 'FCM token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count, _ = FCMToken.objects.filter(
            user=request.user,
            token=token
        ).delete()

        if deleted_count == 0:
            return Response(
                {'error': 'FCM token not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {'message': 'FCM token deleted successfully.'},
            status=status.HTTP_200_OK
        )
