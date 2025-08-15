from rest_framework import serializers
from .models import Carro

class CarroSerializer(serializers.ModelSerializer):
  class Meta:
    model = Carro
    fields = (
      'id',
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
