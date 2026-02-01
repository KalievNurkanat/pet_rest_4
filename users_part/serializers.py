from rest_framework import serializers
from users_part.models import CustomUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()


class UserRegisterSerializer(UserBaseSerializer):
    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
           raise ValidationError("Such a username already exists")
        return username
    
    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
           raise ValidationError("Such an email already exists")
        return email
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            is_active=True
        )

        return user
    

class UserAuthenticateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, data):
        user = authenticate(
            user=data["username"],
            password=data["password"],
            email=data["email"]
        )

        if user is None:
            raise serializers.ValidationError("User not exists")
        
        if not user.is_active:
            raise serializers.ValidationError("user is not active")
        
        data["user"] = user
        return data