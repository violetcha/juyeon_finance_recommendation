from django.urls import path
from . import views

urlpatterns = [
    # 정기예금
    path('deposits/save/', views.save_deposit_products),
    path('deposits/', views.deposit_product_list),
    path('deposits/<int:product_id>/', views.deposit_product_detail),

    # 적금
    path('savings/save/', views.save_saving_products),
    path('savings/', views.saving_product_list),
    path('savings/<int:product_id>/', views.saving_product_detail),
]