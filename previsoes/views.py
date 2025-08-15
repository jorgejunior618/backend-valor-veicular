from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Carro
from .serializers import CarroSerializer

class PrevisaoApiView(APIView):
  def post(self, req):
    serializer = CarroSerializer(data=req.data)
    serializer.is_valid(raise_exception=True)

    return Response(8500.00, status=status.HTTP_200_OK)
