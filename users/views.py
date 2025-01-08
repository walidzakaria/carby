from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoObjectPermissions, AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from .serializers import (
    UserProfileDetailedSerializer, UserSimpleSerializer,
    UserProfileSerializer, UserGroupsSerializer, ProfileSerializer, UserListSerializer,
    UserProfileCreateSerializer, UserPasswordChangeSerializer, UserViewSerializer,
    ActiveUserSerializer
)
from .models import ActiveUser, UserView

from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserProfile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .utils import change_permissions
from users.permissions import HasModelPermissionOrAdmin
from django.core.cache import cache
from datetime import timedelta
from django.utils import timezone

# Create your views here.
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    
    def get(self, request):
        user = request.user
        serializer = UserProfileDetailedSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update user profile",
        request_body=ProfileSerializer,
        responses={200: ProfileSerializer, 400: 'Validation Error'}
    )
    def post(self, request, *args, **kwargs):
        parser_classes = [MultiPartParser, FormParser]
        request_data = request.data.copy()
        request_data['user'] = request.user.pk
        user_profile = UserProfile.objects.filter(user=request.user).first()

        if user_profile:
            profile_serializer = UserProfileSerializer(user_profile, data=request_data)
        else:
            profile_serializer = UserProfileSerializer(data=request_data)

        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = UserSimpleSerializer(request.user, data=request_data)
        if user_serializer.is_valid():
            user_serializer.save()
            response_data = user_serializer.data.copy()
            response_data.update(profile_serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailViewNoId(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
    
    # create new user
    @swagger_auto_schema(
        operation_description="Create user with profile",
        request_body=UserProfileCreateSerializer,
        responses={200: UserProfileCreateSerializer, 400: 'Validation Error'}
    )
    def post(self, request, *args, **kwargs):
        parser_classes = [MultiPartParser, FormParser]
        request_data = request.data.copy()
        user_serializer = UserSimpleSerializer(data=request_data)
        if user_serializer.is_valid():
            password = request_data['password']
            re_password = request_data['re_password']
            
            if password != re_password:
                return Response(data={
                    're_password': "The password isn't retyped correctly."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                validate_password(password)
            except ValidationError as err:
                return Response(data={
                    'password': err
                }, status=status.HTTP_400_BAD_REQUEST)
                
            created_user = user_serializer.save()
            created_user.set_password(password)
            created_user.save()

        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        request_data['user'] = created_user.id
        profile_serializer = UserProfileSerializer(data=request_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            response_data = user_serializer.data.copy()
            response_data.update(profile_serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)    
        
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Update user profile",
        request_body=ProfileSerializer,
        responses={200: ProfileSerializer, 400: 'Validation Error'}
    )
    def put(self, request, *args, **kwargs):
        parser_classes = [MultiPartParser, FormParser]
        request_data = request.data.copy()
        user_profile = UserProfile.objects.filter(user=request_data['id']).first()
        if user_profile:
            profile_serializer = UserProfileSerializer(user_profile, data=request_data)
        else:
            profile_serializer = UserProfileSerializer(data=request_data)

        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_to_edit = User.objects.get(pk=request_data['id'])
        user_serializer = UserSimpleSerializer(user_to_edit, data=request_data)
        if user_serializer.is_valid():
            user_serializer.save()
            response_data = user_serializer.data.copy()
            response_data.update(profile_serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserProfileDetailedSerializer(user)
        return Response(serializer.data)
       
    @swagger_auto_schema(
        operation_description="Update user info partially",
        request_body=UserSimpleSerializer,
        responses={200: UserSimpleSerializer, 400: 'Validation Error'}
    ) 
    def patch(self, request, pk):
        
        user = User.objects.get(pk=pk)
        serializer = UserSimpleSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserPasswordView(APIView):
    queryset = User.objects.all()
    
    @swagger_auto_schema(
        operation_description="User set password",
        request_body=UserPasswordChangeSerializer,
        responses={200: UserPasswordChangeSerializer, 400: 'Validation Error'}
    )
    def patch(self, request, pk):
        
        user = User.objects.get(pk=pk)
        request_data = request.data
        user_serializer = UserPasswordChangeSerializer(data=request_data)
        
        if user_serializer.is_valid():
            password = request_data['password']
            re_password = request_data['re_password']
            
            if password != re_password:
                return Response(data={
                    're_password': ["The password isn't retyped correctly."]
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                validate_password(password)
            except ValidationError as err:
                return Response(data={
                    'password': err
                }, status=status.HTTP_400_BAD_REQUEST)
                
            user.set_password(password)
            user.save()
            return Response(data={'result': 'Accepted'}, status=status.HTTP_202_ACCEPTED)
    
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = UserView.objects.all()
    serializer_class = UserViewSerializer
    lookup_field = 'user__id'

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response = super().update(request, *args, **kwargs)
        user = User.objects.get(pk=request.data['user'])
        change_permissions(user, request.data)
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        user = User.objects.get(pk=request.data['user'])
        change_permissions(user, request.data)
        return response


@api_view(['GET'])
@permission_classes([AllowAny])
def heartbeat(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            active_user = ActiveUser.objects.filter(user=request.user).first()
            if active_user:
                active_user.last_seen = timezone.now()
                active_user.save()
            else:
                print(timezone.now())
                active_user = ActiveUser(user=request.user, last_seen=timezone.now())
                active_user.save()
            return Response(data={'status': 'heartbeat OK'}, status=status.HTTP_200_OK)
        return Response(data={'status': 'hearbeat not OK'}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_online_users(request):
    if request.method == 'GET':
        last_seen = ActiveUser.objects.all()
        serializer = ActiveUserSerializer(last_seen, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
