from rest_framework import serializers
from .models import User
from .services.passwords import hash_password, verify_password
import jwt
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'password', 'password_repeat')

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_repeat')
        validated_data['password_hash'] = hash_password(password)
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'], is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not verify_password(data['password'], user.password_hash):
            raise serializers.ValidationError("Invalid email or password")

        # Генерация JWT
        payload = {'user_id': str(user.id)}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        data['token'] = token
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'middle_name', 'is_active')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name')