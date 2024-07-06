from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator

generatorParams_default = {
    'rescale': 1.0 / 255,
    'shear_range': 0,
    'zoom_range': 0.2,
    'horizontal_flip': True,
    'validation_split': 0.2,
}

datasetParams_default = {
    'resize_resolution': (224, 224),
    'batch_size': 32,
}

def createTrainData(
    faceModelPath,
    generatorParams = generatorParams_default,
    datasetParams = datasetParams_default,
):
    print(datasetParams['resize_resolution'])
    trainData = ImageDataGenerator(
        rescale=1.0 / 255,
        shear_range=generatorParams['shear_range'],
        zoom_range=generatorParams['zoom_range'],
        horizontal_flip=generatorParams['horizontal_flip'],
        validation_split=generatorParams['validation_split']
    )
    
    trainGenerator = trainData.flow_from_directory(
        faceModelPath,
        target_size=datasetParams['resize_resolution'],
        batch_size=datasetParams['batch_size'],
        class_mode='categorical',
        subset='training'
    )
    
    validationGenerator = trainData.flow_from_directory(
        faceModelPath,
        target_size=datasetParams['resize_resolution'],
        batch_size=datasetParams['batch_size'],
        class_mode='categorical',
        subset='validation'
    )
    
    return trainGenerator, validationGenerator