from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class AuthUserSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    def validate_username(self, value):
        return get_object_or_404(User, username=value)

    def validate(self, data):
        user = User.objects.get(username=data['username'])
        token = PasswordResetTokenGenerator()

        if token.check_token(user, data['confirmation_code']) is False:
            raise serializers.ValidationError('Это неверный token')

        return super().validate(data)


class SignupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(), fields=['email', 'username']
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать me в качестве имени пользователя'
            )

        return value

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            if (
                data['username']
                != User.objects.get(email=data['email']).username
            ):
                raise serializers.ValidationError(
                    'Этот email уже используется'
                )

        if User.objects.filter(username__iexact=data['username']).exists():
            if (
                data['email']
                != User.objects.get(username=data['username']).email
            ):
                raise serializers.ValidationError(
                    'Этот username уже используется'
                )

        return super().validate(data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(), fields=['email', 'username']
            )
        ]

    def validate_role(self, value):
        if self.context['request'].user.role == 'user':
            return self.context['request'].user.role

        return value

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать me в качестве имени пользователя'
            )

        return value

    def validate(self, data):
        email = data.get('email', None)
        if User.objects.filter(email=email).exists():
            if data['username'] != User.objects.get(email=email).username:
                raise serializers.ValidationError(
                    'Этот email уже используется'
                )

        return super().validate(data)
