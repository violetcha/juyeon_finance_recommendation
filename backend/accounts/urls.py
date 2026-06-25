from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('check-username/', views.check_username),
    path('check-email/', views.check_email),
    path('login/', views.login_user),
    path('logout/', views.logout_user),

    path('find-username/', views.find_username),
    path('reset-password/', views.reset_password),
    path('password/change/', views.change_password),
    path('withdraw/', views.withdraw),

    path('profile/', views.profile),
    path('profile/update/', views.update_profile),
    path('profile/options/', views.profile_options),
]