from django.urls import path
from django.contrib import admin
from .views import login_view,logout_view, signup
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/', login_view, name="login"),
    path('signup/', signup, name="signup"),
    path('logout/', logout_view, name="logout"),
]
