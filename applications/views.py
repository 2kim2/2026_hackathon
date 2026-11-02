
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import InstalledApp
from .serializers import InstalledAppSerializer

from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import AppPermission
from .serializers import AppPermissionSerializer

from .models import AppExecutionLog
from .serializers import AppExecutionLogSerializer


class InstalledAppListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # 로그인한 사용자의 설치 앱 목록 조회
    def get(self, request):
        apps = InstalledApp.objects.filter(
            user=request.user
        ).order_by('-last_scanned')

        serializer = InstalledAppSerializer(apps, many=True)

        return Response(serializer.data)

    # 설치 앱 정보 등록 또는 갱신
    def post(self, request):
        package_name = request.data.get('package_name')

        if not package_name:
            return Response(
                {'message': '패키지명이 필요합니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 같은 사용자의 동일한 패키지명이 있는지 확인
        existing_app = InstalledApp.objects.filter(
            user=request.user,
            package_name=package_name
        ).first()

        serializer = InstalledAppSerializer(
            instance=existing_app,
            data=request.data,
            partial=existing_app is not None
        )

        if serializer.is_valid():
            serializer.save(
                user=request.user,
                last_scanned=timezone.now()
            )

            if existing_app:
                return Response(
                    {
                        'message': '앱 정보가 갱신되었습니다.',
                        'app': serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'message': '앱 정보가 등록되었습니다.',
                    'app': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AppPermissionListView(APIView):
    permission_classes = [IsAuthenticated]

    # 특정 앱의 권한 목록 조회
    def get(self, request, app_id):
        app = get_object_or_404(
            InstalledApp,
            id=app_id,
            user=request.user
        )

        permissions = AppPermission.objects.filter(
            app=app
        ).order_by('permission_name')

        serializer = AppPermissionSerializer(
            permissions,
            many=True
        )

        return Response(serializer.data)

    # 특정 앱의 권한 정보 등록 또는 갱신
    def post(self, request, app_id):
        app = get_object_or_404(
            InstalledApp,
            id=app_id,
            user=request.user
        )

        permission_data = request.data.get('permissions')

        if not isinstance(permission_data, list):
            return Response(
                {'message': '권한 정보는 배열 형태로 보내야 합니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AppPermissionSerializer(
            data=permission_data,
            many=True
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            for item in serializer.validated_data:
                AppPermission.objects.update_or_create(
                    app=app,
                    permission_name=item['permission_name'],
                    defaults={
                        'is_granted': item['is_granted']
                    }
                )

        saved_permissions = AppPermission.objects.filter(
            app=app
        ).order_by('permission_name')

        result_serializer = AppPermissionSerializer(
            saved_permissions,
            many=True
        )

        return Response(
            {
                'message': '앱 권한 정보가 저장되었습니다.',
                'permissions': result_serializer.data
            },
            status=status.HTTP_200_OK
        )


class AppExecutionLogListView(APIView):
    permission_classes = [IsAuthenticated]

    # 특정 앱의 실행 기록 조회
    def get(self, request, app_id):
        app = get_object_or_404(
            InstalledApp,
            id=app_id,
            user=request.user
        )

        logs = AppExecutionLog.objects.filter(
            app=app
        ).order_by('-occurred_at')

        serializer = AppExecutionLogSerializer(
            logs,
            many=True
        )

        return Response(serializer.data)

    # 실행 기록 저장
    def post(self, request, app_id):
        app = get_object_or_404(
            InstalledApp,
            id=app_id,
            user=request.user
        )

        serializer = AppExecutionLogSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(
                app=app,
                occurred_at=timezone.now()
            )

            return Response(
                {
                    'message': '앱 실행 기록이 저장되었습니다.',
                    'log': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
