from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'
        read_only_fields = ('author', 'estadoLibro', 'created_at', 'updated_at')
