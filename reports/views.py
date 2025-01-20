from decimal import Decimal
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny  # or AllowAny
from collections import OrderedDict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.utils.dateparse import parse_date
from datetime import datetime, time

from operation.models import Vendor

class SupplyOrdersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        vendor = request.query_params.get('vendor')
        quotation_id = request.query_params.get('quotation_id')

        with connection.cursor() as cursor:
            query = '''
                select
                    de.name as description, ql.quantity, ut.description as unit, ql.unit_value, ql.quantity * ql.unit_value as value
                from
                    operation_quotationline ql
                    join definitions_description de on ql.description_id = de.id
                    join definitions_unittype ut on ql.unit_type_id = ut.id
                where
                    ql.quantity != 0 and ql.quotation_id = %s and ql.vendor_id = %s;
            '''
            cursor.execute(query, [quotation_id, vendor])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            
            row_data = [{
                'description': row[0],
                'quantity': row[1],
                'unit': row[2],
                'unit_value': row[3],
                'value': row[4],
            } for row in rows]
            
            selected_vendor = Vendor.objects.get(pk=vendor)
            document_number = f'{quotation_id}-{selected_vendor.id}'
            context = {
                'vendor': selected_vendor.name,
                'code': document_number,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'rows': row_data,
                'total': f"{sum(row['value'] for row in row_data):,.2f}"
            }
            
            response = render(request, 'reports/supply_order.html', context=context)
            return response
            