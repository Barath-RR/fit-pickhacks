from django.urls import path
from . import views
urlpatterns = [
      path('about/', views.monitor, name='monitor'),
      path('', views.landing, name='landing'),
      path('leader/', views.leader, name='landing'),
      path('tournment/', views.tournment, name='landing'),
      path('card/', views.card, name='landing'),
      path('card_e/', views.card_eight, name='landing'),
      path('diet/', views.diet, name='landing'),

]