from authentication.models import CustomUser
from django.core.exceptions import ValidationError
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(required=True)

    class Meta:
        model = CustomUser

        fields = ('email', 'username','password', 'password_confirm')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            password=validated_data['password'],
            email=validated_data.get('email')  # email опционален
        )
        return user

    def validate_email(self, email):
        if email == "" or email is None or len(email) == 0:
            raise ValidationError('Email cannot be an empty string.')
        return email

    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Username already registered.')
        if username == "" or username is None or len(username) == 0:
            raise ValidationError('Username cannot be an empty string.')
        if len(username) < 5:
            raise ValidationError('The username must be at least 5 characters long.')

        return username

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        password_confirm = data.get("password_confirm")
        if password_confirm != password:
            raise ValidationError('Passwords do not match.')

        del data["password_confirm"]
        return data


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required = True,write_only=True)
    email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
