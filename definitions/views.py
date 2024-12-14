from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import (
    IsAdminUser, DjangoModelPermissionsOrAnonReadOnly,
    DjangoModelPermissions, BasePermission, IsAuthenticated
)
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Product, Description, UnitType
from .serializers import ProductSerializer, DescriptionSerializer, UnitTypeSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = IsAuthenticated
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DescriptionViewSet(viewsets.ModelViewSet):
    permission_classes = IsAuthenticated
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


class UnitTypeViewSet(viewsets.ModelViewSet):
    permission_classes = IsAuthenticated
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
