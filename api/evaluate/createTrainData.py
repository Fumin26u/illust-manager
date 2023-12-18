from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator

from api.evaluate.cfg import FACE_MODEL_PATH, RESIZE_RESOLUTION, BATCH_SIZE

def createTrainData(
    faceModelPath = FACE_MODEL_PATH,
    rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True
):
    trainData = ImageDataGenerator(
        rescale=rescale,
        shear_range=shear_range,
        zoom_range=zoom_range,
        horizontal_flip=horizontal_flip
    )
    
    return trainData.flow_from_directory(
        faceModelPath,
        target_size=RESIZE_RESOLUTION,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )