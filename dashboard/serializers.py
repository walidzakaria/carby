from rest_framework import serializers


class CategorySaleSerializer(serializers.Serializer):
    category = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
