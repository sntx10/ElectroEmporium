# import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from applications.account import serializers

User = get_user_model()
# logger = logging.getLogger('django_logger')


class RegisterApiView(CreateAPIView):
    # logger.warning('register')
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer


class ActivationApiView(ListAPIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save(update_fields=['is_active', 'activation_code'])
            return Response({'msg': 'ваш аккаунт успешно активирован'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'некоректный код активации'})


class ChangePasswordApiView(CreateAPIView):
    # logger.warning('change password')
    queryset = User.objects.all()
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]


class ForgotPasswordApiView(CreateAPIView):
    # logger.warning('forgot password')
    queryset = User.objects.all()
    serializer_class = serializers.ForgotPasswordSerializer


class ForgotPasswordConfirmApiView(CreateAPIView):
    # logger.warning('forgot password confirm')
    queryset = User.objects.all()
    serializer_class = serializers.ForgotPasswordConfirmSerializer


class ForgotPasswordCodewordApiView(CreateAPIView):
    # logger.warning('forgot password codeword')
    queryset = User.objects.all()
    serializer_class = serializers.ForgotPasswordCodewordSerializer


class ForgotPasswordPhoneApiView(CreateAPIView):
    # logger.warning('forgot password phone')
    queryset = User.objects.all()
    serializer_class = serializers.ForgotPasswordPhoneSerializer



