from django.urls import path
from . import views

urlpatterns = [
    path('rates/', views.exchange_rate_list),
    path('history/', views.exchange_rate_history),
    path('calculate/', views.exchange_calculate),
]