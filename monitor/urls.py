from django.urls import path
from . import views
urlpatterns = [
      path('cam/', views.monitor, name='cam'),
      path('', views.landing, name='landing'),
      path('leader/', views.leader, name='leader'),
      path('tournment/', views.tournment, name='tournament'),
      path('card/', views.card, name='card'),
      path('card_e/', views.card_eight, name='carde'),
      path('diet/', views.diet, name='diet'),
      path('dietp/', views.form, name='dietp'),
      path('aboutus/', views.about, name='about'),

]