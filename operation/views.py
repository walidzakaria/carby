from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoObjectPermissions, AllowAny
from .models import Customer, Vendor, Quotation, QuotationLine, Stock, QuotationAttachment
from .serializers import CustomerSerializer, VendorSerializer, QuotationSerializer, StockSerializer, QuotationAttachmentSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.utils.dateparse import parse_date

from .serializers import QuotationLineSerializer, QuotationSearchSerizalizer
from users.permissions import HasModelPermissionOrAdmin

class NineRecordsPagination(PageNumberPagination):
    page_size = 9

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [HasModelPermissionOrAdmin]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VendorViewSet(viewsets.ModelViewSet):
    permission_classes = [HasModelPermissionOrAdmin]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class StockViewSet(viewsets.ModelViewSet):
    permission_classes = [HasModelPermissionOrAdmin]
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class QuotationViewSet(viewsets.ModelViewSet):
    # permission_classes = [HasModelPermissionOrAdmin]
    permission_classes = [IsAuthenticated]
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer


    def create(self, request, *args, **kwargs):
        lines = request.data.pop('lines')
        quotation = request.data
        quotation['created_by'] = request.user.pk
        quotation['updated_by'] = request.user.pk

        serializer = self.get_serializer(data=quotation)
        
        if serializer.is_valid():
            new_quotation = serializer.save()
            
            for line in lines:
                line['quotation'] = new_quotation.id
            line_serializer = QuotationLineSerializer(data=lines, many=True)

            
            if line_serializer.is_valid():
                line_serializer.save()
                
                response = {
                    'quotation': serializer.data,
                    'lines': line_serializer.data,
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                new_quotation.delete()
                response = {
                    'quotation': [],
                    'lines': line_serializer.errors,
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'quotation': serializer.errors,
                'lines': [],
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, *args, **kwargs):
        lines = request.data.pop('lines')
        quotation = request.data
        
        quotation['updated_by'] = request.user.pk
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=quotation, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        for line in lines:
            line['quotation'] = instance.id
            
        line_serializer = QuotationLineSerializer(data=lines, many=True)

        if line_serializer.is_valid():
            QuotationLine.objects.filter(quotation=instance).delete()
            
            line_serializer.save()
            
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        return Response(line_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # @action(detail=True, methods=['post'], url_path='upload-supply-order')
    # def upload_supply_order(self, request, pk=None):
    #     quotation = self.get_object()
    #     supply_order = request.FILES.get('supply_order')

    #     if not supply_order:
    #         return Response({'error': 'No supply order file provided'}, status=status.HTTP_400_BAD_REQUEST)

    #     quotation.supply_order.save(supply_order.name, supply_order)
    #     quotation.save()

    #     return Response({'file': quotation.supply_order.name}, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):

        customer = request.query_params.get('customer')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        status = request.query_params.get('status')
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        
        queryset = self.get_queryset().filter(date_time_issued__range=(start_date, end_date))

        if customer:
            queryset = queryset.filter(customer=customer)
        
        if status:
            queryset = queryset.filter(status=status)
        
        paginator = NineRecordsPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        
        if page is not None:
            serializer = QuotationSearchSerizalizer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = QuotationSearchSerizalizer(queryset, many=True)
        return Response(serializer.data)


class QuotationAttachmentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = QuotationAttachment.objects.all()
    serializer_class = QuotationAttachmentSerializer
    

    def create(self, request, *args, **kwargs):
        quotation_id = request.data.get('quotation')
        file_type = request.data.get('file_type')
        quotation = Quotation.objects.get(pk=quotation_id)
        file_number = quotation.get_number(file_type)
        request.data['file_number'] = file_number
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        quotation_id = data.get('quotation')
        file_type = data.get('file_type')
        
        instance = self.get_object()
        if instance.file_type != file_type:
            quotation = Quotation.objects.get(pk=quotation_id)
            file_number = quotation.get_number(file_type)
            data['file_number'] = file_number
            request._full_data = data
        
        if 'file' in request.data and request.data['file'] != instance.file:
            instance.file.delete()
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete()
        return super().destroy(request, *args, **kwargs)
    
    

    @action(detail=True, methods=['get'], url_path='get-by-quotation')
    def get_by_quotation(self, request, pk=None):
        queryset = self.get_queryset().filter(quotation=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
