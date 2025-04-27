from django.db import connection
from .models import Quotation, QuotationLine, Customer, BankAccount
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.decorators import action
from decimal import Decimal

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


from rest_framework.schemas import ManualSchema
from django.utils.dateparse import parse_date
from datetime import datetime, time


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def eta_set_uuid(request, pk):
    if request.method == 'POST':
        quotation = Quotation.objects.filter(id=pk).first()
        
        if quotation:
            total_amount = Decimal(request.data.get('total_amount', 0))
            eta_status = request.data.get('status', '')
            uuid = request.data.get('uuid', '')
            quotation.eta_total_amount = total_amount
            quotation.eta_status = eta_status
            quotation.uuid = uuid
            quotation.save()
            return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def eta_set_status(request, pk):
    if request.method == 'POST':
        if pk.isdigit():
            quotation = Quotation.objects.filter(pk=pk).first()
        else:
            quotation = Quotation.objects.filter(uuid=pk).first()

        if quotation:
            eta_status = request.data.get('status', '')
            status_detailed = request.data.get('status_detailed', '')
            quotation.eta_status = eta_status
            quotation.eta_status_detailed = status_detailed
            quotation.save()
            return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def eta_list_invoices(request):
    if request.method == 'GET':
        
        new_status = request.query_params.get('status', '')
        start_date = parse_date(request.query_params.get('start_date', ''))
        end_date = parse_date(request.query_params.get('end_date', ''))
        end_date = datetime.combine(end_date, time.max)
        
        print(request.query_params)
        print('params', start_date, end_date, new_status)
        date_filter = 'qu.date_time_issued BETWEEN %s AND %s'
        query = f'''
                SELECT DISTINCT
                    qu.id AS "InvoiceID", '0' AS "BranchID", 'EG' AS "Country", cu.governate AS "Governate",
                    cu.region_city AS "RegionCity",
                    cu.street AS "Street", cu.building_number AS "BuildingNumber", '' AS "PostalCode", '' AS "Floor",
                    '' AS "Room", '' AS "Landmark",
                    cu.additional_information AS "AdditionalInformation", cu.type AS "ReceiverType",
                    cu.customer_id AS "ReceiverId", cu.name AS "ReceiverName",
                    qu.date_time_issued AS "DateTimeIssued", qu.id AS "InternalId", '' AS "PurchaseOrderReference",
                    COALESCE(qu.name, '') AS "PurchaseOrderDescription",
                    ba.bank_name AS "BankName", '' AS "BankAddress", ba.account_number AS "BankAccountNo",
                    qu.total_amount AS "TotalAmount",
                    qu.uuid AS "UUID", qu.eta_status AS "Status", 'Planet' AS "Company", 'فرع المنيا' AS "BranchName",
                    eta_status_detailed AS "StatusDetailed",
                    'I' AS "DocumentType", 0 AS "InternalBranchID"

                FROM operation_quotation qu
                JOIN operation_customer cu ON qu.customer_id = cu.id
                JOIN definitions_bankaccount ba ON qu.bank_account_id = ba.id
                WHERE qu.status = 'Invoice' AND {date_filter} AND {"(qu.uuid = '' OR qu.uuid IS NULL)" if new_status == "new" else "(qu.uuid != '' OR qu.uuid IS NOT NULL)"}
            '''

        with connection.cursor() as cursor:
            cursor.execute(query, [start_date, end_date])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            row_data = [dict(zip(columns, row)) for row in rows]
            return Response(row_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def eta_get_invoice(request, pk):
    if request.method == 'GET':
        query = '''
                SELECT
                    qu.id AS "InvoiceID", '0' AS "BranchID", 'EG' AS "Country", cu.governate AS "Governate", cu.region_city AS "RegionCity",
                    cu.street AS "Street", cu.building_number AS "BuildingNumber", '' AS "PostalCode", '' AS "Floor", '' AS "Room", '' AS "Landmark",
                    cu.additional_information AS "AdditionalInformation", cu.type AS "ReceiverType", cu.customer_id AS "ReceiverId", cu.name AS "ReceiverName",
                    qu.date_time_issued AS "DateTimeIssued", qu.id AS "InternalId", '' AS "PurchaseOrderReference", COALESCE(qu.name, '') AS "PurchaseOrderDescription",
                    ba.bank_name AS "BankName", '' AS "BankAddress", ba.account_number AS "BankAccountNo", qu.total_amount AS "TotalAmount",
                    qu.uuid AS "UUID", qu.eta_status AS "Status", 'Planet' AS "Company", 'فرع المنيا' AS "BranchName", eta_status_detailed AS "StatusDetailed",
                    'I' AS "DocumentType", 0 AS "InternalBranchID",
                    qu.id AS "InvoiceLineID", ql.quotation_id AS "InvoiceLineID", de.name AS "Description", 'EGS' AS "ItemType", pr.code AS "ItemCode",
                    ut.code AS "UnitType", ql.quantity AS "Quantity", ql.sales_price AS "UnitValue", de.id AS "InternalCode", 0 AS "ValueDifference",
                    0 AS "ItemsDiscount", 0 AS "DiscountRate", CASE WHEN qu.tax = 'T1' THEN qu.tax_amount ELSE 0 END AS "T1",
                    CASE WHEN qu.tax = 'T2' THEN qu.tax_amount ELSE 0 END AS "T2", 'EGP' AS "SaleCurrency", 1.00 AS "SaleCurrRate"

                FROM operation_quotation qu
                JOIN operation_customer cu ON qu.customer_id = cu.id
                JOIN definitions_bankaccount ba ON qu.bank_account_id = ba.id
                JOIN operation_quotationline ql ON ql.quotation_id = qu.id
                JOIN definitions_description de ON ql.description_id = de.id
                JOIN definitions_product pr ON de.product_id = pr.id
                JOIN definitions_unittype ut ON ql.unit_type_id = ut.id
                WHERE qu.id = %s;
            '''
        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            row_data = [dict(zip(columns, row)) for row in rows]
            return Response(row_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def eta_list_invoice_lines(request, pk):
    if request.method == 'GET':
        query = '''
                SELECT
                    qu.id AS "InvoiceLineID", ql.quotation_id AS "InvoiceID", de.name AS "Description", 'EGS' AS "ItemType", pr.code AS "ItemCode",
                    ut.code AS "UnitType", ql.quantity AS "Quantity", ql.sales_price AS "UnitValue", de.id AS "InternalCode", 0 AS "ValueDifference",
                    0 AS "ItemsDiscount", 0 AS "DiscountRate", CASE WHEN qu.tax = 'T1' THEN qu.tax_amount ELSE 0 END AS "T1",
                    CASE WHEN qu.tax = 'T2' THEN qu.tax_amount ELSE 0 END AS "T2", 'EGP' AS "SaleCurrency", 1.00 AS "SaleCurrRate"

                FROM operation_quotation qu
                JOIN operation_customer cu ON qu.customer_id = cu.id
                JOIN definitions_bankaccount ba ON qu.bank_account_id = ba.id
                JOIN operation_quotationline ql ON ql.quotation_id = qu.id
                JOIN definitions_description de ON ql.description_id = de.id
                JOIN definitions_product pr ON de.product_id = pr.id
                JOIN definitions_unittype ut ON ql.unit_type_id = ut.id
                WHERE qu.id = %s;
            '''
        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            row_data = [dict(zip(columns, row)) for row in rows]
            return Response(row_data, status=status.HTTP_200_OK)
