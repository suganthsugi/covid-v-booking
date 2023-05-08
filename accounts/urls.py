from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('verifyEmail/', views.verifyEmail, name="verifyEmail"),
    path('forgotPassword/', views.forgotPassword, name="forgotPassword"),
    path('adminLogin/', views.adminLogin, name="adminlogin")
]
