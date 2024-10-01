from django.urls import path, include
from rest_framework import routers
from .views import GrayScaleView, ChannelWeightsView, BinaryImageView, ScaleImageView


urlpatterns = [
   path('grayscale', GrayScaleView.as_view()),
   path('channel-weights', ChannelWeightsView.as_view()),
   path('binary', BinaryImageView.as_view()),
   path('scale', ScaleImageView.as_view()),
]