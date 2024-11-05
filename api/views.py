# Global imports
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE, HTTP_200_OK, HTTP_400_BAD_REQUEST
from image_processing_lib.basic_processing import BasicProcessing

#Local imports
from .serializers import ImageSerializer


class GrayScaleView(APIView):
    
    serializer_class  = ImageSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            basic_processing = BasicProcessing()
            image_source = serializer.validated_data.get('image')
            weights = request.query_params.get('weights', None)
            if weights:
                weights = [float(val) for val in weights.split(',')]
            
            try: 
                basic_processing._inMemoryLoad(image_source)   
                basic_processing.grayScaleConversion(weights)
            except:
                return Response({'status': 'There was an error while processing image, please validate params and image'}, status=HTTP_400_BAD_REQUEST)
            
            success, image = basic_processing.getImage()
            if success: return HttpResponse(image.tobytes(), content_type='image/png')
            
        return Response({'status': 'The image is not valid please check the file.'}, status=HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    
    
class ChannelWeightsView(APIView):
    
    serializer_class = ImageSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            basic_processing = BasicProcessing()
            image_source = serializer.validated_data['image']
            weights = request.query_params.get('weights', None)
            
            if not weights: return Response({'status': 'Please provide channel weights to perform operation'}, status=HTTP_400_BAD_REQUEST)
            weights = [float(weight) for weight in weights.split(',')] 
            
            try:
                basic_processing._inMemoryLoad(image_source)
                basic_processing.transform(weights)
            except ValueError as e:
                return Response({'status': f'{e}'}, status=HTTP_400_BAD_REQUEST)
            
            success, image = basic_processing.getImage()
            if success: return HttpResponse(image.tobytes(), content_type='image/png')
        
        return Response({'status': 'The image is not valid please check the file.'}, status=HTTP_415_UNSUPPORTED_MEDIA_TYPE)



class BinaryImageView(APIView):
    
    serializer_class = ImageSerializer
    
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data) 
        if serializer.is_valid():
            basic_processing = BasicProcessing()
            image_source = serializer.validated_data['image']
            try:
                upper = int(request.query_params.get('upper', 255))
                lower = int(request.query_params.get('lower', 90))
                basic_processing._inMemoryLoad(image_source)
                basic_processing.binaryImage(lower, upper)
            except ValueError as e:
                return Response({'status': f'e'}, status=HTTP_400_BAD_REQUEST)
            
            success, image = basic_processing.getImage()
            if success:
                return HttpResponse(image.tobytes(), status=HTTP_200_OK, content_type='image/png')
            
            return Response({'status': 'Error while performing operation binary image'}, status=HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class ScaleImageView(APIView):
    serializer_class = ImageSerializer
    
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            basic_processing = BasicProcessing()
            image_source = serializer.validated_data['image']
            try:
                scale = int(request.query_params.get('scale', 50))
                basic_processing._inMemoryLoad(image_source)
                basic_processing.scale(scale)
            except ValueError as e:
                return Response({'status': f'There was an error while performing operations: {e} '}, status=HTTP_400_BAD_REQUEST)
        success, image = basic_processing.getImage()
        if success: return HttpResponse(image.tobytes(), status=HTTP_200_OK, content_type='image/png')
        
        return Response({'status': 'Error while performing scale please check params and image'}, HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    
    


class BGRPlot(APIView):
    serializer_class = ImageSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            basic_processing = BasicProcessing()
            image_source = serializer.validated_data['image']
            try:
                basic_processing._inMemoryLoad(image_source)
                basic_processing.colorHistogram()
            except ValueError as e:
                return Response({'status', f'There was an error while performing operations {e}'}, HTTP_400_BAD_REQUEST)
                
        success, img_plot = basic_processing.getPlot()
        if success: return HttpResponse(img_plot.tobytes(), status = HTTP_200_OK, content_type='image/png')

        return Response({'status', 'Error while performing plot operations please validate provided image'})
        