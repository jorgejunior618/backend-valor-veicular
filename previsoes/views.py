from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from joblib import load

from .serializers import CarroSerializer
from .functions import gerarPrevisao

class PrevisaoApiView(APIView):
  def __init__(self):
      try:
        print("[INICIALIZAÇÃO]: carregando modelo . . .")
        self.loaded_model = load('model.pkl')
        print("[INICIALIZAÇÃO]: carregando encoder . . .")
        self.te_encoder_loaded = load('te_encoder.pkl')
        print("[INICIALIZAÇÃO]: carregando transformer . . .")
        self.mlb_loaded = load('mlb_transformer.pkl')
        print("[INICIALIZAÇÃO]: Pipeline e encoders carregados com sucesso!")
      except Exception as e:
        print(f"Ocorreu um erro ao carregar os arquivos: {e}")
        self.loaded_model = None
        self.te_encoder_loaded = None
        self.mlb_loaded = None
      
  def post(self, req):
    """
    Recebe dados de um único carro como um dicionário, pré-processa e prevê o preço.

    Args:
      car_data: Dicionário contendo as características do carro.
                Exemplo: {'Car Make': 'Honda', 'Car Model': 'Civic', 'Year': 2020, ...}

    Returns:
      Um dicionário contendo a previsão de preço e um status de sucesso/erro.
    """
    if (self.loaded_model is None or
        self.te_encoder_loaded is None or
        self.mlb_loaded is None):
        return Response(
          {"status": "ERRO", "error": "O Modelo não foi carregado corretamente."},
            status=status.HTTP_400_BAD_REQUEST
        )
    api_friendly_data = self._normalizarJSON(req.data)
    try:
      serializer = CarroSerializer(data=api_friendly_data)
      serializer.is_valid(raise_exception=True)
      car_data = req.data
      prediction_result = gerarPrevisao(
        car_data,
        model=self.loaded_model,
        te_encoder=self.te_encoder_loaded,
        mlb=self.mlb_loaded
      )

      print(f"RESULTADO DA PREDIÇÃO: {prediction_result}")
    except:
      self._obterErros(serializer.errors)
      return Response(
        {'erros': self._obterErros(serializer.errors)},
        status=status.HTTP_400_BAD_REQUEST
      )

    return Response(load('list.pkl'), status=status.HTTP_200_OK)

  def _normalizarJSON(self, data):
    field_mapping = {
      'Car Make': 'Car_Make',
      'Car Model': 'Car_Model',
      'Fuel Type': 'Fuel_Type',
      'Options/Features': 'Options_Features',
    }

    normalized_data = {}
    for key, value in data.items():
      final_key = key if key not in field_mapping else field_mapping[key]
      normalized_data[final_key] = value

    return normalized_data
  
  def _obterErros(self, erros):
    erros_normalizados = {}
    for erro, detalhe in  erros.items():
      erros_normalizados[erro] = detalhe[0]
    return erros_normalizados
