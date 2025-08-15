from django.urls import path
from .views import PrevisaoApiView

urlpatterns = [
    path('previsoes', PrevisaoApiView.as_view(), name='previsoes')
]
