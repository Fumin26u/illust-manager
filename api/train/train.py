import os
from tensorflow import keras

from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

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
def main(
    trainGenerator, 
    validationGenerator, 
    faceModelPath, 
    savePath,
    epochs = 50,
):
    model = createModel(trainGenerator)

    # 各クラスの重み
    classWeights = createWeights(faceModelPath)

    # コンパイル
    model.compile(
        optimizer='adam', 
        loss='categorical_crossentropy', 
        metrics=['accuracy']
    )
    
    # EarlyStopping
    early_stopping = EarlyStopping(
        monitor='val_loss', 
        patience=3, 
        verbose=1, 
        mode='auto',
        restore_best_weights=True
    )
    
    # 訓練
    model.fit(
        trainGenerator, 
        epochs=epochs, 
        class_weight=classWeights,
        callbacks=[early_stopping],
        validation_data=validationGenerator
    )
    model.save(savePath)   
