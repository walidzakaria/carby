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

from operation.models import Vendor, Quotation, QuotationLine
from operation.serializers import QuotationLineDetailedUnitSerializer
from definitions.models import Country

class SupplyOrdersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        vendor = request.query_params.get('vendor')
        quotation_id = request.query_params.get('quotation_id')
        show_template = request.query_params.get('show_template', 'false').lower() == 'true'

        with connection.cursor() as cursor:
            query = '''
                SELECT de. name AS description,
                    co.name country,
                    ql.quantity,
                    ut.description AS unit,
                    ql.unit_value,
                    ql.quantity * ql.unit_value AS value
                FROM operation_quotationline ql
                JOIN definitions_description de ON ql.description_id = de.id
                LEFT JOIN definitions_country co ON ql.country_a_id = co.id
                JOIN definitions_unittype ut ON ql.unit_type_id = ut.id
                WHERE ql.quantity != 0 and ql.quotation_id = %s and ql.vendor_id = %s;
            '''
            cursor.execute(query, [quotation_id, vendor])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            
            row_data = [{
                'description': row[0],
                'country': row[1],
                'quantity': row[2],
                'unit': row[3],
                'unit_value': row[4],
                'value': row[5],
            } for row in rows]
            
            selected_vendor = Vendor.objects.get(pk=vendor)
            document_number = f'{quotation_id}-{selected_vendor.id}'
            context = {
                'vendor': selected_vendor.name,
                'code': document_number,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'rows': row_data,
                'show_template': show_template,
                'total': f"{sum(row['value'] for row in row_data):,.2f}"
            }
            
            response = render(request, 'reports/supply_order.html', context=context)
            return response


class QuotationOrdersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        quotation_id = request.query_params.get('quotation_id')
        show_template = request.query_params.get('show_template', 'false').lower() == 'true'
        label = request.query_params.get('label', 'a')

        quotation = Quotation.objects.get(pk=quotation_id)
        quotation_lines = QuotationLine.objects.filter(quotation=quotation)
        
        row_data = QuotationLineDetailedUnitSerializer(quotation_lines, many=True).data
        tax_dict = {
            'T1': 'ضريبة القيمة المضافة',
            'T2': 'ضريبة الجدول',
        }
        net_amount, total_amount = {
            'a': (quotation.quotation_net_amount_a, quotation.quotation_total_amount_a),
            'b': (quotation.quotation_net_amount_b, quotation.quotation_total_amount_b),
            'c': (quotation.quotation_net_amount_c, quotation.quotation_total_amount_c),
        }[label]
        context = {
            'label': label,
            'customer': quotation.customer.name,
            'code': quotation_id,
            'name': quotation.name,
            'date': quotation.date_time_issued.strftime("%Y-%m-%d"),
            'rows': row_data,
            'conditions': quotation.conditions,
            'net_amount': f"{net_amount:,.2f}",
            'tax': tax_dict[quotation.tax],
            'tax_amount': f"{quotation.tax_amount:,.2f}",
            'total_amount': f"{(total_amount):,.2f}",
            'show_template': show_template,
        }
    
        response = render(request, 'reports/quotation.html', context=context)
        return response
