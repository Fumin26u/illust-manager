import os
import base64
import io
from PIL import Image

def createDirectory(directoryPath):
    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)
        
def saveImage(className, base64Image, saveFileName):
    # Create a folder for images
    outputPath = os.path.join('api/save/', 'output')
    createDirectory(outputPath)
    
    # Create a folder for each class
    classPath = os.path.join(outputPath, className)
    createDirectory(classPath)
    
    # Convert base64 to image and save in the class folder
    image = base64.b64decode(base64Image.split(',')[1])
    imagePath = os.path.join(classPath, saveFileName)
    with open(imagePath, 'wb') as f:
        f.write(image)