from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator

def createTrainData(
    faceModelPath,
    rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True,
    resize_resolution = (224, 224),
    batch_size = 64,
    validation_split = 0.2
):
    trainData = ImageDataGenerator(
        rescale=rescale,
        shear_range=shear_range,
        zoom_range=zoom_range,
        horizontal_flip=horizontal_flip,
        validation_split=validation_split
    )
    
    trainGenerator = trainData.flow_from_directory(
        faceModelPath,
        target_size=resize_resolution,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )
    
    validationGenerator = trainData.flow_from_directory(
        faceModelPath,
        target_size=resize_resolution,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )
    
    return trainGenerator, validationGenerator