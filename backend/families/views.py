
import secrets
import string
import re

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FamilyConnection, FamilyConnectionCode
from .serializers import FamilyConnectionSerializer


User = get_user_model()


# 어르신이 가족 연결 코드 생성
class FamilyConnectionCodeCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != 'senior':
            return Response(
                {'error': '어르신 계정만 연결 코드를 생성할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # 이전에 발급한 미사용 코드 무효화
        FamilyConnectionCode.objects.filter(
            senior=request.user,
            is_used=False
        ).update(is_used=True)

        # 중복되지 않는 8자리 숫자 생성
        while True:
            code = ''.join(
                secrets.choice(string.digits)
                for _ in range(8)
            )

            if not FamilyConnectionCode.objects.filter(
                code=code
            ).exists():
                break

        expires_at = timezone.now() + timedelta(minutes=10)

        connection_code = FamilyConnectionCode.objects.create(
            senior=request.user,
            code=code,
            expires_at=expires_at
        )

        return Response(
            {
                'message': '가족 연결 코드가 생성되었습니다.',
                'code': connection_code.code,
                'expires_at': connection_code.expires_at,
            },
            status=status.HTTP_201_CREATED
        )


# 보호자가 연결 코드로 가족 연결 요청
class FamilyRequestByCodeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != 'guardian':
            return Response(
                {'error': '보호자 계정만 연결 요청을 보낼 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        code = str(request.data.get('code', '')).strip()

        if not re.fullmatch(r'[0-9]{8}', code):
            return Response(
                {'error': '8자리 연결 코드를 입력해 주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            try:
                connection_code = (
                    FamilyConnectionCode.objects
                    .select_for_update()
                    .select_related('senior')
                    .get(code=code)
                )

            except FamilyConnectionCode.DoesNotExist:
                return Response(
                    {'error': '유효하지 않은 연결 코드입니다.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 이미 사용했거나 만료된 코드인지 확인
            if (
                connection_code.is_used
                or connection_code.expires_at <= timezone.now()
                or connection_code.senior.role != 'senior'
            ):
                return Response(
                    {'error': '만료되었거나 사용할 수 없는 코드입니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            senior = connection_code.senior

            # 기존 연결 확인
            connection = FamilyConnection.objects.filter(
                guardian=request.user,
                senior=senior
            ).first()

            if connection:

                if connection.status == 'accepted':
                    return Response(
                        {'error': '이미 연결된 계정입니다.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if connection.status == 'pending':
                    return Response(
                        {'error': '이미 연결 요청을 보냈습니다.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 이전에 거절된 요청이면 다시 대기 상태로 변경
                connection.status = 'pending'
                connection.save()

            else:
                connection = FamilyConnection.objects.create(
                    guardian=request.user,
                    senior=senior
                )

            # 연결 요청이 정상적으로 생성된 경우 코드 사용 처리
            connection_code.is_used = True
            connection_code.save(update_fields=['is_used'])

        return Response(
            {
                'message': '가족 연결 요청을 보냈습니다.',
                'connection_id': connection.id,
                'senior_username': senior.username,
            },
            status=status.HTTP_201_CREATED
        )


# 기존: 보호자가 어르신 아이디로 연결 요청
class FamilyRequestView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != 'guardian':
            return Response(
                {'error': '보호자 계정만 연결 요청을 보낼 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        senior_username = request.data.get('senior_username')

        if not senior_username:
            return Response(
                {'error': '어르신 아이디를 입력해 주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            senior = User.objects.get(username=senior_username)

        except User.DoesNotExist:
            return Response(
                {'error': '해당 사용자를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        if senior.id == request.user.id:
            return Response(
                {'error': '자기 자신에게 연결 요청을 보낼 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if senior.role != 'senior':
            return Response(
                {'error': '어르신 계정에만 연결 요청을 보낼 수 있습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        connection = FamilyConnection.objects.filter(
            guardian=request.user,
            senior=senior
        ).first()

        if connection:

            if connection.status == 'accepted':
                return Response(
                    {'error': '이미 연결된 계정입니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if connection.status == 'pending':
                return Response(
                    {'error': '이미 연결 요청을 보냈습니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            connection.status = 'pending'
            connection.save()

        else:
            connection = FamilyConnection.objects.create(
                guardian=request.user,
                senior=senior
            )

        return Response(
            {
                'message': '가족 연결 요청을 보냈습니다.',
                'connection_id': connection.id,
            },
            status=status.HTTP_201_CREATED
        )


# 어르신이 받은 연결 요청 확인
class FamilyRequestListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != 'senior':
            return Response(
                {'error': '어르신 계정만 요청을 확인할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        requests = FamilyConnection.objects.filter(
            senior=request.user,
            status='pending'
        ).select_related('guardian')

        serializer = FamilyConnectionSerializer(
            requests,
            many=True
        )

        return Response(serializer.data)


# 어르신이 연결 요청 수락 또는 거절
class FamilyResponseView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, connection_id):

        if request.user.role != 'senior':
            return Response(
                {'error': '어르신 계정만 요청에 응답할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        action = request.data.get('action')

        if action not in ['accept', 'reject']:
            return Response(
                {'error': 'accept 또는 reject를 입력해 주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            connection = FamilyConnection.objects.get(
                id=connection_id,
                senior=request.user
            )

        except FamilyConnection.DoesNotExist:
            return Response(
                {'error': '해당 연결 요청을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if connection.status != 'pending':
            return Response(
                {'error': '이미 처리된 연결 요청입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == 'accept':
            connection.status = 'accepted'
            message = '가족 연결을 수락했습니다.'

        else:
            connection.status = 'rejected'
            message = '가족 연결을 거절했습니다.'

        connection.save()

        return Response({
            'message': message,
            'status': connection.status,
        })


# 연결된 가족 목록 조회
class FamilyConnectionListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        connections = FamilyConnection.objects.filter(
            status='accepted'
        ).filter(
            guardian=request.user
        ) | FamilyConnection.objects.filter(
            status='accepted',
            senior=request.user
        )

        connections = connections.select_related(
            'guardian',
            'senior'
        )

        serializer = FamilyConnectionSerializer(
            connections,
            many=True
        )

        return Response(serializer.data)
