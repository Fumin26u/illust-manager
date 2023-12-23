import os
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

BASE_PATH = 'api/evaluate/'

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

from api.utils.getNowTime import getNowTime

# モデルの構築
def createModel(trainExtends):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(224, 224, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(units=128, activation='relu'))
    model.add(Dropout(0.0))
    model.add(Dense(units=len(trainExtends.class_indices), activation='softmax'))
    return model

# モデル作成するディレクトリから各クラスのファイル数を取得
# ファイル数を基に各クラスの重みを均一にする
def createWeights(modelDir):
    # ディレクトリ内の各サブディレクトリを取得
    subdirectories = [d for d in os.listdir(modelDir) if os.path.isdir(os.path.join(modelDir, d))]

    classWeights = dict()
    # 各サブディレクトリ内のファイル数を表示
    for i, subdirectory in enumerate(subdirectories):
        subdirectory_path = os.path.join(modelDir, subdirectory)
        files_in_subdirectory = len([f for f in os.listdir(subdirectory_path) if os.path.isfile(os.path.join(subdirectory_path, f))])
        classWeights[i] = 1.0 / files_in_subdirectory

    return classWeights


# 実行
def main(trainExtends, faceModelPath):
    model = createModel(trainExtends)

    # 各クラスの重み
    classWeights = createWeights(faceModelPath)

    # コンパイル
    model.compile(
        optimizer='adam', 
        loss='categorical_crossentropy', 
        metrics=['accuracy']
    )
    # 訓練
    model.fit(
        trainExtends, 
        epochs=12, 
        class_weight=classWeights
    )
    model.save(f'{BASE_PATH}models/model-{getNowTime()}.h5')   
