# Global imports
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile
import  cv2
from matplotlib import pyplot as plt
from io import BytesIO
import matplotlib


matplotlib.use('agg') #executing in different context since is not thread safe

class BasicProcessing:
    
    def __init__(self):
        self._image = None
        self._plot = None
        
        
    def _inMemoryLoad(self, source:InMemoryUploadedFile):
        """Generate an in memory load image. all operations and image treatment is done 
        through memory np.array. The image is not stored or save in the cloud

        Args:
            source (InMemoryUploadedFile): A InMemoryUploadedFile that contain the image to be converted
            into np.array for cv future treatment
        """
        
        if not source or type(source) != InMemoryUploadedFile:
            raise TypeError("Image is not valid please check if uploaded file is correct.")
        
        # to improve file memory loading I use chunk
        binary_image = [] 
        try:
            for chunk in source.chunks():
                binary_image.append(chunk)
        except (IOError, OSError) as e:
           raise IOError("An error ocurred while reading the file chunks.") 
        
        processed_image = b"".join(binary_image)
        np_array = np.frombuffer(processed_image, np.uint8) 
        
        self._image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
       
        
    def transform(self, arr:list):
        """Applies a transformation to the image by changing the weights such as BGR

        Args:
            arr (list): contains a 9*9 matrix that represents teh new channel weights to be applied

        Raises:
            ValueError: If memory is not loaded in memory
            ValueError: If the array -> matrix is not valid
        """
        if self._image is None:
            raise ValueError("You must have an image to perform this operation.")
        
        if len(arr) != 9:
            raise ValueError("To perform transform array must have 9 values from 0 to 1.")
        
        arr = np.array(arr).reshape(3,3)
        
        self._image = cv2.transform(self._image, arr)
        
        
    def grayScaleConversion(self, weights:list=None):
        """ Converts the image into a grayscale representation

        Args:
            weights (list, optional): You can define specific grayscale weights, if you dont specify them then a standard
            grayscale conversion is performed

        Raises:
            ValueError: If image is not loaded in class
        """
        if self._image is None:
            raise ValueError("You must have an image to perform this operation.")
        
        if weights: # perform transform
            self.transform(weights)
            
        # convert to gray
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        
    
    def channelWeights(self, weights:list):
        """Applies new channel weights by using transform

        Args:
            weights (list): A matrix that represent the channel weight for BGR

        Raises:
            ValueError: If image is not loaded
        """
        if self._image is None:
            raise ValueError("You must have an image to perform this operation.")
        
        self.transform(weights)
       
        
    def getImage(self, extension='.png'):
        """Returns the image with a specific extension

        Args:
            extension (str, optional): a str that represent the new extension. Defaults to '.png'.

        Raises:
            ValueError: If image is not loaded

        Returns:
            _type_: Returns a tuple success is if conversion was possible, result is the encoded image
        """
        if self._image is None:
            raise ValueError("You must have an image to perform this operation.")
        
        success, result = cv2.imencode(extension, self._image)
        
        return success, result


    def getPlot(self, extension='.png'):
        if self._plot is None:
            raise ValueError("You haven't generated any plot.")
        
        success, result = cv2.imencode(extension, self._plot)

        return success, result
    
    
    def binaryImage(self, lower=127, upper=255):
        """Applies binary image operation 

        Args:
            lower (int, optional): lower represent the lower bound to apply threshold. Defaults to 127.
            upper (int, optional):  upper represent the upper bound to apply threshold. Defaults to 255.

        Raises:
            ValueError: If image is not loaded
        """
        if self._image is None:
            raise ValueError("You must have an image to perform this operation.")

        self.grayScaleConversion()
        ret, self._image = cv2.threshold(self._image, lower, upper, cv2.THRESH_BINARY)
 
    
    def scale(self, scaling):
        """Scale the image specific value from 1% to 100%

        Args:
            scaling (_type_): a integer value from 1 to 100 that represent the scale grade

        Raises:
            ValueError: If image is not valid
            ValueError: If scaling is not correct. Scale value must be between 1 to 100 to be valid
        """
        if self._image is None:
            raise ValueError("You must have an image to perform this operation.") 
        
        if scaling <= 0 or scaling > 100:
            raise ValueError("Please validate scale -> scale must be between 1% to 100%")
        h, w = self._image.shape[:2]
        h += scaling * h // 100
        w += scaling * w // 100
        
        self._image = cv2.resize(self._image, (w, h))
        
        
    def colorHistogram(self):
        if self._image is None:
            raise ValueError("You must have an image to perform this operation.")
        
        color = ('b', 'g', 'r')
        plt.title("Color BGR Histogram")
        for i, col in enumerate(color):
            histr = cv2.calcHist([self._image], [i],None, [256],  [0, 256])
            plt.plot(histr)
            plt.xlim([0, 256])
            
            
        buffer = BytesIO() 
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_buffer = np.frombuffer(buffer.getvalue(), np.uint8)
        plt.close()
        buffer.close()
        
        self._plot = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)
        