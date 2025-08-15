from django.contrib import admin
from .models import Carro

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
  list_display = (
    'marca',
    'modelo',
    'ano',
    'quilometragem',
    'combustivel',
    'cor',
    'transmissao',
    'adicionais',
    'condicao',
    'acidente'
  )