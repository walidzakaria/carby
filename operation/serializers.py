from rest_framework import serializers

from .models import (
    Customer, Vendor, Quotation, QuotationLine, Stock, QuotationAttachment, QuotationInsurance,
    # QuotationDelivery, QuotationDeliveryLine
)
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


class QuotationLineDetailedUnitSerializer(serializers.ModelSerializer):
    description_name = serializers.CharField(source='description.name', read_only=True)
    unit_name = serializers.CharField(source='unit_type.description', read_only=True)
    country_a = serializers.CharField(source='country_a.name', read_only=True)
    country_b = serializers.CharField(source='country_b.name', read_only=True)
    country_c = serializers.CharField(source='country_c.name', read_only=True)

    class Meta:
        model = QuotationLine
        fields = '__all__'
        extra_fields = ['description_name', 'unit_name', 'country_a', 'country_b', 'country_c']


class QuotationSerializer(serializers.ModelSerializer):
    lines = QuotationLineDetailedSerializer(many=True, read_only=True)

    class Meta:
        model = Quotation
        fields = '__all__'


class QuotationSearchSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ('id', 'status', 'date_time_issued', 'quotation_total_amount_a', 'total_amount', 'customer', )


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class QuotationAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationAttachment
        fields = '__all__'


class QuotationInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationInsurance
        fields = '__all__'


# class QuotationDeliverySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuotationDelivery
#         fields = '__all__'


# class QuotationDeliveryLineSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuotationDeliveryLine
#         fields = '__all__'
