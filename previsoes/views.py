from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .consts import TE_ENCODER_FILE, LE_ENCODER_FILE, MLB_TRANSFORMER_FILE, SCALER_FILE, MODEL_FILE
from .serializers import CarroSerializer
from .functions import preprocess_new_data, predict_price

class PrevisaoApiView(APIView):
  def __init__(self):
    from joblib import load

    try:
      print("[INICIALIZAÇÃO]: carregando modelo . . .")
      self.loaded_model = load(MODEL_FILE)
      print("[INICIALIZAÇÃO]: carregando encodera . . .")
      self.te_encoder_loaded = load(TE_ENCODER_FILE)
      self.le_encoder_loaded = load(LE_ENCODER_FILE)
      print("[INICIALIZAÇÃO]: carregando transformer . . .")
      self.mlb_loaded = load(MLB_TRANSFORMER_FILE)
      print("[INICIALIZAÇÃO]: carregando scaler . . .")
      self.scaler_loaded = load(SCALER_FILE)
      print("[INICIALIZAÇÃO]: Arquivos de preprocessamento e Modelo carregados.")

    except Exception as e:
      print(f"Ocorreu um erro ao carregar os arquivos: {e}")
      
      self.loaded_model = None
      self.te_encoder_loaded = None
      self.le_encoder_loaded = None
      self.mlb_loaded = None
      self.scaler_loaded = None
      
  def post(self, req):
    if (self.loaded_model is None or
        self.te_encoder_loaded is None or
        self.le_encoder_loaded is None or
        self.scaler_loaded is None or
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

      preprocessed_data = preprocess_new_data(
        entry_data=car_data,
        te_encoder=self.te_encoder_loaded,
        le_encoder=self.le_encoder_loaded,
        scaler=self.scaler_loaded,
        mlb=self.mlb_loaded
      )
      prediction_result = predict_price(
        data=preprocessed_data,
        model=self.loaded_model
      )

      return Response(
        {'sucess': True, 'prediction': prediction_result},
        status=status.HTTP_200_OK
      )
    except Exception as erro:
      print("ERRO:")
      print(erro)
      self._obterErros(serializer.errors)
      return Response(
        {'erros': self._obterErros(serializer.errors)},
        status=status.HTTP_400_BAD_REQUEST
      )

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
