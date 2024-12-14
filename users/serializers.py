from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import ActiveUser, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active',)


class ProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(max_length=200, required=False)
    about = serializers.CharField(max_length=200, required=False)
    photo = serializers.ImageField(required=False)
    
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',
                  'address', 'about', 'photo', )


class UserProfileDetailedSerializer(serializers.ModelSerializer):
    groups = UserGroupsSerializer(many=True)
    profile = UserProfileSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'groups',
                  'profile', 'is_active', )


class UserListSerializer(serializers.ModelSerializer):
    
    photo = serializers.ImageField(source='profile.photo', read_only=True)
    phone_number = serializers.CharField(source='profile.phone_number', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_active', 'photo', 'phone_number', )


class UserProfileCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(max_length=200, required=False)
    about = serializers.CharField(max_length=200, required=False)
    photo = serializers.ImageField(required=False)
    password = serializers.CharField(max_length=255)
    re_password = serializers.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number',
                  'address', 'about', 'photo', 'password', 're_password', )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    
    re_password = serializers.CharField(max_length=255)    
    class Meta:
        model = User
        fields = ('password', 're_password', )



class ActiveUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ActiveUser
        fields = ('id', 'last_seen', 'status', )
