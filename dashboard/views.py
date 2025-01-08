from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny  # or AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.db import connection
import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings


from dashboard.serializers import CategorySaleSerializer
from operation.models import Vendor
from .utils import get_last_monday

# Create your views here.
class UserCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_active=True).count()
        return Response(data={'result': users}, status=status.HTTP_200_OK)


class VendorCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        vendors = Vendor.objects.filter(is_active=True).count()
        return Response(data={'result': vendors}, status=status.HTTP_200_OK)


class WeeklySalesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # @TODO: add real query
        return Response(data={'result': 0.0}, status=status.HTTP_200_OK)



class MonthlyIncomeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # @TODO: add real query
        return Response(data={'result': 0.0}, status=status.HTTP_200_OK)


# class CategorySalesView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, *args, **kwargs):
#         query = """
#             SELECT cat.name AS category,
#                 sum(CASE
#                         WHEN ord.document_type = 'Invoice' THEN oi.total_quantity
#                         ELSE -oi.total_quantity
#                     END) AS total_quantity
#             FROM sales_orderitem oi
#             JOIN sales_order ord ON oi.order_id = ord.id
#             JOIN products_product pr ON oi.product_id = pr.id
#             JOIN products_subcategory sub ON pr.subcategory_id = sub.id
#             JOIN products_category cat ON sub.category_id = cat.id
#             WHERE ord.document_status = 'Active' AND ord.date >= %s
#             GROUP BY cat.name
#             ORDER BY cat.name;
#         """
        
#         today = datetime.date.today()
#         first_date = today + relativedelta(day=1)

#         with connection.cursor() as cursor:
#             params = []
#             params.append(first_date)
#             cursor.execute(query, params)
#             rows = cursor.fetchall()
            
#             report_data = [
#                 {
#                     'category': row[0],
#                     'quantity': row[1],
#                 }
#                 for row in rows
#             ]
            
#             serializer = CategorySaleSerializer(report_data, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)


# class CategoryDailySalesView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, *args, **kwargs):
#         query = """
#             SELECT cat.name AS category,
#                 sum(CASE
#                         WHEN ord.document_type = 'Invoice' THEN oi.total_quantity
#                         ELSE -oi.total_quantity
#                     END) AS total_quantity
#             FROM sales_orderitem oi
#             JOIN sales_order ord ON oi.order_id = ord.id
#             JOIN products_product pr ON oi.product_id = pr.id
#             JOIN products_subcategory sub ON pr.subcategory_id = sub.id
#             JOIN products_category cat ON sub.category_id = cat.id
#             WHERE ord.document_status = 'Active' AND ord.date >= %s
#             GROUP BY cat.name
#             ORDER BY cat.name;
#         """
        
#         today = datetime.date.today()
#         with connection.cursor() as cursor:
#             params = []
#             params.append(today)
#             cursor.execute(query, params)
#             rows = cursor.fetchall()
            
#             report_data = [
#                 {
#                     'category': row[0],
#                     'quantity': row[1],
#                 }
#                 for row in rows
#             ]
            
#             serializer = CategorySaleSerializer(report_data, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)


# class AnnualSalesView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, *args, **kwargs):
#         query = """
#             SELECT TO_CHAR(pu.date, 'MM') AS MONTH,
#                 sum(CASE
#                         WHEN pu.document_type = 'Invoice' THEN pp.net_value
#                         ELSE -pp.net_value
#                     END) AS value,
#                 'purchases' AS TYPE
#             FROM purchases_purchase pu
#             JOIN purchases_purchasepayment pp ON pp.purchase_id = pu.id
#             AND pp.payment_type = 'Payment'
#             WHERE pu.document_status = 'Active' AND pu.date >= %s
#             GROUP BY TO_CHAR(pu.date, 'MM')
#             UNION ALL
#             SELECT TO_CHAR(ord.date, 'MM') AS MONTH,
#                 sum(CASE
#                         WHEN ord.document_type = 'Invoice' THEN op.net_value
#                         ELSE -op.net_value
#                     END) AS value,
#                 'sales' AS TYPE
#             FROM sales_order ord
#             JOIN sales_orderpayment op ON op.order_id = ord.id
#             AND op.payment_type = 'Payment'
#             WHERE ord.document_status = 'Active' AND ord.date >= %s
#             GROUP BY TO_CHAR(ord.date, 'MM')
#             UNION ALL
#             SELECT MONTH,
#                 sum(net_value) AS value,
#                 'expenses' AS TYPE
#             FROM
#             (SELECT TO_CHAR(pp.creation_date, 'MM') AS MONTH,
#                     pp.net_value
#             FROM purchases_purchasepayment pp
#             WHERE pp.payment_type = 'Collection' AND pp.creation_date >= %s
#             UNION ALL SELECT TO_CHAR(tr.creation_date, 'MM') AS MONTH,
#                                 tr.net_value
#             FROM cashflow_transaction tr
#             JOIN cashflow_cashsubcategory sub ON tr.cash_subcategory_id = sub.id
#             JOIN cashflow_cashcategory cat ON sub.cash_category_id = cat.id
#             WHERE cat.cash_type = 'Expense' AND tr.creation_date >= %s ) ex
#             GROUP BY MONTH
#             UNION ALL
#             SELECT MONTH,
#                 sum(net_value) AS value,
#                 'revenue' AS TYPE
#             FROM
#             (SELECT TO_CHAR(pp.creation_date, 'MM') AS MONTH,
#                     pp.net_value
#             FROM sales_orderpayment pp
#             WHERE pp.payment_type = 'Collection' AND pp.creation_date >= %s
#             UNION ALL SELECT TO_CHAR(tr.creation_date, 'MM') AS MONTH,
#                                 tr.net_value
#             FROM cashflow_transaction tr
#             JOIN cashflow_cashsubcategory sub ON tr.cash_subcategory_id = sub.id
#             JOIN cashflow_cashcategory cat ON sub.cash_category_id = cat.id
#             WHERE cat.cash_type = 'Revenue' AND tr.creation_date >= %s) re
#             GROUP BY MONTH
#         """
#         if settings.LOCAL:
#             query = query.replace("TO_CHAR(", "strftime('%%m', ")
#             query = query.replace(", 'MM') AS MONTH", ") AS MONTH")
#         today = datetime.date.today()
#         start_date = today + relativedelta(years=-1, months=1, day=1)
#         print('start_date', start_date)
#         with connection.cursor() as cursor:
#             params = []
#             params.append(start_date)
#             params.append(start_date)
#             params.append(start_date)
#             params.append(start_date)
#             params.append(start_date)
#             params.append(start_date)
#             cursor.execute(query, params)
#             rows = cursor.fetchall()
            
#             result = {
#                 'purchases': [],
#                 'sales': [],
#                 'revenue': [],
#                 'expenses': [],
#             }
            
#             for row in rows:
#                 result[row[2]].append({
#                     'month': row[0],
#                     'value': row[1],
#                 })

#             return Response(data=result, status=status.HTTP_200_OK)