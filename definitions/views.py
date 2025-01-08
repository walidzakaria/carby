from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Description, UnitType
from .serializers import ProductSerializer, DescriptionSerializer, UnitTypeSerializer
from users.permissions import HasModelPermissionOrAdmin

# Create your views here.
class ProductViewSet(ModelViewSet):
    permission_classes = [HasModelPermissionOrAdmin]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def create(self, request, *args, **kwargs):
        descriptions = request.data.pop('descriptions')
        
        product = request.data
        
        product_serializer = ProductSerializer(data=product)
        if product_serializer.is_valid():
            new_product = product_serializer.save()
            
            for description in descriptions:
                description['order'] = new_product.id
            
            
            description_serializer = DescriptionSerializer(data=descriptions, many=True)
            
            if description_serializer.is_valid():
                description_serializer.save()
                
                # recall calculated items
                response_data = {
                    'product': product_serializer.data,
                    'descriptions': description_serializer.data,
                }
                return Response(data=response_data, status=status.HTTP_201_CREATED)
            new_product.delete()
            response_data = {
                'order': [],
                'descriptions': description_serializer.errors,
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        
        print('data', request.data)
        descriptions = request.data.pop('descriptions')
        
        product = request.data
        
        product_id = product['id']
        product_to_edit = Product.objects.get(pk=product_id)
                
        product_serializer = ProductSerializer(product_to_edit, data=product)
        if product_serializer.is_valid():
            product_serializer.save()
            
            for description in descriptions:
                description['product'] = product_id
            
            description_serializer = DescriptionSerializer(data=descriptions, many=True)

            if description_serializer.is_valid():
                # remove old descriptions
                Description.objects.filter(product=product_id).delete()
                
                description_serializer.save()
                
                response_data = {
                    'product': product_serializer.data,
                    'descriptions': description_serializer.data,
                }
                return Response(data=response_data, status=status.HTTP_200_OK)
            response_data = {
                'product': [],
                'descriptions': description_serializer.errors,
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DescriptionViewSet(ModelViewSet):
    permission_classes = [HasModelPermissionOrAdmin]
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


class UnitTypeViewSet(ModelViewSet):
    permission_classes = [HasModelPermissionOrAdmin]
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
