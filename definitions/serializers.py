from rest_framework import serializers

from .models import Product, Description, UnitType, Condition


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'


class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = '__all__'


class ProductDetailedSerializer(serializers.ModelSerializer):

    descriptions = DescriptionSerializer(many=True)    
    class Meta:
        model = Product
        fields = '__all__'


class ConditionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Condition
        fields = '__all__'
