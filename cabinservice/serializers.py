from rest_framework import serializers
from .models import Orders, Services

class OrderSerializer(serializers.ModelSerializer):
    date_of_service = serializers.DateTimeField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', 'iso-8601'])
    class Meta:
       model = Orders
       fields = ('id', 'date_of_service', 'cabin', 'service')

class ServicesSerializer(serializers.ModelSerializer):
   class Meta:
       model = Services
       fields = ('id', 'type_of_service',)
