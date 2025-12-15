from rest_framework import serializers
from .models import Bodega, MovimientoProducto, ProductoBodega

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = '__all__'

class MovimientoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoProducto
        fields = '__all__'

class ProductoBodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoBodega
        fields = '__all__'
