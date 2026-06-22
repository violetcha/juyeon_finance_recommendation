from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.youtube_search),
    path('saved/', views.saved_video_list_create),
    path('saved/<str:video_id>/', views.saved_video_delete),
    path('<str:video_id>/', views.youtube_detail),
]