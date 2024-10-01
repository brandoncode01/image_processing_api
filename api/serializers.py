from rest_framework.serializers import Serializer, ListField, IntegerField, ImageField




class ImageSerializer(Serializer):
    image = ImageField(max_length=150, allow_empty_file=False)
  