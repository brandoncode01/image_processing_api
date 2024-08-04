from rest_framework import serializers

# Todo: define params for black and withe or gray scale image processing
"""
First part of this project will only handle image through base64 future implementation by form-submit body
"""
class GrayImageSerializer(serializers.Serializer):
    #Todo: https://github.com/Hipo/drf-extra-fields
    image = serializers.ImageField