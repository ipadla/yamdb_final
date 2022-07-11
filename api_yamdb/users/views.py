from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import (filters, mixins, permissions, status, views,
                            viewsets)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.permissions import IsAdmin
from users.serializers import (AuthUserSerializer, SignupUserSerializer,
                               UserSerializer)

User = get_user_model()


class AuthView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(
                username=serializer.validated_data['username']
            )
            token = RefreshToken.for_user(user)

        return Response({'token': str(token.access_token)})


class SignupView(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = {
            'email': request.data.get('email', None),
            'username': request.data.get('username', None)
        }

        try:
            user = User.objects.get(
                email=data['email'],
                username=data['username']
            )
        except User.DoesNotExist:
            serializer = SignupUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

        token = PasswordResetTokenGenerator().make_token(user=user)
        email = EmailMessage(
            subject="Успешная регистрация на сайте",
            body='\n'.join(
                (
                    f'username - {data["username"]}',
                    f'confirmation_code - {token}'
                )
            ),
            to=(data['email'],),
            headers={},
        )
        email.content_subtype = 'text'
        email.send()

        return Response(data)


class UsersViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin, )
    search_fields = ('username',)


class UsersDetailViewSet(mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )

    def get_object(self):
        username = self.kwargs.get('username', None)

        if username == 'me':
            username = self.request.user.username

        return get_object_or_404(User, username=username)

    def get_permissions(self):
        permissions = self.permission_classes

        if self.kwargs.get('username', None) == 'me':
            permissions = [IsAuthenticated]
            return [permission() for permission in permissions]

        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username', None) == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
