from django.urls import path
from . import views

urlpatterns = [
    path('banks/', views.bank_search),
    path('routes/', views.route_search),
]