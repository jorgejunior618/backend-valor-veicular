from django.db import models

class Base(models.Model):
  pass

class Carro(Base):
  marca = models.CharField
  modelo = models.CharField
  ano = models.IntegerField
  quilometragem = models.IntegerField
  combustivel = models.CharField
  cor = models.CharField
  transmissao = models.CharField
  adicionais = models.CharField
  condicao = models.CharField
  acidente = models.BooleanField

  class Meta:
    verbose_name = 'Carro'
    verbose_name_plural = 'Carros'

    def __str__(self):
      return f'Carro: {self.marca} - {self.modelo}/{self.ano}'
