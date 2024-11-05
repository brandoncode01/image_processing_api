from django.urls import path, include
from rest_framework import routers
from . import views


urlpatterns = [
   path('grayscale', views.GrayScaleView.as_view()),
   path('channel-weights', views.ChannelWeightsView.as_view()),
   path('binary', views.BinaryImageView.as_view()),
   path('scale', views.ScaleImageView.as_view()),
   path('bgrplot', views.BGRPlot.as_view()),
]