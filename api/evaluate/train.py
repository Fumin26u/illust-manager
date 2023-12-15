import os
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
BASE_PATH = './'

from cfg import BATCH_SIZE, EPOCHS, DROPOUT, RESIZE_RESOLUTION, FACE_MODEL_PATH

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# データ拡張
trainData = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
trainExtends = trainData.flow_from_directory(
    FACE_MODEL_PATH,
    target_size=RESIZE_RESOLUTION,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# モデルの構築
def createModel(trainExtends):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(224, 224, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(units=128, activation='relu'))
    model.add(Dropout(DROPOUT))
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

model = createModel(trainExtends)

import numpy as np
# 各クラスの重み
classWeights = createWeights(FACE_MODEL_PATH)

# コンパイル
model.compile(
    optimizer='adam', 
    loss='categorical_crossentropy', 
    metrics=['accuracy']
)
# 訓練
model.fit(
    trainExtends, 
    epochs=EPOCHS, 
    class_weight=classWeights
)
# 保存
from datetime import datetime
def getNowTime():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
model.save(f'{BASE_PATH}models/model-{getNowTime()}.h5')
