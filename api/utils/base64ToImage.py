import base64, cv2, re
import numpy as np

def base64ToImage(base64Image):
    image_data = base64.b64decode(base64Image.split(',')[1])
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    return image

def getImageExtension(base64Image):
    mimeTypeMatch = re.search(r'^data:image/(\w+);base64,', base64Image)
    if mimeTypeMatch:
        return mimeTypeMatch.group(1).lower()
    else:
        return None