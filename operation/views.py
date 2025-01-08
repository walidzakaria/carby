from django.shortcuts import render

from .models import Customer, Vendor, Quotation
from .serializers import CustomerSerializer, VendorSerializer, QuotationSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import QuotationLineSerializer
from users.permissions import HasModelPermissionOrAdmin


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [HasModelPermissionOrAdmin]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VendorViewSet(viewsets.ModelViewSet):
    permission_classes = [HasModelPermissionOrAdmin]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class QuotationViewSet(viewsets.ModelViewSet):
    permission_classes = [HasModelPermissionOrAdmin]
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer

    # @action(detail=True, methods=['post'])
    # def add_lines(self, request, pk=None):
    #     quotation = self.get_object()
    #     serializer = QuotationLineSerializer(data=request.data, many=True)
    #     if serializer.is_valid():
    #         serializer.save(quotation=quotation)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
