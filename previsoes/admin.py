from django.contrib import admin
from .models import Carro

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
  list_display = (
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