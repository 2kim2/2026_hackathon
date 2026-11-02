from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'role',
            'phone_number',
            'created_at',
        ]

        # 아이디, 사용자 유형, 가입일은 수정 불가
        read_only_fields = [
            'username',
            'role',
            'created_at',
        ]
        