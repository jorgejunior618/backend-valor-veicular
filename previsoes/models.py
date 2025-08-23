from django.db import models

class Base(models.Model):
  pass
class Carro(Base):
  Car_Model = models.CharField
  Year = models.IntegerField
  Mileage = models.IntegerField
  Fuel_Type = models.CharField
  Color = models.CharField
  Transmission = models.CharField
  Options_Features = models.CharField
  Condition = models.CharField
  Accident = models.CharField

  class Meta:
    verbose_name = 'Carro'
    verbose_name_plural = 'Carros'

    def __str__(self):
      return f'Carro: {self.Car_Model}/{self.Year}'
