import cv2
import matplotlib.pyplot as plt
import easyocr
from pylab import rcParams
from IPython.display import Image

rcParams['figure.figsize'] = 8,16
reader = easyocr.Reader(['en', 'hi'])


file_name = "image.jpg"
print(Image(file_name))
output = reader.readtext(file_name)
print(output)