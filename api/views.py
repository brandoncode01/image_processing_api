from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.

"""
There will be different endpoints for specific operations and serializers
for example one serializer for blank and white may take color params
while image restoration may take mask params.
"""
@api_view
def gray_image(request):
    pass