from rest_framework import serializers

from .models import Customer, Vendor, Quotation, QuotationLine
from definitions.models import Description

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class QuotationLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationLine
        fields = '__all__'


class QuotationLineDetailedSerializer(serializers.ModelSerializer):
    description_name = serializers.CharField(source='description.name', read_only=True)

    class Meta:
        model = QuotationLine
        fields = '__all__'
        extra_fields = ['description_name']


class QuotationSerializer(serializers.ModelSerializer):
    lines = QuotationLineDetailedSerializer(many=True, read_only=True)

    class Meta:
        model = Quotation
        fields = '__all__'


class QuotationSearchSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ('id', 'status', 'date_time_issued', 'quotation_total_amount', 'total_amount', 'customer', )