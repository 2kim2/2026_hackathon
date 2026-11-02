from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FamilyConnection
from .serializers import FamilyConnectionSerializer


User = get_user_model()


# 보호자가 어르신에게 연결 요청
class FamilyRequestView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # 보호자만 요청 가능
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

        # 어르신 계정 확인
        try:
            senior = User.objects.get(username=senior_username)
        except User.DoesNotExist:
            return Response(
                {'error': '해당 사용자를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if senior.role != 'senior':
            return Response(
                {'error': '어르신 계정에만 연결 요청을 보낼 수 있습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

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

            # 이전에 거절된 요청이라면 다시 요청
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