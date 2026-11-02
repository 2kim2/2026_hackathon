from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer


User = get_user_model()


# 회원가입
class SignupView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'senior')
        phone_number = request.data.get('phone_number', '')

        if not username or not password:
            return Response(
                {'error': '아이디와 비밀번호를 입력해 주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': '이미 사용 중인 아이디입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_roles = {choice[0] for choice in User.ROLE_CHOICES}

        if role not in valid_roles:
            return Response(
                {'error': '올바르지 않은 사용자 유형입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password)
        except ValidationError as error:
            return Response(
                {'error': list(error.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role,
            phone_number=phone_number
        )

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': '회원가입이 완료되었습니다.',
                'token': token.key,
                'username': user.username,
                'role': user.role,
            },
            status=status.HTTP_201_CREATED
        )


# 로그인
class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': '아이디와 비밀번호를 입력해 주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': '로그인되었습니다.',
                'token': token.key,
                'username': user.username,
                'role': user.role,
            },
            status=status.HTTP_200_OK
        )


# 로그아웃
class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        request.user.auth_token.delete()

        return Response(
            {'message': '로그아웃되었습니다.'},
            status=status.HTTP_200_OK
        )


# 내 정보 조회 및 수정
class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    # 내 정보 조회
    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)


    # 내 정보 수정
    def patch(self, request):

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                'message': '사용자 정보가 수정되었습니다.',
                'user': serializer.data
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )