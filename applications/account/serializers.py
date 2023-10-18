from django.contrib.auth import get_user_model
from rest_framework import serializers
from applications.account import tasks

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=128, min_length=6, write_only=True)
    password_repeat = serializers.CharField(max_length=128, min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_repeat')
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs

    @staticmethod
    def validate_phone_number(phone_number):
        if not phone_number.startswith('+996'):
            raise serializers.ValidationError('Ваш номер должен начинаться на +996')
        if len(phone_number) != 13:
            raise serializers.ValidationError('Некоректный номер телефона')
        if not phone_number[1:].isdigit():
            raise serializers.ValidationError('Некоректный номер телефона')
        return phone_number

    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data['password'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
            codeword=validated_data['codeword'],
            phone_number=validated_data['phone_number']
        )
        code = user.activation_code
        tasks.send_user_activation_link.delay(user.email, code)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=6, write_only=True)
    new_password = serializers.CharField(required=True, min_length=6, write_only=True)
    new_password_repeat = serializers.CharField(required=True, min_length=6, write_only=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Старый пароль введен неверно')
        return old_password

    def validate(self, attrs):
        p1 = attrs['new_password']
        p2 = attrs['new_password_repeat']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('нет такого зарегистрированного пользователя')
        return email

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.create_code_confirm()
        user.save(update_fields=['activation_code'])
        tasks.send_forgot_password_code.delay(email=user.email, activation_code=user.activation_code)
        return user


class ForgotPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, min_length=6)
    password_repeat = serializers.CharField(required=True, write_only=True, min_length=6)

    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs['password_repeat']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    @staticmethod
    def validate_code(code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('неправельный код подтверждения')
        return code

    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('пользователь с данным именем не найден')
        return email

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.activation_code = ''
        user.save(update_fields=['password', 'activation_code'])
        return user


class ForgotPasswordCodewordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    codeword = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)
    new_password_repeat = serializers.CharField(required=True, write_only=True, min_length=6)

    def validate(self, attrs):
        p1 = attrs['new_password']
        p2 = attrs['new_password_repeat']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    @staticmethod
    def validate_codeword(codeword):
        if not User.objects.filter(codeword=codeword).exists():
            raise serializers.ValidationError('неправельное секретное слово подтверждения')
        return codeword

    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('пользователь с данным именем не найден')
        return email

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.set_password(validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class ForgotPasswordPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    @staticmethod
    def validate_phone_number(phone_number):
        if not phone_number.startswith('+996'):
            raise serializers.ValidationError('Ваш номер должен начинаться на +996')
        if len(phone_number) != 13:
            raise serializers.ValidationError('Некоректный номер телефона')
        if not phone_number[1:].isdigit():
            raise serializers.ValidationError('Некоректный номер телефона')
        if not User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Юзера с данным номером не существует')
        return phone_number

    def create(self, validated_data):
        user = User.objects.get(phone_number=validated_data['phone_number'])
        user.create_code_confirm()
        user.save(update_fields=['activation_code'])
        tasks.send_code_to_phone.delay(code=user.activation_code, receiver=user.phone_number)
        return user


