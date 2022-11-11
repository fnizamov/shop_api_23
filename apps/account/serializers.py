from rest_framework import serializers
from django.contrib.auth import get_user_model

from .tasks import send_activation_sms
from .utils import normalize_phone


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'phone', 'password', 'password_confirm')

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Указан неверный формат номера!')
        return phone
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Введенные пароли не совпадают!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_sms(user.phone, user.activation_code)
        return user


class ActivationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, required=True)
    code = serializers.CharField(max_length=10, required=True)

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Указан неверный формат номера!')
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Пользователь с указанным номером телефона не найден.')
        return phone

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Введен неверный код активации!')
        return code

    def activate_account(self):
        phone = self.validated_data.get('phone')
        user = User.objects.get(phone=phone)
        user.is_active = True
        user.activation_code = ''
        user.save()