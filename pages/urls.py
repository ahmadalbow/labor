from django.urls import path, include
from . import views 
urlpatterns = [
    path('',views.index),
    path('gereate', views.gereate),
    path('HMP4040/<str:ip>',views.hmp4040)
]