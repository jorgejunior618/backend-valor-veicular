from rest_framework import serializers
from .models import Carro

class CarroSerializer(serializers.ModelSerializer):
  Car_Model = serializers.CharField(required=True, max_length=50)
  Fuel_Type = serializers.CharField(required=True, max_length=50)
  Color = serializers.CharField(required=True, max_length=50)
  Transmission = serializers.CharField(required=True, max_length=50)
  Condition = serializers.CharField(required=True, max_length=50)
  Year = serializers.IntegerField(required=True, min_value=2000)
  Mileage = serializers.IntegerField(required=True, min_value=0)
  Options_Features = serializers.CharField(required=False, max_length=200)
  Accident = serializers.CharField(required=True, max_length=4)

  class Meta:
    model = Carro
    fields = (
      'id',
      'Car_Model',
      'Fuel_Type',
      'Color',
      'Transmission',
      'Condition',
      'Year',
      'Mileage',
      'Options_Features',
      'Accident'
    )