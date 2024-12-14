from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    UserInfoView, UserDetailView, UserDetailViewNoId, ChangeUserPasswordView,
    heartbeat, get_online_users,
)


urlpatterns = [
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('user-manage/', UserDetailViewNoId.as_view(), name='users-manage'),
    path('user-manage/<int:pk>/', UserDetailView.as_view(), name='user-manage'),
    path('user-set-password/<int:pk>/', ChangeUserPasswordView.as_view(), name='user-set-password'),
    path('heartbeat/', heartbeat, name='heartbeat'),
    path('online-users/', get_online_users, name='online-users'),
]

router = DefaultRouter()

urlpatterns += router.urls
