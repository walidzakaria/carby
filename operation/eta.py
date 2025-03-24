from .models import Quotation, QuotationLine
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.decorators import action
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class QuotationView(APIView):
    @action(detail=True, methods=['post'], url_path='eta_set_uuid')
    def eta_set_uuid(self, request, pk=None):
        quotation = Quotation.objects.filter(id=pk).first()
        
        if quotation:
            
            total_amount = Decimal(request.data.get('total_amount', 0))
            status = request.data.get('status', '')
            uuid = request.data.get('uuid', '')
            quotation.eta_total_amount = total_amount
            quotation.eta_status = status
            quotation.eta_uuid = uuid
            quotation.save()
            return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'], url_path='eta_set_status')
    def eta_set_status(self, request, pk=None):
        if isinstance(pk, str):
            quotation = Quotation.objects.filter(uuid=pk).first()
        else:
            quotation = Quotation.objects.filter(id=pk).first()
        
        if quotation:
            status = request.data.get('status', '')
            status_detailed = request.data.get('status_detailed', '')
            quotation.eta_status = status
            quotation.eta_status_detailed = status_detailed
            quotation.save()
            return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk=None, *args, **kwargs):
        pass